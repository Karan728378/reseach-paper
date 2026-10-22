import inspect
from browser_use.agent.service import Agent

src = inspect.getsource(Agent.get_model_output)
print(src[:2000])
