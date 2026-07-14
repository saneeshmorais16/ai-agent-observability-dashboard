from app.config import DEFAULT_COST_PER_1K_INPUT_TOKENS, DEFAULT_COST_PER_1K_OUTPUT_TOKENS


def estimate_cost(
    prompt_tokens: int,
    completion_tokens: int,
    input_rate: float = DEFAULT_COST_PER_1K_INPUT_TOKENS,
    output_rate: float = DEFAULT_COST_PER_1K_OUTPUT_TOKENS,
) -> dict[str, float | int]:
    prompt_tokens = max(0, int(prompt_tokens))
    completion_tokens = max(0, int(completion_tokens))
    total_tokens = prompt_tokens + completion_tokens
    estimated_cost = (prompt_tokens / 1000 * input_rate) + (completion_tokens / 1000 * output_rate)
    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "estimated_cost": round(estimated_cost, 6),
    }
