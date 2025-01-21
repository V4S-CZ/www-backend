"""Main module of v4s websites backend"""
from datetime import datetime
import os
import json
import sys
from app.features.git import Git
from app.routers import forms
from app.schemas.root import RootResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    swagger_ui_parameters={
        "syntaxHighlight.theme": "monokai",
        "persistAuthorization": True,
        "tryItOutEnabled": True,
    },
    title="v4s websites backend",
    # description="REST API",
    root_path=os.getenv("PATH_PREFIX", "/"),
)

try:
    origins = json.loads(os.getenv("CORS_ORIGINS"))
except:  # noqa: E722
    print(
        'Missing defined ENV variable CORS_ORIGINS, using default value ["*"].',
        file=sys.stderr,
    )
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=RootResponse)
@app.head("/", response_model=RootResponse)
async def root():
    """Root path method"""
    git = Git()
    return {
        "git": git.short_hash(),
        "message": "Hello World",
        "time": datetime.now(),
    }


@app.get("/health-check", response_model=str)
def health_check():
    """Method for docker container health check"""
    return "success"


app.include_router(forms.router)
