import functools
import inspect
from typing import Callable, List
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser, AIMessage, HumanMessage
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import BaseTool
from langchain.graphs import StateGraph

def agent_graph():
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            graph_structure, context = await func(*args, **kwargs)
            workflow = StateGraph()
            for node_name, node_info in graph_structure['nodes'].items():
                agent_node, _ = node_info['agent']
                workflow.add_node(node_name, agent_node)
            for edge in graph_structure['edges']:
                workflow.add_edge(edge['from'], edge['to'])
            if 'entry_point' in graph_structure:
                workflow.set_entry_point(graph_structure['entry_point'])
            graph = workflow.compile()
            result = await graph.ainvoke({
                "messages": [HumanMessage(content=context)],
                "sender": "user",
            })
            return result.get('messages', [])[-1].content
        return wrapper
    return decorator