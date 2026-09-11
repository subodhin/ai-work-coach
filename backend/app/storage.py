evaluations = []


def save_evaluation(evaluation: dict) -> dict:
    evaluations.append(evaluation)
    return evaluation


def get_evaluations() -> list[dict]:
    return evaluations


def clear_evaluations():
    evaluations.clear()