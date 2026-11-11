"""Controlla che i ruleset YAML rispettino lo schema e abbiano id unici."""
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schema" / "ruleset.schema.json").read_text())
RULE = SCHEMA["$defs"]["rule"]


def rule_errors(rule):
    """Restituisce gli errori di una singola regola."""
    props = RULE["properties"]
    errors = [f"campo mancante: {k}" for k in RULE["required"] if k not in rule]
    errors += [f"campo sconosciuto: {k}" for k in rule if k not in props]
    for key in ("scope", "metric", "operator", "severity", "applies_to"):
        if key in rule and rule[key] not in props[key]["enum"]:
            errors.append(f"{key} non valido: {rule[key]!r}")
    return errors


def ruleset_errors(path, seen):
    """Restituisce gli errori di un file di ruleset."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    errors = [f"campo mancante: {k}" for k in SCHEMA["required"]
              if k not in data]
    for rule in data.get("rules", []):
        rid = rule.get("id", "?")
        errors += [f"{rid}: {e}" for e in rule_errors(rule)]
        if rid in seen:
            errors.append(f"{rid}: id duplicato (anche in {seen[rid]})")
        seen[rid] = path.name
    return errors


def main():
    """Valida tutti i ruleset in rules/."""
    seen, failed = {}, False
    for path in sorted((ROOT / "rules").glob("*.yaml")):
        errors = ruleset_errors(path, seen)
        failed = failed or bool(errors)
        status = "OK" if not errors else "ERRORI"
        print(f"{path.name}: {status}")
        for err in errors:
            print(f"  - {err}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
