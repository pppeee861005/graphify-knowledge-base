import subprocess
import shlex
import sys

def check(cmd, name):
    print(f"=== {name} ===")
    try:
        result = subprocess.run(shlex.split(cmd), capture_output=True, text=True, timeout=10)
        output = (result.stdout + result.stderr).strip()
        print(output if output else "NOT_FOUND_OR_NO_OUTPUT")
    except FileNotFoundError:
        print("NOT_INSTALLED")
    except Exception as e:
        print(f"ERROR: {e}")
    print()

check("claude --version", "Claude Code")
check("winget --version", "Winget")
check("git --version", "Git")