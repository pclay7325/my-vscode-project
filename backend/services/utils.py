import pandas as pd
import logging
from kpi_calculations import (
    calculate_availability,
    calculate_performance,
    calculate_quality,
    calculate_oee,
    calculate_downtime_percentage,
    calculate_utilization,
)

def process_csv(file_path: str):
    """
    Process the uploaded CSV file to calculate KPIs for each row and generate a summary.
    """
    logging.info(f"Processing CSV file: {file_path}")
    try:
        # Load CSV
        df = pd.read_csv(file_path)
        logging.info(f"Loaded DataFrame with {len(df)} rows.")
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        raise ValueError(f"Error reading CSV file: {str(e)}")

    if df.empty:
        logging.warning("The uploaded CSV file is empty.")
        raise ValueError("The uploaded CSV file is empty.")

    # Check required columns
    required_columns = ["timestamp", "runtime", "planned_time", "good_units", "total_units", "available_time"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        logging.error(f"Missing columns in CSV: {missing_columns}")
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    # Process timestamps if available
    try:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.sort_values("timestamp", inplace=True)
        logging.info("Timestamps processed and DataFrame sorted.")
    except Exception as e:
        logging.error(f"Error processing timestamps: {e}")
        raise ValueError("Error processing timestamps in the CSV file.")

    # Calculate KPIs
    try:
        df["availability"] = df.apply(lambda row: calculate_availability(row["runtime"], row["planned_time"]), axis=1)
        df["performance"] = df.apply(lambda row: calculate_performance(row["total_units"], 0.5, row["runtime"]), axis=1)
        df["quality"] = df.apply(lambda row: calculate_quality(row["good_units"], row["total_units"]), axis=1)
        df["oee"] = df.apply(lambda row: calculate_oee(row["availability"], row["performance"], row["quality"]), axis=1)
        df["downtime_percentage"] = df.apply(
            lambda row: calculate_downtime_percentage(row["runtime"], row["planned_time"]), axis=1
        )
        df["utilization_percentage"] = df.apply(
            lambda row: calculate_utilization(row["runtime"], row["available_time"]), axis=1
        )
        df["yield_percentage"] = df.apply(
            lambda row: (row["good_units"] / row["total_units"] * 100) if row["total_units"] > 0 else 0, axis=1
        )
        df["throughput"] = df.apply(
            lambda row: (row["total_units"] / row["runtime"]) if row["runtime"] > 0 else 0, axis=1
        )
        logging.info("KPIs calculated successfully.")
    except Exception as e:
        logging.error(f"Error calculating KPIs: {e}")
        raise ValueError("Error calculating KPIs from the CSV data.")

    # Summary statistics
    try:
        summary = {
            "average_oee": round(df["oee"].mean(), 2),
            "average_downtime_percentage": round(df["downtime_percentage"].mean(), 2),
            "average_utilization_percentage": round(df["utilization_percentage"].mean(), 2),
            "average_yield_percentage": round(df["yield_percentage"].mean(), 2),
            "average_throughput": round(df["throughput"].mean(), 2),
        }
        logging.info(f"Summary calculated: {summary}")
    except Exception as e:
        logging.error(f"Error calculating summary statistics: {e}")
        raise ValueError("Error calculating summary statistics.")

    return df, summary
