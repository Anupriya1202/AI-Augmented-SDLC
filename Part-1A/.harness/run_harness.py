"""Independent Part 1A harness using Python's standard library."""
from __future__ import annotations
import ast
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent


def execute(name: str, command: list[str]) -> dict:
    result = subprocess.run(command, cwd=REPO, text=True, capture_output=True, check=False)
    return {"gate": name, "command": command, "exit_code": result.returncode,
            "status": "PASS" if result.returncode == 0 else "FAIL",
            "stdout": result.stdout[-10000:], "stderr": result.stderr[-10000:]}


def style_scan() -> tuple[bool, list[str]]:
    findings = []
    for path in list((ROOT / "src").glob("*.py")) + list((ROOT / "tests").glob("*.py")):
        lines = path.read_text(encoding="utf-8").splitlines()
        for number, line in enumerate(lines, 1):
            if line.rstrip() != line:
                findings.append(f"{path.name}:{number}: trailing whitespace")
            if "\t" in line:
                findings.append(f"{path.name}:{number}: tab indentation is not allowed")
    return not findings, findings


def ast_security_scan() -> tuple[bool, list[str]]:
    forbidden = {"eval", "exec", "compile", "__import__"}
    findings = []
    for path in (ROOT / "src").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in forbidden:
                findings.append(f"{path.name}:{node.lineno}: forbidden dynamic execution call {node.func.id}")
    return not findings, findings


def main() -> int:
    tests = execute("unit_contract_tests", [sys.executable, "-m", "unittest", "discover", "-s", "Part-1A/tests", "-v"])
    compile_gate = execute("syntax_compile", [sys.executable, "-m", "compileall", "-q", "Part-1A/src", "Part-1A/tests"])
    lint_ok, lint_findings = style_scan()
    lint = {"gate": "lint", "command": "standard-library whitespace/indentation checks (Ruff may be run separately)", "exit_code": 0 if lint_ok else 1, "status": "PASS" if lint_ok else "FAIL", "findings": lint_findings}
    secure, findings = ast_security_scan()
    sast = {"gate": "security_static_scan", "command": "AST scan for dynamic execution primitives", "exit_code": 0 if secure else 1,
            "status": "PASS" if secure else "FAIL", "findings": findings}
    results = [tests, compile_gate, lint, sast]
    report = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "gates": results,
              "note": "Standard-library static checks used because third-party packages may not be available offline.",
              "overall": "PASS" if all(item["status"] == "PASS" for item in results) else "FAIL"}
    out = ROOT / "evidence" / "harness-results.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"overall": report["overall"], "gates": [{"gate": x["gate"], "status": x["status"], "exit_code": x["exit_code"]} for x in results]}, indent=2))
    return 0 if report["overall"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
