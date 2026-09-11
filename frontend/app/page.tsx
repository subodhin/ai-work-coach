"use client";

import { useEffect, useState } from "react";

type SkillProfile = {
  problem_framing: number;
  context: number;
  prompting: number;
  reasoning: number;
  verification: number;
  final_output: number;
};

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
  skill_profile: SkillProfile;
  weakest_skill: string;
  challenge: Challenge;
};

const API_URL = "http://localhost:8000";

export default function Home() {
  const [data, setData] = useState<NextChallengeResponse | null>(null);
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
        setError("Unable to connect to the AI Work Coach backend.");
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
          Loading your AI capability profile...
        </p>
      </main>
    );
  }

  if (error || !data) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-zinc-950 text-white">
        <div className="text-center">
          <h1 className="text-xl font-semibold">
            AI Work Coach
          </h1>

          <p className="mt-2 text-zinc-400">
            {error}
          </p>
        </div>
      </main>
    );
  }

  const scores = Object.entries(data.skill_profile);

  const overallScore = Math.round(
    scores.reduce(
      (total, [, score]) => total + score,
      0
    ) / scores.length
  );

  return (
    <main className="min-h-screen bg-zinc-950 text-white">
      <div className="mx-auto max-w-6xl px-6 py-10">

        {/* Header */}

        <header className="mb-10">
          <p className="text-sm font-medium text-blue-400">
            AI WORK COACH
          </p>

          <h1 className="mt-2 text-4xl font-bold tracking-tight">
            Learn AI. Improve your work.
          </h1>

          <p className="mt-3 max-w-2xl text-zinc-400">
            Build practical AI skills through realistic
            workplace challenges and personalized coaching.
          </p>
        </header>

        {/* Overall score */}

        <section className="grid gap-6 md:grid-cols-3">

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
            <p className="text-sm text-zinc-400">
              Overall AI Capability
            </p>

            <div className="mt-3 flex items-end gap-2">
              <span className="text-5xl font-bold">
                {overallScore}
              </span>

              <span className="mb-2 text-zinc-500">
                / 100
              </span>
            </div>
          </div>

          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6 md:col-span-2">
            <p className="text-sm text-zinc-400">
              Current Development Focus
            </p>

            <h2 className="mt-2 text-2xl font-semibold capitalize">
              {data.weakest_skill.replace("_", " ")}
            </h2>

            <p className="mt-2 text-sm text-zinc-400">
              Your next challenge is designed to strengthen
              this skill.
            </p>
          </div>

        </section>

        {/* Skill profile */}

        <section className="mt-8">

          <h2 className="text-xl font-semibold">
            Your AI Skill Profile
          </h2>

          <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">

            {scores.map(([skill, score]) => (
              <div
                key={skill}
                className="rounded-xl border border-zinc-800 bg-zinc-900 p-5"
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm capitalize text-zinc-300">
                    {skill.replace("_", " ")}
                  </span>

                  <span className="font-semibold">
                    {score}
                  </span>
                </div>

                <div className="mt-3 h-2 overflow-hidden rounded-full bg-zinc-800">
                  <div
                    className="h-full rounded-full bg-blue-500"
                    style={{
                      width: `${score}%`,
                    }}
                  />
                </div>
              </div>
            ))}

          </div>

        </section>

        {/* Next challenge */}

        <section className="mt-10">

          <div className="rounded-2xl border border-blue-500/20 bg-blue-500/5 p-8">

            <div className="flex flex-wrap items-center gap-3">
              <span className="rounded-full bg-blue-500/10 px-3 py-1 text-xs font-medium uppercase text-blue-400">
                Next Challenge
              </span>

              <span className="rounded-full bg-zinc-800 px-3 py-1 text-xs capitalize text-zinc-400">
                {data.challenge.difficulty}
              </span>

              <span className="rounded-full bg-zinc-800 px-3 py-1 text-xs capitalize text-zinc-400">
                {data.challenge.role.replace("_", " ")}
              </span>
            </div>

            <h2 className="mt-5 text-3xl font-bold">
              {data.challenge.title}
            </h2>

            <p className="mt-4 max-w-3xl leading-7 text-zinc-400">
              {data.challenge.scenario}
            </p>

            <div className="mt-6">
              <p className="text-sm font-semibold text-zinc-200">
                Your task
              </p>

              <p className="mt-2 max-w-3xl leading-7 text-zinc-400">
                {data.challenge.task}
              </p>
            </div>

            <button
              className="mt-8 rounded-xl bg-white px-6 py-3 font-semibold text-black transition hover:bg-zinc-200"
              onClick={() => {
                alert("Challenge screen coming next.");
              }}
            >
              Start Challenge
            </button>

          </div>

        </section>

      </div>
    </main>
  );
}