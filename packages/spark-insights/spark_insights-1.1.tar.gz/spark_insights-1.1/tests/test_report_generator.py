import unittest
from pyspark.sql import SparkSession
from spark_insights_project.spark_insights.report_generator import report_insights

class TestReportGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder \
            .appName("Spark Test") \
            .getOrCreate()

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_generate_spark_report_html(self):
        data = [("Alice", 1), ("Bob", 2), ("Alice", 1)]
        df = self.spark.createDataFrame(data, ["name", "value"])
        try:
            report_insights(df)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"generate_spark_report_html failed: {e}")

if __name__ == "__main__":
    unittest.main()
