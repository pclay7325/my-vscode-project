import matplotlib.pyplot as plt
import os
import logging

def generate_bar_chart(filename, summary, output_dir):
    """Generate and save a bar chart based on the KPI summary."""
    chart_path = os.path.join(output_dir, f"{filename}_chart.png")
    logging.info(f"Generating bar chart at: {chart_path}")

    try:
        # Data for the bar chart
        metrics = ["Average OEE", "Average Downtime (%)", "Average Utilization (%)", "Average Yield (%)", "Average Throughput"]
        values = [
            summary["average_oee"],
            summary["average_downtime_percentage"],
            summary["average_utilization_percentage"],
            summary["average_yield_percentage"],
            summary["average_throughput"],
        ]

        # Generate the bar chart
        plt.figure(figsize=(8, 5))
        plt.bar(metrics, values, color=["blue", "orange", "green", "purple", "red"])
        plt.title("KPI Summary")
        plt.ylabel("Value")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        # Save the chart
        plt.savefig(chart_path)
        plt.close()
        logging.info(f"Bar chart saved successfully at: {chart_path}")
    except Exception as e:
        logging.error(f"Error generating bar chart: {e}")
        raise

    return chart_path
