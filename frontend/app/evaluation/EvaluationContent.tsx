"use client";

import { useRouter } from "next/navigation";

type SkillScores = {
  problem_framing: number;
  context: number;
  prompting: number;
  reasoning: number;
  verification: number;
  final_output: number;
};

type Evaluation = {
  scores: SkillScores;
  overall_score: number;
  strengths: string[];
  weaknesses: string[];
  recommended_skill: string;
  feedback: string;
};

const skills = [
  {
    key: "problem_framing",
    label: "Problem Framing",
  },
  {
    key: "context",
    label: "Context",
  },
  {
    key: "prompting",
    label: "Prompting",
  },
  {
    key: "reasoning",
    label: "Reasoning",
  },
  {
    key: "verification",
    label: "Verification",
  },
  {
    key: "final_output",
    label: "Final Output",
  },
] as const;

export default function EvaluationContent() {
  const router = useRouter();

  const stored =
    sessionStorage.getItem("latestEvaluation");

  let evaluation: Evaluation | null = null;

  if (stored) {
    try {
      evaluation = JSON.parse(stored);
    } catch {
      evaluation = null;
    }
  }

  if (!evaluation) {
    return (
      <main className="min-h-screen bg-zinc-950 text-white">
        <div className="mx-auto max-w-4xl px-6 py-16 text-center">
          <p className="text-zinc-400">
            No evaluation found.
          </p>

          <button
            onClick={() => router.push("/")}
            className="mt-6 rounded-xl bg-white px-6 py-3 font-semibold text-black transition hover:bg-zinc-200"
          >
            Back to Dashboard
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-zinc-950 text-white">
      <div className="mx-auto max-w-4xl px-6 py-10">

        {/* Header */}

        <div className="mb-10">
          <p className="text-sm font-medium text-blue-400">
            AI WORK COACH
          </p>

          <h1 className="mt-3 text-4xl font-bold">
            Your AI Work Evaluation
          </h1>

          <p className="mt-3 text-zinc-400">
            Here how you performed across the six AI
            working skills.
          </p>
        </div>

        {/* Overall Score */}

        <section className="rounded-2xl border border-zinc-800 bg-zinc-900 p-8">
          <p className="text-sm text-zinc-400">
            Overall Score
          </p>

          <div className="mt-2 flex items-end gap-3">
            <span className="text-6xl font-bold">
              {evaluation.overall_score}
            </span>

            <span className="mb-2 text-zinc-500">
              / 100
            </span>
          </div>

          <p className="mt-4 text-zinc-400">
            Your score reflects how effectively you
            worked with AI, not just the quality of the
            final answer.
          </p>
        </section>

        {/* Skill Breakdown */}

        <section className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-900 p-8">
          <h2 className="text-xl font-semibold">
            Skill Breakdown
          </h2>

          <div className="mt-6 space-y-5">
            {skills.map((skill) => {
              const score =
                evaluation.scores[skill.key];

              return (
                <div key={skill.key}>
                  <div className="mb-2 flex justify-between">
                    <span className="text-sm text-zinc-300">
                      {skill.label}
                    </span>

                    <span className="text-sm font-medium text-white">
                      {score}
                    </span>
                  </div>

                  <div className="h-2 overflow-hidden rounded-full bg-zinc-800">
                    <div
                      className="h-full rounded-full bg-blue-500"
                      style={{
                        width: `${score}%`,
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {/* Strengths / Weaknesses */}

        <div className="mt-6 grid gap-6 md:grid-cols-2">

          <section className="rounded-2xl border border-zinc-800 bg-zinc-900 p-7">
            <h2 className="text-xl font-semibold">
              Strengths
            </h2>

            <ul className="mt-5 space-y-3">
              {evaluation.strengths.map(
                (strength, index) => (
                  <li
                    key={index}
                    className="flex gap-3 text-zinc-400"
                  >
                    <span className="text-green-400">
                      ✓
                    </span>

                    <span>{strength}</span>
                  </li>
                )
              )}
            </ul>
          </section>

          <section className="rounded-2xl border border-zinc-800 bg-zinc-900 p-7">
            <h2 className="text-xl font-semibold">
              Areas to Improve
            </h2>

            <ul className="mt-5 space-y-3">
              {evaluation.weaknesses.map(
                (weakness, index) => (
                  <li
                    key={index}
                    className="flex gap-3 text-zinc-400"
                  >
                    <span className="text-orange-400">
                      !
                    </span>

                    <span>{weakness}</span>
                  </li>
                )
              )}
            </ul>
          </section>

        </div>

        {/* Recommended Focus */}

        <section className="mt-6 rounded-2xl border border-blue-900/50 bg-blue-950/20 p-7">
          <p className="text-sm font-medium text-blue-400">
            Recommended Focus
          </p>

          <h2 className="mt-2 text-2xl font-semibold capitalize">
            {evaluation.recommended_skill.replaceAll(
              "_",
              " "
            )}
          </h2>

          <p className="mt-3 leading-7 text-zinc-400">
            This is currently your weakest skill based
            on this evaluation. Your next challenge will
            focus on improving it.
          </p>
        </section>

        {/* Coach Feedback */}

        <section className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-900 p-7">
          <h2 className="text-xl font-semibold">
            Coach Feedback
          </h2>

          <p className="mt-4 leading-7 text-zinc-400">
            {evaluation.feedback}
          </p>
        </section>

        {/* Actions */}

        <div className="mt-8 flex items-center justify-between">

          <button
            onClick={() => router.push("/")}
            className="rounded-xl border border-zinc-800 px-5 py-3 text-sm font-medium text-zinc-300 transition hover:bg-zinc-900"
          >
            Dashboard
          </button>

          <button
            onClick={() => router.push("/challenge")}
            className="rounded-xl bg-white px-6 py-3 font-semibold text-black transition hover:bg-zinc-200"
          >
            Next Challenge
          </button>

        </div>

      </div>
    </main>
  );
}