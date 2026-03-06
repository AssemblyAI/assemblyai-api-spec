"use client";
import * as React from "react";

function useFernTheme(): "light" | "dark" {
  const [theme, setTheme] = React.useState<"light" | "dark">("light");

  React.useEffect(() => {
    const check = () =>
      setTheme(
        document.documentElement.classList.contains("dark") ? "dark" : "light"
      );
    check();

    const observer = new MutationObserver(check);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["class"],
    });
    return () => observer.disconnect();
  }, []);

  return theme;
}

interface SandboxEmbedProps {
  sandboxId: string;
  height?: string;
}

export function SandboxEmbed({
  sandboxId,
  height = "calc(100vh - var(--header-height, 56px))",
}: SandboxEmbedProps) {
  const theme = useFernTheme();

  return (
    <iframe
      src={`https://sampleapp.ai/sandbox/assemblyai/${sandboxId}?theme=${theme}`}
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
