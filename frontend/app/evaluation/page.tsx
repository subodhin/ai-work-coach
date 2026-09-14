"use client";

import dynamic from "next/dynamic";

const EvaluationContent = dynamic(
  () => import("./EvaluationContent"),
  {
    ssr: false,
  }
);

export default function EvaluationPage() {
  return <EvaluationContent />;
}