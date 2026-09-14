from typing import Literal

from pydantic import BaseModel, Field


SkillName = Literal[
    "problem_framing",
    "context",
    "prompting",
    "reasoning",
    "verification",
    "final_output",
]


# class EvaluationRequest(BaseModel):
#     challenge: str
#     prompt: str
#     ai_output: str
#     reflection: str = ""

class EvaluationRequest(BaseModel):
    challenge_id: str
    challenge: str
    prompt: str
    ai_output: str
    reflection: str = ""


class SkillScores(BaseModel):
    problem_framing: int = Field(ge=0, le=100)
    context: int = Field(ge=0, le=100)
    prompting: int = Field(ge=0, le=100)
    reasoning: int = Field(ge=0, le=100)
    verification: int = Field(ge=0, le=100)
    final_output: int = Field(ge=0, le=100)


class EvaluationResponse(BaseModel):
    scores: SkillScores

    overall_score: int = Field(ge=0, le=100)

    strengths: list[str]

    weaknesses: list[str]

    recommended_skill: SkillName

    feedback: str

