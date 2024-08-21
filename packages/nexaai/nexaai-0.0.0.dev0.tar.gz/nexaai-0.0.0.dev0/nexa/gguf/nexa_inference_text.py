import argparse
import logging
import os
import time
from pathlib import Path
from typing import Iterator, Union, List

from nexa.constants import (
    DEFAULT_TEXT_GEN_PARAMS,
    NEXA_RUN_CHAT_TEMPLATE_MAP,
    NEXA_RUN_COMPLETION_TEMPLATE_MAP,
    NEXA_RUN_MODEL_MAP,
    NEXA_STOP_WORDS_MAP,
)
from nexa.general import pull_model
from nexa.gguf.llama.llama import Llama
from nexa.utils import SpinningCursorAnimation, nexa_prompt, suppress_stdout_stderr
from nexa.gguf.llama import llama

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class NexaTextInference:
    """
    A class used for load text models and run text generation.

    Methods:
    run: Run the text generation loop.
    run_streamlit: Run the Streamlit UI.

    Args:
    model_path (str): Path or identifier for the model in Nexa Model Hub.
    stop_words (list): List of stop words for early stopping.
    profiling (bool): Enable timing measurements for the generation process.
    streamlit (bool): Run the inference in Streamlit UI.
    temperature (float): Temperature for sampling.
    max_new_tokens (int): Maximum number of new tokens to generate.
    top_k (int): Top-k sampling parameter.
    top_p (float): Top-p sampling parameter
    """
    def __init__(self, model_path, stop_words=None, **kwargs):
        self.params = DEFAULT_TEXT_GEN_PARAMS
        self.params.update(kwargs)
        self.model = None

        self.model_path = None
        self.downloaded_path = None
        if model_path in NEXA_RUN_MODEL_MAP:
            logging.debug(f"Found model {model_path} in public hub")
            self.model_path = NEXA_RUN_MODEL_MAP.get(model_path)
            self.downloaded_path = pull_model(self.model_path)
        elif os.path.exists(model_path):
            logging.debug(f"Using local model at {model_path}")
            self.downloaded_path = model_path
        else:
            logging.debug(f"Trying to use model from hub at {model_path}")
            self.downloaded_path = pull_model(model_path)

        if self.downloaded_path is None:
            logging.error(
                f"Model ({model_path}) is not appicable. Please refer to our docs for proper usage.",
                exc_info=True,
            )
            exit(1)

        self.stop_words = (
            stop_words if stop_words else NEXA_STOP_WORDS_MAP.get(model_path, [])
        )

        self.profiling = kwargs.get("profiling", False)

        self.chat_format = NEXA_RUN_CHAT_TEMPLATE_MAP.get(model_path, None)
        self.completion_template = NEXA_RUN_COMPLETION_TEMPLATE_MAP.get(
            model_path, None
        )

        if not kwargs.get("streamlit", False):
            self._load_model()
            if self.model is None:
                logging.error(
                    "Failed to load model or tokenizer. Exiting.", exc_info=True
                )
                exit(1)
    def embed(
        self,
        input: Union[str, List[str]],
        normalize: bool = False,
        truncate: bool = True,
        return_count: bool = False,
    ):
        """Embed a string.

        Args:
            input: The utf-8 encoded string or a list of string to embed.
            normalize: whether to normalize embedding in embedding dimension.
            trunca
            truncate: whether to truncate tokens to window length before generating embedding.
            return count: if true, return (embedding, count) tuple. else return embedding only.


        Returns:
            A list of embeddings
        """
        return self.model.embed(input, normalize, truncate, return_count)    

    @SpinningCursorAnimation()
    def _load_model(self):
        logging.debug(f"Loading model from {self.downloaded_path}")
        start_time = time.time()
        with suppress_stdout_stderr():
            self.model = Llama(
                model_path=self.downloaded_path,
                verbose=self.profiling,
                chat_format=self.chat_format,
                n_gpu_layers=-1,  # Uncomment to use GPU acceleration
            )
        load_time = time.time() - start_time
        if self.profiling:
            logging.debug(f"Model loaded in {load_time:.2f} seconds")
        if (
            self.completion_template is None
            and (
                chat_format := self.model.metadata.get("tokenizer.chat_template", None)
            )
            is not None
        ):
            self.chat_format = chat_format
            logging.debug("Chat format detected")

        self.conversation_history = [] if self.chat_format else None

    def run(self):
        while True:
            generated_text = ""
            try:
                if not (user_input := nexa_prompt()):
                    continue

                generation_start_time = time.time()

                if self.chat_format:
                    output = self._chat(user_input)
                    first_token = True
                    for chunk in output:
                        if first_token:
                            decoding_start_time = time.time()
                            prefill_time = decoding_start_time - generation_start_time
                            first_token = False
                        delta = chunk["choices"][0]["delta"]
                        if "role" in delta:
                            print(delta["role"], end=": ", flush=True)
                            generated_text += delta["role"]
                        elif "content" in delta:
                            print(delta["content"], end="", flush=True)
                            generated_text += delta["content"]

                else:
                    output = self._complete(user_input)
                    first_token = True
                    for chunk in output:
                        if first_token:
                            decoding_start_time = time.time()
                            prefill_time = decoding_start_time - generation_start_time
                            first_token = False
                        delta = chunk["choices"][0]["text"]
                        print(delta, end="", flush=True)
                        generated_text += delta


                if self.chat_format:
                    self.conversation_history.append(
                        {"role": "assistant", "content": generated_text}
                    )
            except KeyboardInterrupt:
                pass
            except Exception as e:
                logging.error(f"Error during generation: {e}", exc_info=True)
            print("\n")

    def _chat(self, user_input: str) -> Iterator:
        self.conversation_history.append({"role": "user", "content": user_input})
        return self.model.create_chat_completion(
            messages=self.conversation_history,
            temperature=self.params["temperature"],
            max_tokens=self.params["max_new_tokens"],
            top_k=self.params["top_k"],
            top_p=self.params["top_p"],
            stream=True,
            stop=self.stop_words,
        )

    def _complete(self, user_input: str) -> Iterator:
        prompt = (
            self.completion_template.format(input=user_input)
            if self.completion_template
            else user_input
        )
        return self.model.create_completion(
            prompt=prompt,
            temperature=self.params["temperature"],
            max_tokens=self.params["max_new_tokens"],
            top_k=self.params["top_k"],
            top_p=self.params["top_p"],
            echo=False,  # Echo the prompt back in the output
            stream=True,
            stop=self.stop_words,
        )

    def run_streamlit(self, model_path: str):
        """
        Run the Streamlit UI.
        """
        logging.info("Running Streamlit UI...")

        script_path = (
            Path(os.path.abspath(__file__)).parent
            / "streamlit"
            / "streamlit_text_chat.py"
        )

        import sys

        from streamlit.web import cli as stcli

        sys.argv = ["streamlit", "run", str(script_path), model_path]
        sys.exit(stcli.main())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run text generation with a specified model"
    )
    parser.add_argument(
        "model_path",
        type=str,
        help="Path or identifier for the model in Nexa Model Hub",
    )
    parser.add_argument(
        "-t", "--temperature", type=float, default=0.8, help="Temperature for sampling"
    )
    parser.add_argument(
        "-m",
        "--max_new_tokens",
        type=int,
        default=256,
        help="Maximum number of new tokens to generate",
    )
    parser.add_argument(
        "-k", "--top_k", type=int, default=50, help="Top-k sampling parameter"
    )
    parser.add_argument(
        "-p", "--top_p", type=float, default=1.0, help="Top-p sampling parameter"
    )
    parser.add_argument(
        "-sw",
        "--stop_words",
        nargs="*",
        default=[],
        help="List of stop words for early stopping",
    )
    parser.add_argument(
        "-pf",
        "--profiling",
        action="store_true",
        help="Enable timing measurements for the generation process",
    )
    parser.add_argument(
        "-st",
        "--streamlit",
        action="store_true",
        help="Run the inference in Streamlit UI",
    )
    args = parser.parse_args()
    kwargs = {k: v for k, v in vars(args).items() if v is not None}
    model_path = kwargs.pop("model_path")
    stop_words = kwargs.pop("stop_words", [])
    inference = NexaTextInference(model_path, stop_words=stop_words, **kwargs)
    if args.streamlit:
        inference.run_streamlit(model_path)
    else:
        inference.run()
