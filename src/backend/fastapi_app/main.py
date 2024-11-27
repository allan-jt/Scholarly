from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import aioredis


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    app.state.redis = await aioredis.from_url("redis://database:6379")
    yield
    # On shutdown
    await app.state.redis.close()


app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
def read_root():
    return "Hello, World!"


@app.get("/hello/{name}")
async def say_hello(name: str):
    cache = await app.state.redis.get(name)
    if cache:
        return f"{name} from Redis!"

    # key | value | expiration in seconds
    await app.state.redis.set(name, "Hello World!", ex=30)
    return f"Hello {name}!"
