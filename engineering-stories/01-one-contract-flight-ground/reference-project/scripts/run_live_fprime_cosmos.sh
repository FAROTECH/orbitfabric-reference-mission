#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 4 ]]; then
  echo "usage: $0 <fprime-project-ref-dir> <openc3-fprime-plugin-dir> <cosmos-project-dir> <work-dir>" >&2
  exit 2
fi

REF_DIR="$(cd "$1" && pwd)"
PLUGIN_SOURCE="$(cd "$2" && pwd)"
COSMOS_PROJECT_DIR="$(cd "$3" && pwd)"
WORK_DIR="$(mkdir -p "$4" && cd "$4" && pwd)"
EVIDENCE_DIR="${WORK_DIR}/evidence"
PLUGIN_DIR="${WORK_DIR}/openc3-cosmos-fprime-r1"
API_PASSWORD="orbitfabric-r1-live-acceptance"
COMPOSE_PROJECT_NAME="orbitfabric_r1_live"
FPRIME_PID=""
PLUGIN_VERSION="0.1.0"

mkdir -p "${EVIDENCE_DIR}"
export OPENC3_API_PASSWORD="${API_PASSWORD}"
export OPENC3_DEMO=0
export COMPOSE_PROJECT_NAME
export OPENC3_USER_ID="$(id -u)"
export OPENC3_GROUP_ID="$(id -g)"

log() { printf '[r1-live] %s\n' "$*"; }

compose_args() {
  COMPOSE_ARGS=(docker compose --project-directory "${COSMOS_PROJECT_DIR}" --env-file "${COSMOS_PROJECT_DIR}/.env")
  if [[ -f "${COSMOS_PROJECT_DIR}/.env.local" ]]; then
    COMPOSE_ARGS+=(--env-file "${COSMOS_PROJECT_DIR}/.env.local")
  fi
  COMPOSE_ARGS+=(-f "${COSMOS_PROJECT_DIR}/compose.yaml")
  if [[ -f "${COSMOS_PROJECT_DIR}/compose.override.yaml" ]]; then
    COMPOSE_ARGS+=(-f "${COSMOS_PROJECT_DIR}/compose.override.yaml")
  fi
}

capture_cosmos_diagnostics() {
  compose_args
  (cd "${COSMOS_PROJECT_DIR}" && "${COMPOSE_ARGS[@]}" ps -a) \
    >"${EVIDENCE_DIR}/cosmos-ps.txt" 2>&1 || true
  (cd "${COSMOS_PROJECT_DIR}" && "${COMPOSE_ARGS[@]}" logs --no-color --timestamps) \
    >"${EVIDENCE_DIR}/cosmos-runtime.log" 2>&1 || true
}

cleanup() {
  status=$?
  capture_cosmos_diagnostics
  if [[ -n "${FPRIME_PID}" ]] && kill -0 "${FPRIME_PID}" 2>/dev/null; then
    kill "${FPRIME_PID}" 2>/dev/null || true
    wait "${FPRIME_PID}" 2>/dev/null || true
  fi
  if [[ -x "${COSMOS_PROJECT_DIR}/openc3.sh" ]]; then
    (cd "${COSMOS_PROJECT_DIR}" && ./openc3.sh cleanup local force >/dev/null 2>&1) || true
  fi
  exit "${status}"
}
trap cleanup EXIT INT TERM

cosmos_cli() {
  local local_dir="$1"
  shift
  compose_args
  (cd "${local_dir}" && "${COMPOSE_ARGS[@]}" run -T --rm \
    -v "$(pwd):/openc3/local:z" -w /openc3/local \
    -e OPENC3_API_PASSWORD="${OPENC3_API_PASSWORD}" --no-deps \
    openc3-cosmos-cmd-tlm-api ruby /openc3/bin/openc3cli "$@")
}

wait_http() {
  for _ in {1..120}; do
    if curl -fsS http://localhost:2900 >/dev/null 2>&1; then return 0; fi
    sleep 2
  done
  return 1
}

wait_listener() {
  python - "$1" <<'PY'
import sys, time
port_hex = f"{int(sys.argv[1]):04X}"
for _ in range(60):
    for source in ("/proc/net/tcp", "/proc/net/tcp6"):
        try:
            lines = open(source, encoding="ascii").read().splitlines()[1:]
        except OSError:
            continue
        for line in lines:
            fields = line.split()
            local_address = fields[1]
            state = fields[3]
            if local_address.rsplit(":", 1)[-1].upper() == port_hex and state == "0A":
                raise SystemExit(0)
    time.sleep(1)
raise SystemExit(1)
PY
}

