"use client";
import * as React from "react";

const SPEECH_SEGMENTS = [
  { start: 0.5, end: 2.8, label: "Hello, I'd like to check on my order status...", confidence: 0.85 },
  { start: 4.2, end: 7.1, label: "um... it was placed last Tuesday I think", confidence: 0.35 },
  { start: 9.0, end: 11.5, label: "The order number is 4-5-7-2", confidence: 0.92 },
];

const TOTAL_DURATION = 14;
const WAVEFORM_POINTS = 280;

function generateWaveform(segments: typeof SPEECH_SEGMENTS): number[] {
  const points: number[] = [];
  for (let i = 0; i < WAVEFORM_POINTS; i++) {
    const time = (i / WAVEFORM_POINTS) * TOTAL_DURATION;
    let amplitude = 0;
    for (const seg of segments) {
      if (time >= seg.start && time <= seg.end) {
        const segProgress = (time - seg.start) / (seg.end - seg.start);
        const envelope = Math.sin(segProgress * Math.PI);
        const noise = Math.sin(time * 47) * 0.3 + Math.sin(time * 123) * 0.2 + Math.sin(time * 67) * 0.15;
        amplitude = envelope * (0.5 + noise * 0.5);
        amplitude = Math.max(0.08, Math.min(1, amplitude));
        break;
      }
    }
    points.push(amplitude);
  }
  return points;
}

interface EotMarker {
  time: number;
  type: "semantic" | "acoustic";
  segmentIndex: number;
}

function computeEotMarkers(
  confidenceThreshold: number,
  minSilenceWhenConfident: number,
  maxTurnSilence: number
): EotMarker[] {
  const markers: EotMarker[] = [];
  for (let i = 0; i < SPEECH_SEGMENTS.length; i++) {
    const seg = SPEECH_SEGMENTS[i];
    const speechEnd = seg.end;
    const minSilenceSec = minSilenceWhenConfident / 1000;
    const maxSilenceSec = maxTurnSilence / 1000;

    if (seg.confidence >= confidenceThreshold) {
      const eotTime = speechEnd + minSilenceSec;
      if (eotTime <= TOTAL_DURATION) {
        markers.push({ time: eotTime, type: "semantic", segmentIndex: i });
      }
    } else {
      const eotTime = speechEnd + maxSilenceSec;
      if (eotTime <= TOTAL_DURATION) {
        markers.push({ time: eotTime, type: "acoustic", segmentIndex: i });
      }
    }
  }
  return markers;
}

const PRESETS = {
  aggressive: { confidence: 0.4, minSilence: 160, maxSilence: 400 },
  balanced: { confidence: 0.4, minSilence: 400, maxSilence: 1280 },
  conservative: { confidence: 0.7, minSilence: 800, maxSilence: 3600 },
};

