#!/usr/bin/env python3
"""Build the standalone cocompact proof and audit its logical dependencies."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def run(*args):
    process = subprocess.Popen(args, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    chunks = []
    for line in process.stdout:
        print(line, end="", flush=True)
        chunks.append(line)
    status = process.wait()
    if status:
        raise SystemExit(status)
    return "".join(chunks)


# Ensure every included local module is reachable from the cocompact entry point
# and no project-local dependency lives outside this directory.
modules = {"Singularity." + p.stem: p for p in (ROOT / "Singularity").glob("*.lean")}
reachable = set()
def visit(module):
    if module in reachable:
        return
    if module not in modules:
        raise SystemExit(f"Missing local dependency: {module}")
    reachable.add(module)
    for line in re.findall(r"^import\s+(.+)$", modules[module].read_text(), re.M):
        for dep in line.split():
            if dep.startswith("Singularity."):
                visit(dep)
visit("Singularity.FuchsianCocompactSingularity")
if reachable != set(modules):
    raise SystemExit(f"Unneeded local modules: {set(modules) - reachable}")

expected = set()
declaration_sources = {}
for path in sorted((ROOT / "Singularity").glob("*.lean")):
    for name in re.findall(r"^(?:theorem|def) ([\w.]+)", path.read_text(), re.M):
        full_name = "Singularity." + name
        if full_name in declaration_sources:
            raise SystemExit(f"Duplicate declaration name: {full_name} in {declaration_sources[full_name]} and {path}")
        declaration_sources[full_name] = path
        expected.add(full_name)

audit_names = set(re.findall(r"^#print axioms (\S+)",
                            (ROOT / "Audit.lean").read_text(), re.M))
if audit_names != expected:
    raise SystemExit(f"Audit coverage mismatch: {audit_names ^ expected}")

build_output = run("lake", "build")
audit_output = run("lake", "env", "lean", "Audit.lean")
statement_output = run("lake", "env", "lean", "THEOREM.lean")
(ROOT / "THEOREM_STATEMENTS.txt").write_text(statement_output)
reported = set()
for name, dependencies in re.findall(
        r"'([^']+)' depends on axioms: \[([^\]]*)\]", audit_output):
    reported.add(name)
    axioms = {s.strip() for s in dependencies.split(",") if s.strip()}
    if axioms - ALLOWED:
        raise SystemExit(f"Unexpected axioms for {name}: {axioms - ALLOWED}")
reported.update(re.findall(r"'([^']+)' does not depend on any axioms", audit_output))
if reported != expected:
    raise SystemExit(f"Missing or unexpected audit reports: {reported ^ expected}")

report = (
    "COCOMPACT THEOREM: singularity for discrete nonelementary cocompact PSL(2,R) groups, with finite positive semigroup-generating probability support; symmetry is not assumed. All project-local dependencies are included.\n"
    f"Audited {len(expected)} theorem/definition declarations.\n"
    "Allowed axioms: propext, Classical.choice, Quot.sound.\n\n"
    + build_output + "\n" + audit_output
)
(ROOT / "VERIFICATION.txt").write_text(report)
print(f"Verified {len(expected)} declarations; no additional axioms detected.")
