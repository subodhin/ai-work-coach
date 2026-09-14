from .challenges import (
    get_all_challenges,
    get_challenge_by_id,
)


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
def get_next_skill1(
    evaluations: list[dict],
    skill_profile: dict,
) -> str:

    if not evaluations:
        return "problem_framing"

    # Start with the historically weakest skills.
    candidates = sorted(
        skill_profile.items(),
        key=lambda item: item[1],
    )

    for skill, score in candidates:

        # Look for the most recent evaluation
        # that targeted this skill.
        skill_evaluations = []

        for evaluation in evaluations:
            challenge = get_challenge_by_id(
                evaluation["challenge_id"]
            )

            if (
                challenge
                and challenge["target_skill"] == skill
            ):
                skill_evaluations.append(evaluation)

        if not skill_evaluations:
            return skill

        latest = skill_evaluations[-1]

        # If this skill was recently practiced and
        # the latest score is strong, move to another skill.
        latest_score = latest["scores"][skill]

        if latest_score < 70:
            return skill

    # If every practiced skill is strong,
    # return the historically weakest one.
    return candidates[0][0]


def get_next_skill(
    evaluations: list[dict],
    skill_profile: dict,
) -> str:

    if not evaluations:
        return "problem_framing"

    # Track the most recent score for each skill.
    recent_scores = {}

    # Track the skill practiced in the latest challenge.
    latest_evaluation = evaluations[-1]

    latest_challenge = get_challenge_by_id(
        latest_evaluation["challenge_id"]
    )

    latest_skill = (
        latest_challenge["target_skill"]
        if latest_challenge
        else None
    )

    for evaluation in evaluations:

        challenge = get_challenge_by_id(
            evaluation["challenge_id"]
        )

        if not challenge:
            continue

        target_skill = challenge["target_skill"]

        recent_scores[target_skill] = (
            evaluation["scores"][target_skill]
        )

    # Sort skills by their most recent score.
    #
    # We want the weakest skill that:
    # 1. Was not just practiced
    # 2. Has a recent score below 70
    candidates = sorted(
        recent_scores.items(),
        key=lambda item: item[1],
    )

    for skill, latest_score in candidates:

        if skill == latest_skill:
            continue

        if latest_score < 70:
            return skill

    # If no previously-practiced skill needs work,
    # look for an unpracticed skill using the
    # historical profile.
    for skill, score in sorted(
        skill_profile.items(),
        key=lambda item: item[1],
    ):

        if skill != latest_skill and skill not in recent_scores:
            return skill

    # If everything is reasonably strong,
    # move to the weakest skill that wasn't just practiced.
    for skill, score in sorted(
        skill_profile.items(),
        key=lambda item: item[1],
    ):

        if skill != latest_skill:
            return skill

    # Final fallback.
    return latest_skill

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