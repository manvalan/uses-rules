"""Check that the YAML rulesets follow the schema and have unique ids."""
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schema" / "ruleset.schema.json").read_text())
RULE = SCHEMA["$defs"]["rule"]


def rule_errors(rule):
    """Return the errors of a single rule."""
    props = RULE["properties"]
    errors = [f"missing field: {k}" for k in RULE["required"] if k not in rule]
    errors += [f"unknown field: {k}" for k in rule if k not in props]
    for key in ("scope", "metric", "operator", "severity", "applies_to"):
        if key in rule and rule[key] not in props[key]["enum"]:
            errors.append(f"invalid {key}: {rule[key]!r}")
    return errors


def ruleset_errors(path, seen):
    """Return the errors of a ruleset file."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    errors = [f"missing field: {k}" for k in SCHEMA["required"]
              if k not in data]
    for rule in data.get("rules", []):
        rid = rule.get("id", "?")
        errors += [f"{rid}: {e}" for e in rule_errors(rule)]
        if rid in seen:
            errors.append(f"{rid}: duplicate id (also in {seen[rid]})")
        seen[rid] = path.name
    return errors


def main():
    """Validate every ruleset in rules/."""
    seen, failed = {}, False
    for path in sorted((ROOT / "rules").glob("*.yaml")):
        errors = ruleset_errors(path, seen)
        failed = failed or bool(errors)
        status = "OK" if not errors else "ERRORS"
        print(f"{path.name}: {status}")
        for err in errors:
            print(f"  - {err}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
