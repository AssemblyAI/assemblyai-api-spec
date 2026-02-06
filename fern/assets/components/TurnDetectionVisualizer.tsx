"use client";
import * as React from "react";

const SEGMENTS = [
  { start: 0.5, end: 2.8, confidence: 0.85 },
  { start: 4.2, end: 7.1, confidence: 0.35 },
  { start: 9.0, end: 11.5, confidence: 0.92 },
];

const DURATION = 14;

const PRESETS: Record<string, { confidence: number; minSilence: number; maxSilence: number; label: string }> = {
  aggressive: { confidence: 0.4, minSilence: 160, maxSilence: 400, label: "Aggressive" },
  balanced: { confidence: 0.4, minSilence: 400, maxSilence: 1280, label: "Balanced" },
  conservative: { confidence: 0.7, minSilence: 800, maxSilence: 3600, label: "Conservative" },
};

interface EotResult {
  time: number;
  type: "semantic" | "acoustic";
  segIndex: number;
}

function computeEot(conf: number, minMs: number, maxMs: number): EotResult[] {
  const results: EotResult[] = [];
  for (let i = 0; i < SEGMENTS.length; i++) {
    const seg = SEGMENTS[i];
    const nextSeg = i < SEGMENTS.length - 1 ? SEGMENTS[i + 1] : null;
    if (seg.confidence >= conf) {
      const t = seg.end + minMs / 1000;
      if (t <= DURATION && (!nextSeg || t < nextSeg.start)) {
        results.push({ time: t, type: "semantic", segIndex: i });
      }
    } else {
      const t = seg.end + maxMs / 1000;
      if (t <= DURATION && (!nextSeg || t < nextSeg.start)) {
        results.push({ time: t, type: "acoustic", segIndex: i });
      }
    }
  }
  return results;
}

function generateWaveformBars(start: number, end: number, seed: number): number[] {
  const count = Math.max(8, Math.floor((end - start) * 12));
  const bars: number[] = [];
  let s = seed;
  for (let i = 0; i < count; i++) {
    s = (s * 1103515245 + 12345) & 0x7fffffff;
    const frac = i / count;
    const envelope = Math.sin(frac * Math.PI) * 0.6 + 0.3;
    const noise = (s % 100) / 100;
    bars.push(Math.max(0.15, Math.min(1, envelope * (0.5 + noise * 0.5))));
  }
  return bars;
}

