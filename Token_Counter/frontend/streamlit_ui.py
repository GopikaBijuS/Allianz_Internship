import streamlit as st
import requests

Api_URL = "http://localhost:8000"

st.set_page_config(page_title="Local LLM Analyzer",layout="wide")

# -----------------------------------------
# SESSION STATE
# -----------------------------------------

if "selected_chat" not in st.session_state:
    st.session_state.selected_chat = None

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

if "generated_result" not in st.session_state:
    st.session_state.generated_result = None


# -----------------------------------------
# REUSABLE UI
# -----------------------------------------

def show_metrics(input_tokens,output_tokens,elapsed_time,cost):

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Input Tokens",input_tokens)
        st.metric("Output Tokens",output_tokens)

    with col2:
        st.metric("Elapsed Time",elapsed_time)
        st.metric("Inference Cost",cost)


def show_response_card(result):

    st.subheader("Response")

    st.info(
        f"Prompt Type: {result['prompt_type'].title()}"
    )

    st.info(
        f"Model Used: {result['model']}"
    )

    st.write(result["response"])

    show_metrics(
        result["input_tokens"],
        result["output_tokens"],
        result["elapsed_time"],
        result["cost"]
    )

# -----------------------------------------
# SIDEBAR
# -----------------------------------------

st.sidebar.title("History")

try:
    history_response = requests.get(f"{Api_URL}/history")
    history = history_response.json()

except Exception:
    history = []

for item in history:
    chat_id = item[0]
    prompt = item[1]
    title = (
        prompt[:25] + "..." if len(prompt) > 25
        else prompt
    )

    if st.sidebar.button(title,key=f"history_{chat_id}"):
        st.session_state.selected_chat = item
        st.session_state.edit_mode = False
        st.rerun()

# -----------------------------------------
# MAIN PAGE
# -----------------------------------------

st.title("Local LLM Analyzer")
selected = st.session_state.selected_chat

# -----------------------------------------
# NEW PROMPT PAGE
# -----------------------------------------

if selected is None:
    st.subheader("Generate Response")
    prompt = st.text_area("Prompt",height=200)
    
    temperature = st.slider(
        "Temperature",
        0.0,
        1.5,
        0.7,
        0.1
    )

    top_p = st.slider(
        "Top P",
        0.1,
        1.0,
        0.9,
        0.05
    )
    top_k = st.slider(
        "Top K",
        10,
        100,
        40,
        1
    )

    max_tokens = st.slider(
        "Max Tokens",
        50,
        1000,
        200,
        50
    )

    if st.button("Generate"):
        payload = {
            "prompt": prompt,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_tokens": max_tokens
        }

        try:
            response = requests.post(f"{Api_URL}/generate", json=payload)
            if response.status_code == 200:
                result = response.json()
                st.session_state.generated_result = result
            else:
                error_detail = response.text
                st.error(f"Generation Failed: {error_detail}")
        except requests.RequestException as exc:
            st.error(f"Request Failed: {exc}")

    if st.session_state.generated_result:
        show_response_card(
            st.session_state.generated_result)

# -----------------------------------------
# HISTORY DETAILS
# -----------------------------------------

else:
    chat_id = selected[0]
    prompt = selected[1]
    response_text = selected[2]
    model = selected[3]
    temperature = selected[4]
    top_p = selected[5]
    top_k = selected[6]
    max_tokens = selected[7]
    input_tokens = selected[8]
    output_tokens = selected[9]
    elapsed_time = selected[10]
    cost = selected[11]

    # -----------------------------------------
    # EDIT MODE
    # -----------------------------------------

    if st.session_state.edit_mode:

        st.subheader("Edit Prompt")
        updated_prompt = st.text_area("Prompt",value=prompt,height=200)
        updated_temperature = st.slider("Temperature", 0.0, 1.5, temperature, 0.1)
        updated_top_p = st.slider("Top P", 0.1, 1.0, top_p, 0.05)
        updated_top_k = st.slider("Top K", 10, 100, top_k, 1)
        updated_max_tokens = st.slider("Max Tokens", 50, 1000, max_tokens, 50)


        if st.button("Update"):

            payload = {
                "prompt": updated_prompt,
                "temperature": updated_temperature,
                "top_p": updated_top_p,
                "top_k": updated_top_k,
                "max_tokens": updated_max_tokens
            }
            try:
                response = requests.put(f"{Api_URL}/history/{chat_id}", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.generated_result = result
                    st.success("Updated Successfully")
                else:
                    error_detail = response.text
                    st.error(f"Update Failed: {error_detail}")
            except requests.RequestException as exc:
                st.error(f"Request Failed: {exc}")

        if st.session_state.generated_result:

            st.divider()
            show_response_card(st.session_state.generated_result)
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Save Changes"):
                st.session_state.edit_mode = False
                st.session_state.selected_chat = None
                st.session_state.generated_result = None
                st.rerun()

        with col2:
            if st.button("Cancel"):
                st.session_state.edit_mode = False
                st.session_state.generated_result = None
                st.rerun()

    # -----------------------------------------
    # VIEW MODE
    # -----------------------------------------

    else:
        st.subheader("Prompt")
        st.info(prompt)
        st.subheader("Response")
        st.write(response_text)
        st.divider()
        show_metrics(input_tokens,output_tokens,elapsed_time,cost)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("temperature",temperature)
        with col2:
            st.metric("top_p",top_p)
            pass
        with col3:
            st.metric("top_k",top_k)
        with col4:
            st.metric("max_tokens",max_tokens)

        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button(model,disabled=True)

        with col2:
            if st.button("Edit"):
                st.session_state.edit_mode = True
                st.rerun()

        with col3:
            if st.button("Delete"):
                requests.delete(f"{Api_URL}/history/{chat_id}")
                st.session_state.selected_chat = None
                st.rerun()

        if st.button("New Prompt"):
            st.session_state.selected_chat = None
            st.session_state.generated_result = None
            st.rerun()