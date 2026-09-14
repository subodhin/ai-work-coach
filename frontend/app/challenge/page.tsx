"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type Challenge = {
  id: string;
  title: string;
  role: string;
  difficulty: string;
  target_skill: string;
  scenario: string;
  task: string;
  rubric: string[];
};

type NextChallengeResponse = {
  challenge: Challenge;
  weakest_skill: string;
};

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000";
  
export default function ChallengePage() {
  const router = useRouter();

  const [data, setData] =
    useState<NextChallengeResponse | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadChallenge() {
      try {
        const response = await fetch(
          `${API_URL}/challenges/next`
        );

        if (!response.ok) {
          throw new Error("Failed to load challenge");
        }

        const result: NextChallengeResponse =
          await response.json();

        setData(result);
      } catch (error) {
        setError("Unable to load the challenge.");
      } finally {
        setLoading(false);
      }
    }

    loadChallenge();
  }, []);

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-zinc-950 text-white">
        <p className="text-zinc-400">
          Loading challenge...
        </p>
      </main>
    );
  }

  if (error || !data) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-zinc-950 text-white">
        <p className="text-zinc-400">
          {error || "Challenge not found."}
        </p>
      </main>
    );
  }

  const { challenge } = data;

  return (
    <main className="min-h-screen bg-zinc-950 text-white">
      <div className="mx-auto max-w-4xl px-6 py-10">

        {/* Header */}

        <div className="mb-8">
          <p className="text-sm font-medium text-blue-400">
            AI WORK COACH
          </p>

          <h1 className="mt-3 text-4xl font-bold">
            {challenge.title}
          </h1>

          <div className="mt-4 flex flex-wrap gap-3">
            <span className="rounded-full bg-zinc-800 px-3 py-1 text-sm capitalize text-zinc-300">
              {challenge.role.replaceAll("_", " ")}
            </span>

            <span className="rounded-full bg-zinc-800 px-3 py-1 text-sm capitalize text-zinc-300">
              {challenge.difficulty}
            </span>

            <span className="rounded-full bg-blue-500/10 px-3 py-1 text-sm capitalize text-blue-400">
              Focus:{" "}
              {challenge.target_skill.replaceAll("_", " ")}
            </span>
          </div>
        </div>

        {/* Scenario */}

        <section className="rounded-2xl border border-zinc-800 bg-zinc-900 p-7">
          <h2 className="text-xl font-semibold">
            Scenario
          </h2>

          <p className="mt-4 leading-7 text-zinc-400">
            {challenge.scenario}
          </p>
        </section>

        {/* Task */}

        <section className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-900 p-7">
          <h2 className="text-xl font-semibold">
            Your Task
          </h2>

          <p className="mt-4 leading-7 text-zinc-400">
            {challenge.task}
          </p>
        </section>

        {/* Evaluation */}

        <section className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-900 p-7">
          <h2 className="text-xl font-semibold">
            What will be evaluated?
          </h2>

          <ul className="mt-4 space-y-3">
            {challenge.rubric.map(
              (criterion, index) => (
                <li
                  key={index}
                  className="flex gap-3 text-zinc-400"
                >
                  <span className="text-blue-400">
                    •
                  </span>

                  <span>{criterion}</span>
                </li>
              )
            )}
          </ul>
        </section>

        {/* Continue */}

        <div className="mt-8 flex justify-end">
          <button
            onClick={() =>
              router.push("/challenge/submit")
            }
            className="rounded-xl bg-white px-6 py-3 font-semibold text-black transition hover:bg-zinc-200"
          >
            Continue to Submission
          </button>
        </div>

      </div>
    </main>
  );
}