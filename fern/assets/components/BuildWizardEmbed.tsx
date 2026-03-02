"use client";
import * as React from "react";

const SDK_URL =
  "https://cdn.jsdelivr.net/npm/@sampleapp.ai/sdk@1.0.60/dist/index.standalone.umd.js";
const API_KEY = "3ZVJcRgexi5xBUtxhny9iGAz";

interface BuildWizardEmbedProps {
  height?: string;
}

function loadScript(src: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const existing = document.querySelector(
      `script[src="${src}"]`
    ) as HTMLScriptElement | null;
    if (existing) {
      if ((window as any).SampleAppStandalone) {
        resolve();
      } else {
        existing.addEventListener("load", () => resolve());
        existing.addEventListener("error", () =>
          reject(new Error("Failed to load SampleApp SDK"))
        );
      }
      return;
    }
    const script = document.createElement("script");
    script.src = src;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("Failed to load SampleApp SDK"));
    document.head.appendChild(script);
  });
}

export function BuildWizardEmbed({
  height = "calc(100vh - 80px)",
}: BuildWizardEmbedProps) {
  const containerRef = React.useRef<HTMLDivElement>(null);
  const instanceRef = React.useRef<{ unmount: () => void } | null>(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    let cancelled = false;

    async function init() {
      try {
        await loadScript(SDK_URL);

        if (cancelled || !containerRef.current) return;

        const sdk = (window as any).SampleAppStandalone;
        if (!sdk?.BuildWizardIllustrated) {
          throw new Error("SampleApp SDK BuildWizardIllustrated not available");
        }

        instanceRef.current = sdk.BuildWizardIllustrated(
          {
            apiKey: API_KEY,
          },
          containerRef.current
        );

        setLoading(false);
      } catch (err: any) {
        if (!cancelled) {
          setError(err.message || "Failed to load build wizard");
          setLoading(false);
        }
      }
    }

    init();

    return () => {
      cancelled = true;
      if (instanceRef.current) {
        instanceRef.current.unmount();
        instanceRef.current = null;
      }
    };
  }, []);

  return (
    <div
      style={{
        width: "100%",
        height,
        position: "relative",
        overflow: "hidden",
      }}
    >
      {loading && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: "var(--grayscale-2, #f9fafb)",
            color: "var(--grayscale-11, #6b7280)",
            fontSize: "14px",
          }}
        >
          Loading...
        </div>
      )}
      {error && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: "var(--grayscale-2, #f9fafb)",
            color: "#dc2626",
            fontSize: "14px",
          }}
        >
          {error}
        </div>
      )}
      <div ref={containerRef} style={{ width: "100%", height: "100%" }} />
    </div>
  );
}
