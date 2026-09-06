#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-static}"
if [[ "${MODE}" != "static" && "${MODE}" != "live" ]]; then
  echo "usage: $0 [static|live]" >&2
  exit 2
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
PROJECT_DIR="${REPO_ROOT}/engineering-stories/01-one-contract-flight-ground/reference-project"
WORK_ROOT="${PROJECT_DIR}/.work"
DEPS_DIR="${WORK_ROOT}/deps"
BUILD_DIR="${WORK_ROOT}/build"
VENV_DIR="${WORK_ROOT}/venv"
EVIDENCE_DIR="${WORK_ROOT}/evidence"

CORE_SHA="a25917e81c90396df2b189834e83cf852fa4da5f"
FPRIME_ADAPTER_SHA="598f0ca09a39c10b17e3c588d0f2c7112fe52e06"
COSMOS_ADAPTER_SHA="1e6f477ba0571996fa72dfd0b719a522dcc84ff1"
FPRIME_SHA="8a62e455a90b6d4f498c332d45d65a2a819988d8"
FPP_SHA="93f484b7521a8e8894cba25b26e633cc87d8e37a"
OPENC3_FPRIME_SHA="f80d6a2d112a9f2680ad9f404bca2ac116315d33"
COSMOS_PROJECT_SHA="9eb454f06fe0113d05aa6945d88b627155a2aa47"

log() { printf '[reference-project] %s\n' "$*"; }
fail() { printf '[reference-project] ERROR: %s\n' "$*" >&2; exit 1; }

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "required command not found: $1"
}

python_is_312() {
  "$1" - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if sys.version_info[:2] == (3, 12) else 1)
PY
}

select_python() {
  local requested="${ORBITFABRIC_REFERENCE_PYTHON:-}"
  local candidate=""

  if [[ -n "${requested}" ]]; then
    command -v "${requested}" >/dev/null 2>&1 \
      || fail "ORBITFABRIC_REFERENCE_PYTHON not found: ${requested}"
    python_is_312 "${requested}" \
      || fail "Reference Project requires Python 3.12.x; ${requested} reports $("${requested}" --version 2>&1)"
    printf '%s\n' "${requested}"
    return
  fi

  for candidate in python3.12 python3; do
    if command -v "${candidate}" >/dev/null 2>&1 && python_is_312 "${candidate}"; then
      printf '%s\n' "${candidate}"
      return
    fi
  done

  fail "Python 3.12.x is required. Install Python 3.12 with venv support, or set ORBITFABRIC_REFERENCE_PYTHON to a Python 3.12 interpreter."
}

ensure_checkout() {
  local name="$1" url="$2" sha="$3" recurse="${4:-no}"
  local dir="${DEPS_DIR}/${name}"
  if [[ ! -d "${dir}/.git" ]]; then
    log "cloning ${name}"
    git clone --filter=blob:none "${url}" "${dir}"
  fi
  git -C "${dir}" fetch --quiet origin
  git -C "${dir}" checkout --quiet --detach "${sha}"
  if [[ "${recurse}" == "yes" ]]; then
    git -C "${dir}" submodule update --init --recursive
  fi
  local actual
  actual="$(git -C "${dir}" rev-parse HEAD)"
  [[ "${actual}" == "${sha}" ]] || fail "${name}: expected ${sha}, got ${actual}"
}

require_command git
PYTHON_BIN="$(select_python)"
log "using $("${PYTHON_BIN}" --version 2>&1)"

if [[ "${MODE}" == "live" ]]; then
  require_command docker
  docker compose version >/dev/null 2>&1 || fail "Docker Compose v2 is required for live mode"
fi

mkdir -p "${DEPS_DIR}" "${BUILD_DIR}" "${EVIDENCE_DIR}"

ensure_checkout core https://github.com/FAROTECH/orbitfabric.git "${CORE_SHA}"
ensure_checkout fprime-adapter https://github.com/FAROTECH/orbitfabric-fprime-adapter.git "${FPRIME_ADAPTER_SHA}"
ensure_checkout cosmos-adapter https://github.com/FAROTECH/orbitfabric-openc3-cosmos-adapter.git "${COSMOS_ADAPTER_SHA}"
ensure_checkout fprime https://github.com/nasa/fprime.git "${FPRIME_SHA}" yes
ensure_checkout fpp https://github.com/nasa/fpp.git "${FPP_SHA}"
ensure_checkout openc3-fprime https://github.com/OpenC3/openc3-cosmos-fprime.git "${OPENC3_FPRIME_SHA}"
if [[ "${MODE}" == "live" ]]; then
  ensure_checkout cosmos-project https://github.com/OpenC3/cosmos-project.git "${COSMOS_PROJECT_SHA}"
