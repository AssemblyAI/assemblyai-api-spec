import express from "express";
import { randomUUID } from "node:crypto";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { isInitializeRequest } from "@modelcontextprotocol/sdk/types.js";
import { createMcpServer } from "./server.js";

// --- Configuration ---
const MAX_SESSIONS = 1000;
const SESSION_TIMEOUT_MS = 30 * 60 * 1000; // 30 minutes
const SESSION_CLEANUP_INTERVAL_MS = 5 * 60 * 1000; // check every 5 min
const RATE_LIMIT_WINDOW_MS = 60 * 1000; // 1 minute
const RATE_LIMIT_MAX_REQUESTS = 60; // per IP per window

const app = express();

// Request size limit
app.use(express.json({ limit: "1mb" }));

// Security headers (matching LiveKit's approach)
app.use((_req, res, next) => {
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "DENY");
  res.setHeader("Content-Security-Policy", "frame-ancestors 'none'");
  res.setHeader("Referrer-Policy", "no-referrer-when-downgrade");
  next();
});

// --- Rate Limiting (in-memory, per IP) ---
const rateLimitMap = new Map<string, { count: number; resetAt: number }>();

function rateLimit(req: express.Request, res: express.Response, next: express.NextFunction) {
  const ip = req.ip || req.socket.remoteAddress || "unknown";
  const now = Date.now();

  let entry = rateLimitMap.get(ip);
  if (!entry || now > entry.resetAt) {
    entry = { count: 0, resetAt: now + RATE_LIMIT_WINDOW_MS };
    rateLimitMap.set(ip, entry);
  }

  entry.count++;
  res.setHeader("X-RateLimit-Limit", RATE_LIMIT_MAX_REQUESTS.toString());
  res.setHeader("X-RateLimit-Remaining", Math.max(0, RATE_LIMIT_MAX_REQUESTS - entry.count).toString());

  if (entry.count > RATE_LIMIT_MAX_REQUESTS) {
    res.status(429).json({
      jsonrpc: "2.0",
      error: { code: -32000, message: "Rate limit exceeded. Try again later." },
      id: null,
    });
    return;
  }

  next();
}

// Clean up stale rate limit entries periodically
setInterval(() => {
  const now = Date.now();
  for (const [ip, entry] of rateLimitMap) {
    if (now > entry.resetAt) rateLimitMap.delete(ip);
  }
}, RATE_LIMIT_WINDOW_MS);

// --- Session Management ---
interface SessionEntry {
  transport: StreamableHTTPServerTransport;
  lastActivity: number;
}

const sessions = new Map<string, SessionEntry>();

function cleanupSession(sid: string) {
  const entry = sessions.get(sid);
  if (entry) {
    entry.transport.close().catch(() => {});
    sessions.delete(sid);
  }
}

// Periodic cleanup of idle sessions
setInterval(() => {
  const now = Date.now();
  for (const [sid, entry] of sessions) {
    if (now - entry.lastActivity > SESSION_TIMEOUT_MS) {
      console.error(`Cleaning up idle session: ${sid}`);
      cleanupSession(sid);
    }
  }
}, SESSION_CLEANUP_INTERVAL_MS);

// --- Routes ---

// Health check
app.get("/health", (_req, res) => {
  res.json({ status: "ok", sessions: sessions.size });
});

// MCP endpoint - POST for client messages
app.post("/mcp", rateLimit, async (req, res) => {
  const sessionId = req.headers["mcp-session-id"] as string | undefined;

  if (sessionId && sessions.has(sessionId)) {
    // Existing session — update activity timestamp
    const entry = sessions.get(sessionId)!;
    entry.lastActivity = Date.now();
    await entry.transport.handleRequest(req, res, req.body);
    return;
  }

  if (!sessionId && isInitializeRequest(req.body)) {
    // Reject if at session capacity
    if (sessions.size >= MAX_SESSIONS) {
      res.status(503).json({
        jsonrpc: "2.0",
        error: { code: -32000, message: "Server at capacity. Try again later." },
        id: null,
      });
      return;
    }

    // New session
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: () => randomUUID(),
      onsessioninitialized: (sid) => {
        sessions.set(sid, { transport, lastActivity: Date.now() });
      },
    });

    transport.onclose = () => {
      const sid = [...sessions.entries()].find(
        ([, e]) => e.transport === transport
      )?.[0];
      if (sid) sessions.delete(sid);
    };

    const server = createMcpServer();
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
    return;
  }

  res.status(400).json({
    jsonrpc: "2.0",
    error: { code: -32000, message: "Bad request: no valid session or initialize request" },
    id: null,
  });
});

// MCP endpoint - GET for SSE stream (server-initiated messages)
app.get("/mcp", rateLimit, async (req, res) => {
  const sessionId = req.headers["mcp-session-id"] as string;
  const entry = sessions.get(sessionId);
  if (!entry) {
    res.status(400).json({
      jsonrpc: "2.0",
      error: { code: -32000, message: "Invalid or missing session ID" },
      id: null,
    });
    return;
  }
  entry.lastActivity = Date.now();
  await entry.transport.handleRequest(req, res);
});

// MCP endpoint - DELETE for session cleanup
app.delete("/mcp", async (req, res) => {
  const sessionId = req.headers["mcp-session-id"] as string;
  cleanupSession(sessionId);
  res.status(200).end();
});

const port = Number(process.env.PORT) || 3000;
app.listen(port, () => {
  console.error(`AssemblyAI Docs MCP server running on port ${port}`);
  console.error(`MCP endpoint: http://localhost:${port}/mcp`);
});
