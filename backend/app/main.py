from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from .challenges import (
    get_all_challenges,
    get_challenge_by_id,
)
from .coaching import (
    calculate_skill_profile,
    get_weakest_skill,
    get_challenge_for_skill,
)
from .evaluator import evaluate_submission
from .llm.gemini import GeminiProvider
from .schemas import EvaluationRequest, EvaluationResponse
from .storage import (
    save_evaluation,
    get_evaluations,
)
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


app = FastAPI(
    title="AI Work Coach",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
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
def get_next_challenge():

    evaluations = get_evaluations()

    skill_profile = calculate_skill_profile(
        evaluations
    )

    weakest_skill = get_weakest_skill(
        skill_profile
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
def evaluate(request: EvaluationRequest):

    try:
        provider = GeminiProvider()

        result = evaluate_submission(
            provider=provider,
            request=request,
        )

        # Store the evaluation.
        save_evaluation(
            result.model_dump()
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Evaluation failed: {str(e)}",
        )


# --------------------------------------------------
# Evaluations
# --------------------------------------------------

@app.get("/evaluations")
def get_all_evaluations():

    return {
        "evaluations": get_evaluations()
    }