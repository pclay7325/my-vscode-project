import os

def generate_html(filename, summary, bar_chart_path, trend_chart_path=None):
    """Generate HTML for the PDF report."""
    return f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; }}
                h1 {{ color: #1e3a8a; text-align: center; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
                th {{ background-color: #f4f4f4; }}
                img {{ display: block; margin: 20px auto; max-width: 100%; }}
            </style>
        </head>
        <body>
            <h1>Manufacturing KPI Report</h1>
            <p>File Name: {filename}</p>
            <h2>KPI Summary</h2>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Average OEE</td><td>{summary['average_oee']}</td></tr>
                <tr><td>Average Downtime (%)</td><td>{summary['average_downtime_percentage']}</td></tr>
                <tr><td>Average Utilization (%)</td><td>{summary['average_utilization_percentage']}</td></tr>
                <tr><td>Average Yield (%)</td><td>{summary['average_yield_percentage']}</td></tr>
                <tr><td>Average Throughput (units/hour)</td><td>{summary['average_throughput']}</td></tr>
            </table>
            <img src="file:///{os.path.abspath(bar_chart_path)}" alt="Bar Chart">
        </body>
    </html>
    """
