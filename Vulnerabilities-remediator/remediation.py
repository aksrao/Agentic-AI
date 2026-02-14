import json
import os
import google.genai as genai
from dotenv import load_dotenv
import re

load_dotenv()
# def extract_json(text: str):
#     """
#     Extract the first JSON array from Gemini output.
#     """
#     match = re.search(r"\[\s*{.*?}\s*\]", text, re.DOTALL)
#     if not match:
#         raise ValueError("No JSON array found in Gemini response")
#     return json.loads(match.group(0))


GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")

client = genai.Client(api_key=GEMINI_API_KEY)

# with open("high_vulns.json") as f:
#     filtered_vulns = json.load(f)


prompt = f"""
You are a DevOps assistant.

You are allowed to remediate tools using Homebrew.

Rules:
- Only use Homebrew commands
- Only call the MCP tool run_remediation
- Allowed commands:
  - brew update
  - brew upgrade
  - brew upgrade <package>
- Do not suggest sudo or destructive commands

If an upgrade is needed, call run_remediation.
"""

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents = prompt,
    tools=["run_remediation"]
    )

print(response.text)

# try:
#     remediation_plan = extract_json(response.text)

#     # ✅ WRITE TO FILE
#     with open("remediation_plan.json", "w") as f:
#         json.dump(remediation_plan, f, indent=2)

#     print("✅ remediation_plan.json created successfully")

# except Exception as e:
#     print("❌ RAW GEMINI RESPONSE:")
#     print(response.text)
#     raise RuntimeError("Gemini returned invalid JSON") from e

# try:
#     remediation_plan = json.loads(response.text)
# except json.JSONDecodeError:
#     raise RuntimeError("Gemini returned invalid JSON")

# with open("remediation_plan.json", "w") as f:
#     json.dump(remediation_plan, f, indent=2)