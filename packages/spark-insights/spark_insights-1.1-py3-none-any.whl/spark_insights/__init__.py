from .report_generator import report_insights as _report_insights
from pyspark.sql import DataFrame as SparkDataFrame

def report_insights(df):
    if not isinstance(df, SparkDataFrame):
        raise TypeError("Input must be a Spark DataFrame.")
    return _report_insights(df)