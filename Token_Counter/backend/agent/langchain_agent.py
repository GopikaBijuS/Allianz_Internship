from langchain.agents import (
    AgentExecutor,
    create_react_agent
)

from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from tools.langchain_tools import (
    compare_topics_tool,
    retrieve_documents,
    summarize_topic_tool,
    generate_report_tool
)


def build_agent(
        model_name: str,
        temperature: float
):
    llm = ChatOllama(
        model=model_name,
        temperature=temperature
    )

    tools = [
        retrieve_documents,
        summarize_topic_tool,
        generate_report_tool,
        compare_topics_tool
    ]

    prompt = PromptTemplate.from_template("""
    You are an intelligent research assistant.

    Rules:
    If the question refers to:
    - my documents
    - uploaded files
    - curriculum
    - notes
    - local information
    you should use retrieve_documents.

    1. Answer directly for:
        - What is ...
        - Explain ...
        - How does ...

    2. Use summarize_topic_tool ONLY if the user explicitly requests a summary.

    3. Use compare_topics_tool ONLY if the user explicitly requests a comparison or differentiation.

    4. Use generate_report_tool ONLY if the user explicitly requests a report.

    5. Do not use tools unnecessarily.

    6. If no tool is needed,
    provide the final answer directly.

    You have access to these tools:

    {tools}

    Use the following format exactly:

    Question: {input}
    Thought: think step by step
    Action: one of [{tool_names}]
    Action Input: input for the action
    Observation: result of the action
    ...
    Thought: I now know the final answer
    Final Answer: answer to the user

    STRICT FORMAT RULES:

    After every Thought:
    - either Action + Action Input
    - or Final Answer
    Never explain that you are using a tool.
    Return the result directly to the user.

    {agent_scratchpad}
    """)

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors= "Your output did not follow the required format. "
        "After Thought you must provide either "
        "Action/Action Input or Final Answer.",
        return_intermediate_steps=True,
        early_stopping_method="generate"
    )

    return executor