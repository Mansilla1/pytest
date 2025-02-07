from fastapi import APIRouter, status, FastAPI


router = APIRouter()


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
)
async def heath_check():
    return {"status": "ok"}


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