export function TurnDetectionVisualizer() {
  const [preset, setPreset] = React.useState<string>("balanced");

  const config = PRESETS[preset];
  const eotMarkers = React.useMemo(
    () => computeEot(config.confidence, config.minSilence, config.maxSilence),
    [config.confidence, config.minSilence, config.maxSilence]
  );

  const waveforms = React.useMemo(
    () => SEGMENTS.map((seg, i) => generateWaveformBars(seg.start, seg.end, (i + 1) * 7919)),
    []
  );

  const toX= (t: number) => (t / DURATION) * 100;

  const turnsNotEnded: Set<number> = new Set();
  for (let i = 0; i < SEGMENTS.length; i++) {
    const seg = SEGMENTS[i];
    const nextSeg = i < SEGMENTS.length - 1 ? SEGMENTS[i + 1] : null;
    const isAbove = seg.confidence >= config.confidence;
    const silenceMs = isAbove ? config.minSilence : config.maxSilence;
    const eotTime = seg.end + silenceMs / 1000;
    if (nextSeg && eotTime >= nextSeg.start) {
      turnsNotEnded.add(i);
    }
  }

  return (
    <div
      id="turn-detection-visualizer"
      style={{
        border: "1px solid var(--grayscale-a4, #e5e7eb)",
        borderRadius: "12px",
        padding: "24px",
        backgroundColor: "var(--grayscale-2, #f9fafb)",
        margin: "16px 0",
        overflow: "hidden",
        maxWidth: "100%",
        boxSizing: "border-box" as const,
      }}
    >
      <div style={{ marginBottom: "16px" }}>
        <span style={{ fontSize: "15px", fontWeight: 600, color: "var(--grayscale-12, #111827)" }}>
          Turn Detection Visualizer
        </span>
      </div>

      <div style={{ display: "flex", gap: "8px", marginBottom: "16px", flexWrap: "wrap" as const }}>
        {Object.entries(PRESETS).map(([key, p]) => {
          const isActive = preset === key;
          return (
            <button
              key={key}
              onClick={() => setPreset(key)}
              style={{
                padding: "6px 16px",
                border: isActive ? "2px solid var(--accent-9, #4f46e5)" : "1px solid var(--grayscale-a4, #d1d5db)",
                borderRadius: "6px",
                background: isActive ? "var(--accent-3, #eef2ff)" : "var(--grayscale-1, #ffffff)",
                cursor: "pointer",
                fontSize: "13px",
                fontWeight: isActive ? 600 : 400,
                color: isActive ? "var(--accent-11, #4338ca)" : "var(--grayscale-12, #111827)",
              }}
            >
              {p.label}
            </button>
          );
        })}
      </div>

      <div
        style={{
          position: "relative" as const,
          background: "var(--grayscale-1, #ffffff)",
          borderRadius: "8px",
          border: "1px solid var(--grayscale-a4, #e5e7eb)",
          padding: "16px 12px",
          marginBottom: "16px",
          overflowX: "auto" as const,
        }}
      >
        <div style={{ position: "relative" as const, height: "130px", minWidth: "500px" }}>
          {SEGMENTS.map((seg, i) => {
            const left = toX(seg.start);
            const width = toX(seg.end) - left;
            const isAbove = seg.confidence >= config.confidence;
            const bars = waveforms[i];
            const continued = turnsNotEnded.has(i);
            return (
              <div key={"seg-" + i}>
                <div
                  style={{
                    position: "absolute" as const,
                    left: left + "%",
                    width: width + "%",
                    top: "22px",
                    height: "48px",
                    display: "flex",
                    alignItems: "center",
                    gap: "1px",
                    padding: "0 2px",
                    boxSizing: "border-box" as const,
                  }}
                >
                  {bars.map((h, bi) => (
                    <div
                      key={bi}
                      style={{
                        flex: 1,
                        height: (h * 100) + "%",
                        borderRadius: "1px",
                        background: isAbove ? "var(--accent-9, #4f46e5)" : "var(--accent-7, #818cf8)",
                        opacity: 0.65,
                        minWidth: "2px",
                      }}
                    />
                  ))}
                </div>
                <div
                  style={{
                    position: "absolute" as const,
                    left: left + "%",
                    width: width + "%",
                    top: "6px",
                    fontSize: "10px",
                    color: "var(--grayscale-10, #4b5563)",
                    textAlign: "center" as const,
                    whiteSpace: "nowrap" as const,
                  }}
                >
                  {"conf: " + seg.confidence}
                </div>
                {continued && (
                  <div
                    style={{
                      position: "absolute" as const,
                      left: toX(seg.end) + "%",
                      width: toX(SEGMENTS[i + 1].start) - toX(seg.end) + "%",
                      top: "42px",
                      height: "4px",
                      background: "var(--accent-5, #a5b4fc)",
                      opacity: 0.5,
                      borderRadius: "2px",
                    }}
                  />
                )}
              </div>
            );
          })}

          {SEGMENTS.map((seg, i) => {
            const isAbove = seg.confidence >= config.confidence;
            const silenceMs = isAbove ? config.minSilence : config.maxSilence;
            const silenceEnd = seg.end + silenceMs / 1000;
            const nextSeg = i < SEGMENTS.length - 1 ? SEGMENTS[i + 1] : null;
            if (silenceEnd > DURATION) return null;
            if (nextSeg && silenceEnd >= nextSeg.start) return null;
            const startX = toX(seg.end);
            const endX = toX(silenceEnd);
            const color = isAbove ? "#22c55e" : "#f59e0b";
            return (
              <div key={"wait-" + i}>
                <div
                  style={{
                    position: "absolute" as const,
                    left: startX + "%",
                    width: (endX - startX) + "%",
                    top: "42px",
                    height: "8px",
                    borderRadius: "4px",
                    background: color,
                    opacity: 0.25,
                  }}
                />
              </div>
            );
          })}

          {eotMarkers.map((m, i) => {
            const x = toX(m.time);
            const color = m.type === "semantic" ? "#22c55e" : "#f59e0b";
            const label = m.type === "semantic" ? "min_silence" : "max_silence";
            return (
              <div key={"eot-" + i}>
                <div
                  style={{
                    position: "absolute" as const,
                    left: x + "%",
                    top: "10px",
                    bottom: "30px",
                    width: "2px",
                    background: color,
                    transform: "translateX(-1px)",
                  }}
                />
                <div
                  style={{
                    position: "absolute" as const,
                    left: x + "%",
                    top: "78px",
                    transform: "translateX(-50%)",
                    fontSize: "10px",
                    fontWeight: 600,
                    color: color,
                    whiteSpace: "nowrap" as const,
                    textAlign: "center" as const,
                    lineHeight: 1.3,
                  }}
                >
                  {"EoT"}
                  <br />
                  <span style={{ fontSize: "8px", fontWeight: 400, color: "var(--grayscale-9, #9ca3af)" }}>{label}</span>
                </div>
              </div>
            );
          })}

          {turnsNotEnded.size > 0 && Array.from(turnsNotEnded).map((idx) => {
            const seg = SEGMENTS[idx];
            const nextSeg = SEGMENTS[idx + 1];
            const midX = toX((seg.end + nextSeg.start) / 2);
            return (
              <div
                key={"cont-" + idx}
                style={{
                  position: "absolute" as const,
                  left: midX + "%",
                  top: "78px",
                  transform: "translateX(-50%)",
                  fontSize: "9px",
                  color: "var(--grayscale-9, #9ca3af)",
                  whiteSpace: "nowrap" as const,
                  fontStyle: "italic" as const,
                }}
              >
                turn continues
              </div>
            );
          })}
        </div>
      </div>

      <div style={{ display: "flex", gap: "16px", marginBottom: "12px", fontSize: "12px", color: "var(--grayscale-11, #6b7280)", flexWrap: "wrap" as const }}>
        <span style={{ display: "inline-flex", alignItems: "center", gap: "5px" }}>
          <span style={{ width: "8px", height: "8px", borderRadius: "50%", background: "#22c55e", display: "inline-block" }} />
          EoT (min_silence_when_confident)
        </span>
        <span style={{ display: "inline-flex", alignItems: "center", gap: "5px" }}>
          <span style={{ width: "8px", height: "8px", borderRadius: "50%", background: "#f59e0b", display: "inline-block" }} />
          EoT (max_turn_silence)
        </span>
        {turnsNotEnded.size > 0 && (
          <span style={{ display: "inline-flex", alignItems: "center", gap: "5px", fontStyle: "italic" as const }}>
            <span style={{ width: "16px", height: "3px", borderRadius: "2px", background: "var(--accent-5, #a5b4fc)", opacity: 0.6, display: "inline-block" }} />
            Turn continues
          </span>
        )}
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr auto",
          gap: "4px 12px",
          fontSize: "12px",
          color: "var(--grayscale-11, #6b7280)",
          marginBottom: "12px",
        }}
      >
        <code style={{ fontSize: "11px" }}>end_of_turn_confidence_threshold</code>
        <span style={{ fontWeight: 600, color: "var(--grayscale-12, #111827)" }}>{config.confidence}</span>
        <code style={{ fontSize: "11px" }}>min_end_of_turn_silence_when_confident</code>
        <span style={{ fontWeight: 600, color: "var(--grayscale-12, #111827)" }}>{config.minSilence} ms</span>
        <code style={{ fontSize: "11px" }}>max_turn_silence</code>
        <span style={{ fontWeight: 600, color: "var(--grayscale-12, #111827)" }}>{config.maxSilence} ms</span>
      </div>

      <p style={{ margin: "0", fontSize: "12px", color: "var(--grayscale-10, #6b7280)", lineHeight: 1.5 }}>
        When confidence {"\u2265"} threshold, EoT triggers after <code>min_end_of_turn_silence_when_confident</code>.{" "}
        When confidence {"<"} threshold, EoT triggers after <code>max_turn_silence</code>.{" "}
        If the silence period extends into the next speech segment, the turn continues.
      </p>
    </div>
  );
}
