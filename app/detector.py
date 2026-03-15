import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Sightengine API — purpose-built for AI image detection
# Free tier: 500 operations/month — enough for demo
# Get keys at: https://sightengine.com (free signup)
SIGHTENGINE_USER = os.getenv("SIGHTENGINE_USER")
SIGHTENGINE_SECRET = os.getenv("SIGHTENGINE_SECRET")


def detect_ai_image(image_bytes: bytes, filename: str) -> dict:
    """
    Uses Sightengine API to detect AI-generated images.
    Simple HTTP call — no ML libraries, works on any Python version.

    Returns:
        dict with is_ai_generated, confidence, label, ai_score, real_score
    """
    try:
        response = requests.post(
            "https://api.sightengine.com/1.0/check.json",
            files={"media": (filename, image_bytes)},
            data={
                "models": "genai",
                "api_user": SIGHTENGINE_USER,
                "api_secret": SIGHTENGINE_SECRET,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "success":
            raise RuntimeError(f"Sightengine error: {data.get('error', {}).get('message', 'Unknown error')}")

        # ai_generated is a score from 0.0 to 1.0
        ai_score = float(data.get("type", {}).get("ai_generated", 0.0))
        real_score = round(1.0 - ai_score, 4)
        is_ai = ai_score >= 0.5

        return {
            "is_ai_generated": is_ai,
            "confidence": round(ai_score if is_ai else real_score, 4),
            "label": "AI Generated" if is_ai else "Real / Authentic",
            "ai_score": round(ai_score, 4),
            "real_score": real_score,
        }

    except requests.exceptions.Timeout:
        raise RuntimeError("Request timed out. Try again.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Sightengine API request failed: {str(e)}")
