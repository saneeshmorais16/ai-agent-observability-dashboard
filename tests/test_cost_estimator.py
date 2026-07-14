from app.cost_estimator import estimate_cost


def test_cost_estimation():
    cost = estimate_cost(1000, 500, input_rate=0.001, output_rate=0.002)
    assert cost["total_tokens"] == 1500
    assert cost["estimated_cost"] == 0.002
