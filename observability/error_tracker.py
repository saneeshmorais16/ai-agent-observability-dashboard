from app.metrics import error_summary


def get_error_summary() -> dict:
    return error_summary()
