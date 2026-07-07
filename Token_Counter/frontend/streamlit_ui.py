import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Research Assistant Agent",
    layout="wide"
)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "session_id" not in st.session_state:
    st.session_state.session_id = str(
        uuid.uuid4()
    )

if "generated_result" not in st.session_state:
    st.session_state.generated_result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("Research Agent")

st.sidebar.info(
    f"Session:\n{st.session_state.session_id[:12]}"
)

if st.sidebar.button(
        "New Conversation"
):
    try:
        requests.delete(
            f"{API_URL}/session/"
            f"{st.session_state.session_id}"
        )
    except:
        pass

    st.session_state.session_id = str(
        uuid.uuid4()
    )

    st.session_state.generated_result = None
    st.session_state.chat_history = []

    st.rerun()

st.sidebar.divider()

try:
    response = requests.get(
        f"{API_URL}/history/"
        f"{st.session_state.session_id}"
    )

    history = response.json()

except:
    history = []

st.sidebar.subheader("Session History")

for item in reversed(history):

    prompt = item[2]

    title = (
        prompt[:30] + "..."
        if len(prompt) > 30
        else prompt
    )

    st.sidebar.write(f"• {title}")

# ---------------------------------------------------
# MAIN PAGE
# ---------------------------------------------------

st.title(
    "Research Assistant Agent"
)

st.caption(
    "LangChain + Ollama + Tool Calling"
)

# ---------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------

for chat in st.session_state.chat_history:

    with st.chat_message(
            chat["role"]
    ):
        st.markdown(
            chat["content"]
        )

# ---------------------------------------------------
# USER INPUT
# ---------------------------------------------------

prompt = st.chat_input(
    "Ask something..."
)

if prompt:

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message(
            "user"
    ):
        st.markdown(prompt)

    payload = {
        "session_id":
            st.session_state.session_id,
        "prompt":
            prompt,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_tokens": 500
    }

    with st.spinner(
            "Thinking..."
    ):

        try:
            response = requests.post(
                f"{API_URL}/generate",
                json=payload
            )

            if response.status_code == 200:

                result = response.json()

                answer = result[
                    "response"
                ]

                st.session_state.generated_result = result

                st.session_state.chat_history.append(
                    {
                        "role":
                            "assistant",
                        "content":
                            answer
                    }
                )

                with st.chat_message(
                        "assistant"
                ):
                    st.markdown(
                        answer
                    )

                    st.divider()

                    col1, col2 = st.columns(
                        2
                    )

                    with col1:
                        st.metric(
                            "Input Tokens",
                            result[
                                "input_tokens"
                            ]
                        )

                        st.metric(
                            "Output Tokens",
                            result[
                                "output_tokens"
                            ]
                        )

                    with col2:
                        st.metric(
                            "Latency",
                            result[
                                "elapsed_time"
                            ]
                        )

                        st.metric(
                            "Model",
                            result[
                                "model"
                            ]
                        )

                    st.metric(
                        "Prompt Type",
                        result[
                            "prompt_type"
                        ]
                    )

                    # -------------------
                    # Agent Trace
                    # -------------------

                    if result.get(
                            "agent_trace"
                    ):

                        with st.expander(
                                "Agent Trace"
                        ):

                            for step in result[
                                "agent_trace"
                            ]:
                                st.code(
                                    str(step)
                                )

            else:
                st.error(
                    response.text
                )

        except Exception as exc:
            st.error(
                str(exc)
            )

# ---------------------------------------------------
# METRICS DASHBOARD
# ---------------------------------------------------

st.divider()

st.subheader(
    "Session Metrics"
)

try:

    history_response = requests.get(
        f"{API_URL}/history/"
        f"{st.session_state.session_id}"
    )

    session_history = (
        history_response.json()
    )

    total_input = sum(
        row[9]
        for row in session_history
    )

    total_output = sum(
        row[10]
        for row in session_history
    )

    total_latency = round(
        sum(
            row[11]
            for row in session_history
        ),
        2
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:
        st.metric(
            "Total Input Tokens",
            total_input
        )

    with col2:
        st.metric(
            "Total Output Tokens",
            total_output
        )

    with col3:
        st.metric(
            "Total Latency",
            total_latency
        )

except:
    pass

# ---------------------------------------------------
# AGENT LOGS
# ---------------------------------------------------

st.divider()

if st.button(
        "Show Agent Logs"
):
    try:

        logs = requests.get(
            f"{API_URL}/agent_logs/"
            f"{st.session_state.session_id}"
        ).json()

        for log in logs:

            with st.expander(
                    f"Prompt: {log[2][:50]}"
            ):

                st.write(
                    f"Model: {log[4]}"
                )

                st.write(
                    "Tools Used:"
                )

                st.code(
                    log[5]
                )

                st.write(
                    "Response:"
                )

                st.write(
                    log[3]
                )

    except:
        st.warning(
            "No logs found."
        )