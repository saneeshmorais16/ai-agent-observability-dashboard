from app.metrics import calculate_dashboard_metrics


def get_dashboard_metrics() -> dict:
    return calculate_dashboard_metrics()
