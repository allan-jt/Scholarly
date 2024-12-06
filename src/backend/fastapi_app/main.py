# Standard library imports
from contextlib import asynccontextmanager

# Third party imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pyspark.sql.types import IntegerType

# Local application imports
from routes import query
from services import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    await initialize_redis()
    SparkSessionSingleton()
    yield
    # On shutdown
    await close_redis()
    stop_spark_session()


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
    sparkContext = get_spark_context()
    numbers = [1, 200, 3, 4, 5]

    rdd = sparkContext.parallelize(numbers)
    df = sparkSession.createDataFrame(rdd, IntegerType())
    return df.sort("value").collect()


@app.get("/hello1/{name}")
async def say_hello(name: str):
    redis_db = get_redis_results()
    cache = await redis_db.get(name)
    if cache:
        return f"{name} from Redis!"

    # key | value | expiration in seconds
    await redis_db.set(name, "Hello World!", ex=30)
    return f"Hello {name}!"


@app.get("/hello2/{name}")
async def say_hello(name: str):
    redis_db = get_redis_chunks()
    cache = await redis_db.get(name)
    if cache:
        return f"{name} from Redis!"

    # key | value | expiration in seconds
    await redis_db.set(name, "Hello World!", ex=30)
    return f"Hello {name}!"
