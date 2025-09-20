import json
from pathlib import Path
from typing import Any, Dict, List

INSTRUMENTS_DIR = Path("data/instruments")
RESPONSES_DIR = Path("data/responses")


def load_json(json_path: Path) -> Dict[str, Any]:
    with json_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_questionnaire(questionnaire_name: str) -> Dict[str, Any]:
    questionnaire_path = INSTRUMENTS_DIR / f"{questionnaire_name}.json"
    return load_json(questionnaire_path)


def latest_patient_response(patient_dir: Path) -> Path:
    """
    .glob yields an iterator of all .json files in the patient directory
    max(... ) finds the one with the latest filename considering patient responses
    are in ISO 8601 format (YYYY-MM-DD.json) (lexicographically sortable).

    NOTE: now I added a metadata.json file, so we need to ensure we do not pick that one.
    We do this by specifying the pattern "????-??-??.json" which matches only files
    with names in the correct date format.
    """
    # LOAD the latest response file THAT IS NOT called "metadata.json".
    latest_response = max(patient_dir.glob("????-??-??.json"))
    return latest_response


def load_patient_responses(patient: str) -> Dict[str, Any]:
    patient_dir = RESPONSES_DIR / patient
    patient_response_path = latest_patient_response(patient_dir)
    return load_json(patient_response_path)


def load_patient_metadata(patient: str) -> Dict[str, Any]:
    patient_dir = RESPONSES_DIR / patient
    metadata_path = patient_dir / "metadata.json"
    return load_json(metadata_path)


def load_instruments() -> List[Dict[str, Any]]:
    instruments = []
    for istrument_file in INSTRUMENTS_DIR.glob("*.json"):
        instrument = load_json(istrument_file)
        instruments.append(instrument)
    return instruments


if __name__ == "__main__":
    # Example usage
    responses = load_patient_responses("P001")
    # questionnaire = load_questionnaire("psqi")
    print(responses)
    print("\n\n\n")
    print(responses["questionnaires"]["PSQI"])
    print("\n\n\n")
    print(type(responses["questionnaires"]["PSQI"]))
    print("\n\n\n")
    for questionnare in responses["questionnaires"]:
        print(f"{questionnare}:")
        for key, value in responses["questionnaires"][questionnare].items():
            print(f"\t{key}: {value}")
