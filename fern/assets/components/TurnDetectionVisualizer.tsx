"use client";
import * as React from "react";

const SEGMENTS = [
  { start: 0.5, end: 2.8, confidence: 0.85 },
  { start: 4.2, end: 7.1, confidence: 0.35 },
  { start: 9.0, end: 11.5, confidence: 0.92 },
];

const DURATION = 14;

const PRESETS = {
  aggressive: { confidence: 0.4, minSilence: 160, maxSilence: 400 },
  balanced: { confidence: 0.4, minSilence: 400, maxSilence: 1280 },
  conservative: { confidence: 0.7, minSilence: 800, maxSilence: 3600 },
};

function getActivePreset(c: number, min: number, max: number): string | null {
  for (const [name, p] of Object.entries(PRESETS)) {
    if (c === p.confidence && min === p.minSilence && max === p.maxSilence) return name;
  }
  return null;
}

interface EotResult {
  time: number;
  type: "semantic" | "acoustic";
  segIndex: number;
}

function computeEot(conf: number, minMs: number, maxMs: number): EotResult[] {
  const results: EotResult[] = [];
  for (let i = 0; i < SEGMENTS.length; i++) {
    const seg = SEGMENTS[i];
    if (seg.confidence >= conf) {
      const t = seg.end + minMs / 1000;
      if (t <= DURATION) results.push({ time: t, type: "semantic", segIndex: i });
    } else {
      const t = seg.end + maxMs / 1000;
      if (t <= DURATION) results.push({ time: t, type: "acoustic", segIndex: i });
    }
  }
  return results;
}

