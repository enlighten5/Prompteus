import functools
from typing import Callable, List
from langchain.prompts import ChatPromptTemplate
from langchain.schema import AIMessage
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import BaseTool

def agent(model_name: str = "gpt-3.5-turbo", tools: List[BaseTool] = None):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            prompt = func.__doc__
            if not prompt:
                raise ValueError(f"Function {func.__name__} must have a docstring to use as a prompt")
            template = ChatPromptTemplate.from_messages([
                ("system", prompt),
                ("human", "{input}")
            ])
            llm = ChatOpenAI(model_name=model_name)
            agent = create_openai_functions_agent(llm, tools or [], template)
            agent_executor = AgentExecutor(agent=agent, tools=tools or [], verbose=True)
            additional_context = func(*args, **kwargs)
            async def agent_node(state):
                combined_input = {**state, **(additional_context or {})}
                result = await agent_executor.ainvoke(combined_input)
                return {
                    "messages": [AIMessage(content=result['output'])],
                    "sender": func.__name__
                }
            return agent_node, additional_context
        return wrapper
    return decorator