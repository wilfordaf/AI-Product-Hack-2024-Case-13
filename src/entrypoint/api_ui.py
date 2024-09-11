import warnings

import uvicorn
from fastapi import FastAPI, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse

from src.service.entities.api_models.input import (
    AddTagsByCVUserRequestBody,
    AddTagsByDialogueUserRequestBody,
    AddTagsByLinkUserRequestBody,
    AddTagsByTextUserRequestBody,
    AddUserRequestBody,
    GetIsAdminRequestBody,
    GetRankingUserRequestBody,
    GetTagsByUserRequestBody,
)
from src.service.entities.api_models.input.get_users_by_event_request_body import (
    GetUsersByEventRequestBody,
)
from src.service.entities.api_models.output import (
    PingResponse,
    SuccessStatusResponse,
    TagTitlesResponse,
    UserRankingResponse,
)
from src.service.service_assembler import ServiceAssembler
from src.service.utils.logging import ConsoleLogger

warnings.filterwarnings("ignore")

app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1})

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


@app.get(
    "/api/v1/user/get-ranking",
    description="Get ranking of users",
    response_description="Ranking of users",
    response_model=UserRankingResponse,
    tags=["API"],
    status_code=200,
)
async def get_ranking_user(
    telegram_id: str = Query(..., description="User's Telegram ID"),
    event_title: str = Query(..., description="Title of the event"),
) -> JSONResponse:
    logger.info("Request /user/get-ranking")
    data = GetRankingUserRequestBody(telegram_id=telegram_id, event_title=event_title)
    response = service.get_user_ranking_response(data)
    header, body = response["header"], response["body"]
    return JSONResponse(content=body, headers=header)


@app.get(
    "/api/v1/user/is-admin",
    description="Check if the user is admin",
    response_description="Success status",
    response_model=SuccessStatusResponse,
    tags=["API"],
    status_code=200,
)
async def get_is_admin(
    telegram_id: str = Query(..., description="User's Telegram ID"),
    event_title: str = Query(..., description="Title of the event"),
) -> JSONResponse:
    logger.info("Request /user/is-admin")
    data = GetIsAdminRequestBody(telegram_id=telegram_id, event_title=event_title)
    response = service.get_is_admin_response(data)
    header, body = response["header"], response["body"]
    return JSONResponse(content=body, headers=header)


@app.get(
    "/api/v1/event/get-users",
    description="Get users by event title",
    response_description="Success status",
    response_model=UserRankingResponse,
    tags=["API"],
    status_code=200,
)
async def get_users_by_event(event_title: str = Query(..., description="Title of the event")) -> JSONResponse:
    logger.info("Request /event/get-users")
    data = GetUsersByEventRequestBody(event_title=event_title)
    response = service.get_users_by_event_response(data)
    header, body = response["header"], response["body"]
    return JSONResponse(content=body, headers=header)


@app.get(
    "/api/v1/user/get-tags",
    description="Get tags by user's Telegram ID",
    response_description="Success status",
    response_model=TagTitlesResponse,
    tags=["API"],
    status_code=200,
)
async def get_tags_by_user(telegram_id: str = Query(..., description="User's Telegram ID")) -> JSONResponse:
    logger.info("Request /event/get-users")
    data = GetTagsByUserRequestBody(telegram_id=telegram_id)
    response = service.get_tags_by_user_response(data)
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


@app.patch(
    "/api/v1/user/add-tags/text",
    description="Add new tags to the user from text input",
    response_description="Success status",
    response_model=SuccessStatusResponse,
    tags=["API"],
    status_code=200,
)
async def add_tags_by_text_user(data: AddTagsByTextUserRequestBody) -> JSONResponse:
    logger.info("Request /user/add-tags/text")
    response = service.get_add_tags_by_text_to_user_response(data)
    header, body = response["header"], response["body"]
    return JSONResponse(content=body, headers=header)


@app.patch(
    "/api/v1/user/add-tags/link",
    description="Add new tags to the user from link input",
    response_description="Success status",
    response_model=SuccessStatusResponse,
    tags=["API"],
    status_code=200,
)
async def add_tags_by_link_user(data: AddTagsByLinkUserRequestBody) -> JSONResponse:
    logger.info("Request /user/add-tags/link")
    response = service.get_add_tags_by_link_to_user_response(data)
    header, body = response["header"], response["body"]
    return JSONResponse(content=body, headers=header)


@app.patch(
    "/api/v1/user/add-tags/cv",
    description="Add new tags to the user from cv input",
    response_description="Success status",
    response_model=SuccessStatusResponse,
    tags=["API"],
    status_code=200,
)
async def add_tags_by_cv_user(data: AddTagsByCVUserRequestBody) -> JSONResponse:
    logger.info("Request /user/add-tags/cv")

    file_content = await data.file.read()
    file_content_str = file_content.decode("utf-8")
    input = AddTagsByTextUserRequestBody(telegram_id=data.telegram_id, text=file_content_str)

    response = service.get_add_tags_by_cv_to_user_response(input)
    header, body = response["header"], response["body"]
    return JSONResponse(content=body, headers=header)


@app.patch(
    "/api/v1/user/add-tags/dialogue",
    description="Add new tags to the user from dialogue input",
    response_description="Success status",
    response_model=SuccessStatusResponse,
    tags=["API"],
    status_code=200,
)
async def add_tags_by_dialogue_user(data: AddTagsByDialogueUserRequestBody) -> JSONResponse:
    logger.info("Request /user/add-tags/cv")

    file_content = await data.file.read()
    file_content_str = file_content.decode("utf-8")
    input = AddTagsByTextUserRequestBody(telegram_id=data.telegram_id, text=file_content_str)

    response = service.get_add_tags_by_dialogue_to_user_response(input)
    header, body = response["header"], response["body"]
    return JSONResponse(content=body, headers=header)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9090)
