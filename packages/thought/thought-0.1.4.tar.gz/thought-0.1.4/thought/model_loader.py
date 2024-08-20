import importlib.util
from llama_cpp import Llama


def load_model(model_path, gpu_layers=-1, main_gpu=0, context_size=0, batches=512, threads=512, force_memory=False, embedding=False, verbose=False):
    """
    Loads a model to memory with our recommended defaults
    :param force_memory:
    :param main_gpu:
    :param model_path:
    :param gpu_layers:
    :param context_size:
    :param batches:
    :param threads:
    :param embedding:
    :param verbose:
    :return:
    """

    flash_attn = importlib.util.find_spec("flash_attn")
    found_flash_attn = flash_attn is not None

    llm = Llama(
        model_path=model_path,
        n_gpu_layers=gpu_layers,
        n_ctx=context_size,
        n_batch=batches,
        n_threads=threads,
        verbose=verbose,
        embedding=embedding,
        main_gpu=main_gpu,
        use_mlock=force_memory,
        flash_attn=found_flash_attn
    )

    def thought_embed(self, text):
        return self.create_embedding(text)

    def thought_generate(self, prompt,
                         max_tokens=512,
                         stop=[],
                         temperature=1.0,
                         top_k=10,
                         top_p=0.05,
                         repeat_penalty=1.2,
                         presence_penalty=0.0,
                         frequency_penalty=0.0,
                         seed=-1,
                         call_back=None):
        return generate(self, prompt,
                        max_tokens=512,
                        stop=[],
                        temperature=1.0,
                        top_k=10,
                        top_p=0.05,
                        repeat_penalty=1.2,
                        presence_penalty=0.0,
                        frequency_penalty=0.0,
                        seed=-1,
                        call_back=None)

    llm.thought_embed = thought_embed.__get__(llm)
    llm.thought_generate = thought_generate.__get__(llm)

    return llm

def generate(llm,
             prompt,
             max_tokens=512,
             stop=[],
             temperature=1.0,
             top_k=10,
             top_p=0.05,
             repeat_penalty=1.2,
             presence_penalty=0.0,
             frequency_penalty=0.0,
             seed=-1,
             call_back=None):
    """
    Generate on the llm
    :param llm:
    :param prompt:
    :param max_tokens:
    :param stop:
    :param temperature:
    :param top_k:
    :param top_p:
    :param repeat_penalty:
    :param presence_penalty:
    :param frequency_penalty:
    :param seed:
    :param call_back:
    :return:
    """
    tokens = llm(
        prompt,
        max_tokens=max_tokens,
        stop=stop,
        seed=seed,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        repeat_penalty=repeat_penalty,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
        stream=True,
        echo=False,
    )

    output = ""
    for token in tokens:
        output += token["choices"][0]['text']
        if call_back is not None:
            call_back(token)

    return output

def embed(llm, text):
    """
    Use the model to create a vector embedding of text
    :param llm:
    :param text:
    :return:
    """
    return llm.create_embedding(text)