from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.detector import detect_ai_image
from app.agent import generate_explanation
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="AI Image Detector API",
    description="Detects whether an uploaded image is AI-generated or real using Hive AI + LangChain",
    version="1.0.0",
)

# CORS - allows your React or Streamlit frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace * with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Allowed image formats
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
MAX_FILE_SIZE_MB = 5


@app.get("/")
def root():
    """Health check endpoint"""
    return {"status": "running", "message": "AI Detector API is live"}


@app.post("/detect")
async def detect_image(file: UploadFile = File(...)):
    """
    Main endpoint — accepts image upload and returns:
    - is_ai_generated (bool)
    - confidence score
    - label (AI Generated / Real)
    - AI explanation from LangChain agent
    """

    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Allowed: JPEG, PNG, WEBP"
        )

    # Read file bytes
    image_bytes = await file.read()

    # Validate file size (prevent abuse)
    size_mb = len(image_bytes) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large: {size_mb:.1f}MB. Maximum allowed: {MAX_FILE_SIZE_MB}MB"
        )

    try:
        # Step 1: Run detection model
        detection_result = detect_ai_image(image_bytes, file.filename)

        # Step 2: Generate explanation using LangChain agent
        explanation = generate_explanation(detection_result, file.filename)

        # Step 3: Return combined response
        return JSONResponse(content={
            "filename": file.filename,
            "verdict": detection_result["label"],
            "is_ai_generated": detection_result["is_ai_generated"],
            "confidence_percent": round(detection_result["confidence"] * 100, 1),
            "ai_score": detection_result["ai_score"],
            "real_score": detection_result["real_score"],
            "explanation": explanation,
            "status": "success"
        })

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
