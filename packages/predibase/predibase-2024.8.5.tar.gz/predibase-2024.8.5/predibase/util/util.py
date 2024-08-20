from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from transformers import PreTrainedTokenizer


def remove_prefix(s: str, prefix: str) -> str:
    if not s.startswith(prefix):
        return s

    return s[len(prefix) :]


def remove_suffix(s: str, suffix: str) -> str:
    if not s.endswith(suffix):
        return s

    return s[: -len(suffix)]


def get_pre_trained_tokenizer(
    pretrained_model_name_or_path: str | pathlib.Path,
    **kwargs,
) -> "PreTrainedTokenizer":
    """Returns the tokenizer associated with the given base model.

    :param pretrained_model_name_or_path: (str | pathlib.Path) HuggingFace ID of the base model.
    :param kwargs: (dict) Additional keyword parameters accepted by the "from_pretrained()" method in the Transformers
        library.
    :return: (PreTrainedTokenizer) the tokenizer for the specified base model ID.
    """
    # TODO(travis): can we remove this function? looks like it's only used by a test
    try:
        from transformers import AutoTokenizer
    except ImportError:
        raise ImportError(
            "The 'transformers' library is required to use `get_pre_trained_tokenizer`. Please install it using 'pip install transformers'.",
        )

    base_model_tokenizer: "PreTrainedTokenizer" = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path=pretrained_model_name_or_path,
        **kwargs,
    )
    return base_model_tokenizer


def tokenize_and_count(text: str, tokenizer: "PreTrainedTokenizer") -> int:
    """Returns the count of tokens in the text input, given the tokenizer provided.

    :param text: (str) a text string whose tokens are to be counted.
    :param tokenizer: (PreTrainedTokenizer) the tokenizer corresponding to the given base model.
    :return: (int) number of tokens in the text string according to the tokenizer provided.
    """
    tokens: list[str] = tokenizer.tokenize(text)
    return len(tokens)
