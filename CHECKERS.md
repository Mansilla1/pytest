# Cyclomatic Complexity Tools

## tl;dr

|         |  being maintained |  pre-commit hook |  good documentation |  easy/simple to set up |  report file | current version | recommendation |
|---------|-------------------|-------------------------|---------------------|------------------------|--------------|-----------------| -----------------|
|    [Wily](https://github.com/tonybaloney/wily) |         ❌        |            ❌           |          ✅         |           ❌           |      ❌      |      1.25.0     | 😨 |
|   [Radon](https://github.com/rubik/radon) |         ✅        |     ✅ (using [xenon](https://github.com/rubik/xenon))    |          ❌         |           ✅           |      ✅      |      6.0.1      | 😁 |
| [Vulture](https://github.com/jendrikseipp/vulture) |         ✅        |            ✅           |          ✅         |           ✅           |      ❌      |       2.14      | 😄 |
|  [Lizard](https://github.com/terryyin/lizard) |         ✅        |            ❌           |          ✅         |           ✅           |      ✅      |     1.17.19     | 😄 |
|  [Pylint](https://github.com/pylint-dev/pylint) |         ✅        |            ❌           |          ✅         |           ✅           |      ✅      |      3.3.4      | 🙂 |

## Tools

### Wily
> A command-line application for tracking, reporting on complexity of Python tests and applications.

```bash
# installing
poetry add --group checkers wily

# using
# note: make sure there are no uncommitted changes.
poetry run wily build src/ -n 100
poetry run wily diff --detail src/
poetry run wily report src/ --format HTML
```

#### pros
- Detailed Cyclomatic Complexity (CC), and more information for each changes (commits history)
- It is possible to generate the report file, but in order for the command to "stop" the pipeline we must first use the `wily diff` command and then `wily report`; or just redirect the output of the first command to a file. It won't be as detailed as the report but it might be enough.

#### cons
- Apparently it is no longer being maintained (last release was Oct 11, 2023)
- A bit more difficult to understand at first
- It doesn't have a pre-commit hook, but there is a config example in the documentation
- The way to generate the final report file as an artifact is not so simple.

#### pre-commit config

```yaml
repos:
  - repo: local
    hooks:
    - id: wily
      name: wily
      entry: poetry run wily diff --detail
      verbose: true
      language: python
      additional_dependencies: [wily]
```

#### pipeline config

```yaml
jobs:
  lint:
    - name: Wily
      # run: poetry run wily diff --detail src/ | tee wily-report.txt
      run: poetry run wily diff --detail src/ && \
      poetry run wily report src/ --format HTML
```

### Radon (with Xenon)
> Radon is a Python tool that computes various metrics from the source code. Radon can compute:
>
> - McCabe's complexity, i.e. cyclomatic complexity
> - raw metrics (these include SLOC, comment lines, blank lines, &c.)
> - Halstead metrics (all of them)
> - Maintainability Index (the one used in Visual Studio)

```bash
# installing
poetry add --group checkers radon[toml] # it's required to configure Radon from pyproject.toml file

# using
poetry run radon cc  \ # compute Cyclomatic Complexity
  -a \     # calculate the average complexity at the end
  -nc \    # only results with a complexity rank of C or worse
  --json \ # results will be converted into JSON
  --output-file "radon-report.json"
  src/
```

<br>

> Xenon is a monitoring tool based on Radon. It monitors your code's complexity. Ideally, Xenon is run every time you commit code. Through command line options, you can set various thresholds for the complexity of your code. It will fail (i.e. it will exit with a non-zero exit code) when any of these requirements is not met.

```bash
# installing
poetry add --group checkers xenon

# using
poetry run xenon src/
```

| **CC Score** | **Rank** | **Risk** |
|-------------|--------|---------------------------------|
| 🟩 **1 - 5** | **A** | Low - Simple block |
| 🟩 **6 - 10** | **B** | Low - Well structured and stable block |
| 🟨 **11 - 20** | **C** | Moderate - Slightly complex block |
| 🟧 **21 - 30** | **D** | More than moderate - More complex block |
| 🟥 **31 - 40** | **E** | High - Complex block, alarming |
| 🟥 **41+** | **F** | Very high - Error-prone, unstable block |

#### pros
- pre-commit hook already defined
- Radon can be used with .ipynb files to inspect code metrics for Python cells.
- The settings can be defined in the file `pyproject.toml`

#### cons
- The documentation isn't as helpful as it should be, and it's missing some parts.
- Xenon is just a Radon wrapper, but we don't have access to its commands/parameters.
- The way to generate the final report file as an artifact is not so simple, because it's Xenon that runs the pipeline and Radon that generates the report; or just redirect the output of Xenon command to a file. It won't be as detailed as the report but it might be enough.

#### pre-commit config
```yaml
repos:
  - repo: https://github.com/rubik/xenon
    rev: v0.9.0
    hooks:
    - id: xenon
```

#### pipeline config

```yaml
jobs:
  lint:
    - name: Xenon
      run: poetry run xenon src/
```

### Vulture

> Vulture finds unused code in Python programs. This is useful for cleaning up and finding errors in large code bases. If you run Vulture on both your library and test suite you can find untested code.
>
> Due to Python's dynamic nature, static code analyzers like Vulture are likely to miss some dead code. Also, code that is only called implicitly may be reported as unused. Nonetheless, Vulture can be a very helpful tool for higher code quality.

Confidence values are based on the next tables:

| Code type | Confidence value |
| ------------------- | -- |
| function/method/class argument, unreachable code | 100% |
| import | 90% |
| attribute, class, function, method, property, variable | 60% |

```bash
# installing
poetry add --group checkers vulture

# using
poetry run vulture src/ --min-confidence 90
```

#### pros
- pre-commit hook already defined
- It's a great COMPLEMENTARY tool.
- The settings can be defined in the file `pyproject.toml`

#### cons
- it's not a tool for complexity focused, but for finding dead/unused code, but in the end one thing helps the other.

#### pre-commit config

```yaml
repos:
  - repo: https://github.com/jendrikseipp/vulture
    rev: 'v2.3'
    hooks:
      - id: vulture
        args: ["src"]
```

#### pipeline config

```yaml
jobs:
  lint:
    - name: Vulture
      run: poetry run vulture src/
```

#### pyproject.toml config
```yaml
[tool.vulture]
ignore_decorators = ["@router.*"]
paths = ["src"]
min_confidence = 90
```

### Lizard

> Lizard is an extensible Cyclomatic Complexity Analyzer for many programming languages including C/C++ (doesn't require all the header files or Java imports). It also does copy-paste detection (code clone detection/code duplicate detection) and many other forms of static code analysis.

```bash
# installing
poetry add --group checkers lizard

# using
poetry run lizard -l python --output_file lizard-report.html src/
poetry run lizard -Eduplicate -l python --output_file lizard-duplicated-report.html src/ # Code Duplicate Detector
```

| **Metric**       | **What it Measures**               | **Interpretation**                              |
|-----------------|---------------------------------|--------------------------------|
| **NLOC**        | Actual lines of code           | Higher = harder to read |
| **CCN**         | Cyclomatic complexity          | >10 is a warning, >15 is critical |
| **token**       | Function tokens                | More tokens = more code to process |
| **PARAM**       | Function parameters            | >5 parameters may indicate poor design |
| **length**      | Total function length          | >100 lines is hard to maintain |
| **Warning cnt** | Warnings found                 | >0 indicates problematic functions |

#### pros
- supports several other programming languages besides Python.

#### cons
- It doesn't have a pre-commit hook
- Lizard requires syntactically correct code. Upon processing input with incorrect or unknown syntax:
  - Lizard guarantees to terminate eventually (i.e., no forever loops, hangs) without hard failures (e.g., exit, crash, exceptions).
  - There is a chance of a combination of the following soft failures:
    - omission
    - misinterpretation
    - improper analysis / tally
    - success (the code under consideration is not relevant, e.g., global macros in C)
- This approach makes the Lizard implementation simpler and more focused with partial parsers for various languages. Developers of Lizard attempt to minimize the possibility of soft failures. Hard failures are bugs in Lizard code, while soft failures are trade-offs or potential bugs.

#### pre-commit config

```yaml
repos:
  - repo: local
    hooks:
    - id: lizard
      name: lizard
      entry: poetry run lizard src/
      verbose: true
      language: python
      additional_dependencies: [lizard]
```

#### pipeline config

```yaml
jobs:
  lint:
    - name: Lizard
      run: poetry run lizard -l python --output_file lizard-report.html src/
```

### Pylint - Design Checker

> Pylint is a static code analyser for Python 2 or 3. The latest version supports Python 3.9.0 and above.
>
>  Pylint analyses your code without actually running it. It checks for errors, enforces a coding standard, looks for code smells, and can make suggestions about how the code could be refactored.

<br>

> Design Checker is provided by `pylint.extensions.mccabe`.
> You can now use this plugin for finding complexity issues in your code base.

```bash
# installing
poetry add --group checkers pylint

# using
# note: enable Design Checker
poetry run pylint src/ --enable=design
poetry run pylint src/ --load-plugins=pylint.extensions.mccabe
```

#### pros
- It's a tool that is already part of some of our projects.

#### cons
- It doesn't have a pre-commit hook, but there is a config example in the documentation

#### pre-commit config

```yaml
repos:
  - repo: local
    hooks:
    - id: pylint
      name: pylint
      entry: poetry run pylint src/ --enable=design
      language: system
      types: [python]
```

#### pipeline config

```yaml
jobs:
  lint:
    - name: Pylint
      run: poetry run pylint src/ --enable=design
```