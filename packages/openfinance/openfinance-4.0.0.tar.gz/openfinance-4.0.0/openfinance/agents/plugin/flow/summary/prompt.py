# flake8: noqa
from openfinance.agentflow.prompt.base import DynamicPromptTemplate

prompt_template ="""
{% if role %}
Role: you are {{role}}
{% else %}
Role: you are a stock analyst
{% endif %}
{% if goal %}
Goal: {{goal}}
{% else %}
Goal: think factor by factor to answer concretly and helpfully
{% endif %}
{% if restriction %}
Restriction: {{restriction}}
{% else %}
Restriction: think based on negative and positive
{% endif %}

Question: {{content}}
Document:
```
{{document}}
```
Begin to answer in Chinese!
"""

chinese_prompt_template ="""
{% if role %}
角色: 你是 {{role}}
{% else %}
角色: 你是一个资深的分析员
{% endif %}
{% if goal %}
目标: {{goal}}
{% else %}
目标: 按照因子逐个分析，然后提供有益的、具体的中文回答
{% endif %}
{% if restriction %}
Restriction: {{restriction}}
{% else %}
Restriction: 尽量基于提供的Document来回答，不要要求进一步信息
{% endif %}

Question: {{content}}
Document:
```
{{document}}
```
开始回答!
"""

PROMPT = DynamicPromptTemplate(
    prompt=chinese_prompt_template, 
    variables=["content", "document", "role", "goal", "restriction"]
)