wait_fprime_interface() {
  local snapshot="${EVIDENCE_DIR}/fprime-interface-readiness.log"
  compose_args
  : >"${snapshot}"
  for _ in {1..90}; do
    (cd "${COSMOS_PROJECT_DIR}" && "${COMPOSE_ARGS[@]}" logs --no-color --timestamps --since 2m) \
      >"${snapshot}" 2>&1 || true
    if grep -q 'FPRIME_INT: Connection Success' "${snapshot}"; then
      grep -E 'FPRIME_INT: (Starting packet reading|Connect .*50000|Connection Success)' \
        "${snapshot}" >"${EVIDENCE_DIR}/fprime-interface-ready.txt" || true
      return 0
    fi
    sleep 1
  done
  return 1
}

log "locating native F Prime Ref binary"
FPRIME_BIN="$(find "${REF_DIR}" -type f -path '*/bin/Ref' -perm -111 -print -quit)"
test -n "${FPRIME_BIN}"
printf '%s\n' "${FPRIME_BIN}" >"${EVIDENCE_DIR}/fprime-binary.txt"

log "preparing isolated COSMOS runtime"
(cd "${COSMOS_PROJECT_DIR}" && ./openc3.sh cleanup local force) >/dev/null 2>&1 || true
(cd "${COSMOS_PROJECT_DIR}" && ./openc3.sh run) >"${EVIDENCE_DIR}/cosmos-start.log" 2>&1
wait_http

for _ in {1..30}; do
  if cosmos_cli "${COSMOS_PROJECT_DIR}" setpassword >"${EVIDENCE_DIR}/setpassword.log" 2>&1; then
    break
  fi
  sleep 2
done

grep -q . "${EVIDENCE_DIR}/setpassword.log" || true

log "assembling FPRIME plugin from native dictionary output"
rm -rf "${PLUGIN_DIR}"
cp -a "${PLUGIN_SOURCE}" "${PLUGIN_DIR}"
cp "${WORK_DIR}/../openc3-fprime/generated-target/cmd.txt" "${PLUGIN_DIR}/targets/FPRIME/cmd_tlm/cmd.txt"
cp "${WORK_DIR}/../openc3-fprime/generated-target/tlm.txt" "${PLUGIN_DIR}/targets/FPRIME/cmd_tlm/tlm.txt"
mkdir -p "${PLUGIN_DIR}/targets/FPRIME/procedures"
cp "${WORK_DIR}/../cosmos-projection/verification_projection/cosmos/verification.py" \
  "${PLUGIN_DIR}/targets/FPRIME/procedures/verification.py"
cp "${WORK_DIR}/../cosmos-projection/verification_projection/cosmos/verification_suite.py" \
  "${PLUGIN_DIR}/targets/FPRIME/procedures/verification_suite.py"
cat >"${PLUGIN_DIR}/targets/FPRIME/procedures/r1_telemetry_readiness.py" <<'PY'
import time

from openc3.script import tlm

TELEMETRY = "FPRIME Ref.blockDrv.BD_Cycles BD_Cycles"
DEADLINE = time.monotonic() + 30.0
last_value = None

while time.monotonic() < DEADLINE:
    last_value = tlm(TELEMETRY, type="RAW")
    if last_value is not None:
        print(f"R1 telemetry path ready: {TELEMETRY} = {last_value}")
        break
    time.sleep(0.5)
else:
    raise RuntimeError(f"R1 telemetry path did not become observable within 30 seconds: {TELEMETRY}")
PY

log "building and loading native OpenC3 F Prime plugin"
cosmos_cli "${PLUGIN_DIR}" rake build VERSION="${PLUGIN_VERSION}" >"${EVIDENCE_DIR}/plugin-build.log" 2>&1
GEM="${PLUGIN_DIR}/openc3-cosmos-fprime-${PLUGIN_VERSION}.gem"
test -f "${GEM}"
cosmos_cli "${PLUGIN_DIR}" validate "$(basename "${GEM}")" DEFAULT >"${EVIDENCE_DIR}/plugin-validate.log" 2>&1
cosmos_cli "${PLUGIN_DIR}" load "$(basename "${GEM}")" DEFAULT >"${EVIDENCE_DIR}/plugin-load.log" 2>&1

