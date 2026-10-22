import sys
from pathlib import Path

AUDIT_DIR = Path(r"C:\testing\research_audit_20261015_231500")
sys.path.insert(0, str(AUDIT_DIR))

# Let's import message manager types
from browser_use.agent.message_manager.service import MessageManager
import inspect

print("Checking ContentPart types in browser_use:")
import browser_use.agent.message_manager.views as views
for attr in dir(views):
    if "Content" in attr or "Part" in attr or "Message" in attr:
        print(" ", attr)
