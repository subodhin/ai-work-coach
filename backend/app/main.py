import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from .challenges import (
    get_all_challenges,
    get_challenge_by_id,
)

from .coaching import (
    calculate_skill_profile,
    get_weakest_skill,
    get_next_skill,
    get_challenge_for_skill,
)

from .evaluator import evaluate_submission
from .llm.gemini import GeminiProvider
from .schemas import EvaluationRequest, EvaluationResponse

from .storage import (
    init_db,
    save_evaluation,
    get_evaluations,
)


app = FastAPI(
    title="AI Work Coach",
    version="0.1.0",
)

init_db()


# --------------------------------------------------
# CORS
# --------------------------------------------------

frontend_url = os.getenv(
    "FRONTEND_URL",
    "http://localhost:3000",
)
print("CORS FRONTEND_URL::::::::::::::::::::::::::::::::::::::::::::::", frontend_url)
print("CORS FRONTEND_URL:", frontend_url)
print("CORS ORIGINS:", [frontend_url])
print("ENV FRONTEND_URL:", os.getenv("FRONTEND_URL"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Health
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# --------------------------------------------------
# AI Test
# --------------------------------------------------

@app.get("/test-ai")
def test_ai():

    try:
        provider = GeminiProvider()

        response = provider.generate(
            system_prompt="You are a helpful assistant.",
            user_prompt=(
                "Say hello to the AI Work Coach "
                "in one short sentence."
            ),
        )

        return {
            "response": response
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI request failed: {str(e)}",
        )


# --------------------------------------------------
# Challenges
# --------------------------------------------------

@app.get("/challenges")
def get_challenges():

    return {
        "challenges": get_all_challenges()
    }


@app.get("/challenges/next")
def get_next_challenge(user_id: str = "demo-user"):

    evaluations = get_evaluations(user_id)
    # ----------------------------------------------
    # First-time user
    # ----------------------------------------------

    if not evaluations:

        challenge = get_challenge_for_skill(
            "problem_framing"
        )

        if challenge is None:
            raise HTTPException(
                status_code=404,
                detail="No suitable challenge found",
            )

        return {
            "skill_profile": calculate_skill_profile([]),
            "weakest_skill": "problem_framing",
            "reason": (
                "This is your first challenge. "
                "Let's establish your baseline."
            ),
            "challenge": challenge,
        }

    # ----------------------------------------------
    # Existing user
    # ----------------------------------------------

    skill_profile = calculate_skill_profile(
        evaluations
    )

    # Use adaptive coaching logic to determine
    # which skill should be practiced next.
    weakest_skill = get_next_skill(
        evaluations,
        skill_profile,
    )

    challenge = get_challenge_for_skill(
        weakest_skill
    )

    if challenge is None:
        raise HTTPException(
            status_code=404,
            detail="No suitable challenge found",
        )

    return {
        "skill_profile": skill_profile,
        "weakest_skill": weakest_skill,
        "reason": (
            f"{weakest_skill.replace('_', ' ').title()} "
            "is currently the next skill to practice."
        ),
        "challenge": challenge,
    }


@app.get("/challenges/{challenge_id}")
def get_challenge(challenge_id: str):

    challenge = get_challenge_by_id(
        challenge_id
    )

    if challenge is None:
        raise HTTPException(
            status_code=404,
            detail="Challenge not found",
        )

    return challenge


# --------------------------------------------------
# Evaluation
# --------------------------------------------------

@app.post(
    "/evaluate",
    response_model=EvaluationResponse,
)
def evaluate(
    request: EvaluationRequest,
    user_id: str = "demo-user",
):
    try:

        provider = GeminiProvider()

        result = evaluate_submission(
            provider=provider,
            request=request,
        )

        evaluation_data = result.model_dump()

        evaluation_data["challenge_id"] = (
            request.challenge_id
        )
        evaluation_data["user_id"] = user_id
        save_evaluation(
            evaluation_data
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Evaluation failed: {str(e)}",
        )


# --------------------------------------------------
# Latest Evaluation
# --------------------------------------------------

@app.get("/evaluations/latest")
def get_latest_evaluation(
    user_id: str = "demo-user",
):

    evaluations = get_evaluations(user_id)

    if not evaluations:

        raise HTTPException(
            status_code=404,
            detail="No evaluations found",
        )

    return evaluations[-1]


# --------------------------------------------------
# Evaluations
# --------------------------------------------------

@app.get("/evaluations")
def get_all_evaluations(
    user_id: str = "demo-user",
):

    return {
        "evaluations": get_evaluations(user_id)
    }

# --------------------------------------------------
# Progress
# --------------------------------------------------

@app.get("/progress")
def get_progress(
    user_id: str = "demo-user",
):

    evaluations = get_evaluations(user_id)

    if not evaluations:

        return {
            "has_progress": False,
            "message": "No evaluations yet.",
        }

    skill_profile = calculate_skill_profile(
        evaluations
    )

    weakest_skill = get_weakest_skill(
        skill_profile
    )

    latest = evaluations[-1]

    # Identify the skill targeted by the latest challenge.
    latest_challenge = get_challenge_by_id(
        latest["challenge_id"]
    )

    target_skill = (
        latest_challenge["target_skill"]
        if latest_challenge
        else None
    )

    # Find the previous attempt for the same skill.
    previous = None

    if target_skill:

        for evaluation in reversed(
            evaluations[:-1]
        ):

            challenge = get_challenge_by_id(
                evaluation["challenge_id"]
            )

            if (
                challenge
                and challenge["target_skill"]
                == target_skill
            ):

                previous = evaluation
                break

    # Calculate improvement.
    improvement = None

    if previous and target_skill:

        improvement = (
            latest["scores"][target_skill]
            - previous["scores"][target_skill]
        )

    return {
        "has_progress": True,

        "overall_score": round(
            sum(skill_profile.values())
            / len(skill_profile)
        ),

        "skill_profile": skill_profile,

        "weakest_skill": weakest_skill,

        "latest_scores": latest["scores"],

        "target_skill": target_skill,

        "previous_target_score": (
            previous["scores"][target_skill]
            if previous and target_skill
            else None
        ),

        "current_target_score": (
            latest["scores"][target_skill]
            if target_skill
            else None
        ),

        "improvement": improvement,

        "attempt_count": len(evaluations),
    }