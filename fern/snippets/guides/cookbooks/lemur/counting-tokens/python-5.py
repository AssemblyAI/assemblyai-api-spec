# Estimate tokens (roughly 4 characters = 1 token)
estimated_tokens = total_chars / 4
tokens_in_millions = estimated_tokens / 1_000_000

print(f"Estimated input tokens: {estimated_tokens:,.0f}")
