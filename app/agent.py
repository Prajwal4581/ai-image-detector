import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client directly — no LangChain needed
# This avoids all Python 3.14 + Pydantic compatibility issues
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_explanation(detection_result: dict, filename: str) -> str:
    """
    Calls Groq API directly to generate a human-readable explanation
    of the detection result. No LangChain dependency.
    """

    prompt = f"""
You are an AI forensics expert. A user uploaded an image and our detection model analyzed it.

Detection Results:
- File: {filename}
- Verdict: {detection_result['label']}
- AI-Generated Probability: {detection_result['ai_score']}
- Real/Authentic Probability: {detection_result['real_score']}

Based on these scores, provide a clear and informative explanation that includes:
1. What the verdict means in simple terms
2. Why AI-generated images are detected (mention visual artifacts, pixel patterns, GAN/diffusion model signatures)
3. What the confidence score means for reliability
4. A short note on limitations of AI detection

Keep it under 150 words. Be professional but easy to understand.
Do NOT mention "I" or act as a chatbot. Just give the analysis directly.
"""

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        # Fallback if Groq fails — don't crash the whole app
        return (
            f"Verdict: {detection_result['label']} with "
            f"{round(detection_result['confidence'] * 100, 1)}% confidence. "
            f"AI Score: {detection_result['ai_score']}, "
            f"Real Score: {detection_result['real_score']}."
        )
