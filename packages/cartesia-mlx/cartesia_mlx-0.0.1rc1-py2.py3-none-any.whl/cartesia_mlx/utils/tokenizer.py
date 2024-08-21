import hf_olmo  # noqa
from transformers import AutoTokenizer

from cartesia_mlx.utils.configure import set_cfg


class Tokenizer:
    """Tokenizer Wrapper for Huggingface AutoTokenizer."""

    base_cfg = dict(
        _class_="utils.tokenizer.Tokenizer",
        name="allenai/OLMo-1.7-7B",
    )

    def __init__(self, cfg=None, parent=None):
        super().__init__()
        set_cfg(self, cfg, parent)
        self.name: str  # Linting type hint
        self.tokenizer = AutoTokenizer.from_pretrained(self.name)

    def tokenize(self, x: list) -> list:
        """Tokenize list of strings."""
        tokens = self.tokenizer(x).input_ids
        return tokens

    def detokenize(self, tokens: list) -> list:
        """Detokenize list of tokens."""
        return self.tokenizer.batch_decode(tokens, clean_up_tokenization_spaces=False)
