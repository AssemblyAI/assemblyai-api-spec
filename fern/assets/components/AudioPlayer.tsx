"use client";
import * as React from "react";

interface AudioPlayerProps {
  src: string;
  type?: string;
  fallbackText?: string;
}

export function AudioPlayer({
  src,
  type = "audio/mpeg",
  fallbackText = "Your browser does not support the audio element.",
}: AudioPlayerProps) {
  return (
    <audio controls style={{ width: "100%" }}>
      <source src={src} type={type} />
      {fallbackText} <a href={src}>Download the audio</a>.
    </audio>
  );
}
