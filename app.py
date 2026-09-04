import os
import streamlit as st
from groq import Groq

# Page Setup
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate social media posts, captions, and hashtags instantly using Groq.")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key_input = st.text_input(
        "Groq API Key",
        type="password",
        help="Get a free key from console.groq.com",
        value=os.environ.get("GROQ_API_KEY", "")
    )
    st.markdown("[Get Free Groq API Key](https://console.groq.com/keys)")

# User Form
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        platform = st.selectbox("Platform", ["LinkedIn", "Instagram", "Twitter / X", "Facebook", "YouTube", "Blog"])
        content_type = st.selectbox("Content Type", ["Educational", "Promotional", "Storytelling", "Thought Leadership"])
        tone = st.selectbox("Tone", ["Professional", "Casual & Friendly", "Energetic", "Witty", "Persuasive"])

    with col2:
        topic = st.text_input("Topic / Main Idea", placeholder="e.g., 5 Python tips for beginners")
        target_audience = st.text_input("Target Audience", placeholder="e.g., Students, Developers")
        include_hashtags = st.checkbox("Include Hashtags", value=True)

    submit_button = st.form_submit_button("Generate Content", use_container_width=True)

# Content Generation
if submit_button:
    if not api_key_input:
        st.error("Please enter a Groq API Key in the sidebar.")
    elif not topic.strip():
        st.error("Please enter a topic.")
    else:
        try:
            client = Groq(api_key=api_key_input)

            system_prompt = (
                "You are an expert social media strategist. "
                "Generate clear, platform-tailored posts with clean Markdown."
            )

            user_prompt = f"""
            Create a post for {platform}.
            - Type: {content_type}
            - Topic: {topic}
            - Audience: {target_audience if target_audience else 'General'}
            - Tone: {tone}
            - Hashtags: {'Yes' if include_hashtags else 'No'}

            Structure:
            1. **Catchy Hook**
            2. **Main Post / Caption**
            3. **Call to Action (CTA)**
            4. **Hashtags** (if requested)
            """

            with st.spinner("Generating post..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1024,
                )

            output_text = response.choices[0].message.content

            st.success("Done!")
            st.markdown("---")
            st.markdown(output_text)

            # Download Option
            st.download_button(
                label="Download Text File",
                data=output_text,
                file_name=f"{platform.lower()}_post.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error: {str(e)}")
