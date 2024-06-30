# Prompteus

Forge AI agents from simple Python functions. Turn your docstrings into powerful prompts and weave complex AI workflows with ease.

## 🌟 Features

- **Simple Decorators**: Transform ordinary functions into LLM-powered agents with a single decorator.
- **Docstring Prompts**: Utilize Python's natural docstring syntax to define your AI prompts.
- **Flexible Agent Creation**: Easily create and customize AI agents for various tasks.
- **Graph-based Workflows**: Construct complex AI workflows by connecting agents in a graph structure.
- **Seamless Integration**: Works smoothly with popular LLM libraries like LangChain.

## 🚀 Installation

Install Prompteus using pip:

```bash
pip install prompteus
```

## 🔧 Usage

### Simple LLM Interaction

```python
from prompteus import llm_interact

@llm_interact(model_name="gpt-3.5-turbo")
def generate_story(theme: str):
    """
    Create a short story based on the given theme.
    The story should be engaging and no longer than 100 words.
    """
    return theme

story = generate_story("A robot learning to paint")
print(story)
```

### Create an AI Agent

```python
from prompteus import agent
from your_custom_tools import ImageAnalysisTool

@agent(model_name="gpt-3.5-turbo", tools=[ImageAnalysisTool()])
def image_analyst():
    """
    Analyze the given image and provide a detailed description.
    Use the ImageAnalysisTool when needed to get more information about specific elements in the image.
    """
    return {}  # Additional context if needed

image_agent, _ = image_analyst()
result = await image_agent({"input": "path/to/image.jpg"})
print(result['messages'][-1].content)
```

### Constructing an Agent Workflow

```python
from prompteus import agent_graph

@agent_graph()
async def analyze_and_critique(image_path: str):
    graph_structure = {
        'nodes': {
            'image_analyst': {'agent': image_analyst()},
            'art_critic': {'agent': art_critic()},
        },
        'edges': [
            {'from': 'image_analyst', 'to': 'art_critic'},
        ],
        'entry_point': 'image_analyst'
    }
    return graph_structure, image_path

result = await analyze_and_critique("path/to/artwork.jpg")
print(result)
```