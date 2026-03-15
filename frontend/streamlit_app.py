import streamlit as st
import requests
from PIL import Image
import io

# ---- Page Config ----
st.set_page_config(
    page_title="AI Image Detector",
    page_icon="🔍",
    layout="centered"
)

# ---- Title ----
st.title("🔍 AI Image Detector")
st.markdown("**Upload an image to detect whether it's AI-generated or real.**")
st.divider()

# ---- Backend URL ----
# Change this to your deployed backend URL when you deploy on Render
BACKEND_URL = "http://localhost:8000/detect"

# ---- File Upload ----
uploaded_file = st.file_uploader(
    "Choose an image...",
    type=["jpg", "jpeg", "png", "webp"],
    help="Max file size: 5MB"
)

if uploaded_file is not None:
    # Show uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption=f"Uploaded: {uploaded_file.name}", use_container_width=True)

    st.divider()

    # Analyze button
    if st.button("🔎 Analyze Image", type="primary", use_container_width=True):
        with st.spinner("Analyzing image... Please wait..."):
            try:
                # Reset file pointer before sending
                uploaded_file.seek(0)

                # Send to FastAPI backend
                response = requests.post(
                    BACKEND_URL,
                    files={"file": (uploaded_file.name, uploaded_file, uploaded_file.type)},
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()

                    st.divider()

                    # ---- Verdict Display ----
                    if result["is_ai_generated"]:
                        st.error(f"🤖 **Verdict: {result['verdict']}**")
                    else:
                        st.success(f"✅ **Verdict: {result['verdict']}**")

                    # ---- Confidence Scores ----
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Confidence", f"{result['confidence_percent']}%")
                    with col2:
                        st.metric("AI Score", f"{round(result['ai_score'] * 100, 1)}%")
                    with col3:
                        st.metric("Real Score", f"{round(result['real_score'] * 100, 1)}%")

                    # ---- Progress Bar ----
                    st.markdown("**AI Generation Probability:**")
                    st.progress(result["ai_score"])

                    # ---- Explanation from LangChain Agent ----
                    st.divider()
                    st.markdown("### 🧠 AI Analysis")
                    st.info(result["explanation"])

                else:
                    error_detail = response.json().get("detail", "Unknown error")
                    st.error(f"❌ Error: {error_detail}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure FastAPI server is running on port 8000.")
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. Try again.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

# ---- Footer ----
st.divider()
st.markdown(
    "<center><small>Built with FastAPI + LangChain + Hive AI + Streamlit</small></center>",
    unsafe_allow_html=True
)
