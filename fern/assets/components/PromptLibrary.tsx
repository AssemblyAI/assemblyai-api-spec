"use client";
import * as React from "react";

// Supabase configuration
// The URL is public and safe to hardcode.
// All Edge Functions are deployed with --no-verify-jwt for public access.
// Security is handled server-side via validation and moderation queue.
const SUPABASE_URL = "https://iejauyqxykvyvztblitn.supabase.co";

// Edge Function URLs (all deployed with --no-verify-jwt)
const GET_PROMPTS_URL = `${SUPABASE_URL}/functions/v1/get-prompts`;
const SUBMIT_PROMPT_URL = `${SUPABASE_URL}/functions/v1/submit-prompt`;
const VOTE_PROMPT_URL = `${SUPABASE_URL}/functions/v1/vote-prompt`;

// Generate or retrieve a session ID for vote tracking
const getSessionId = (): string => {
  if (typeof window === 'undefined') return 'server';
  let sessionId = sessionStorage.getItem('prompt_library_session_id');
  if (!sessionId) {
    sessionId = `session_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
    sessionStorage.setItem('prompt_library_session_id', sessionId);
  }
  return sessionId;
};

// Simple profanity filter - basic list of words to block
const PROFANITY_LIST = [
  "fuck", "shit", "ass", "damn", "bitch", "bastard", "crap", "piss",
  "dick", "cock", "pussy", "cunt", "whore", "slut", "fag", "nigger",
  "retard", "idiot", "stupid", "dumb", "hate", "kill", "die"
];

const containsProfanity = (text: string): boolean => {
  const lowerText = text.toLowerCase();
  return PROFANITY_LIST.some(word => {
    const regex = new RegExp(`\\b${word}\\b`, 'i');
    return regex.test(lowerText);
  });
};

const isSpam = (text: string): boolean => {
  // Check for excessive repetition
  const words = text.toLowerCase().split(/\s+/);
  const uniqueWords = new Set(words);
  if (words.length > 5 && uniqueWords.size < words.length * 0.3) {
    return true;
  }
  // Check for too many URLs
  const urlCount = (text.match(/https?:\/\//g) || []).length;
  if (urlCount > 2) {
    return true;
  }
  return false;
};

interface Prompt {
  id: string;
  content: string;
  upvotes: number;
  downvotes: number;
  created_at: string;
}


export function PromptLibrary() {
  const [searchQuery, setSearchQuery] = React.useState("");
  const [prompts, setPrompts] = React.useState<Prompt[]>([]);
  const [filteredPrompts, setFilteredPrompts] = React.useState<Prompt[]>([]);
  const [topPrompts, setTopPrompts] = React.useState<Prompt[]>([]);
  const [newPrompt, setNewPrompt] = React.useState("");
  const [isSubmitting, setIsSubmitting] = React.useState(false);
  const [submitStatus, setSubmitStatus] = React.useState<{ type: 'success' | 'error' | null; message: string }>({ type: null, message: '' });
  const [votedPrompts, setVotedPrompts] = React.useState<Set<string>>(new Set());
  const [isLoading, setIsLoading] = React.useState(true);
  const [loadError, setLoadError] = React.useState<string | null>(null);

  // Fetch prompts from Edge Function on mount
  React.useEffect(() => {
    const fetchPrompts = async () => {
      try {
        setIsLoading(true);
        setLoadError(null);
        
        // Fetch approved prompts via Edge Function (no auth required)
        const response = await fetch(GET_PROMPTS_URL, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        if (!response.ok) {
          throw new Error(`Failed to fetch prompts: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.prompts && Array.isArray(result.prompts)) {
          setPrompts(result.prompts);
        } else {
          setPrompts([]);
        }
      } catch (error) {
        console.error('Failed to fetch prompts:', error);
        setLoadError('Unable to load prompts from the database.');
        setPrompts([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPrompts();
  }, []);

  // Initialize top prompts and filtered prompts (sorted by score, top 6)
  React.useEffect(() => {
    const sorted = [...prompts].sort((a, b) => (b.upvotes - b.downvotes) - (a.upvotes - a.downvotes));
    setTopPrompts(sorted.slice(0, 6));
    setFilteredPrompts(sorted);
  }, [prompts]);

  // Filter prompts based on search query
  React.useEffect(() => {
    if (!searchQuery.trim()) {
      const sorted = [...prompts].sort((a, b) => (b.upvotes - b.downvotes) - (a.upvotes - a.downvotes));
      setFilteredPrompts(sorted);
      return;
    }
    const query = searchQuery.toLowerCase();
    const filtered = prompts.filter(p => p.content.toLowerCase().includes(query));
    setFilteredPrompts(filtered.sort((a, b) => (b.upvotes - b.downvotes) - (a.upvotes - a.downvotes)));
  }, [searchQuery, prompts]);

  const handleVote = async (promptId: string, voteType: 'up' | 'down') => {
    if (votedPrompts.has(promptId)) {
      return; // Already voted on this prompt
    }

    // Optimistic update
    setPrompts(prev => prev.map(p => {
      if (p.id === promptId) {
        return {
          ...p,
          upvotes: voteType === 'up' ? p.upvotes + 1 : p.upvotes,
          downvotes: voteType === 'down' ? p.downvotes + 1 : p.downvotes
        };
      }
      return p;
    }));
    setVotedPrompts(prev => new Set([...prev, promptId]));

    // Send vote to Edge Function (no auth required - deployed with --no-verify-jwt)
    try {
      const response = await fetch(VOTE_PROMPT_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt_id: promptId,
          vote_type: voteType,
          session_id: getSessionId(),
        }),
      });

      if (!response.ok) {
        // Handle non-JSON responses
        const contentType = response.headers.get('content-type');
        let errorMsg = 'Vote failed';
        if (contentType && contentType.includes('application/json')) {
          const error = await response.json();
          errorMsg = error.error || errorMsg;
        } else {
          const text = await response.text();
          errorMsg = `Server error: ${response.status} - ${text || 'Unknown error'}`;
        }
        console.error('Vote failed:', errorMsg);
        // Revert optimistic update on failure
        setPrompts(prev => prev.map(p => {
          if (p.id === promptId) {
            return {
              ...p,
              upvotes: voteType === 'up' ? p.upvotes - 1 : p.upvotes,
              downvotes: voteType === 'down' ? p.downvotes - 1 : p.downvotes
            };
          }
          return p;
        }));
        setVotedPrompts(prev => {
          const newSet = new Set(prev);
          newSet.delete(promptId);
          return newSet;
        });
      }
    } catch (error) {
      console.error('Vote request failed:', error);
    }
  };

  const handleSubmit = async () => {
    if (!newPrompt.trim()) {
      setSubmitStatus({ type: 'error', message: 'Please enter a prompt before submitting.' });
      return;
    }

    if (newPrompt.length < 20) {
      setSubmitStatus({ type: 'error', message: 'Prompt must be at least 20 characters long.' });
      return;
    }

    if (newPrompt.length > 1000) {
      setSubmitStatus({ type: 'error', message: 'Prompt must be less than 1000 characters.' });
      return;
    }

    if (containsProfanity(newPrompt)) {
      setSubmitStatus({ type: 'error', message: 'Your prompt contains inappropriate language. Please revise and try again.' });
      return;
    }

    if (isSpam(newPrompt)) {
      setSubmitStatus({ type: 'error', message: 'Your prompt appears to be spam. Please submit a valid transcription prompt.' });
      return;
    }

    setIsSubmitting(true);
    setSubmitStatus({ type: null, message: '' });

    try {
      // Submit via Edge Function (no auth required - deployed with --no-verify-jwt)
      const response = await fetch(SUBMIT_PROMPT_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content: newPrompt }),
      });

      // Handle non-JSON responses (e.g., "Method not allowed")
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text();
        throw new Error(`Server error: ${response.status} - ${text || 'Unknown error'}`);
      }

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || 'Failed to submit prompt');
      }

      setSubmitStatus({ 
        type: 'success', 
        message: 'Thank you! Your prompt has been submitted for review. It will appear in the library once approved.' 
      });
      setNewPrompt("");
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to submit prompt. Please try again.';
      setSubmitStatus({ type: 'error', message: errorMessage });
    } finally {
      setIsSubmitting(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  // Styles matching PromptGenerator
  const containerStyle: React.CSSProperties = {
    border: "1px solid var(--grayscale-a4, #e5e7eb)",
    borderRadius: "8px",
    padding: "24px",
    backgroundColor: "var(--grayscale-2, #f9fafb)",
  };

  const labelStyle: React.CSSProperties = {
    display: "block",
    fontSize: "14px",
    fontWeight: 500,
    marginBottom: "8px",
    color: "var(--grayscale-12, #111827)",
  };

  const inputStyle: React.CSSProperties = {
    width: "100%",
    padding: "12px",
    border: "1px solid var(--grayscale-a4, #d1d5db)",
    borderRadius: "6px",
    fontSize: "14px",
    backgroundColor: "var(--grayscale-1, #ffffff)",
    color: "var(--grayscale-12, #111827)",
  };

  const textareaStyle: React.CSSProperties = {
    ...inputStyle,
    height: "120px",
    fontFamily: "monospace",
    resize: "vertical",
  };

  const cardStyle: React.CSSProperties = {
    border: "1px solid var(--grayscale-a4, #e5e7eb)",
    borderRadius: "8px",
    padding: "16px",
    backgroundColor: "var(--grayscale-1, #ffffff)",
    marginBottom: "12px",
  };

  const topCardStyle: React.CSSProperties = {
    ...cardStyle,
    flex: "1 1 calc(50% - 8px)",
    minWidth: "280px",
    maxWidth: "calc(50% - 8px)",
  };

  const buttonStyle: React.CSSProperties = {
    display: "inline-flex",
    alignItems: "center",
    gap: "6px",
    padding: "8px 16px",
    border: "none",
    borderRadius: "6px",
    fontSize: "14px",
    fontWeight: 500,
    cursor: "pointer",
    backgroundColor: "#3b82f6",
    color: "#ffffff",
  };

  const voteButtonStyle: React.CSSProperties = {
    display: "inline-flex",
    alignItems: "center",
    gap: "4px",
    padding: "6px 12px",
    border: "1px solid var(--grayscale-a4, #d1d5db)",
    borderRadius: "4px",
    fontSize: "13px",
    cursor: "pointer",
    backgroundColor: "transparent",
    color: "var(--grayscale-11, #6b7280)",
  };

  const disabledVoteButtonStyle: React.CSSProperties = {
    ...voteButtonStyle,
    cursor: "not-allowed",
    opacity: 0.6,
  };

  const promptTextStyle: React.CSSProperties = {
    fontFamily: "monospace",
    fontSize: "13px",
    whiteSpace: "pre-wrap",
    color: "var(--grayscale-12, #111827)",
    marginBottom: "12px",
    maxHeight: "150px",
    overflow: "auto",
  };

  const statusStyle = (type: 'success' | 'error'): React.CSSProperties => ({
    padding: "12px",
    borderRadius: "6px",
    fontSize: "14px",
    marginTop: "12px",
    backgroundColor: type === 'success' ? "#dcfce7" : "#fee2e2",
    color: type === 'success' ? "#166534" : "#991b1b",
    border: `1px solid ${type === 'success' ? "#86efac" : "#fecaca"}`,
  });

  const scoreStyle: React.CSSProperties = {
    fontSize: "12px",
    color: "var(--grayscale-11, #6b7280)",
    marginLeft: "8px",
  };

  const sectionTitleStyle: React.CSSProperties = {
    fontSize: "16px",
    fontWeight: 600,
    marginBottom: "16px",
    color: "var(--grayscale-12, #111827)",
  };

  const loadingStyle: React.CSSProperties = {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "40px",
    color: "var(--grayscale-11, #6b7280)",
    fontSize: "14px",
  };

  const errorBannerStyle: React.CSSProperties = {
    padding: "12px",
    borderRadius: "6px",
    fontSize: "14px",
    marginBottom: "16px",
    backgroundColor: "#fef3c7",
    color: "#92400e",
    border: "1px solid #fcd34d",
  };

  return (
    <div style={containerStyle}>
      <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
        {/* Loading State */}
        {isLoading && (
          <div style={loadingStyle}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ animation: "spin 1s linear infinite", marginRight: "8px" }}>
              <circle cx="12" cy="12" r="10" strokeDasharray="32" strokeDashoffset="12" />
            </svg>
            Loading prompts...
          </div>
        )}

        {/* Error Banner */}
        {loadError && !isLoading && (
          <div style={errorBannerStyle}>
            {loadError}
          </div>
        )}

        {/* Search Section */}
        <div>
          <label style={labelStyle}>Search prompts</label>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search for prompts by keyword (e.g., medical, verbatim, code-switching...)"
            style={inputStyle}
          />
        </div>

        {/* Top Prompts - Hidden when searching */}
        {!searchQuery && (
          <div>
            <div style={sectionTitleStyle}>Top prompts by community votes</div>
            {isLoading ? (
              <div style={{ color: "var(--grayscale-11, #6b7280)", fontSize: "14px" }}>Loading...</div>
            ) : topPrompts.length === 0 ? (
              <div style={{ color: "var(--grayscale-11, #6b7280)", fontSize: "14px" }}>No prompts available yet. Be the first to submit one!</div>
            ) : (
            <div style={{ display: "flex", gap: "16px", flexWrap: "wrap" }}>
              {topPrompts.map((prompt, index) => (
                <div key={prompt.id} style={topCardStyle}>
                  <div style={{ display: "flex", alignItems: "center", marginBottom: "8px" }}>
                    <span style={{ 
                      backgroundColor: index === 0 ? "#fbbf24" : index === 1 ? "#9ca3af" : "#cd7f32",
                      color: "#ffffff",
                      padding: "2px 8px",
                      borderRadius: "4px",
                      fontSize: "12px",
                      fontWeight: 600
                    }}>
                      #{index + 1}
                    </span>
                    <span style={scoreStyle}>
                      {prompt.upvotes - prompt.downvotes} points
                    </span>
                  </div>
                  <div style={promptTextStyle}>{prompt.content}</div>
                  <div style={{ display: "flex", gap: "8px", alignItems: "center", flexWrap: "wrap" }}>
                    <button
                      onClick={() => handleVote(prompt.id, 'up')}
                      disabled={votedPrompts.has(prompt.id)}
                      style={votedPrompts.has(prompt.id) ? disabledVoteButtonStyle : voteButtonStyle}
                      title={votedPrompts.has(prompt.id) ? "You've already voted" : "Upvote"}
                    >
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3" />
                      </svg>
                      {prompt.upvotes}
                    </button>
                    <button
                      onClick={() => handleVote(prompt.id, 'down')}
                      disabled={votedPrompts.has(prompt.id)}
                      style={votedPrompts.has(prompt.id) ? disabledVoteButtonStyle : voteButtonStyle}
                      title={votedPrompts.has(prompt.id) ? "You've already voted" : "Downvote"}
                    >
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17" />
                      </svg>
                      {prompt.downvotes}
                    </button>
                    <button
                      onClick={() => copyToClipboard(prompt.content)}
                      style={{ ...voteButtonStyle, marginLeft: "auto" }}
                      title="Copy prompt"
                    >
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
                      </svg>
                      Copy
                    </button>
                  </div>
                </div>
              ))}
            </div>
            )}
          </div>
        )}

        {/* Search Results / All Prompts */}
        {searchQuery && (
          <div>
            <div style={sectionTitleStyle}>
              {filteredPrompts.length} result{filteredPrompts.length !== 1 ? 's' : ''} for "{searchQuery}"
            </div>
            {filteredPrompts.length === 0 ? (
              <div style={{ color: "var(--grayscale-11, #6b7280)", fontSize: "14px" }}>
                No prompts found matching your search. Try different keywords or submit your own prompt below!
              </div>
            ) : (
              filteredPrompts.map(prompt => (
                <div key={prompt.id} style={cardStyle}>
                  <div style={promptTextStyle}>{prompt.content}</div>
                  <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                    <button
                      onClick={() => handleVote(prompt.id, 'up')}
                      disabled={votedPrompts.has(prompt.id)}
                      style={votedPrompts.has(prompt.id) ? disabledVoteButtonStyle : voteButtonStyle}
                    >
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3" />
                      </svg>
                      {prompt.upvotes}
                    </button>
                    <button
                      onClick={() => handleVote(prompt.id, 'down')}
                      disabled={votedPrompts.has(prompt.id)}
                      style={votedPrompts.has(prompt.id) ? disabledVoteButtonStyle : voteButtonStyle}
                    >
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17" />
                      </svg>
                      {prompt.downvotes}
                    </button>
                    <span style={scoreStyle}>{prompt.upvotes - prompt.downvotes} points</span>
                    <button
                      onClick={() => copyToClipboard(prompt.content)}
                      style={{ ...voteButtonStyle, marginLeft: "auto" }}
                    >
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
                      </svg>
                      Copy
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {/* Submit Section */}
        <div>
          <div style={sectionTitleStyle}>Submit your own prompt</div>
          <label style={labelStyle}>Your prompt</label>
          <textarea
            value={newPrompt}
            onChange={(e) => setNewPrompt(e.target.value)}
            placeholder="Share a prompt that works well for your use case. Include specific instructions, authoritative language, and examples. Your prompt will be reviewed before appearing in the library."
            style={textareaStyle}
          />
          <div style={{ fontSize: "12px", color: "var(--grayscale-11, #6b7280)", marginTop: "4px" }}>
            {newPrompt.length} / 1000 characters (minimum 20)
          </div>
          <button
            onClick={handleSubmit}
            disabled={isSubmitting}
            style={{
              ...buttonStyle,
              marginTop: "12px",
              opacity: isSubmitting ? 0.7 : 1,
              cursor: isSubmitting ? "not-allowed" : "pointer",
            }}
          >
            {isSubmitting ? (
              <>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ animation: "spin 1s linear infinite" }}>
                  <circle cx="12" cy="12" r="10" strokeDasharray="32" strokeDashoffset="12" />
                </svg>
                Submitting...
              </>
            ) : (
              <>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
                </svg>
                Submit your own prompt
              </>
            )}
          </button>
          {submitStatus.type && (
            <div style={statusStyle(submitStatus.type)}>
              {submitStatus.message}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
