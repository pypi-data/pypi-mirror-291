from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql.functions import count, when, isnull
import pandas as pd
from jinja2 import Template
import webbrowser
import os
def report_insights(df: SparkDataFrame):
    if not isinstance(df, SparkDataFrame):
        raise TypeError("Input must be a Spark DataFrame.")

    # Overview
    num_rows = df.count()
    num_cols = len(df.columns)
    data_types = dict(df.dtypes)

    # Descriptive Statistics
    pandas_df = df.toPandas()
    descriptive_stats = pandas_df.describe(include='all').transpose().to_html(classes='table table-striped table-hover')

    # Missing Values
    missing_values = df.select([count(when(isnull(c), c)).alias(c) for c in df.columns]).collect()[0].asDict()
    missing_values_df = pd.DataFrame(list(missing_values.items()), columns=['Column', 'Missing Values'])
    missing_values_html = missing_values_df.to_html(classes='table table-striped table-hover', index=False)

    # Duplicates
    num_duplicates = df.count() - df.dropDuplicates().count()

    # Unique Values
    unique_values = {col: df.select(col).distinct().count() for col in df.columns}
    unique_values_df = pd.DataFrame(list(unique_values.items()), columns=['Column', 'Unique Values'])
    unique_values_html = unique_values_df.to_html(classes='table table-striped table-hover', index=False)

    # Generate HTML Report
    report_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Data Health Report</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Roboto', sans-serif;
                background-color: #f0f4f8;
                color: #333;
                margin: 0;
                padding: 0;
            }
            h1 {
                color: #ffffff;
                background-color: #007bff;
                padding: 20px;
                border-radius: 5px 5px 0 0;
                font-size: 2.5rem;
                text-align: center;
            }
            h2 {
                color: #007bff;
                margin-top: 20px;
                font-size: 1.75rem;
            }
            .summary {
                margin: 20px;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                padding: 20px;
            }
            p {
                font-size: 1.125rem;
                color: #555;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                font-size: 1.125rem;
                color: #333;
            }
            .table {
                margin-top: 20px;
                border-radius: 8px;
                overflow: hidden;
            }
            .table thead {
                background-color: #007bff;
                color: #ffffff;
            }
            .table th, .table td {
                padding: 12px;
                text-align: left;
            }
            .table-striped tbody tr:nth-of-type(odd) {
                background-color: #f9f9f9;
            }
            .table-hover tbody tr:hover {
                background-color: #f1f1f1;
            }
            .container {
                max-width: 1200px;
                margin: auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Data Health Report</h1>
            <div class="summary">
                <h2>Overview</h2>
                <p><strong>Number of Rows:</strong> {{ num_rows }}</p>
                <p><strong>Number of Columns:</strong> {{ num_cols }}</p>
                <p><strong>Data Types:</strong></p>
                <ul>
                {% for key, value in data_types.items() %}
                    <li>{{ key }}: {{ value }}</li>
                {% endfor %}
                </ul>
            </div>
            <div class="summary">
                <h2>Descriptive Statistics</h2>
                {{ descriptive_stats|safe }}
            </div>
            <div class="summary">
                <h2>Missing Values</h2>
                {{ missing_values_html|safe }}
            </div>
            <div class="summary">
                <h2>Duplicates</h2>
                <p><strong>Number of Duplicate Rows:</strong> {{ num_duplicates }}</p>
            </div>
            <div class="summary">
                <h2>Unique Values</h2>
                {{ unique_values_html|safe }}
            </div>
        </div>
    </body>
    </html>
    """

    template = Template(report_template)
    html_report = template.render(
        num_rows=num_rows,
        num_cols=num_cols,
        data_types=data_types,
        descriptive_stats=descriptive_stats,
        missing_values_html=missing_values_html,
        num_duplicates=num_duplicates,
        unique_values_html=unique_values_html
    )

    # Display the HTML report directly in Databricks
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import lit

    # If you are running this code in Databricks, you can use displayHTML
    try:
        displayHTML(html_report)
    except NameError:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
            temp_file.write(html_report.encode('utf-8'))
            temp_file_path = temp_file.name

        # Open the temporary file in the default web browser
        webbrowser.open_new_tab(f"file://{os.path.abspath(temp_file_path)}")