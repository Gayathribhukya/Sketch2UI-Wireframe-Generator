from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os

from backend.detect import detect_ui_components
from backend.generator import generate_html
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For now allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "processed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.mount("/processed", StaticFiles(directory="processed"), name="processed")


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(OUTPUT_FOLDER, "processed_" + file.filename)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    components = detect_ui_components(input_path, output_path)
    html_code = generate_html(components)

    return {
        "message": "Processing complete",
        "processed_image": f"http://localhost:8000/processed/processed_{file.filename}",
        "components": components,
        "code": html_code
    }