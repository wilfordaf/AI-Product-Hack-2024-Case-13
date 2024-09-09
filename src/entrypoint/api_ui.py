import warnings

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from starlette.responses import RedirectResponse

from service.entities.api_models.input import (
    AddTagsUserRequestBody,
    AddUserRequestBody,
    GetRankingUserRequestBody,
)
from service.entities.api_models.output import (
    PingResponse,
    SuccessStatusResponse,
    UserRankingResponse,
)
from src.service.service_assembler import ServiceAssembler
from src.service.utils.logging import ConsoleLogger
from src.service.utils.monitoring import (
    api_version,
    cpu_utilization_percent,
    log_levels_distribution,
)

warnings.filterwarnings("ignore")

app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1})
instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/openapi.json", "/favicon.ico"],
    inprogress_name="in_progress",
    inprogress_labels=True,
)

TRACKED_METRICS = [
    metrics.requests(),
    metrics.latency(),
    cpu_utilization_percent(),
    log_levels_distribution(),
    api_version(),
]

for metric in TRACKED_METRICS:
    instrumentator.add(metric)

instrumentator.instrument(app, metric_namespace="bia_incident", metric_subsystem="bia_incident")
instrumentator.expose(app, include_in_schema=False, should_gzip=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = ConsoleLogger()
service = ServiceAssembler()


@app.exception_handler(Exception)
async def custom_exception_handler(_: Request, exception: Exception):
    logger.error(f"Error encountered while processing request: {str(exception)}")
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exception)})


@app.get("/", include_in_schema=False)
def docs():
    logger.info("Request /docs")
    return RedirectResponse(url="/docs")


@app.get(
    "/api/v1/ping",
    description="Check service status",
    response_description="API version and models info",
    response_model=PingResponse,
    tags=["DEV"],
    status_code=200,
)
async def ping() -> JSONResponse:
    logger.info("Request /ping")
    response = service.get_ping_response()
    header, body = response["header"], response["body"]
    return JSONResponse(content=body, headers=header)


@app.post(
    "/api/v1/user/add",
    description="Add new user to the system",
    response_description="Success status",
    response_model=SuccessStatusResponse,
    tags=["API"],
    status_code=200,
)
async def add_user(data: AddUserRequestBody) -> JSONResponse:
    logger.info("Request /user/add")
    response = service.get_add_user_response(data)
    header, body = response["header"], response["body"]
    return JSONResponse(content=body, headers=header)


@app.post(
    "/api/v1/user/add-tags",
    description="Add new tags to the user",
    response_description="Success status",
    response_model=SuccessStatusResponse,
    tags=["API"],
    status_code=200,
)
async def add_tags_user(data: AddTagsUserRequestBody) -> JSONResponse:
    logger.info("Request /user/add-tags")
    response = service.get_add_tags_to_user_response(data)
    header, body = response["header"], response["body"]
    return JSONResponse(content=body, headers=header)


@app.post(
    "/api/v1/user/get-ranking",
    description="Get ranking of users",
    response_description="Success status",
    response_model=UserRankingResponse,
    tags=["API"],
    status_code=200,
)
async def get_ranking_user(queue: str, data: GetRankingUserRequestBody) -> JSONResponse:
    logger.info(f"Пришёл запрос predict в очередь {queue}")
    response = service.get_predict_response(queue, f"{data.title} {data.text}", data.issue_key)
    header, body = response["header"], response["body"]
    return JSONResponse(content=body, headers=header)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9090)
