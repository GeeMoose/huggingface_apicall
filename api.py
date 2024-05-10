from tryon import router as api_router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI(
        title="tryon——put on your clothes",
        description='''The app is called "virtual tryon" and it is a new way to put on your cloth in new day. 
        ''',
        version="0.0.1",
    )
    # CORS domain
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router)
    return app


app = create_app()