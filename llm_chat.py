import functools
import inspect
from typing import Callable
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.chat_models import ChatOpenAI

def llm_interact(model_name: str = "gpt-3.5-turbo"):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            prompt = func.__doc__
            if not prompt:
                raise ValueError(f"Function {func.__name__} must have a docstring to use as a prompt")
            template = ChatPromptTemplate.from_messages([
                ("system", prompt),
                ("user", "{input}")
            ])
            llm = ChatOpenAI(model_name=model_name)
            chain = template | llm | StrOutputParser()
            is_async = inspect.iscoroutinefunction(func)
            if is_async:
                async def async_wrapper():
                    context = await func(*args, **kwargs)
                    result = await chain.ainvoke({"input": context})
                    return result
                return async_wrapper()
            else:
                context = func(*args, **kwargs)
                result = chain.invoke({"input": context})
                return result
        return wrapper
    return decorator