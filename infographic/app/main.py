from utils.loader import load_patient_responses
from utils.preprocess import split_answers_and_comments

PATIENT = "P001"

if __name__ == "__main__":
    responses = load_patient_responses(PATIENT)
    answers, comments = split_answers_and_comments(responses)

    print("responses:")
    print(responses)

    print("Answers:")
    print(answers)
    print("\nComments:")
    print(comments)
