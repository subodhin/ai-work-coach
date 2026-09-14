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
                    user_id TEXT NOT NULL DEFAULT 'demo-user',
                    challenge_id TEXT NOT NULL,
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

            # Add user_id to an existing database if the table
            # was created before user support was added.
            cur.execute(
                """
                ALTER TABLE evaluations
                ADD COLUMN IF NOT EXISTS user_id
                TEXT NOT NULL DEFAULT 'demo-user'
                """
            )

        conn.commit()


def save_evaluation(evaluation: dict) -> dict:

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO evaluations (
                    user_id,
                    challenge_id,
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
                    %(user_id)s,
                    %(challenge_id)s,
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
                    "user_id": evaluation.get(
                        "user_id",
                        "demo-user",
                    ),
                    "challenge_id": evaluation[
                        "challenge_id"
                    ],
                    **evaluation["scores"],
                    "overall_score": evaluation[
                        "overall_score"
                    ],
                    "strengths": psycopg.types.json.Jsonb(
                        evaluation["strengths"]
                    ),
                    "weaknesses": psycopg.types.json.Jsonb(
                        evaluation["weaknesses"]
                    ),
                    "recommended_skill": evaluation[
                        "recommended_skill"
                    ],
                    "feedback": evaluation[
                        "feedback"
                    ],
                },
            )

            saved = cur.fetchone()

        conn.commit()

    return saved


def get_evaluations(
    user_id: str = "demo-user",
) -> list[dict]:

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT *
                FROM evaluations
                WHERE user_id = %(user_id)s
                ORDER BY id ASC
                """,
                {
                    "user_id": user_id
                },
            )

            rows = cur.fetchall()

    evaluations = []

    for row in rows:

        evaluations.append(
            {
                "user_id": row["user_id"],
                "challenge_id": row["challenge_id"],
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
                "weaknesses": row[
                    "weaknesses"
                ],
                "recommended_skill": row[
                    "recommended_skill"
                ],
                "feedback": row["feedback"],
            }
        )

    return evaluations