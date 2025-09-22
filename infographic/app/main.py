from utils.loader import load_instruments, load_patient_responses
from utils.preprocess import split_answers_and_comments
from utils.process import process_responses
from visualisation.dashboards import dashboard_v1a, dashboard_v1b

PATIENT = "P001"

if __name__ == "__main__":
    responses = load_patient_responses(PATIENT)
    answers, comments = split_answers_and_comments(responses)
    responses = process_responses(answers, comments)
    instruments = load_instruments()
    dashboard_v1a(PATIENT, instruments, responses)
    dashboard_v1b(PATIENT, instruments, responses)
