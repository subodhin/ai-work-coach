from .challenges import get_all_challenges


SKILL_NAMES = [
    "problem_framing",
    "context",
    "prompting",
    "reasoning",
    "verification",
    "final_output",
]


def calculate_skill_profile(evaluations: list[dict]) -> dict:
    """
    Calculate the employee's average score for each skill.
    """

    if not evaluations:
        return {
            skill: 0
            for skill in SKILL_NAMES
        }

    profile = {}

    for skill in SKILL_NAMES:
        scores = [
            evaluation["scores"][skill]
            for evaluation in evaluations
            if skill in evaluation.get("scores", {})
        ]

        if scores:
            profile[skill] = round(sum(scores) / len(scores))
        else:
            profile[skill] = 0

    return profile


def get_weakest_skill(skill_profile: dict) -> str:
    """
    Find the skill with the lowest score.
    """

    return min(
        skill_profile,
        key=skill_profile.get,
    )


def get_challenge_for_skill(
    skill: str,
    difficulty: str | None = None,
) -> dict | None:
    """
    Find a challenge targeting the requested skill.
    """

    challenges = get_all_challenges()

    matching = [
        challenge
        for challenge in challenges
        if challenge["target_skill"] == skill
    ]

    if difficulty:
        difficulty_matches = [
            challenge
            for challenge in matching
            if challenge["difficulty"] == difficulty
        ]

        if difficulty_matches:
            return difficulty_matches[0]

    if matching:
        return matching[0]

    return None