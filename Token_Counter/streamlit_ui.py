import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Cost & Token Analyzer",
    layout="wide"
)

st.title("Cost & Token Analyzer")

text = st.text_area("Enter Text",height=200)

uploaded_file = st.file_uploader(
    "Or Upload a Text File",type=["txt"])

if uploaded_file is not None:

    text = uploaded_file.read().decode("utf-8")

    st.text_area("File Content",text,height=200)

model = st.selectbox(
    "Select Model",
    [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-3.5-turbo"
    ]
)

if st.button("Analyze"):

    payload = {
        "text": text,
        "model": model
    }

    response = requests.post("http://127.0.0.1:8000/token_count/",json=payload)

    if response.status_code == 200:

        result = response.json()

        st.success("Analysis Completed")

        col1, col2 = st.columns(2)

        with col1:

            st.metric("Token Count",result["token_count"])

            st.metric("Cost (USD)",f"${result['estimated_cost']:.6f}")

        with col2:

            st.metric("Model",result["model"])

            st.metric("Cost (USD)",f"${result['estimated_cost']:.6f}")

    else:
        st.error(response.json()["detail"])\
        
if st.button("View History"):

    response = requests.get("http://127.0.0.1:8000/history")

    df = pd.DataFrame(response.json(), columns=["ID", "Text", "Model", "Token Count", "Cost (USD)"])
    st.dataframe(df)
    # history = response.json()

    # for row in history:

    #     col1, col2 = st.columns([8,1])

    #     with col1:

    #         st.write(
    #             f"{row[0]} | {row[2]} | {row[3]} tokens"
    #         )

    #     with col2:

    #         if st.button(
    #             "Delete",
    #             key=f"del_{row[0]}"
    #         ):

    #             requests.delete(
    #                 f"http://127.0.0.1:8000/history/{row[0]}"
    #             )

    #             st.rerun()
    #         if st.button(
    #             "Edit",
    #             key=f"edit_{row[0]}"
    #         ):

    #             st.session_state.edit_id = row[0]

    #             st.session_state.edit_text = row[1]

    #             st.session_state.edit_model = row[2]