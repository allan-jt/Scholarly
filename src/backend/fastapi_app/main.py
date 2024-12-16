# Standard library imports
from contextlib import asynccontextmanager
import os

# Third party imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from fastapi.responses import StreamingResponse
import uuid

# Local application imports
from routes import query
from services import *
from services.pdf import store_in_redis
import json


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    await initialize_redis()
    SparkSessionSingleton()
    SummarizerSingleton()
    yield
    # On shutdown
    await close_redis()
    stop_spark_session()


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


# @app.get("/spark")
# async def get_spark():
#     sparkSession = get_spark_session()
#     sparkContext = get_spark_context()
#     with open("./services/summarizer/chunk.json") as f:
#         temp = json.load(f)
#     chunks = []
#     for i in temp:
#         chunks.append(i["text"])
#     # chunks = [
#     #     "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet nulla auctor, vestibulum magna sed, convallis ex. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.",
#     #     "Integer posuere erat a ante venenatis dapibus posuere velit aliquet. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Maecenas faucibus mollis interdum.",
#     #     "Aenean lacinia bibendum nulla sed consectetur. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec id elit non mi porta gravida at eget metus.",
#     #     "Vestibulum id ligula porta felis euismod semper. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec ullamcorper nulla non metus auctor fringilla.",
#     #     "Cras justo odio, dapibus ac facilisis in, egestas eget quam. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec id elit non mi porta gravida at eget metus.",
#     #     """Predicting temporal progress from visual trajectories is an important task for embodied agents that interact with the physical world. A robot capable of generalizable progress estimation can in principle discern desirable and undesirable behaviors to learn visuomotor skills in new environments. This is most often studied in reinforcement learning literature [51], where progress estimation is equivalent to universal value learning under specific choices of reward function. However, universal value estimation comes with a number of key challenges: (1) broad generalization to new tasks and scenes, (2) the ability to accurately estimate state in partially observed environments, and (3) temporal consistency (i.e. satisfying the Bellman equation) over long horizons. Most existing methods trained on relatively small amounts of vision-only data [8, 40, 1] lack the semantic, spatial, and temporal understanding needed to ground task progress in the space-time manifold of video, preventing generalization. Moreover, they often reason over single frames, inducing a high-degree of uncertainty in partially observed environments which in turn can effect the consistency of predictions for poorly estimated states. However, these challenges are not insurmountable: modern vision language models (VLMs) exhibit marked generalization and reasoning capabilities, potentially making them useful for value estimation. Though not often considered as candidates for value estimation, VLMs excel at its aforementioned core challenges. First, state-of-the-art VLMs have exhibited strong spatial reasoning and temporal understanding capabilities across various vision tasks [44, 9, 25, 21], allowing them to generalize to novel scenarios. Second, large transformer-based VLMs have the requisite context window [22] to reason over large amounts of historical information to accurately estimate state from observation sequences when predicting task progress. Finally, VLMs make predictions auto-regressively, meaning they commit to their own outputs as inputs for subsequent predictions, imposing consistency constraints on long generations. For example, a VLM is unlikely to estimate that a task is 50% completed if it already has a 50% completion prediction in context. However, how exactly a VLM should be used to predict values is unclear. Empirically, we find that simply placing a video in-context and prompting the model to return progress predictions for each frame fails – our analysis suggests strong temporal correlations between successive frames often cause VLMs to produce uninformative monotonic values that disregard the actual quality of the trajectory and differences between frames (Section 4) – and a different approach is needed. To effectively leverage the broad knowledge of VLMs, we introduce Generative Value Learning (GVL), a universal value estimation method enabled by long-context VLMs, which crucially operates over shuffled frames. At its core, GVL asks frozen state-of-the-art VLMs, such as Gemini-1.5-Pro [22], to auto-regressively predict the completion percentage of a task specified in natural language for a sequence of shuffled input video frames; see Fig. 2. Perhaps surprisingly we find that simply shuffling the frames of the input video effectively overcomes the strong implicit temporal bias found in video, enabling VLMs to generate meaningful values. While GVL is capable of generating values in a zero-shot manner, we find that the performance of GVL scales with examples via multi-modal in-context learning. Providing more examples of visual “unshuffling” in context increases performance, irrespective of the target embodiment. For example, human videos can improve GVL’s performance on predicting robot task progress. To facilitate large-scale value prediction evaluation, we additionally introduce a new evaluation metric, Value-Order Correlation (VOC), measuring how well predicted values correlate with the ground-truth timestep order in expert videos; as we will show, VOC is also a useful metric for measuring dataset and trajectory quality, which allows GVL to be used for applications beyond valuebased policy learning such as data quality estimation and success detection. We first evaluate GVL’s value prediction quality with VOC on a large suite of real-world robotics datasets, spanning 51 datasets, 20 embodiments, and more than 300 tasks. This includes 50 datasets from Open-X (OXE) dataset [45] in addition to our own bimanual manipulation dataset containing 250 challenging real-world tasks on an ALOHA platform [71], which are considerably longer horizon and more fine-grained than those in the OXE dataset. In aggregate, GVL exhibits strong zero-shot value prediction capabilities with highly positive VOC scores on most datasets; its performance further improves with various types of multi-modal in-context examples. Using GVL, we demonstrate scalable foundation model supervision for robot learning at various data abstraction levels. Specifically, GVL can help measure dataset quality in OXE. Second, it can be used for success detection, enabling imitation learning on mixed-quality datasets. Finally, the raw value estimates from GVL can be used for advantage-weighted regression for real-world offline reinforcement learning [47, 46]. In summary, our contributions are 1. Generative Value Learning (GVL), a universal value prediction framework via VLM in-context autoregressive value estimation on shuffled video frames. 2. An extensive evaluation on real-world datasets demonstrating GVL’s zero-shot scalability and multi-modal in-context learning capabilities. 3. Demonstration that GVL can be used in downstream applications including dataset quality estimation, success detection, and advantage-weighted regression for real-world control. Reward and value foundation models. Several works have tried to learn transferable reward and value functions from diverse data. Early works learned models using robot [52] or even human videos with discriminators [8], contrastive learning [3] or offline RL [40, 41, 4] to guide manipulation tasks. With the advent of recent language and vision foundation models, several works have integrated them into various robotic applications such as semantic planning [1, 27, 56, 70, 14], imitation learning [6, 57], and symbolic programming [58, 36, 56, 63, 26, 39, 55, 14, 38, 67]. Most related to our work, LLMs and VLMs have been used as reward models. Kwon et al. [34], Mahmoudieh et al. [43] use language models to provide reward values for RL agents, while Klissarov et al. [32], Wang et al. [64], Kwon et al. [34] use them to provide preference feedback. Ma et al. [42], Yu et al. [69], Xie et al. [66] even have LLMs generate their code. These works use only the language capabilities of foundation models. More recent works directly use VLMs as zero-shot reward models [50] or success detectors [15, 23]. Critically, in these works the VLM acts only as an (often sparse) reward function which predicts success, and not a value function that predicts task progress. Though some works use chain-of-thought prompting [61] or active learning [33], they generally do not make use of the autoregressive, long-context, or in-context learning capabilities of state-of-art VLMs. As a consequence, they often evalaute reward prediction only on simple and simulated tasks. To our knowledge, we are the first to demonstrate that VLMs are capable of generalizable per-frame value estimation on real world tasks which can be used for downstream tasks like dataset selection. In-context learning for robotics. In-context learning has been explored in the robot learning literature, primarily focusing on action generation [16, 19, 11, 68, 13, 37, 20]. However, all these prior works require explicit, and often extensive training, on their robot tasks in order to realize in-context learning capabilities, and generalization is achieved only on narrow distribution of tasks. In contrast, we demonstrate that visual value estimation already enjoys flexible multi-modal in-context learning from pre-trained VLMs without any robot specific fine-tuning.""",
#     # ]

