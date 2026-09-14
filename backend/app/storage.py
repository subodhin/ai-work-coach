import os

import psycopg
from psycopg.rows import dict_row


DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL not configured")

    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row,
    )


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS evaluations (
                    id SERIAL PRIMARY KEY,
                    problem_framing INTEGER NOT NULL,
                    context INTEGER NOT NULL,
                    prompting INTEGER NOT NULL,
                    reasoning INTEGER NOT NULL,
                    verification INTEGER NOT NULL,
                    final_output INTEGER NOT NULL,
                    overall_score INTEGER NOT NULL,
                    strengths JSONB NOT NULL,
                    weaknesses JSONB NOT NULL,
                    recommended_skill TEXT NOT NULL,
                    feedback TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

        conn.commit()


def save_evaluation(evaluation: dict) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO evaluations (
                    problem_framing,
                    context,
                    prompting,
                    reasoning,
                    verification,
                    final_output,
                    overall_score,
                    strengths,
                    weaknesses,
                    recommended_skill,
                    feedback
                )
                VALUES (
                    %(problem_framing)s,
                    %(context)s,
                    %(prompting)s,
                    %(reasoning)s,
                    %(verification)s,
                    %(final_output)s,
                    %(overall_score)s,
                    %(strengths)s,
                    %(weaknesses)s,
                    %(recommended_skill)s,
                    %(feedback)s
                )
                RETURNING *
                """,
                {
                    **evaluation["scores"],
                    "overall_score": evaluation["overall_score"],
                    "strengths": psycopg.types.json.Jsonb(
                        evaluation["strengths"]
                    ),
                    "weaknesses": psycopg.types.json.Jsonb(
                        evaluation["weaknesses"]
                    ),
                    "recommended_skill": evaluation[
                        "recommended_skill"
                    ],
                    "feedback": evaluation["feedback"],
                },
            )

            saved = cur.fetchone()

        conn.commit()

    return saved


def get_evaluations() -> list[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM evaluations
                ORDER BY created_at ASC
                """
            )

            rows = cur.fetchall()

    evaluations = []

    for row in rows:
        evaluations.append(
            {
                "scores": {
                    "problem_framing": row[
                        "problem_framing"
                    ],
                    "context": row["context"],
                    "prompting": row["prompting"],
                    "reasoning": row["reasoning"],
                    "verification": row[
                        "verification"
                    ],
                    "final_output": row[
                        "final_output"
                    ],
                },
                "overall_score": row[
                    "overall_score"
                ],
                "strengths": row["strengths"],
                "weaknesses": row["weaknesses"],
                "recommended_skill": row[
                    "recommended_skill"
                ],
                "feedback": row["feedback"],
            }
        )

    return evaluations