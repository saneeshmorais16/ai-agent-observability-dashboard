from app.metrics import calculate_dashboard_metrics
from app.synthetic_data import generate_synthetic_data


def main() -> None:
    result = generate_synthetic_data(reset=True)
    metrics = calculate_dashboard_metrics()
    print(f"Generated {result['runs_created']} synthetic agent runs.")
    print(f"Total runs: {metrics['total_agent_runs']}")
    print(f"High-risk prompts: {metrics['high_risk_prompts']}")
    print(f"Estimated total cost: {metrics['estimated_total_cost']}")
    print("Run the API with: uvicorn app.main:app --reload")


if __name__ == "__main__":
    main()