function SliderParam(props: {
  label: string;
  value: number;
  displayValue: string;
  min: number;
  max: number;
  step: number;
  onChange: (v: number) => void;
  parseValue: (s: string) => number;
}) {
  return (
    <div style={{ display: "flex", flexDirection: "column" as const, gap: "4px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
        <span style={{ fontSize: "12px", fontWeight: 500, color: "var(--grayscale-11, #6b7280)", fontFamily: "monospace" }}>{props.label}</span>
        <span style={{ fontSize: "14px", fontWeight: 600, color: "var(--grayscale-12, #111827)", marginLeft: "8px", whiteSpace: "nowrap" as const }}>{props.displayValue}</span>
      </div>
      <input
        type="range"
        min={props.min}
        max={props.max}
        step={props.step}
        value={props.value}
        onChange={(e) => props.onChange(props.parseValue(e.target.value))}
        style={{ width: "100%", accentColor: "var(--accent-9, #4f46e5)", cursor: "pointer" }}
      />
    </div>
  );
}

export function TurnDetectionVisualizer() {
  const [isOpen, setIsOpen] = React.useState(false);
  const [confidence, setConfidence] = React.useState(0.4);
  const [minSilence, setMinSilence] = React.useState(400);
  const [maxSilence, setMaxSilence] = React.useState(1280);

  const eotMarkers = React.useMemo(
    () => computeEot(confidence, minSilence, maxSilence),
    [confidence, minSilence, maxSilence]
  );

  const activePreset = getActivePreset(confidence, minSilence, maxSilence);

  if (!isOpen) {
    return (
      <p style={{ margin: "16px 0" }}>
        <a
          href="#turn-detection-visualizer"
          onClick={(e) => { e.preventDefault(); setIsOpen(true); }}
          style={{ color: "var(--accent-9, #4f46e5)", textDecoration: "underline", cursor: "pointer", fontWeight: 500 }}
        >
          Open the interactive turn detection visualizer
        </a>
        {" "}to see how parameters affect end-of-turn detection.
      </p>
    );
  }

  const toX = (t: number) => (t / DURATION) * 100;

  const presetBtn = (name: "aggressive" | "balanced" | "conservative") => {
    const isActive = activePreset === name;
    return (
      <button
        key={name}
        onClick={() => {
          const v = PRESETS[name];
          setConfidence(v.confidence);
          setMinSilence(v.minSilence);
          setMaxSilence(v.maxSilence);
        }}
        style={{
          padding: "5px 14px",
          border: isActive ? "2px solid var(--accent-9, #4f46e5)" : "1px solid var(--grayscale-a4, #d1d5db)",
          borderRadius: "6px",
          background: isActive ? "var(--accent-3, #eef2ff)" : "var(--grayscale-1, #ffffff)",
          cursor: "pointer",
          fontSize: "13px",
          fontWeight: isActive ? 600 : 400,
          color: isActive ? "var(--accent-11, #4338ca)" : "var(--grayscale-12, #111827)",
        }}
      >
        {name.charAt(0).toUpperCase() + name.slice(1)}
      </button>
    );
  };

  return (
    <div
      id="turn-detection-visualizer"
      style={{
        border: "1px solid var(--grayscale-a4, #e5e7eb)",
        borderRadius: "12px",
        padding: "24px",
        backgroundColor: "var(--grayscale-2, #f9fafb)",
        margin: "16px 0",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
        <span style={{ fontSize: "15px", fontWeight: 600, color: "var(--grayscale-12, #111827)" }}>
          Turn Detection Visualizer
        </span>
        <button
          onClick={() => setIsOpen(false)}
          style={{
            background: "none",
            border: "1px solid var(--grayscale-a4, #d1d5db)",
            borderRadius: "6px",
            padding: "4px 12px",
            cursor: "pointer",
            fontSize: "13px",
            color: "var(--grayscale-11, #6b7280)",
          }}
        >
          Close
        </button>
      </div>

      <div style={{ display: "flex", gap: "8px", marginBottom: "20px", flexWrap: "wrap" as const }}>
        {presetBtn("aggressive")}
        {presetBtn("balanced")}
        {presetBtn("conservative")}
      </div>

      <div
        style={{
          position: "relative" as const,
          background: "var(--grayscale-1, #ffffff)",
          borderRadius: "8px",
          border: "1px solid var(--grayscale-a4, #e5e7eb)",
          padding: "16px 12px",
          marginBottom: "20px",
          overflowX: "auto" as const,
        }}
      >
        <div style={{ position: "relative" as const, height: "100px", minWidth: "500px" }}>
          {SEGMENTS.map((seg, i) => {
            const left = toX(seg.start);
            const width = toX(seg.end) - left;
            const isAbove = seg.confidence >= confidence;
            return (
              <div key={"seg-" + i}>
                <div
                  style={{
                    position: "absolute" as const,
                    left: left + "%",
                    width: width + "%",
                    top: "30px",
                    height: "28px",
                    borderRadius: "6px",
                    background: isAbove ? "var(--accent-7, #818cf8)" : "var(--accent-5, #a5b4fc)",
                    opacity: 0.7,
                  }}
                />
                <div
                  style={{
                    position: "absolute" as const,
                    left: left + "%",
                    width: width + "%",
                    top: "12px",
                    fontSize: "11px",
                    color: "var(--grayscale-10, #4b5563)",
                    textAlign: "center" as const,
                    whiteSpace: "nowrap" as const,
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                  }}
                >
                  {"conf: " + seg.confidence}
                </div>
              </div>
            );
          })}

          {SEGMENTS.map((seg, i) => {
            const isAbove = seg.confidence >= confidence;
            const silenceMs = isAbove ? minSilence : maxSilence;
            const silenceEnd = seg.end + silenceMs / 1000;
            if (silenceEnd > DURATION) return null;
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
                    top: "40px",
                    height: "8px",
                    borderRadius: "4px",
                    background: color,
                    opacity: 0.3,
                  }}
                />
              </div>
            );
          })}

          {eotMarkers.map((m, i) => {
            const x = toX(m.time);
            const color = m.type === "semantic" ? "#22c55e" : "#f59e0b";
            const label = m.type === "semantic" ? "semantic" : "acoustic";
            return (
              <div key={"eot-" + i}>
                <div
                  style={{
                    position: "absolute" as const,
                    left: x + "%",
                    top: "6px",
                    bottom: "10px",
                    width: "2px",
                    background: color,
                    transform: "translateX(-1px)",
                  }}
                />
                <div
                  style={{
                    position: "absolute" as const,
                    left: x + "%",
                    top: "68px",
                    transform: "translateX(-50%)",
                    fontSize: "10px",
                    fontWeight: 600,
                    color: color,
                    whiteSpace: "nowrap" as const,
                  }}
                >
                  EoT
                </div>
                <div
                  style={{
                    position: "absolute" as const,
                    left: x + "%",
                    top: "80px",
                    transform: "translateX(-50%)",
                    fontSize: "9px",
                    color: "var(--grayscale-9, #9ca3af)",
                    whiteSpace: "nowrap" as const,
                  }}
                >
                  {label}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div style={{ display: "flex", gap: "12px", marginBottom: "16px", fontSize: "12px", color: "var(--grayscale-11, #6b7280)" }}>
        <span style={{ display: "inline-flex", alignItems: "center", gap: "5px" }}>
          <span style={{ width: "8px", height: "8px", borderRadius: "50%", background: "#22c55e", display: "inline-block" }} />
          Semantic EoT
        </span>
        <span style={{ display: "inline-flex", alignItems: "center", gap: "5px" }}>
          <span style={{ width: "8px", height: "8px", borderRadius: "50%", background: "#f59e0b", display: "inline-block" }} />
          Acoustic EoT
        </span>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "16px" }}>
        <SliderParam
          label="end_of_turn_confidence_threshold"
          value={confidence}
          displayValue={confidence.toFixed(2)}
          min={0}
          max={1}
          step={0.05}
          onChange={setConfidence}
          parseValue={parseFloat}
        />
        <SliderParam
          label="min_end_of_turn_silence_when_confident"
          value={minSilence}
          displayValue={minSilence + " ms"}
          min={0}
          max={2000}
          step={20}
          onChange={setMinSilence}
          parseValue={parseInt}
        />
        <SliderParam
          label="max_turn_silence"
          value={maxSilence}
          displayValue={maxSilence + " ms"}
          min={100}
          max={5000}
          step={20}
          onChange={setMaxSilence}
          parseValue={parseInt}
        />
      </div>

      <p style={{ margin: "16px 0 0 0", fontSize: "13px", color: "var(--grayscale-11, #6b7280)", lineHeight: 1.6 }}>
        Drag the sliders to see how end-of-turn detection changes.{" "}
        <strong style={{ color: "#22c55e" }}>Semantic</strong> EoT triggers when confidence {"\u2265"} threshold after <code>min_end_of_turn_silence_when_confident</code>.{" "}
        <strong style={{ color: "#f59e0b" }}>Acoustic</strong> EoT triggers when confidence {"<"} threshold after <code>max_turn_silence</code>.
      </p>
    </div>
  );
}