export function TurnDetectionVisualizer() {
  const [isOpen, setIsOpen] = React.useState(false);
  const [confidence, setConfidence] = React.useState(0.4);
  const [minSilence, setMinSilence] = React.useState(400);
  const [maxSilence, setMaxSilence] = React.useState(1280);
  const [playbackTime, setPlaybackTime] = React.useState(-1);
  const [isPlaying, setIsPlaying] = React.useState(false);
  const animRef = React.useRef<number | null>(null);
  const startTimeRef = React.useRef<number>(0);

  const waveform = React.useMemo(() => generateWaveform(SPEECH_SEGMENTS), []);
  const eotMarkers = React.useMemo(
    () => computeEotMarkers(confidence, minSilence, maxSilence),
    [confidence, minSilence, maxSilence]
  );

  const startPlayback = () => {
    setIsPlaying(true);
    setPlaybackTime(0);
    startTimeRef.current = performance.now();
    const animate = (now: number) => {
      const elapsed = (now - startTimeRef.current) / 1000;
      if (elapsed >= TOTAL_DURATION) {
        setPlaybackTime(TOTAL_DURATION);
        setIsPlaying(false);
        return;
      }
      setPlaybackTime(elapsed);
      animRef.current = requestAnimationFrame(animate);
    };
    animRef.current = requestAnimationFrame(animate);
  };

  const stopPlayback = () => {
    if (animRef.current) cancelAnimationFrame(animRef.current);
    setIsPlaying(false);
    setPlaybackTime(-1);
  };

  React.useEffect(() => {
    return () => {
      if (animRef.current) cancelAnimationFrame(animRef.current);
    };
  }, []);

  const applyPreset = (preset: keyof typeof PRESETS) => {
    const p = PRESETS[preset];
    setConfidence(p.confidence);
    setMinSilence(p.minSilence);
    setMaxSilence(p.maxSilence);
    stopPlayback();
  };

  if (!isOpen) {
    return (
      <p style={{ margin: "16px 0" }}>
        <a
          href="#turn-detection-visualizer"
          onClick={(e) => {
            e.preventDefault();
            setIsOpen(true);
          }}
          style={{
            color: "var(--accent-9, #4f46e5)",
            textDecoration: "underline",
            cursor: "pointer",
            fontWeight: 500,
          }}
        >
          Open the interactive turn detection visualizer
        </a>{" "}
        to see how these parameters affect end-of-turn detection.
      </p>
    );
  }

  const containerStyle: React.CSSProperties = {
    border: "1px solid var(--grayscale-a4, #e5e7eb)",
    borderRadius: "12px",
    padding: "24px",
    backgroundColor: "var(--grayscale-2, #f9fafb)",
    marginTop: "16px",
    marginBottom: "16px",
  };

  const headerStyle: React.CSSProperties = {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "20px",
  };

  const titleStyle: React.CSSProperties = {
    fontSize: "16px",
    fontWeight: 600,
    color: "var(--grayscale-12, #111827)",
    margin: 0,
  };

  const closeBtnStyle: React.CSSProperties = {
    background: "none",
    border: "1px solid var(--grayscale-a4, #d1d5db)",
    borderRadius: "6px",
    padding: "4px 12px",
    cursor: "pointer",
    fontSize: "13px",
    color: "var(--grayscale-11, #6b7280)",
  };

  const waveformContainerStyle: React.CSSProperties = {
    position: "relative",
    height: "180px",
    backgroundColor: "var(--grayscale-1, #ffffff)",
    borderRadius: "8px",
    border: "1px solid var(--grayscale-a4, #e5e7eb)",
    marginBottom: "20px",
    overflow: "hidden",
  };

  const sliderContainerStyle: React.CSSProperties = {
    display: "grid",
    gridTemplateColumns: "1fr 1fr 1fr",
    gap: "16px",
    marginBottom: "20px",
  };

  const sliderGroupStyle: React.CSSProperties = {
    display: "flex",
    flexDirection: "column",
    gap: "6px",
  };

  const sliderLabelStyle: React.CSSProperties = {
    fontSize: "12px",
    fontWeight: 500,
    color: "var(--grayscale-11, #6b7280)",
  };

  const sliderValueStyle: React.CSSProperties = {
    fontSize: "14px",
    fontWeight: 600,
    color: "var(--grayscale-12, #111827)",
  };

  const sliderStyle: React.CSSProperties = {
    width: "100%",
    accentColor: "var(--accent-9, #4f46e5)",
    cursor: "pointer",
  };

  const presetBtnStyle = (active: boolean): React.CSSProperties => ({
    padding: "6px 14px",
    border: active ? "2px solid var(--accent-9, #4f46e5)" : "1px solid var(--grayscale-a4, #d1d5db)",
    borderRadius: "6px",
    background: active ? "var(--accent-3, #eef2ff)" : "var(--grayscale-1, #ffffff)",
    cursor: "pointer",
    fontSize: "13px",
    fontWeight: active ? 600 : 400,
    color: active ? "var(--accent-11, #4338ca)" : "var(--grayscale-12, #111827)",
  });

  const playBtnStyle: React.CSSProperties = {
    padding: "8px 20px",
    border: "none",
    borderRadius: "6px",
    background: "var(--accent-9, #4f46e5)",
    color: "#ffffff",
    cursor: "pointer",
    fontSize: "13px",
    fontWeight: 500,
  };

  const legendItemStyle = (color: string): React.CSSProperties => ({
    display: "inline-flex",
    alignItems: "center",
    gap: "6px",
    fontSize: "12px",
    color: "var(--grayscale-11, #6b7280)",
  });

  const legendDotStyle = (color: string): React.CSSProperties => ({
    width: "10px",
    height: "10px",
    borderRadius: "50%",
    backgroundColor: color,
    display: "inline-block",
  });

  const activePreset =
    confidence === PRESETS.aggressive.confidence &&
    minSilence === PRESETS.aggressive.minSilence &&
    maxSilence === PRESETS.aggressive.maxSilence
      ? "aggressive"
      : confidence === PRESETS.balanced.confidence &&
        minSilence === PRESETS.balanced.minSilence &&
        maxSilence === PRESETS.balanced.maxSilence
      ? "balanced"
      : confidence === PRESETS.conservative.confidence &&
        minSilence === PRESETS.conservative.minSilence &&
        maxSilence === PRESETS.conservative.maxSilence
      ? "conservative"
      : null;

  const timeToX = (time: number, width: number) => (time / TOTAL_DURATION) * width;

  const svgWidth = 700;
  const svgHeight = 160;
  const waveformTop = 20;
  const waveformHeight = 80;
  const barWidth = svgWidth / WAVEFORM_POINTS;

  return (
    <div style={containerStyle} id="turn-detection-visualizer">
      <div style={headerStyle}>
        <h4 style={titleStyle}>Turn Detection Visualizer</h4>
        <button
          style={closeBtnStyle}
          onClick={() => {
            stopPlayback();
            setIsOpen(false);
          }}
        >
          Close
        </button>
      </div>

      <div style={{ display: "flex", gap: "12px", marginBottom: "16px", flexWrap: "wrap", alignItems: "center" }}>
        <span style={{ fontSize: "13px", fontWeight: 500, color: "var(--grayscale-11, #6b7280)" }}>Presets:</span>
        {(["aggressive", "balanced", "conservative"] as const).map((p) => (
          <button key={p} style={presetBtnStyle(activePreset === p)} onClick={() => applyPreset(p)}>
            {p.charAt(0).toUpperCase() + p.slice(1)}
          </button>
        ))}
        <div style={{ marginLeft: "auto" }}>
          <button style={playBtnStyle} onClick={isPlaying ? stopPlayback : startPlayback}>
            {isPlaying ? "Stop" : "Play Animation"}
          </button>
        </div>
      </div>

      <div style={waveformContainerStyle}>
        <svg
          viewBox={`0 0 ${svgWidth} ${svgHeight}`}
          width="100%"
          height="100%"
          preserveAspectRatio="none"
          style={{ display: "block" }}
        >
          <line x1="0" y1={waveformTop + waveformHeight / 2} x2={svgWidth} y2={waveformTop + waveformHeight / 2} stroke="var(--grayscale-a4, #e5e7eb)" strokeWidth="1" />

          {SPEECH_SEGMENTS.map((seg, i) => {
            const x1 = timeToX(seg.start, svgWidth);
            const x2 = timeToX(seg.end, svgWidth);
            return (
              <rect
                key={`seg-bg-${i}`}
                x={x1}
                y={waveformTop}
                width={x2 - x1}
                height={waveformHeight}
                fill="var(--accent-3, #eef2ff)"
                opacity="0.5"
              />
            );
          })}

          {waveform.map((amp, i) => {
            const x = i * barWidth;
            const h = amp * waveformHeight * 0.9;
            const y = waveformTop + (waveformHeight - h) / 2;
            const time = (i / WAVEFORM_POINTS) * TOTAL_DURATION;
            const inSpeech = SPEECH_SEGMENTS.some((s) => time >= s.start && time <= s.end);
            const isPast = playbackTime >= 0 && time <= playbackTime;
            let fill = inSpeech ? "var(--accent-7, #818cf8)" : "var(--grayscale-a4, #d1d5db)";
            if (isPast && inSpeech) fill = "var(--accent-9, #4f46e5)";
            if (isPast && !inSpeech) fill = "var(--grayscale-6, #9ca3af)";
            return (
              <rect key={`bar-${i}`} x={x} y={y} width={Math.max(barWidth - 0.5, 1)} height={h} rx="0.5" fill={fill} />
            );
          })}

          {SPEECH_SEGMENTS.map((seg, i) => {
            const minSilenceSec = minSilence / 1000;
            const maxSilenceSec = maxSilence / 1000;
            const silenceEnd = seg.confidence >= confidence ? seg.end + minSilenceSec : seg.end + maxSilenceSec;
            const silenceBarStart = timeToX(seg.end, svgWidth);
            const silenceBarEnd = timeToX(Math.min(silenceEnd, TOTAL_DURATION), svgWidth);
            const isSemanticPath = seg.confidence >= confidence;
            const color = isSemanticPath ? "#22c55e" : "#f59e0b";
            return (
              <rect
                key={`silence-${i}`}
                x={silenceBarStart}
                y={waveformTop + waveformHeight + 4}
                width={Math.max(silenceBarEnd - silenceBarStart, 0)}
                height="6"
                rx="3"
                fill={color}
                opacity="0.4"
              />
            );
          })}

          {eotMarkers.map((marker, i) => {
            const x = timeToX(marker.time, svgWidth);
            const color = marker.type === "semantic" ? "#22c55e" : "#f59e0b";
            const show = playbackTime < 0 || playbackTime >= marker.time;
            if (!show) return null;
            return (
              <g key={`eot-${i}`}>
                <line x1={x} y1={waveformTop - 4} x2={x} y2={waveformTop + waveformHeight + 14} stroke={color} strokeWidth="2" strokeDasharray="4 2" />
                <rect x={x - 22} y={waveformTop - 16} width="44" height="16" rx="4" fill={color} />
                <text x={x} y={waveformTop - 5} textAnchor="middle" fontSize="9" fontWeight="600" fill="#fff">
                  EoT
                </text>
              </g>
            );
          })}

          {SPEECH_SEGMENTS.map((seg, i) => {
            const x = timeToX(seg.start, svgWidth);
            const confColor = seg.confidence >= confidence ? "#22c55e" : "#f59e0b";
            return (
              <g key={`conf-${i}`}>
                <text x={x + 4} y={waveformTop + waveformHeight + 24} fontSize="9" fill="var(--grayscale-11, #6b7280)">
                  conf: {seg.confidence.toFixed(2)}
                </text>
                <circle cx={x + 2} cy={waveformTop + waveformHeight + 21} r="2.5" fill={confColor} />
              </g>
            );
          })}

          {playbackTime >= 0 && (
            <line
              x1={timeToX(playbackTime, svgWidth)}
              y1={0}
              x2={timeToX(playbackTime, svgWidth)}
              y2={svgHeight}
              stroke="var(--grayscale-12, #111827)"
              strokeWidth="1.5"
              opacity="0.6"
            />
          )}

          {Array.from({ length: TOTAL_DURATION + 1 }).map((_, i) => {
            const x = timeToX(i, svgWidth);
            return (
              <g key={`tick-${i}`}>
                <text x={x} y={svgHeight - 2} fontSize="8" fill="var(--grayscale-9, #9ca3af)" textAnchor="middle">
                  {i}s
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      <div style={{ display: "flex", gap: "16px", marginBottom: "16px", flexWrap: "wrap" }}>
        <span style={legendItemStyle("#22c55e")}>
          <span style={legendDotStyle("#22c55e")} /> Semantic EoT (confidence met + min silence)
        </span>
        <span style={legendItemStyle("#f59e0b")}>
          <span style={legendDotStyle("#f59e0b")} /> Acoustic EoT (max silence exceeded)
        </span>
      </div>

      <div style={sliderContainerStyle}>
        <div style={sliderGroupStyle}>
          <span style={sliderLabelStyle}>end_of_turn_confidence_threshold</span>
          <span style={sliderValueStyle}>{confidence.toFixed(2)}</span>
          <input
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={confidence}
            onChange={(e) => setConfidence(parseFloat(e.target.value))}
            style={sliderStyle}
          />
          <span style={{ fontSize: "11px", color: "var(--grayscale-9, #9ca3af)" }}>0 = instant EoT on silence, 1 = disable semantic</span>
        </div>
        <div style={sliderGroupStyle}>
          <span style={sliderLabelStyle}>min_end_of_turn_silence_when_confident</span>
          <span style={sliderValueStyle}>{minSilence} ms</span>
          <input
            type="range"
            min="0"
            max="2000"
            step="20"
            value={minSilence}
            onChange={(e) => setMinSilence(parseInt(e.target.value))}
            style={sliderStyle}
          />
          <span style={{ fontSize: "11px", color: "var(--grayscale-9, #9ca3af)" }}>Silence required when confidence is above threshold</span>
        </div>
        <div style={sliderGroupStyle}>
          <span style={sliderLabelStyle}>max_turn_silence</span>
          <span style={sliderValueStyle}>{maxSilence} ms</span>
          <input
            type="range"
            min="100"
            max="5000"
            step="20"
            value={maxSilence}
            onChange={(e) => setMaxSilence(parseInt(e.target.value))}
            style={sliderStyle}
          />
          <span style={{ fontSize: "11px", color: "var(--grayscale-9, #9ca3af)" }}>Max silence before EoT regardless of confidence</span>
        </div>
      </div>

      <div style={{ fontSize: "13px", color: "var(--grayscale-11, #6b7280)", lineHeight: 1.6 }}>
        <p style={{ margin: "0 0 8px 0" }}>
          The example above shows three speech segments with different confidence scores.
          Drag the sliders to see how adjusting each parameter changes when end-of-turn (EoT) is detected.
        </p>
        <p style={{ margin: 0 }}>
          <strong>Semantic detection</strong> (green) triggers when confidence {"\u2265"} threshold and silence exceeds <code>min_end_of_turn_silence_when_confident</code>.{" "}
          <strong>Acoustic detection</strong> (amber) triggers when confidence {"<"} threshold and silence exceeds <code>max_turn_silence</code>.
        </p>
      </div>
    </div>
  );
}
