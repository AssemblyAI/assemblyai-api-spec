import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import react from "@astrojs/react";

export default defineConfig({
  site: "https://www.assemblyai.com",
  base: "/docs",
  integrations: [
    starlight({
      title: "AssemblyAI Docs",
      logo: {
        light: "./src/assets/logo-light.svg",
        dark: "./src/assets/AssemblyAI_White.svg",
        replacesTitle: true,
      },
      favicon: "/favicon.png",
      customCss: ["./src/styles/custom.css"],
      // No social links
      components: {
        // Override head to inject scripts
        Head: "./src/components/Head.astro",
      },
      sidebar: [
        {
          label: "Getting Started",
          items: [
            { label: "Overview", slug: "" },
            {
              label: "Transcribe a pre-recorded audio file",
              slug: "getting-started/transcribe-an-audio-file",
            },
            {
              label: "Transcribe streaming audio",
              slug: "getting-started/transcribe-streaming-audio",
            },
            { label: "Models", slug: "getting-started/models" },
          ],
        },
        {
          label: "Pre-recorded Speech-to-text",
          items: [
            {
              label: "Overview",
              slug: "pre-recorded-audio",
            },
            {
              label: "Model selection",
              slug: "pre-recorded-audio/select-the-speech-model",
            },
            {
              label: "Speaker diarization",
              slug: "pre-recorded-audio/speaker-diarization",
            },
          ],
        },
        {
          label: "Streaming Speech-to-text",
          items: [
            {
              label: "Overview",
              slug: "universal-streaming",
            },
          ],
        },
        {
          label: "Speech Understanding",
          items: [
            {
              label: "Speaker Identification",
              slug: "speech-understanding/speaker-identification",
            },
            {
              label: "Entity Detection",
              slug: "speech-understanding/entity-detection",
            },
            {
              label: "Sentiment Analysis",
              slug: "speech-understanding/sentiment-analysis",
            },
          ],
        },
        {
          label: "LLM Gateway",
          items: [
            { label: "Overview", slug: "llm-gateway/overview" },
          ],
        },
        {
          label: "API Reference",
          items: [
            {
              label: "Interactive API Reference",
              link: "/docs/api-reference",
            },
          ],
        },
        {
          label: "FAQ",
          items: [{ label: "Overview", slug: "faq" }],
        },
      ],
      head: [
        {
          tag: "meta",
          attrs: {
            property: "og:site_name",
            content: "AssemblyAI Docs",
          },
        },
      ],
    }),
    react(),
  ],
  // Redirects are handled by Vercel (vercel.json) at the edge for
  // better performance. Only simple, non-parameterized redirects go here.
  redirects: {},
});
