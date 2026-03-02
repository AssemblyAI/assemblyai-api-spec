"use client";
import * as React from "react";

interface SandboxEmbedProps {
  sandboxId: string;
  height?: string;
}

export function SandboxEmbed({
  sandboxId,
  height = "calc(100vh - var(--header-height, 56px))",
}: SandboxEmbedProps) {
  return (
    <iframe
      src={`https://sampleapp.ai/sandbox/assemblyai/${sandboxId}`}
      style={{
        width: "100%",
        height,
        border: "none",
        display: "block",
      }}
      allow="microphone; camera"
    />
  );
}
