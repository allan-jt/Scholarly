# Standard library imports
from contextlib import asynccontextmanager

# Third party imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import aioredis

# Local application imports
from routes import query

from services import get_spark_session, get_spark_context


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    app.state.redis_results = await aioredis.from_url("redis://database:6379/1")
    app.state.redis_other = await aioredis.from_url("redis://database:6379/2")
    yield
    # On shutdown
    await app.state.redis_results.close()
    await app.state.redis_other.close()


app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(query, prefix="/query")


@app.get("/")
def read_root():
    return "Hello, World!"


@app.get("/spark")
async def get_spark():
    sparkSession = get_spark_session()
    sparkSession.spa


@app.get("/hello1/{name}")
async def say_hello(name: str):
    cache = await app.state.redis_results.get(name)
    if cache:
        return f"{name} from Redis!"

    # key | value | expiration in seconds
    await app.state.redis_results.set(name, "Hello World!", ex=30)
    return f"Hello {name}!"


@app.get("/hello2/{name}")
async def say_hello(name: str):
    cache = await app.state.redis_other.get(name)
    if cache:
        return f"{name} from Redis!"

    # key | value | expiration in seconds
    await app.state.redis_other.set(name, "Hello World!", ex=30)
    return f"Hello {name}!"
