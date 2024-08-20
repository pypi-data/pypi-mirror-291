# flake8: noqa
from openfinance.agentflow.prompt.base import DynamicPromptTemplate

plan_prompt_template_v1 = """
{% if role %}
Role: you are {{role}}
{% if backgroud %}
Backgroud: {{backgroud}}
{% endif %}
{% else %}
Role: you are a stock analysis
{% endif %}

Task : you need to find out possible factors about Question. 
Question: {{content}}

Answer in this format:
```
Task: input task to solve in English
Thought: list associated factor names that you need to solve the task thoroughly.
Subtasks: list all indicator names to evaluate each factor and you must be in valid JSON format.
```
Let's begin!
"""


plan_prompt_template = """
{% if role %}
Role: you are {{role}}
{% if backgroud %}
Backgroud: {{backgroud}}
{% endif %}
{% else %}
Role: you are a senior stock analyst
{% endif %}

Question: {{content}}
Requirement: You only need to build a analysis framework

Answering format:

Task: the english translation of Question
Thought: list most related factors and list all indicators of each factor
Subtasks: in valid JSON format as {"factor": ["indicator",...],...}

Let's begin!
"""


PLAN_PROMPT = DynamicPromptTemplate(
    prompt = plan_prompt_template, 
    variables = ["content", "role", "goal", "backgroud"]
)