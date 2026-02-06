# LLM Playground

This repository aims to quickly test some AI models using Collab.

## How to use it

On [play.ipynb](play.ipynb) click on "Open in Collab",
modify as you need and have fun!

### Prompts

You may have noticed the file [`prompts/`](https://github.com/RickBarretto/llm-playground/tree/main/prompts),
this folder includes the output given by each model depending on the questions I do.

Feel free to open any of them to see how each model responds to the same prompt.

## RickLM

`ricklm` is the minimal wrapper the notebook installs to run a few PT-BR friendly models and simple generation tasks.

The reason why this exists is to avoid mistyping or mismatching package versions.

For instance, the code above is too error prone, since I can type anything:

```python
pipeline("text-generator", "owner/ai-model-7b-instruct")
```

But using a DSL I have a code/type oriented interface that minimizes those errors:

```python
model = AmadeusVerbo(size="7B") # 7B is a Literal with fixed options
poem = Poem(by=model, style="Gregório de Matos")
...
```

### Steps

1. Install `ricklm`
2. Choose a model families and its size.
3. Run some task, like poem generation via `Poem`
4. Clean the runtime for reuse
