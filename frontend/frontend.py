import streamlit as st
import requests
import json

BACKEND_URL = "http://backend:8000/chat/stream"  # docker-compose name

st.title("Financial Literacy RAG Assistant")

question = st.text_input("Ask a question:")

if st.button("Ask") and question:
    trace_box = st.empty()
    answer_box = st.empty()

    trace_steps = []
    answer_text = ""

    with requests.post(BACKEND_URL, json={"question": question}, stream=True) as r:
        for line in r.iter_lines():
            if not line:
                continue

            decoded = line.decode("utf-8")

            if decoded.startswith("data: "):
                payload = decoded.replace("data: ", "")
                event = json.loads(payload)

                if event["type"] == "trace":
                    trace_steps.append(event["trace"])
                    trace_box.markdown("### Reasoning Trace")
                    trace_box.json(trace_steps)

                elif event["type"] == "answer":
                    answer_text = event["answer"]
                    answer_box.markdown("### Answer")
                    answer_box.write(answer_text)

                elif event["type"] == "done":
                    break
