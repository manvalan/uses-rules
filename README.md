# uses-rules

Code quality rules used by
[uses-certifier](https://github.com/manvalan/uses-certifier) to stamp every
method, class and source file we produce.

Rules are written in YAML, one entry per rule, so they can be read,
discussed in code review and versioned like code.

## Contents

| File | What it holds |
|---|---|
| `rules/ctfiyh.yaml` | Rules from *Code That Fits in Your Head* (Mark Seemann): rule of seven, 80/24 rule, activated objects, nesting |
| `rules/clean-code.yaml` | Rules from *Clean Code* (Robert C. Martin), PEP 8 and PEP 257 |
| `certification.yaml` | Scoring and stamp levels (Gold, Silver, Bronze) |
| `schema/ruleset.schema.json` | JSON schema for rulesets, also useful for editor completion |
| `scripts/validate.py` | Ruleset checker, run in CI on every push |

## Rule summary

| Id | Scope | Rule | Severity |
|---|---|---|---|
| CTF-001 | method | cyclomatic complexity ≤ 7 | error |
| CTF-002 | method | activated objects ≤ 7 | warning |
| CTF-003 | method | length ≤ 24 lines | error |
| CTF-004 | method | lines ≤ 80 characters | warning |
| CTF-005 | file | lines ≤ 80 characters | warning |
| CTF-006 | method | parameters ≤ 4 | warning |
| CTF-007 | method | nesting ≤ 3 | warning |
| CTF-008 | class | methods ≤ 12 | warning |
| CTF-009 | class | total complexity ≤ 49 | warning |
| CC-001 | method | parameters ≤ 3 | info |
| CC-002 | method | no boolean parameters | warning |
| CC-003 | method | docstring on public functions | info |
| CC-004 | class | docstring on public classes | info |
| CC-005 | method | no bare `except:` | error |
| CC-006 | method | returns ≤ 4 | info |
| CC-007 | class | length ≤ 300 lines | warning |
| CC-008 | class | fields ≤ 7 | warning |
| CC-009 | file | length ≤ 500 lines | warning |
| CC-010 | file | no TODO / FIXME / XXX | info |

## Rule format

```yaml
- id: CTF-001                     # unique, PREFIX-NNN
  name: cyclomatic-complexity
  title: Cyclomatic complexity of at most 7
  scope: function                 # function | class | module
  metric: cyclomatic_complexity   # metric computed by the certifier
  operator: "<="                  # <= < >= > == !=
  threshold: 7
  severity: error                 # error | warning | info
  applies_to: all                 # all (default) | public
  languages: [python]             # optional: restrict to some languages
  enabled: true                   # optional
  source: "ch. 7.2 - The rule of seven"
  rationale: Why the rule exists.
```

### Available metrics

| Metric | Scope | Languages |
|---|---|---|
| `cyclomatic_complexity` | function | all |
| `length_lines` | function, class, module | all |
| `max_line_width` | function, module | all |
| `parameter_count` | function | all |
| `method_count`, `weighted_complexity` | class | all |
| `todo_count` | module | all |
| `activated_objects`, `max_nesting`, `return_count`, `boolean_parameters`, `bare_except_count`, `has_docstring` | function | Python |
| `field_count`, `has_docstring` | class | Python |

"All" means the languages read through
[lizard](https://github.com/terryyin/lizard): C, C++, C#, Java, JavaScript,
TypeScript, Go, Rust, Kotlin, Swift, PHP, Ruby, Scala, Lua and more. Python
is analysed through its AST, which gives more precise metrics.

## Stamp levels

Every element starts at 100 points and loses 20 points per error, 7 per
warning and 2 per info. It then receives the first level it satisfies:

| Level | Minimum score | Errors | Warnings |
|---|---|---|---|
| Gold | 95 | 0 | 0 |
| Silver | 80 | 0 | any |
| Bronze | 60 | 0 | any |
| Not certified | | | |

A class is worth the worst of itself and its methods, a source file the
worst of itself and everything it contains.

## Adding or changing a rule

1. Edit the right ruleset YAML file, or add a new one in `rules/`.
2. Run `python scripts/validate.py`.
3. Bump the ruleset `version` and open a pull request.

A project can tune thresholds without touching this repository through the
`.uses-certifier.yaml` file described in the certifier README.