fi

if [[ -x "${VENV_DIR}/bin/python" ]] && ! python_is_312 "${VENV_DIR}/bin/python"; then
  log "removing incompatible virtual environment: $("${VENV_DIR}/bin/python" --version 2>&1)"
  rm -rf "${VENV_DIR}"
fi

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  log "creating Python 3.12 virtual environment"
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi
source "${VENV_DIR}/bin/activate"
python_is_312 python || fail "virtual environment is not Python 3.12.x"

python -m pip install --upgrade pip
python -m pip install -r "${DEPS_DIR}/fprime/requirements.txt"
python -m pip install "${DEPS_DIR}/core" "${DEPS_DIR}/fprime-adapter"
python -m pip install --no-deps "${DEPS_DIR}/cosmos-adapter"
python -m pip install 'PyYAML>=6.0' 'jsonschema>=4.23' 'rfc8785>=0.1.4'

test "$(git -C "${DEPS_DIR}/fpp" rev-list -n 1 v3.2.0)" = "${FPP_SHA}"

rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}" "${EVIDENCE_DIR}"

log "exporting canonical Reference Mission integration input"
orbitfabric export integration-input-set "${REPO_ROOT}/mission" \
  --output-dir "${BUILD_DIR}/input-set"
sha256sum "${BUILD_DIR}/input-set/integration_input_manifest.json" \
  > "${EVIDENCE_DIR}/core-input-manifest.sha256"

log "projecting canonical mission slice into F Prime"
orbitfabric-fprime run \
  --operation fpp_contract_projection \
  --input-set-manifest "${BUILD_DIR}/input-set/integration_input_manifest.json" \
  --profile "${PROJECT_DIR}/profiles/fprime.yaml" \
  --output-dir "${BUILD_DIR}/fprime-projection"
cp "${BUILD_DIR}/fprime-projection/integration_result.json" \
  "${EVIDENCE_DIR}/fprime-integration-result.json"

log "materializing Reference Project F Prime deployment"
python "${PROJECT_DIR}/scripts/materialize_fprime_story.py" \
  --fprime-root "${DEPS_DIR}/fprime" \
  --projection "${BUILD_DIR}/fprime-projection" \
  --output-project "${BUILD_DIR}/fprime-project"
python "${PROJECT_DIR}/scripts/configure_fprime_server_role.py" \
  --project "${BUILD_DIR}/fprime-project"
cp "${BUILD_DIR}/fprime-project/ENGINEERING_STORY_FIXTURE.json" \
  "${EVIDENCE_DIR}/fprime-story-fixture.json"

log "running native F Prime generate/build"
(
  cd "${BUILD_DIR}/fprime-project/Ref"
  fprime-util generate
  fprime-util build
)

DICTIONARY="$(find "${BUILD_DIR}/fprime-project/Ref" -type f -name 'RefTopologyDictionary.json' -print -quit)"
[[ -n "${DICTIONARY}" ]] || fail "native F Prime Dictionary not found"
cp "${DICTIONARY}" "${EVIDENCE_DIR}/RefTopologyDictionary.json"
sha256sum "${EVIDENCE_DIR}/RefTopologyDictionary.json" \
  > "${EVIDENCE_DIR}/fprime-dictionary.sha256"

python - "${EVIDENCE_DIR}/RefTopologyDictionary.json" <<'PY'
import json
import sys
from pathlib import Path
path = Path(sys.argv[1])
data = json.loads(path.read_text())
commands = {x['name'] for x in data.get('commands', [])}
telemetry = {x['name'] for x in data.get('telemetryChannels', [])}
assert 'Ref.payload.OF_StopAcquisition' in commands
assert 'Ref.payload.OF_AcquisitionActive' in telemetry
PY

