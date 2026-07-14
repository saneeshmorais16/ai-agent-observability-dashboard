import re

RISK_RULES = [
    ("prompt_injection", "high", r"ignore (all )?(previous|system) instructions|developer message|system prompt"),
    ("jailbreak_attempt", "high", r"jailbreak|do anything now|dan mode|bypass safety"),
    ("credential_seeking", "critical", r"password|api key|secret key|token|credential"),
    ("data_exfiltration", "critical", r"exfiltrate|steal|dump database|private data|customer data"),
    ("unsafe_instruction_override", "high", r"override policy|disable guardrails|skip approval"),
    ("sensitive_data_warning", "medium", r"personal data|private prompt|private conversation|email inbox"),
]


def detect_prompt_risks(text: str) -> list[dict]:
    risks = []
    haystack = text.lower()
    for risk_type, level, pattern in RISK_RULES:
        if re.search(pattern, haystack):
            risks.append(
                {
                    "risk_type": risk_type,
                    "risk_level": level,
                    "explanation": f"Matched rule for {risk_type.replace('_', ' ')}.",
                }
            )
    return risks


def highest_risk_level(flags: list[dict]) -> str:
    order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
    if not flags:
        return "low"
    return max((flag["risk_level"] for flag in flags), key=lambda level: order[level])
