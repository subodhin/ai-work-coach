import json

from .llm.base import LLMProvider
from .schemas import EvaluationRequest, EvaluationResponse


SKILLS = [
    "problem_framing",
    "context",
    "prompting",
    "reasoning",
    "verification",
    "final_output",
]


def evaluate_submission(
    provider: LLMProvider,
    request: EvaluationRequest,
) -> EvaluationResponse:

    system_prompt = f"""
You are an AI workforce skills evaluator.

Evaluate how effectively an employee worked with AI
on a realistic workplace task.

Evaluate these six skills:

1. problem_framing
   Did the employee clearly define the problem and desired outcome?

2. context
   Did the employee provide useful and relevant context to the AI?

3. prompting
   Did the employee give the AI clear, specific, and effective instructions?

4. reasoning
   Did the employee demonstrate structured thinking and consider
   possible approaches or hypotheses?

5. verification
   Did the employee check, validate, challenge, or verify the AI output?

6. final_output
   Is the resulting work clear, useful, accurate, and actionable?

Score every skill from 0 to 100.

Be evidence-based.
Evaluate the employee's AI-working behavior,
not just the quality of the final AI answer.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "scores": {{
        "problem_framing": 0,
        "context": 0,
        "prompting": 0,
        "reasoning": 0,
        "verification": 0,
        "final_output": 0
    }},
    "overall_score": 0,
    "strengths": [],
    "weaknesses": [],
    "recommended_skill": "",
    "feedback": ""
}}
"""

    user_prompt = f"""
Evaluate the following employee submission.

CHALLENGE:
{request.challenge}

EMPLOYEE PROMPT:
{request.prompt}

AI OUTPUT:
{request.ai_output}

EMPLOYEE REFLECTION:
{request.reflection}
"""

    # Send the evaluation request to the LLM provider.
    content = provider.generate(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    # Clean up the LLM response.
    content = content.strip()

    if content.startswith("```json"):
        content = content[len("```json"):].strip()

    elif content.startswith("```"):
        content = content[len("```"):].strip()

    if content.endswith("```"):
        content = content[:-3].strip()

    # Parse the LLM response as JSON.
    try:
        data = json.loads(content)

        # Get skill scores.
        scores = data["scores"]

        # Calculate overall score in Python.
        data["overall_score"] = round(
            sum(scores.values()) / len(scores)
        )

        # Find the weakest skill.
        data["recommended_skill"] = min(
            scores,
            key=scores.get,
        )

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM returned invalid JSON: {content}"
        ) from exc

    # Validate the final response using Pydantic.
    return EvaluationResponse.model_validate(data)