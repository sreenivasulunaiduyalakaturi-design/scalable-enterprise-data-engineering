"""Data-quality gate between bronze and silver."""
class DataQualityError(Exception):
    pass


def check_bad_row_ratio(bronze_count: int, silver_count: int, max_ratio: float):
    if bronze_count == 0:
        raise DataQualityError("Bronze layer is empty")
    ratio = (bronze_count - silver_count) / bronze_count
    if ratio > max_ratio:
        raise DataQualityError(f"Rejected {ratio:.1%} of rows (limit {max_ratio:.0%})")
    return ratio
