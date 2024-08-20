# flake8: noqa
from openfinance.agentflow.prompt.base import PromptTemplate

prompt ="""You must choose the most related function from:
{tools}

Answer in the following format:

Question: the input question you must answer
Thought: you should think which function to use and only choose one
Function: function to choose, should be one of [{tool_names}]
Function Input: input parameters to function, or None if not exsits

You can only think one step forward. Begin!

Question: {content}
Thought:
"""

FUNC_PROPMT = PromptTemplate(
    prompt=prompt, 
    variables=["tools", "tool_names", "content"]
)