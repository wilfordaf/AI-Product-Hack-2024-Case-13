from typing import Dict

import psutil

from src.service.utils.logging import ConsoleLogger


def get_cpu_utilization() -> float:
    current_cpu_utilization_percent: float = psutil.cpu_percent(interval=0.01)
    return current_cpu_utilization_percent


def get_log_levels_distribution() -> Dict[str, int]:
    distribution_dict, logs_record = {}, []
    if (in_memory_handler := ConsoleLogger.get_in_memory_handler()) is not None:
        logs_record = in_memory_handler.get_saved_log_records()

    for log in logs_record:
        level_name = log.levelname
        if level_name not in distribution_dict:
            distribution_dict[level_name] = 0

        distribution_dict[level_name] += 1

    return distribution_dict
