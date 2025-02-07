import tomllib

from fastapi import APIRouter, status, FastAPI


router = APIRouter()


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
)
async def heath_check():
    return {"status": "ok"}


@router.get(
    "/version",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Successful version check",
            "content": {
                "application/json": {
                    "example": {"version": "0.1.0"},
                },
            },
        },
    },
    summary="Retrieve application version",
    description="Fetches the application version from the `pyproject.toml` file.",
)
async def version_check():
    """
    Retrieve the application version.

    Reads the `pyproject.toml` file to fetch the version specified under the `[tool.poetry]` section.
    """
    with open("pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)
    return {"version": pyproject["tool"]["poetry"]["version"]}


def create_app() -> FastAPI:
    root_app = FastAPI(
        title="TestAPI",
        description="TestAPI",
        version="0.1.0",
        separate_input_output_schemas=False,
        docs_url="/dev_docs",
        redoc_url="/docs",
    )
    root_app.include_router(router)
    return root_app
