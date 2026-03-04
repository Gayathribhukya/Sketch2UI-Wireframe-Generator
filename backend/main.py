from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import shutil

from backend.detect import detect_ui_components
from backend.generator import generate_html

app = FastAPI()

# -----------------------------
# CORS (allow frontend requests)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your Vercel URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Ensure folders exist
# -----------------------------
os.makedirs("uploads", exist_ok=True)
os.makedirs("processed", exist_ok=True)

# -----------------------------
# Static folder for processed images
# -----------------------------
app.mount("/processed", StaticFiles(directory="processed"), name="processed")

# -----------------------------
# Backend base URL
# -----------------------------
BACKEND_URL = "https://sketch2ui-wireframe-generator.onrender.com"

# -----------------------------
# Root route
# -----------------------------
@app.get("/")
def root():
    return {"message": "Sketch2UI Backend is Running"}

# -----------------------------
# Upload endpoint
# -----------------------------
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:

        upload_path = f"uploads/{file.filename}"

        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        processed_filename = f"processed_{file.filename}"
        processed_path = f"processed/{processed_filename}"

        components = detect_ui_components(upload_path, processed_path)

        generated_code = generate_html(components)

        processed_image_url = f"{BACKEND_URL}/processed/{processed_filename}"

        return {
            "message": "Processing complete",
            "processed_image": processed_image_url,
            "code": generated_code
        }

    except Exception as e:
        return {"error": str(e)}