# FPRIME_INT is allowed to enter ATTEMPTING while the native peer is absent.
# OpenC3 retries failed interface connections. Start the single-client F Prime
# TcpServer only after plugin installation has completed so transient interface
# bootstrap cannot consume the one accepted flight-side connection.
log "starting native F Prime target on TCP 50000 after COSMOS plugin bootstrap"
"${FPRIME_BIN}" -a 0.0.0.0 -p 50000 \
  >"${EVIDENCE_DIR}/fprime.stdout" 2>"${EVIDENCE_DIR}/fprime.stderr" &
FPRIME_PID=$!
# Verify LISTEN state passively so readiness checking does not consume and
# immediately close the first accepted connection.
wait_listener 50000

# Plugin load is not equivalent to runtime readiness. The OpenC3 operator starts
# FPRIME_INT asynchronously, so wait for the native interface to establish its
# actual TCP connection before issuing the first Story command.
log "waiting for native OpenC3 FPRIME_INT connection"
wait_fprime_interface
grep -q 'Accepted client' "${EVIDENCE_DIR}/fprime.stdout"
log "FPRIME_INT connected to native F Prime target"

# A connected interface is still weaker than telemetry-path readiness. Use the
# Ref deployment's native periodic block-driver cycle telemetry as an independent
# heartbeat before starting the Story. This keeps bootstrap readiness separate
# from the generated scenario assertion on OF_AcquisitionActive.
log "waiting for native F Prime telemetry path readiness"
cosmos_cli "${COSMOS_PROJECT_DIR}" script run FPRIME/procedures/r1_telemetry_readiness.py \
  >"${EVIDENCE_DIR}/fprime-telemetry-readiness.txt" 2>&1
grep -q 'R1 telemetry path ready:' "${EVIDENCE_DIR}/fprime-telemetry-readiness.txt"
log "native F Prime telemetry path is observable"

log "running OrbitFabric-generated verification suite against live F Prime"
SCRIPT_ID="$(cosmos_cli "${COSMOS_PROJECT_DIR}" script spawn \
  FPRIME/procedures/verification_suite.py \
  --suite OrbitFabricVerificationSuite \
  --group OrbitFabricVerificationGroup \
  --script test_scenario \
  2>"${EVIDENCE_DIR}/script-runner.stderr" | tee "${EVIDENCE_DIR}/script-runner.stdout" | tail -n 1)"
[[ "${SCRIPT_ID}" =~ ^[0-9]+$ ]]
printf '%s\n' "${SCRIPT_ID}" >"${EVIDENCE_DIR}/script-id.txt"

for _ in {1..30}; do
  cosmos_cli "${COSMOS_PROJECT_DIR}" script status "${SCRIPT_ID}" --verbose \
    >"${EVIDENCE_DIR}/script-status.txt" 2>&1 || true
  if grep -qE '"state"[[:space:]]*=>[[:space:]]*"(completed|completed_errors|crashed|killed|stopped)"' \
      "${EVIDENCE_DIR}/script-status.txt"; then
    break
  fi
  sleep 2
done

grep -qE '"state"[[:space:]]*=>[[:space:]]*"completed"' "${EVIDENCE_DIR}/script-status.txt"

cat >"${EVIDENCE_DIR}/live-proof.json" <<EOF
{
  "kind": "orbitfabric.reference_mission.engineering_story_01.live_proof",
  "version": "0.1-candidate",
  "status": "passed",
  "fprime_target": "Ref",
  "fprime_tcp_port": 50000,
  "cosmos_target": "FPRIME",
  "command": "Ref.payload.OF_StopAcquisition",
  "telemetry_packet": "Ref.payload.OF_AcquisitionActive",
  "telemetry_item": "OF_AcquisitionActive",
  "script_runner_id": ${SCRIPT_ID}
}
EOF

sha256sum "${EVIDENCE_DIR}/live-proof.json" \
  "${WORK_DIR}/../cosmos-projection/verification_projection/cosmos/verification.py" \
  "${WORK_DIR}/../cosmos-projection/verification_projection/cosmos/verification_suite.py" \
  >"${EVIDENCE_DIR}/SHA256SUMS"

log "LIVE F PRIME <-> COSMOS proof PASS"
