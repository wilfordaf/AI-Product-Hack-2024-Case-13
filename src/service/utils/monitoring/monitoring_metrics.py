from typing import Callable

from prometheus_client import Counter, Histogram
from prometheus_client import Info as ClientInfo
from prometheus_fastapi_instrumentator.metrics import Info

from service import version
from src.service.utils.monitoring.monitoring_methods import (
    get_cpu_utilization,
    get_log_levels_distribution,
)


def cpu_utilization_percent() -> Callable[[Info], None]:
    histogram = Histogram("cpu_utilization_percent", "CPU load %")

    def instrumentation(_: Info) -> None:
        histogram.observe(get_cpu_utilization())

    return instrumentation


def log_levels_distribution() -> Callable[[Info], None]:
    counter = Counter(
        "log_levels_distribution",
        "Count of log of each level above ConsoleLogger.getEffectiveLevel() included",
        labelnames=("level",),
    )

    def instrumentation(_: Info) -> None:
        for level, count in get_log_levels_distribution().items():
            counter.labels(level).inc(count)

    return instrumentation


def api_version() -> Callable[[Info], None]:
    i = ClientInfo("api_version", "test")

    def instrumentation(_: Info) -> None:
        i.info({"version": version})

    return instrumentation
