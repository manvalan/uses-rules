# uses-rules

Regole di qualità del codice usate da
[uses-certifier](https://github.com/manvalan/uses-certifier) per bollinare
ogni metodo, classe e sorgente che produciamo.

Le regole sono scritte in YAML, una per voce, così si leggono, si discutono
in code review e si versionano come il codice.

## Contenuto

| File | Cosa contiene |
|---|---|
| `rules/ctfiyh.yaml` | Regole da *Code That Fits in Your Head* (Mark Seemann): regola del sette, regola 80/24, oggetti attivati, annidamento |
| `rules/clean-code.yaml` | Regole da *Clean Code* (Robert C. Martin), PEP 8 e PEP 257 |
| `certification.yaml` | Punteggio e livelli del bollino (Oro, Argento, Bronzo) |
| `schema/ruleset.schema.json` | Schema JSON dei ruleset, utile anche per l'autocompletamento nell'editor |
| `scripts/validate.py` | Controllo dei ruleset, eseguito in CI a ogni push |

## Riepilogo delle regole

| Id | Ambito | Regola | Gravità |
|---|---|---|---|
| CTF-001 | metodo | complessità ciclomatica ≤ 7 | error |
| CTF-002 | metodo | oggetti attivati ≤ 7 | warning |
| CTF-003 | metodo | lunghezza ≤ 24 righe | error |
| CTF-004 | metodo | righe ≤ 80 caratteri | warning |
| CTF-005 | sorgente | righe ≤ 80 caratteri | warning |
| CTF-006 | metodo | parametri ≤ 4 | warning |
| CTF-007 | metodo | annidamento ≤ 3 | warning |
| CTF-008 | classe | metodi ≤ 12 | warning |
| CTF-009 | classe | complessità totale ≤ 49 | warning |
| CC-001 | metodo | parametri ≤ 3 | info |
| CC-002 | metodo | nessun parametro booleano | warning |
| CC-003 | metodo | docstring sulle funzioni pubbliche | info |
| CC-004 | classe | docstring sulle classi pubbliche | info |
| CC-005 | metodo | nessun `except:` generico | error |
| CC-006 | metodo | return ≤ 4 | info |
| CC-007 | classe | lunghezza ≤ 300 righe | warning |
| CC-008 | classe | campi ≤ 7 | warning |
| CC-009 | sorgente | lunghezza ≤ 500 righe | warning |
| CC-010 | sorgente | nessun TODO / FIXME / XXX | info |

## Formato di una regola

```yaml
- id: CTF-001                     # univoco, PREFISSO-NNN
  name: cyclomatic-complexity
  title: Complessità ciclomatica al massimo 7
  scope: function                 # function | class | module
  metric: cyclomatic_complexity   # metrica calcolata dal certificatore
  operator: "<="                  # <= < >= > == !=
  threshold: 7
  severity: error                 # error | warning | info
  applies_to: all                 # all (predefinito) | public
  languages: [python]             # facoltativo: limita la regola ad alcuni linguaggi
  enabled: true                   # facoltativo
  source: "cap. 7.2 - La regola del sette"
  rationale: Perché la regola esiste.
```

### Metriche disponibili

| Metrica | Ambito | Linguaggi |
|---|---|---|
| `cyclomatic_complexity` | function | tutti |
| `length_lines` | function, class, module | tutti |
| `max_line_width` | function, module | tutti |
| `parameter_count` | function | tutti |
| `method_count`, `weighted_complexity` | class | tutti |
| `todo_count` | module | tutti |
| `activated_objects`, `max_nesting`, `return_count`, `boolean_parameters`, `bare_except_count`, `has_docstring` | function | Python |
| `field_count`, `has_docstring` | class | Python |

"Tutti" indica i linguaggi letti tramite [lizard](https://github.com/terryyin/lizard):
C, C++, C#, Java, JavaScript, TypeScript, Go, Rust, Kotlin, Swift, PHP,
Ruby, Scala, Lua e altri. Python viene analizzato con l'AST, che dà metriche
più precise.

## Livelli del bollino

Ogni elemento parte da 100 punti e perde 20 punti per ogni error, 7 per ogni
warning e 2 per ogni info. Poi riceve il primo livello che soddisfa:

| Livello | Punteggio minimo | Error | Warning |
|---|---|---|---|
| Oro | 95 | 0 | 0 |
| Argento | 80 | 0 | qualsiasi |
| Bronzo | 60 | 0 | qualsiasi |
| Non certificato | | | |

Una classe vale quanto il peggiore tra lei e i suoi metodi, un sorgente quanto
il peggiore tra lui e tutto ciò che contiene.

## Aggiungere o cambiare una regola

1. Modificare il file YAML del ruleset giusto, oppure aggiungerne uno nuovo in `rules/`.
2. Eseguire `python scripts/validate.py`.
3. Alzare `version` del ruleset e aprire una pull request.

Un progetto può adattare le soglie senza toccare questo repository, con il
file `.uses-certifier.yaml` descritto nel README del certificatore.
