from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router
from settings import settings

app = FastAPI()

origins = [
    f"http://{settings.host_frontend}:{settings.port_frontend}"
]


app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(router)


