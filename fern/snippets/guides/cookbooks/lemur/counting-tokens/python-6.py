# Calculate input costs for different models (rates per 1M tokens)
gpt5_cost = 1.25 * tokens_in_millions
claude_sonnet_cost = 3.00 * tokens_in_millions
gemini_pro_cost = 1.25 * tokens_in_millions

print(f"\nEstimated input costs:")
print(f"GPT-5: ${gpt5_cost:.4f}")
print(f"Claude 4.5 Sonnet: ${claude_sonnet_cost:.4f}")
print(f"Gemini 2.5 Pro: ${gemini_pro_cost:.4f}")
