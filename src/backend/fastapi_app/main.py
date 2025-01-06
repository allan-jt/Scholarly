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


# @app.get("/test_chunk")
# async def test_chunk():
#     # Assign a unique ID to the request
#     request_id = str(uuid.uuid4())

#     # Since this request doesn't come with any anything
#     # we use experimental pdf links below
#     pdf_links = [
#         "http://arxiv.org/pdf/2411.02973.pdf",
#         # "http://arxiv.org/pdf/FAKE_URL",  # should raise exception
#         "https://arxiv.org/pdf/2412.06593",
#     ]

#     # We extract the PDFs and store them in Redis
#     await store_in_redis(request_id, pdf_links)

#     # We use chunker to chunk the individual PDFs
#     chunked_pdfs = await ChunkerSingleton().chunker(request_id)
#     return chunked_pdfs.collect()
