"""Controlling multiple nvim instances."""

from pydantic import BaseModel
import fastapi
from contextlib import asynccontextmanager
from rich import print
import typer

from dataclasses import dataclass

from starlette.requests import Request
from fastapi import Depends
import uvicorn


@dataclass
class AppState:
    active_servers: set[str]
    server_buffers: dict[int, set[int]]


async def get_app_state(request: Request) -> AppState:
    """Retrieve the app state from a starlette request."""
    yield request.app.state.app_state


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    """Handle startup and shutdown logic."""
    app.state.app_state = AppState(set(), {})
    yield
    pass


app = fastapi.FastAPI(lifespan=lifespan)


@app.get("/")
def health_check():
    return dict(detail="Alive")


class Input(BaseModel):
    message: str
    loaded_files: list[str]
    server: str


class Identity(BaseModel):
    server: str


SUCCESS_RESPONSE = dict(detail="success")


@app.post("/register")
def register(
    identity: Identity,
    app_state: AppState = Depends(get_app_state),
) -> dict:
    """Register that a new vim server is live."""
    print("Registering server: {}".format(identity.server))
    app_state.active_servers.add(identity.server)
    return SUCCESS_RESPONSE


@app.post("/disconnect")
def disconnect(
    identity: Identity,
    app_state: AppState = Depends(get_app_state),
) -> dict:
    """Remove an nvim instance from a list of active servers."""
    print("Removing server: {}".format(identity.server))
    try:
        app_state.active_servers.remove(identity.server)
    except KeyError:
        print("Key error exception?")
    return SUCCESS_RESPONSE


@app.post("/")
def hello_post(input: Input) -> dict:
    print("Received info from server running on: {}".format(input.server))
    return input.model_dump()


@app.get("/buffer/{bufnr}")
async def get_buffer_name(
    bufnr: int,
    app_state: AppState = Depends(get_app_state),
) -> dict:
    print("Bufnr: {}".format(bufnr))
    registered_buffers = app_state.server_buffers.get(0, set())
    registered_buffers.add(bufnr)
    app_state.server_buffers[0] = registered_buffers
    print(app_state)
    return SUCCESS_RESPONSE


cli = typer.Typer()


@cli.command()
def main(host: str = "localhost", port: int = 8881):
    uvicorn.run(
        "nvim_mgr:app",
        host=host,
        port=port,
        reload=True,
    )
