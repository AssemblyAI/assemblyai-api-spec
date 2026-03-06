FROM node:20-slim AS builder

WORKDIR /app

# Copy docs content from repo root (build context should be repo root)
COPY fern/ ./fern/
COPY openapi.yml asyncapi.yml usm-streaming.yml usm-streaming-u3-pro.yml streaming-token.yml llm-gateway.yml ./

# Copy and install MCP server
COPY mcp-server/package*.json ./mcp-server/
WORKDIR /app/mcp-server
RUN npm ci

COPY mcp-server/ ./

# Build content index from docs
RUN npx tsx src/content/ingest.ts

# Compile TypeScript
RUN npx tsc

# --- Production stage ---
FROM node:20-slim

WORKDIR /app
COPY --from=builder /app/mcp-server/build ./build
COPY --from=builder /app/mcp-server/data ./data
COPY --from=builder /app/mcp-server/node_modules ./node_modules
COPY --from=builder /app/mcp-server/package.json ./

EXPOSE 3000

CMD ["node", "build/index.js"]
