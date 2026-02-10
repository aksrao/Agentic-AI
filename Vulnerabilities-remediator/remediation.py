import json
import os
import google.genai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")

client = genai.Client(api_key=GEMINI_API_KEY)

with open("medium_vulns.json") as f:
    filtered_vulns = json.load(f)


prompt = f"""
You are a DevSecOps remediation assistant.

You MUST respond with ONLY valid JSON.
DO NOT include markdown.
DO NOT include explanations.
DO NOT include extra text.

Return an array of objects using this schema EXACTLY:

[
  {{
    "cve": "string",
    "package": "string",
    "safe_to_fix": boolean,
    "reason": "string",
    "remediation_type": "apt|pip|npm|none",
    "command": "string",
    "restart_required": boolean
  }}
]

LOW severity vulnerabilities:
{json.dumps(filtered_vulns[:10], indent=2)}
"""

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents = prompt
    )

print(response.text)

# try:
#     remediation_plan = json.loads(response.text)
# except json.JSONDecodeError:
#     raise RuntimeError("Gemini returned invalid JSON")

# with open("remediation_plan.json", "w") as f:
#     json.dump(remediation_plan, f, indent=2)