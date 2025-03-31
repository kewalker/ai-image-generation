from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
import torch
from io import BytesIO
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# Load the model
model_id = "runwayml/stable-diffusion-v1-5"  # Change if you want SDXL
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe.to("cuda" if torch.cuda.is_available() else "cpu")

# FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can change this to specific URLs if needed)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Mount the /static directory to serve static files (e.g., index.html)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create a POST endpoint to generate images
class Prompt(BaseModel):
    text: str

@app.post("/generate")
async def generate_image(prompt: Prompt):
    image = pipe(prompt.text).images[0]

    # Convert to bytes
    img_io = BytesIO()
    image.save(img_io, format="PNG")
    img_io.seek(0)

    return StreamingResponse(img_io, media_type="image/png")

# Serve the index.html file when visiting the root endpoint "/"
@app.get("/")
async def get_index():
    return HTMLResponse(content=open("static/index.html").read(), status_code=200)

# Run with: uvicorn app:app --host 0.0.0.0 --port 8000
