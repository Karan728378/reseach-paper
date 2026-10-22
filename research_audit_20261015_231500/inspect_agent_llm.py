import inspect
from browser_use import Agent

# Inspect Agent initialization and run
print("Agent.__init__ parameters:")
sig = inspect.signature(Agent.__init__)
for name, param in sig.parameters.items():
    print(f"  {name}: {param.default}")

print("\nChecking Agent._get_model_response or similar in Agent:")
for attr in dir(Agent):
    if "model" in attr or "llm" in attr or "step" in attr or "message" in attr:
        print(f"  {attr}")
