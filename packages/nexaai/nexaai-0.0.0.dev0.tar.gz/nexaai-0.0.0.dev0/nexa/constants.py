import os
from pathlib import Path

NEXA_CACHE_ROOT = Path(os.getenv("NEXA_CACHE_ROOT") or "~/.cache/nexa").expanduser()
NEXA_TOKEN_PATH = NEXA_CACHE_ROOT / "token"
NEXA_MODELS_HUB_DIR = NEXA_CACHE_ROOT / "hub"
NEXA_MODELS_HUB_OFFICIAL_DIR = NEXA_MODELS_HUB_DIR / "official"
NEXA_MODEL_LIST_PATH = NEXA_MODELS_HUB_DIR / "model_list.json"
NEXA_API_URL = "https://model-hub-backend.nexa4ai.com"
NEXA_OFFICIAL_BUCKET = "https://public-storage.nexa4ai.com/"

NEXA_LOGO = """
      _|    _|  _|_|_|  _|    _|    _|_|      _|_|    _|_|_|_|
      _|_|  _|  _|       _|  _|   _|    _|  _|    _|     _|
      _|_|_|_|  _|_|_|     _|     _|_|_|_|  _|_|_|_|     _|
      _|  _|_|  _|        _| _|   _|    _|  _|    _|     _|
      _|    _|  _|_|_|  _|    _|  _|    _|  _|    _|  _|_|_|_|
"""
# Maokun TODO: Update the model info and find a good default precision for each model

PRODUCER_INFO = dict(
    # producer_name="nexa.ai",  # onnxruntime: Model producer not matched: Expected "pytorch"
    producer_version="0.0.0",
    doc_string="Model exported by Nexa.ai",
)

NEXA_RUN_MODEL_MAP_TEXT = {
    "octopus-v2": "Octopus-v2:q4_0",
    "octopus-v4": "Octopus-v4:q4_0",
    "gpt2": "gpt2:q4_0",
    "tinyllama": "TinyLlama-1.1B-Chat-v1.0:fp16",
    "llama2": "Llama-2-7b-chat:q4_0",
    "llama3": "Meta-Llama-3-8B-Instruct:q4_0",
    "llama3.1": "Meta-Llama-3.1-8B-Instruct:q4_0",
    "gemma": "gemma-1.1-2b-instruct:q4_0",
    "gemma2": "gemma-2-2b-instruct:q4_0",
    "qwen1.5": "Qwen1.5-7B-Instruct:q4_0",
    "qwen2": "Qwen2-1.5B-Instruct:q4_0",
    "mistral": "Mistral-7B-Instruct-v0.3:q4_0",
    "codegemma": "codegemma-2b:q4_0",
    "codellama": "CodeLlama-7b-Instruct:q4_0",
    "codeqwen": "CodeQwen1.5-7B-Instruct:q4_0",
    "deepseek-coder": "deepseek-coder-1.3b-instruct:q4_0",
    "dolphin-mistral": "dolphin-2.8-mistral-7b:q4_0",
    "nomic-embed-text": "nomic-embed-text-v1.5:fp16",
    "phi2": "Phi-2:q4_0",
    "phi3": "Phi-3-mini-128k-instruct:q4_0",
}

NEXA_RUN_MODEL_MAP_ONNX = {
    "gpt2": "gpt2:onnx-cpu-int8",
    "phi3": "Phi-3-mini-4k-instruct:onnx-cpu-int4",
    "llama2": "Llama-2-7b-chat:onnx-cpu-int8",
    "llama3": "Meta-Llama-3-8B-Instruct:onnx-cpu-int8",
    "llama3.1": "Meta-Llama-3.1-8B-Instruct:onnx-cpu-int8",
    "qwen2": "Qwen2-1.5B-Instruct:onnx-cpu-int8",
    "gemma": "gemma-2b-instruct:onnx-cpu-int8",
    "gemma1.1": "gemma-1.1-2b-instruct:onnx-cpu-int8",
    "mistral": "Mistral-7B-Instruct-v0.3:onnx-cpu-int8",
    "phi3v": "Phi-3-vision-128k-instruct:onnx-cpu-int4",
    "sd1-5": "stable-diffusion-v1-5:onnx-cpu-fp32",
    "lcm-dreamshaper": "lcm-dreamshaper-v7:onnx-cpu-fp32",
    "whisper": "whisper-tiny.en:onnx-cpu-fp32",
    "ljspeech": "ljspeech-jets:onnx-cpu-fp32",
}

