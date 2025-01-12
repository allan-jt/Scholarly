# Standard library imports
from contextlib import asynccontextmanager
import os

# Third party imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from fastapi.responses import StreamingResponse

# Local application imports
from routes import query
from services import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    await RedisSingleton().initialize()
    SparkSessionSingleton()
    SummarizerSingleton()
    yield
    # On shutdown
    await RedisSingleton().close()
    SparkSessionSingleton().close()


app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FE_API_URL")],  # React's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(query, prefix="/query")


@app.get("/")
def read_root():
    return "Hello, World!"


# Since these requests doesn't come with any anything
# we use experimental pdf links below
# pdf_links = [
#     "http://arxiv.org/pdf/2411.02973.pdf",
#     # "http://arxiv.org/pdf/FAKE_URL",  # should raise exception
#     "https://arxiv.org/pdf/2412.06593",
# ]


@app.get("/test_chunk")
async def test_chunk():
    param = {"pdf_link": "http://arxiv.org/pdf/2411.02973.pdf"}
    pdf_bytes = await fetch_single_pdf(param["pdf_link"])
    return ChunkerSingleton().chunk_pdf(pdf_bytes)


@app.get("/test_summary")
async def test_summary():
    param = {"pdf_link": "http://arxiv.org/pdf/2411.02973.pdf"}
    pdf_bytes = await fetch_single_pdf(param["pdf_link"])
    chunked_pdf = ChunkerSingleton().chunk_pdf(pdf_bytes)

    chunked_pdf_rdd = (
        SparkSessionSingleton().get_spark_context().parallelize(chunked_pdf)
    )
    summary = SummarizerSingleton().summarize_chunked_sections(chunked_pdf_rdd)
    return summary.collect()
