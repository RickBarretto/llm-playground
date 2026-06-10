# LLM Playground

This repository aims to quickly test some AI models using Collab.

## How to use it

On [play.ipynb](https://colab.research.google.com/github/RickBarretto/llm-playground/blob/main/play.ipynb) click on "Open in Collab",
modify as you need and have fun!

### Google Colab

Use a GPU runtime before loading a model: `Runtime` -> `Change runtime type` -> `T4 GPU` or better.

To test any branch or tag in Colab, set `GIT_REF` to the branch or tag name you want. For example: `"main"`, `"api-v2"`, `"v1.0.0"`.

```python
GIT_REF = "api-v2"  # branch or tag

!rm -rf /content/llm-playground
!git clone https://github.com/RickBarretto/llm-playground /content/llm-playground
%cd /content/llm-playground
!git fetch --all --tags
!git checkout $GIT_REF
!pip install -U /content/llm-playground
```

Minimal `ask()` test:

```python
from pathlib import Path
from ricklm import models

model = models.AmadeusVerbo("3B")

with model as m:
    output = m.ask("Escreva uma frase curta sobre o Brasil.")
    print(output)
    Path("/content/ask.txt").write_text(output, encoding="utf-8")
```

Minimal `chat()` test:

```python
from pathlib import Path
from ricklm import models

model = models.AmadeusVerbo("3B")

with model as m:
    history = m.chat([
        "Escreva uma frase sobre o Brasil.",
        "Agora transforme essa frase em um verso.",
    ])

    print(history[-1])
    print(history[-1].ai)
    print(history.last.ai)
    Path("/content/chat-last.txt").write_text(history[-1], encoding="utf-8")
```

### Prompts

You may have noticed the file [`prompts/`](https://github.com/RickBarretto/llm-playground/tree/main/prompts),
this folder includes the prompts that we pass to the test subjects and also judges models.

The json files are passed to our target models, so they can generate what we want.
The markdown files are passed to our judge models, and we pass the target's outputs and inputs.

### Evaluations

Here is where you'll find the output and the evaluation made by judge models.
This has the following structure: `evaluations/:scope/:model/`.

**Input**

`prompt.txt` represents the exact prompt passed to the target model
to generate the output.

**Output**

Output files follows this pattern: `:n.txt`, where `:n` is the iteration.
This represents a direct output from the model, without any modification.

**Evaluation**

The evaluation files are stored as structured json. 
This follows the following pattern: `:n.:eval.:judge-model.json`,
where `:n` refers to the iteration, 
`:eval` the evaluation prompt that is found at `prompts/*.md`,
and `:judge-model`, the model used for this evaluation.

## RickLM

`ricklm` is the minimal wrapper the notebook installs to run a few PT-BR friendly models and simple generation tasks.

The reason why this exists is to avoid mistyping or mismatching package versions.

For instance, the code above is too error prone, since I can type anything:

```python
pipeline("text-generator", "owner/ai-model-7b-instruct")
```

But using a model API I have a code/type oriented interface that minimizes those errors:

```python
from ricklm import models

model = models.AmadeusVerbo("3B")
```

Ask returns the model answer as normalized UTF-8 text. It is a `str`, so printing or writing it to disk does not expose JSON or Python objects:

```python
from ricklm import models

model = models.AmadeusVerbo("3B")

with model as m:
    output = m.ask("Meu prompt")
    print(output)
```

For an interactive chat, type `sair`, `exit`, or `quit` to finish. Each message is also a `str`:

```python
with model as m:
    for output in m.chat():
        print(output)
```

`chat()` renders each message naturally:

```text
Usuário:

Meu prompt

Amadeus-Verbo-FI-Qwen2.5-3B-PT-BR-Instruct:

Resposta do modelo
```

For scripted prompts, `chat()` behaves like a lazy history. `history[-1]` renders only the last user/model turn, and `history[-1].ai` or `history.last.ai` returns only the model answer:

```python
with model as m:
    history = m.chat(["Meu prompt"])
    print(history[-1])
    print(history[-1].ai)
    print(history.last.ai)
```

### Steps

1. Install `ricklm`
2. Choose a model families and its size.
3. Run `ask()` or `chat()`.
4. Upload back to Github if you wish
5. Clean the runtime for reuse


## Versioning

This repository contains two different things that evolve at different speeds:

1. The `ricklm` Python API.
2. The research artifacts produced with that API, such as prompts, generated outputs, poems, and evaluations.

Because of that, tags use different prefixes depending on what is being versioned.

### API versions

API releases use semantic versioning and are tagged with a `v` prefix:

```text
v1.0.0
v1.1.0
v2.0.0
```

These tags refer to the `ricklm` package interface: model classes, method names, return types, task helpers, and installation behavior.

Use an API tag when you need stable code behavior. For example, in Colab:

```python
GIT_REF = "v2.0.0"
```

Semantic versioning means:

- `MAJOR`: breaking API changes, such as replacing one public API with another.
- `MINOR`: backward-compatible features, such as adding a new model wrapper.
- `PATCH`: backward-compatible fixes, such as bug fixes or documentation corrections.

### Research steps

Research/data releases are tagged with an `s` prefix:

```text
s1
s2
s3
```

These tags refer to research milestones, not package stability. A step may include new prompts, generated outputs, evaluation files, notebook changes, or a specific snapshot of an experiment.

Research steps are intentionally not semantic-versioned. They are ordered checkpoints in the research process, created when the experiment meaningfully changes or when a result should be preserved.

Use a step tag when you want to reproduce a specific experiment snapshot:

```python
GIT_REF = "s3"
```

### Branches

Branches are for work in progress:

```text
main
api-v2
experiment/new-prompts
```

Use a branch in Colab when testing ongoing work:

```python
GIT_REF = "api-v2"
```

Branches may change over time. If you need reproducibility, prefer a `v*` API tag or an `s*` research step tag.

### Rule of thumb

- Use `v*` tags to pin the `ricklm` API.
- Use `s*` tags to pin research artifacts and experiment snapshots.
- Use branches only while developing or testing unfinished changes.