NEXA_RUN_MODEL_MAP_VLM = {
    "nanollava": "nanoLLaVA:model-fp16",
    "llava-phi3": "llava-phi-3-mini:model-q4_0",
    # "llava1.5": "/usr/share/ollama/.ollama/models/blobs/sha256-170370233dd5c5415250a2ecd5c71586352850729062ccef1496385647293868",
    "llava-llama3": "llava-llama-3-8b-v1.1:model-q4_0",
    "llava1.6-mistral": "llava-v1.6-mistral-7b:model-q4_0",
    "llava1.6-vicuna": "llava-v1.6-vicuna-7b:model-q4_0",
}

NEXA_RUN_MODEL_MAP_VOICE = {
    "whisper-large": "whisper-large:bin-large-v3",
    "whisper-tiny": "whisper-tiny:bin-tiny",
}

NEXA_RUN_MODEL_MAP_FUNCTION_CALLING = {
  "llama2-function-calling": "Llama2-7b-function-calling:q3_K_M",
}



NEXA_RUN_PROJECTOR_MAP = {
    "nanollava": "nanoLLaVA:projector-fp16",
    "llava-phi3": "llava-phi-3-mini:projector-q4_0",
    # "llava1.5": "/usr/share/ollama/.ollama/models/blobs/sha256-72d6f08a42f656d36b356dbe0920675899a99ce21192fd66266fb7d82ed07539",
    "llava-llama3": "llava-llama-3-8b-v1.1:projector-q4_0",
    "llava1.6-mistral": "llava-v1.6-mistral-7b:projector-q4_0",
    "llava1.6-vicuna": "llava-v1.6-vicuna-7b:projector-q4_0",
}

NEXA_RUN_MODEL_MAP_IMAGE = {
    "sd1-4": "stable-diffusion-v1-4:q4_0",
    "sd1-5": "stable-diffusion-v1-5:q4_0",
    "sd2-1": "stable-diffusion-v2-1:fp16",
    "sdxl-turbo": "sdxl-turbo:q8_0",
    "lcm-dreamshaper": "lcm-dreamshaper-v7:fp16",
}

NEXA_RUN_MODEL_MAP = {
    **NEXA_RUN_MODEL_MAP_TEXT,
    **NEXA_RUN_MODEL_MAP_VLM,
    **NEXA_RUN_MODEL_MAP_IMAGE,
}

NEXA_RUN_CHAT_TEMPLATE_MAP = {
    "llama2": "llama-2",
    "llama3": "llama-3",
    "llama3.1": "llama-3",
    "gemma": "gemma",
    "qwen1.5": "qwen",
    "qwen2": "qwen",
    "mistral": "mistral-instruct",
}

NEXA_RUN_COMPLETION_TEMPLATE_MAP = {
    "octopus-v2": "Below is the query from the users, please call the correct function and generate the parameters to call the function.\n\nQuery: {input} \n\nResponse:",
    "octopus-v4": "<|system|>You are a router. Below is the query from the users, please call the correct function and generate the parameters to call the function.<|end|><|user|>{input}<|end|><|assistant|>",
}

NEXA_RUN_MODEL_PRECISION_MAP = {
    "sd1-4": "q4_0",
    "sd1-5": "q4_0",
    "sd2-1": "q4_0",
    "lcm-dreamshaper": "f16",
}

EXIT_COMMANDS = ["/exit", "/quit", "/bye"]
EXIT_REMINDER = f"Please use Ctrl + d or one of {EXIT_COMMANDS} to exit.\n"

NEXA_STOP_WORDS_MAP = {"octopus-v2": ["<nexa_end>"]}

DEFAULT_TEXT_GEN_PARAMS = {
    "temperature": 0.7,
    "max_new_tokens": 2048,
    "top_k": 50,
    "top_p": 1.0,
}

DEFAULT_IMG_GEN_PARAMS = {
    "num_inference_steps": 20,
    "num_images_per_prompt": 1,
    "height": 512,
    "width": 512,
    "guidance_scale": 7.5,
    "output_path": "generated_images/image.png",
    "random_seed": 0,
}

DEFAULT_IMG_GEN_PARAMS_LCM = {
    "num_inference_steps": 4,
    "num_images_per_prompt": 1,
    "height": 512,
    "width": 512,
    "guidance_scale": 1.0,
    "output_path": "generated_images/image.png",
    "random_seed": 0,
}

DEFAULT_IMG_GEN_PARAMS_TURBO = {
    "num_inference_steps": 5,
    "num_images_per_prompt": 1,
    "height": 512,
    "width": 512,
    "guidance_scale": 5.0,
    "output_path": "generated_images/image.png",
    "random_seed": 0,
}

DEFAULT_VOICE_GEN_PARAMS = {
    "output_dir": "transcriptions",
    "beam_size": 5,
    "language": None,
    "task": "transcribe",
    "temperature": 0.0,
    "compute_type": "default"
}