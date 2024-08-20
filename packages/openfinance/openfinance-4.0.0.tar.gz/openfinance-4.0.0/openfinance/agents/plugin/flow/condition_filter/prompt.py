# flake8: noqa
from openfinance.agentflow.prompt.base import DynamicPromptTemplate

prompt ="""
Case1: 是否属于选取特定标签的选股策略？比如 强势股,破位上涨,向上反转,30日新低
Result: 按照json格式输出 {"result":[{"label": ""]}
Case2: 是否属于包含指标的筛选策略，比如RSI大于30 
Result: 比较符号可以选择 gt (大于，高于)、lt（小于，低于）、eq（等于）, 按照json格式输出 {"result":[{"indicator": "", "symbol": "", "value": }]}
Case3: 都不符合
Result: None

Question: {{content}}
Constrain: 你必须从上面Case中选择最适合的一个,并且按照要求输出Result

Answer Format:
```
Thought: your thought
Result: your Result
```
"""

FUNC_PROPMT = DynamicPromptTemplate(
    prompt=prompt, 
    variables=["content"]
)