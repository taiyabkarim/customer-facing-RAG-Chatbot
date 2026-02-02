# -*- coding: utf-8 -*-
"""Real-time chatbot for support queries.ipynb

Original file is located at
    https://colab.research.google.com/drive/1Nn_pnRwATrWrfHyVR2xwX7G2Pxis-t9X
"""
import os
import gradio as gr
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from an environment variable for security
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-flash-latest')

# 3. KNOWLEDGE BASE
store_policy = """
URBAN KICKS POLICY:
1. SHIPPING: Free shipping on orders over $50. Standard: 3-5 days. Express: 1-2 days ($15).
2. RETURNS: Accepted within 30 days of purchase. Items must be unworn with tags attached.
3. SALE ITEMS: All items marked 'Final Sale' cannot be returned or exchanged.
4. HOURS: Support is available Mon-Fri, 9am - 5pm EST.
"""

# 4. THE LOGIC (The Brain)
def ask_ai(message, history):
    # Construct the RAG prompt
    prompt = f"""
    Context: {store_policy}
    Question: {message}
    Instruction: Answer strictly from context. Keep it short and polite.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"System Error: {e}"

# 5. LAUNCH THE APP
print("--------------------------------------------------")
print("⏳ Starting Gradio... Look for the 'Running on public URL' link below!")
print("--------------------------------------------------")

# This creates the UI and the Link automatically
demo = gr.ChatInterface(
    fn=ask_ai,
    title="👟 Urban Kicks AI Agent",
    description="Ask about shipping, returns, or store policy.",
    examples=["How much is express shipping?", "Can I return a sale item?", "What are your hours?"]
)

demo.launch(share=True, debug=True)