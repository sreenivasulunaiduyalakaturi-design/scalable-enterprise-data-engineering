import pytest
from pyspark.sql import SparkSession
from src.etl.transform import clean
from src.etl.quality import check_bad_row_ratio, DataQualityError


@pytest.fixture(scope="module")
def spark():
    s = SparkSession.builder.master("local[1]").appName("test").getOrCreate()
    yield s
    s.stop()


def test_clean_removes_bad_rows_and_dupes(spark):
    rows = [(1, "C1", "home", 2, 10.0, "2024-01-01"),
            (1, "C1", "home", 2, 10.0, "2024-01-01"),   # duplicate
            (2, "",   "home", 1, 5.0,  "2024-01-01"),   # missing customer
            (3, "C3", "home", -1, 5.0, "2024-01-01")]   # bad quantity
    df = spark.createDataFrame(rows, "order_id long, customer_id string, category string, "
                                     "quantity int, unit_price double, order_date string")
    out = clean(df).collect()
    assert len(out) == 1 and out[0]["revenue"] == 20.0


def test_quality_gate():
    assert check_bad_row_ratio(100, 95, 0.1) == pytest.approx(0.05)
    with pytest.raises(DataQualityError):
        check_bad_row_ratio(100, 50, 0.1)
