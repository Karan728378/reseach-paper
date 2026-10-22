import inspect
from browser_use import Agent

print("Checking AgentOutput definition:")
# Create a dummy agent instance (without starting browser)
agent = Agent(task="dummy task")
print(f"agent.AgentOutput: {agent.AgentOutput}")
print(f"agent.AgentOutput fields: {list(agent.AgentOutput.model_fields.keys())}")