log "generating OpenC3 F Prime target from native Dictionary"
python "${PROJECT_DIR}/scripts/generate_cosmos_fprime_target.py" \
  --plugin-root "${DEPS_DIR}/openc3-fprime" \
  --dictionary "${EVIDENCE_DIR}/RefTopologyDictionary.json" \
  --output-dir "${BUILD_DIR}/openc3-fprime"
cp "${BUILD_DIR}/openc3-fprime/openc3-fprime-dry-run.json" \
  "${EVIDENCE_DIR}/openc3-fprime-dry-run.json"
cp "${BUILD_DIR}/openc3-fprime/generated-target/cmd.txt" \
  "${EVIDENCE_DIR}/openc3-fprime-cmd.txt"
cp "${BUILD_DIR}/openc3-fprime/generated-target/tlm.txt" \
  "${EVIDENCE_DIR}/openc3-fprime-tlm.txt"

log "projecting canonical Scenario into COSMOS verification intent"
orbitfabric-openc3-cosmos run \
  --operation verification_projection \
  --input-set-manifest "${BUILD_DIR}/input-set/integration_input_manifest.json" \
  --profile "${PROJECT_DIR}/profiles/cosmos.yaml" \
  --operation-input scenario "${REPO_ROOT}/scenarios/payload_stop_acquisition_verification.yaml" \
  --output-dir "${BUILD_DIR}/cosmos-projection"

cp "${BUILD_DIR}/cosmos-projection/integration_result.json" \
  "${EVIDENCE_DIR}/cosmos-integration-result.json"
cp "${BUILD_DIR}/cosmos-projection/verification_projection/verification_projection_plan.json" \
  "${EVIDENCE_DIR}/cosmos-verification-plan.json"
cp "${BUILD_DIR}/cosmos-projection/verification_projection/cosmos/verification.py" \
  "${EVIDENCE_DIR}/cosmos-verification.py"
cp "${BUILD_DIR}/cosmos-projection/verification_projection/cosmos/verification_suite.py" \
  "${EVIDENCE_DIR}/cosmos-verification-suite.py"

python - "${EVIDENCE_DIR}/cosmos-verification-plan.json" "${EVIDENCE_DIR}/cosmos-verification.py" <<'PY'
import json
import sys
from pathlib import Path
plan = json.loads(Path(sys.argv[1]).read_text())
assert plan['status'] == 'executable_subset'
operations = plan['operations']
send = [x for x in operations if x['operation'] == 'send_command']
waits = [x for x in operations if x['operation'] == 'wait_telemetry']
assert len(send) == 1 and send[0]['resolved']['target'] == 'FPRIME'
assert send[0]['resolved']['command'] == 'Ref.payload.OF_StopAcquisition'
assert len(waits) == 1 and waits[0]['resolved']['target'] == 'FPRIME'
assert waits[0]['resolved']['packet'] == 'Ref.payload.OF_AcquisitionActive'
assert waits[0]['resolved']['item'] == 'OF_AcquisitionActive'
assert waits[0]['resolved']['expected_value'] == 0
not_projected = {x['kind'] for x in plan['atoms'] if x['disposition'] == 'not_projected'}
for required in ('initial_mode', 'initial_telemetry', 'expect_event',
                 'expect_payload_lifecycle', 'expect_scenario_status'):
    assert required in not_projected
procedure = Path(sys.argv[2]).read_text()
assert "cmd('FPRIME Ref.payload.OF_StopAcquisition')" in procedure
assert "wait_check('FPRIME Ref.payload.OF_AcquisitionActive OF_AcquisitionActive == 0', 5, type='RAW')" in procedure
PY

if [[ "${MODE}" == "live" ]]; then
  log "executing live OpenC3 COSMOS <-> F Prime loop"
  bash "${PROJECT_DIR}/scripts/run_live_fprime_cosmos.sh" \
    "${BUILD_DIR}/fprime-project/Ref" \
    "${DEPS_DIR}/openc3-fprime" \
    "${DEPS_DIR}/cosmos-project" \
    "${BUILD_DIR}/live"
  rm -rf "${EVIDENCE_DIR}/live"
  cp -a "${BUILD_DIR}/live/evidence" "${EVIDENCE_DIR}/live"
fi

log "${MODE} proof PASS"
log "evidence: ${EVIDENCE_DIR}"
