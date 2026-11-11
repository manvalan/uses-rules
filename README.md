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
| `principles/design.yaml` | 27 design principles from The Pragmatic Programmer, Clean Code, Clean Architecture, Refactoring, Working Effectively with Legacy Code and Code That Fits in Your Head |
| `certification.yaml` | Scoring and stamp levels (Gold, Silver, Bronze) |
| `schema/*.schema.json` | JSON schemas for rulesets and principles, also useful for editor completion |
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
| CC-011 | method | no duplicated function bodies (DRY) | warning |
| CC-012 | file | no commented-out code | info |

## Design principles

The rules above are measured by the certifier. The principles in
`principles/design.yaml` cannot be measured: agents and reviewers apply
them when they write or change code, answer each check question for the
code they touched, and report every case where a principle was not
followed. `measured_by` names the rules that measure part of a
principle. `uses-certifier guide` prints them with summary, how to apply
them and examples.

**Design and structure**

| Id | Principle | Measured by | Check question |
|---|---|---|---|
| DP-001 | DRY - Don't Repeat Yourself | CC-011 | Is any rule, formula or constant I touched written in more than one place? |
| DP-002 | Orthogonality | - | Would replacing the database, the UI or an external service force changes in the code I touched? |
| DP-003 | Don't live with broken windows | CC-010, CC-012 | Did I leave any hack, dead code, commented-out code or known problem behind? |
| DP-004 | Tracer bullets and walking skeleton | - | Does the feature I am building already run end to end, even if it does very little? |
| DP-005 | Fractal architecture | CTF-008, CTF-009 | Can someone understand each level I touched without reading the level below? |
| DP-006 | Functional core, imperative shell | - | Does any business decision in my code also perform I/O? |
| DP-007 | Command Query Separation | - | Does any method I wrote both change state and return a value? |
| DP-008 | Parse, don't validate | - | Does my core logic receive raw strings or dicts that it has to check again? |
| DP-009 | Objects protect their invariants | - | Can a caller put one of my objects into an invalid state? |

**Writing and readability**

| Id | Principle | Measured by | Check question |
|---|---|---|---|
| DP-010 | Intention-revealing names | - | If I hide every body, do the names alone explain what the code does? |
| DP-011 | Small functions that do one thing, at one level of abstraction | CTF-001, CTF-003, CTF-006, CTF-007 | Does any function I wrote mix high-level steps with low-level details? |
| DP-012 | Code as documentation | CC-012 | Does any comment I wrote repeat what the code already says? |
| DP-013 | The Boy Scout rule | - | Is every file I touched at least as clean as before, ideally cleaner? |
| DP-014 | Tell, don't ask (Law of Demeter) | - | Did I write chains of getters or decide things using another object's internal data? |
| DP-015 | Explicit error handling | CC-005 | Can any failure in my code be silently ignored or confused with a valid result? |

**Architecture and dependencies**

| Id | Principle | Measured by | Check question |
|---|---|---|---|
| DP-016 | Single responsibility | CC-007, CC-008 | Is there more than one reason for the classes I changed to change? |
| DP-017 | Dependencies point inward | - | Does any domain module I touched import infrastructure or framework code? |
| DP-018 | Explicit dependencies | - | Does my code reach for a global, a singleton or the environment instead of receiving it? |
| DP-019 | Composition over inheritance | - | Did I add a subclass where passing a collaborator would do? |

**Continuous improvement**

| Id | Principle | Measured by | Check question |
|---|---|---|---|
| DP-020 | The two hats | - | Does any of my commits both restructure code and change its behaviour? |
| DP-021 | Small, verifiable steps | - | Could each of my steps be reverted on its own with the build still green? |
| DP-022 | Recognise code smells | CTF-003, CTF-006, CTF-008, CC-007, CC-011 | Which smells remain in the code I touched, and why did I leave them? |
| DP-023 | Rule of three | - | Did I copy something a third time, or merge code that changes for different reasons? |

**Safety and maintenance**

| Id | Principle | Measured by | Check question |
|---|---|---|---|
| DP-024 | Tests before changes | - | Was the code I changed covered by tests before I changed it? |
| DP-025 | Find and use seams | - | Could I test the code I touched without its real external dependencies? |
| DP-026 | Characterization tests | - | Before changing legacy code, did I pin its current behaviour with tests? |
| DP-027 | Tests first, outside-in | - | Is every behaviour I added or changed covered by a test that failed without my change? |

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
| `duplicate_count` | function | all (functions of 6+ lines; Python compared on the syntax tree) |
| `commented_code_lines` | module | Python |
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

1. Edit the right ruleset YAML file, or add a new one in `rules/`
   (measurable rules) or `principles/` (design principles).
2. Run `python scripts/validate.py`.
3. Bump the ruleset `version` and open a pull request.

A project can tune thresholds without touching this repository through the
`.uses-certifier.yaml` file described in the certifier README.
