def calculate_availability(runtime: float, planned_time: float) -> float:
    if planned_time <= 0:
        raise ValueError("Planned time must be greater than zero.")
    return runtime / planned_time

def calculate_performance(total_units: int, ideal_cycle_time: float, runtime: float) -> float:
    if runtime <= 0 or ideal_cycle_time <= 0:
        raise ValueError("Runtime and ideal cycle time must be greater than zero.")
    return (total_units * ideal_cycle_time) / runtime

def calculate_quality(good_units: int, total_units: int) -> float:
    if total_units <= 0:
        raise ValueError("Total units must be greater than zero.")
    return good_units / total_units

def calculate_oee(availability: float, performance: float, quality: float) -> float:
    return availability * performance * quality

def calculate_downtime_percentage(runtime: float, planned_time: float) -> float:
    if planned_time <= 0:
        raise ValueError("Planned time must be greater than zero.")
    return ((planned_time - runtime) / planned_time) * 100

def calculate_utilization(runtime: float, available_time: float) -> float:
    if available_time <= 0:
        raise ValueError("Available time must be greater than zero.")
    return (runtime / available_time) * 100
