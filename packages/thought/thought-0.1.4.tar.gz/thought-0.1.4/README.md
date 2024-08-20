# thought
Thought is a light wrapper for llama cpp, the building block for implementing and managing an efficient LLM integration

## Installation

```bash
pip install thought
```

## Get started quickly

### Imports

The following imports cover all the functionality of loading, embedding and generating
```python
# loader
from thought.model_loader import load_model
from thought.model_loader import generate
from thought.model_loader import embed

# downloader
from thought.model_downloader import get_models
from thought.model_downloader import download_model
from thought.model_downloader import add_model
```

### Downloading a model to play with

The following code shows you how to download models, especially useful when hot deploying to dockers and you need your code to download the models for runtime.

```python
# gets a bunch of models, set to true to download a bunch of models - not recommended!
get_models(use_verified=False)
# add a specific model - right click copy link of GGUF from hugging face
add_model("https://huggingface.co/mradermacher/DarkIdol-Llama-3.1-8B-Instruct-1.2-Uncensored-i1-GGUF/resolve/main/DarkIdol-Llama-3.1-8B-Instruct-1.2-Uncensored.i1-Q4_K_M.gguf")
add_model("https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF/blob/main/nomic-embed-text-v1.5.Q4_K_M.gguf")
# download the added models
download_model("DarkIdol-Llama-3.1-8B-Instruct-1.2-Uncensored", "i1-Q4_K_M")
download_model("nomic-embed-text-v1.5", "Q4_K_M")
```

### Embedding text with a model

The flag `embedding=True` needs to be on!

```python
llm = load_model("./model_db/nomic-embed-text-v1.5.Q4_K_M.gguf", verbose=True, embedding=True)
text = "I think therefore I am"

vectors = embed(llm, text)
# or
vectors = llm.thought_embed(text)


print(vectors)
```

### Generating text from the LLM

Please note we do not do any weird prompt templating or black boxing on your input prompt. You need to look at the model 
and provide the prompt with the correct "tokens" in your prompt.

```python
llm = load_model("./model_db/DarkIdol-Llama-3.1-8B-Instruct-1.2-Uncensored-Q4_K_S-imat.gguf", verbose=True, embedding=False)

text = "I think therefore I am"

response = generate(llm, "Explain this text<|eot_id|>User:"+text+"<|eot_id|>AI:", stop=["\n"], seed=123456, call_back=token_stream)
#or
response = llm.thought_generate("Explain this text<|eot_id|>User:"+text+"<|eot_id|>AI:", stop=["\n"], seed=123456, call_back=token_stream)

print(response)
```

## Developing

First create a virtual environment on Python 11 or higher

### Windows
```
python -m venv .venv
.\.venv\Scripts\activate
pip install poetry
poetry install
```

### GPU support (Cuda)
llama-cpp-python seems not to build with CUDA support on Windows or Linux by default. Here are the basic commands we end up running each time we install.

#### Windows
Please replace the CUDA version with your version you have on your disk.
```powershell
$env:CMAKE_ARGS="-DGGML_CUDA=on"   
$env:CUDACXX="C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin\nvcc.exe"
poetry run pip install llama-cpp-python --no-cache-dir --force-reinstall --upgrade --verbose
```

#### Linux
```bash
CUDACXX=/usr/local/cuda-12/bin/nvcc CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_CUDA_ARCHITECTURES=all-major" poetry run pip install llama-cpp-python --no-cache --force-reinstall --upgrade --verbose
```

## Build
```
poetry build
python -m twine upload --repository pypi dist/*
```

