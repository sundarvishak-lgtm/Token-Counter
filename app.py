import streamlit as st
import tiktoken
import os
from groq import Groq
st.title("Token Counter + Prompt Compressor”)
system_prompt = st.text_area("System prompt”, height=150)
conversation_history = st.text_area("Conversation history”, height=100)
new_message = st.text_area("New message”, height=80)
if st.button("Count + Compress”):
api_key = st.secrets["GROQ_API_KEY”]
encoder = tiktoken.get_encoding("cl100k_base”)
system_tokens = len(encoder.encode(system_prompt))
history_tokens = len(encoder.encode(conversation_history))
message_tokens = len(encoder.encode(new_message))
total_tokens = system_tokens + history_tokens + message_tokens
st.subheader(”Token breakdown”)
st.write(f”System prompt: **{system_tokens} tokens**”)
st.write(f”Conversation history: **{history_tokens} tokens**”)
st.write(f”New message: **{message_tokens} tokens**”)
st.write(f”Total: **{total_tokens} tokens** ({round((total_tokens / 131072) * 100, 1)}% of limit)”)
st.subheader(”Compressed system prompt”)
client = Groq(api_key=api_key)
response = client.chat.completions.create(
model=”llama-3.3-70b-versatile”,
messages=[
{”role”: “system”, “content”: “You are an expert at making AI system prompts shorter without losing meaning. Remove filler, redundancy, and over-explanation. Keep all instructions intact.”},
{”role”: “user”, “content”: f”Compress this system prompt:\n\n{system_prompt}”}
]
)
compressed = response.choices[0].message.content
compressed_tokens = len(encoder.encode(compressed))
saved = system_tokens - compressed_tokens
st.text_area(”Compressed version”, value=compressed, height=150)
st.write(f”Before: **{system_tokens} tokens** → After: **{compressed_tokens} tokens** → Saved: **{saved} tokens**”)