#     rdd = sparkContext.parallelize(chunks)
#     summarized_chunks = SummarizerSingleton().summarize(rdd)
#     return summarized_chunks.collect()


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


@app.get("/test_chunk")
async def test_chunk():
    # Assign a unique ID to the request
    request_id = str(uuid.uuid4())

    # Since this request doesn't come with any anything
    # we use experimental pdf links below
    pdf_links = [
        "http://arxiv.org/pdf/2411.02973.pdf",
        # "http://arxiv.org/pdf/FAKE_URL",  # should raise exception
        "https://arxiv.org/pdf/2412.06593",
    ]

    # We extract the PDFs and store them in Redis
    await store_in_redis(request_id, pdf_links)

    # We use chunker to chunk the individual PDFs
    chunked_pdfs = await ChunkerSingleton().chunker(request_id)
    return chunked_pdfs.collect()


@app.get("/test_summarize")
async def test_summarize():
    # Assign a unique ID to the request
    request_id = str(uuid.uuid4())

    # Since this request doesn't come with any anything
    # we use experimental pdf links below
    pdf_links = [
        "http://arxiv.org/pdf/2411.02973.pdf",
        # "http://arxiv.org/pdf/FAKE_URL",  # should raise exception
        "https://arxiv.org/pdf/2412.06593",
    ]

    # We extract the PDFs and store them in Redis
    await store_in_redis(request_id, pdf_links)

    # We use chunker to chunk the individual PDFs
    chunked_pdfs = await ChunkerSingleton().chunker(request_id)
    return SummarizerSingleton().summarize_pdfs(chunked_pdfs).collect()
