import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="wide"
)

# App Header
st.title("✍️ AI Content Assistant")
st.write("Generate customized posts with engaging captions and relevant hashtags powered by Groq.")

# Sidebar - API Key Configuration
st.sidebar.header("🔑 API Settings")
api_key = st.sidebar.text_input(
    "Enter your Groq API Key:",
    type="password",
    help="Get a free key from console.groq.com"
)

# Input Controls Section
st.subheader("⚙️ Content Parameters")

col1, col2 = st.columns(2)

with col1:
    content_type = st.selectbox(
        "Content Type",
        ["Educational Post", "Product Launch", "Story / Case Study", "Promotional Announcement", "Opinion / Thought Leadership"]
    )
    platform = st.selectbox(
        "Target Platform",
        ["LinkedIn", "Instagram", "Twitter / X", "Facebook", "Threads"]
    )
    tone = st.select_slider(
        "Tone of Voice",
        options=["Casual", "Friendly", "Professional", "Enthusiastic", "Bold / Authoritative"]
    )

with col2:
    topic = st.text_input(
        "Topic / Keyword",
        placeholder="e.g., Python tips for beginners, Launching a new SaaS app..."
    )
    target_audience = st.text_input(
        "Target Audience",
        placeholder="e.g., Software Engineers, Small Business Owners, Students..."
    )

# Content Generation Trigger
if st.button("🚀 Generate Post", type="primary", use_container_width=True):
    # Validation checks
    if not api_key:
        st.error("Please provide a valid Groq API key in the sidebar.")
    elif not topic.strip():
        st.warning("Please enter a topic before generating.")
    elif not target_audience.strip():
        st.warning("Please specify the target audience.")
    else:
        try:
            # Initialize Groq client
            client = Groq(api_key=api_key)

            # Construct Prompt
            system_prompt = "You are an expert social media content strategist and copywriter."
            user_prompt = f"""
Create a compelling social media post based on the following details:

- **Platform:** {platform}
- **Content Type:** {content_type}
- **Topic:** {topic}
- **Target Audience:** {target_audience}
- **Tone:** {tone}

### Structure of the Output:
1. **Main Post Content:** Tailored specifically for {platform}'s best practices (formatting, structure, line breaks, length).
2. **Caption / Call to Action (CTA):** A strong finishing sentence or caption to drive engagement.
3. **Hashtags:** Provide 5 to 10 highly relevant, trending hashtags for this topic and platform.
"""

            with st.spinner("Drafting your post via Groq..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1024
                )

                output_text = response.choices[0].message.content

            # Display Results
            st.markdown("---")
            st.subheader("📋 Generated Post")
            st.markdown(output_text)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")