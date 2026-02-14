from mcp.server.fastmcp import FastMCP
import subprocess
import shlex

mcp = FastMCP("remediation-executor")

ALLOWED_COMMANDS = (
    "sudo apt install",
    "sudo apt-get install",
    "sudo apt-get install --only-upgrade",
    "sudo npm install -g",
    "npm install -g",
)

BLOCKLIST = (
    "rm ",
    "reboot",
    "shutdown",
    "mkfs",
    "dd ",
    "systemctl",
    "kernel",
    "chmod",
    "chown",
)


def is_safe_command(cmd: str) -> bool:
    if any(bad in cmd for bad in BLOCKLIST):
        return False
    return cmd.startswith(ALLOWED_COMMANDS)

@mcp.tool()
def run_remediation(command: str) -> str:
    """
    Execute an approved remediation command.
    Example: upgrade Node.js
    """

    if not is_safe_command(command):
        return f"❌ BLOCKED by policy: {command}"

    try:
        result = subprocess.run(
            shlex.split(command),
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.stdout + result.stderr

    except Exception as e:
        return f"Execution failed: {str(e)}"
    
if __name__ == "__main__":
    mcp.run()