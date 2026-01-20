"use client";
import * as React from "react";

interface AudioPlayerProps {
  src: string;
  title?: string;
}

export function AudioPlayer({ src, title }: AudioPlayerProps) {
  const [isPlaying, setIsPlaying] = React.useState(false);
  const [currentTime, setCurrentTime] = React.useState(0);
  const [duration, setDuration] = React.useState(0);
  const [isLoaded, setIsLoaded] = React.useState(false);
  const [isHovered, setIsHovered] = React.useState(false);
  const audioRef = React.useRef<HTMLAudioElement>(null);

  const formatTime = (time: number) => {
    if (isNaN(time)) return "0:00";
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, "0")}`;
  };

  const handlePlayPause = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration);
      setIsLoaded(true);
    }
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const time = parseFloat(e.target.value);
    if (audioRef.current) {
      audioRef.current.currentTime = time;
      setCurrentTime(time);
    }
  };

  const handleEnded = () => {
    setIsPlaying(false);
    setCurrentTime(0);
  };

  const progress = duration > 0 ? (currentTime / duration) * 100 : 0;

  // Use CSS custom properties that Fern defines, with fallbacks
  // Light: accent #2545D3, Dark: accent #df9844
  // Dark background: #09060F, Dark border: #2A2522
  const accentColor = "var(--accent-9, #2545D3)";
  const accentHoverColor = "var(--accent-10, #1a36a8)";

  return (
    <div
      style={{
        borderRadius: "8px",
        border: "1px solid var(--grayscale-a4, #E5E5E5)",
        backgroundColor: "var(--grayscale-2, #f9fafb)",
        padding: "16px",
        margin: "16px 0",
      }}
    >
      <audio
        ref={audioRef}
        src={src}
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
        onEnded={handleEnded}
        preload="metadata"
      />

      {title && (
        <div
          style={{
            fontSize: "14px",
            fontWeight: 500,
            color: "var(--grayscale-12, #374151)",
            marginBottom: "12px",
          }}
        >
          {title}
        </div>
      )}

      <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
        {/* Play/Pause Button */}
        <button
          onClick={handlePlayPause}
          disabled={!isLoaded}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            width: "40px",
            height: "40px",
            borderRadius: "50%",
            backgroundColor: !isLoaded ? "var(--grayscale-8, #9ca3af)" : (isHovered ? accentHoverColor : accentColor),
            color: "white",
            border: "none",
            cursor: isLoaded ? "pointer" : "not-allowed",
            transition: "background-color 0.2s",
          }}
          aria-label={isPlaying ? "Pause" : "Play"}
        >
          {isPlaying ? (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <rect x="6" y="4" width="4" height="16" rx="1" />
              <rect x="14" y="4" width="4" height="16" rx="1" />
            </svg>
          ) : (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8 5.14v14l11-7-11-7z" />
            </svg>
          )}
        </button>

        {/* Progress Bar */}
        <div style={{ flex: 1, display: "flex", alignItems: "center", gap: "8px" }}>
          <span
            style={{
              fontSize: "12px",
              color: "var(--grayscale-11, #6b7280)",
              width: "40px",
              textAlign: "right",
              fontFamily: "monospace",
            }}
          >
            {formatTime(currentTime)}
          </span>

          <div style={{ flex: 1, position: "relative", height: "8px" }}>
            <div
              style={{
                position: "absolute",
                inset: 0,
                backgroundColor: "var(--grayscale-a4, #e5e7eb)",
                borderRadius: "9999px",
              }}
            />
            <div
              style={{
                position: "absolute",
                top: 0,
                bottom: 0,
                left: 0,
                backgroundColor: accentColor,
                borderRadius: "9999px",
                width: `${progress}%`,
              }}
            />
            <input
              type="range"
              min="0"
              max={duration || 0}
              value={currentTime}
              onChange={handleSeek}
              style={{
                position: "absolute",
                inset: 0,
                width: "100%",
                height: "100%",
                opacity: 0,
                cursor: "pointer",
              }}
              aria-label="Seek"
            />
          </div>

          <span
            style={{
              fontSize: "12px",
              color: "var(--grayscale-11, #6b7280)",
              width: "40px",
              fontFamily: "monospace",
            }}
          >
            {formatTime(duration)}
          </span>
        </div>
      </div>
    </div>
  );
}
