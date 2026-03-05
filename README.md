# LLM Playground

This repository aims to quickly test some AI models using Collab.

## How to use it

On [play.ipynb](play.ipynb) click on "Open in Collab",
modify as you need and have fun!

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
4. Upload back to Github if you wish
5. Clean the runtime for reuse
