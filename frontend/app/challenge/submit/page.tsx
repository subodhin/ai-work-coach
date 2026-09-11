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

const API_URL = "http://localhost:8000";

export default function SubmissionPage() {
  const router = useRouter();

  const [data, setData] =
    useState<NextChallengeResponse | null>(null);

  const [prompt, setPrompt] = useState("");
  const [aiOutput, setAiOutput] = useState("");
  const [reflection, setReflection] = useState("");

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
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

  async function handleSubmit() {
    if (!data) {
      return;
    }

    if (!prompt.trim() || !aiOutput.trim()) {
      setError(
        "Please provide both your AI prompt and AI output."
      );
      return;
    }

    setSubmitting(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/evaluate`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            challenge: data.challenge.task,
            prompt: prompt,
            ai_output: aiOutput,
            reflection: reflection,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Evaluation failed");
      }

      const result = await response.json();

      sessionStorage.setItem(
        "latestEvaluation",
        JSON.stringify(result)
      );

      router.push("/evaluation");
    } catch (error) {
      setError(
        "Unable to evaluate your submission. Please try again."
      );
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-zinc-950 text-white">
        <p className="text-zinc-400">
          Loading challenge...
        </p>
      </main>
    );
  }

  if (!data) {
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

          <h1 className="mt-3 text-3xl font-bold">
            Submit Your Work
          </h1>

          <p className="mt-3 text-zinc-400">
            Complete the challenge using an AI tool,
            then submit your work for evaluation.
          </p>
        </div>

        {/* Challenge */}

        <section className="rounded-2xl border border-zinc-800 bg-zinc-900 p-7">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <h2 className="text-xl font-semibold">
              {challenge.title}
            </h2>

            <span className="rounded-full bg-blue-500/10 px-3 py-1 text-sm capitalize text-blue-400">
              {challenge.target_skill.replaceAll(
                "_",
                " "
              )}
            </span>
          </div>

          <p className="mt-4 leading-7 text-zinc-400">
            {challenge.task}
          </p>
        </section>

        {/* Prompt */}

        <section className="mt-6">
          <label className="mb-2 block text-sm font-medium text-zinc-200">
            1. Your AI Prompt
          </label>

          <textarea
            value={prompt}
            onChange={(event) =>
              setPrompt(event.target.value)
            }
            placeholder="Paste the prompt you gave to the AI..."
            rows={7}
            className="w-full rounded-xl border border-zinc-800 bg-zinc-900 p-4 text-sm text-white outline-none placeholder:text-zinc-600 focus:border-blue-500"
          />
        </section>

        {/* AI Output */}

        <section className="mt-6">
          <label className="mb-2 block text-sm font-medium text-zinc-200">
            2. AI Output
          </label>

          <textarea
            value={aiOutput}
            onChange={(event) =>
              setAiOutput(event.target.value)
            }
            placeholder="Paste the AI response here..."
            rows={10}
            className="w-full rounded-xl border border-zinc-800 bg-zinc-900 p-4 text-sm text-white outline-none placeholder:text-zinc-600 focus:border-blue-500"
          />
        </section>

        {/* Reflection */}

        <section className="mt-6">
          <label className="mb-2 block text-sm font-medium text-zinc-200">
            3. What did you change after reviewing
            the AI response?
          </label>

          <textarea
            value={reflection}
            onChange={(event) =>
              setReflection(event.target.value)
            }
            placeholder="Describe what you reviewed, corrected, verified, or improved..."
            rows={6}
            className="w-full rounded-xl border border-zinc-800 bg-zinc-900 p-4 text-sm text-white outline-none placeholder:text-zinc-600 focus:border-blue-500"
          />
        </section>

        {/* Error */}

        {error && (
          <div className="mt-6 rounded-xl border border-red-900 bg-red-950/30 p-4 text-sm text-red-400">
            {error}
          </div>
        )}

        {/* Actions */}

        <div className="mt-8 flex items-center justify-between">
          <button
            onClick={() => router.back()}
            className="rounded-xl border border-zinc-800 px-5 py-3 text-sm font-medium text-zinc-300 transition hover:bg-zinc-900"
          >
            Back
          </button>

          <button
            onClick={handleSubmit}
            disabled={submitting}
            className="rounded-xl bg-white px-6 py-3 font-semibold text-black transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {submitting
              ? "Evaluating..."
              : "Evaluate My Work"}
          </button>
        </div>

      </div>
    </main>
  );
}