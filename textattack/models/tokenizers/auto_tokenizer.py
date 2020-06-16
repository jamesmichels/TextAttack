import transformers

from textattack.models.tokenizers import Tokenizer
from textattack.shared import AttackedText


class AutoTokenizer(Tokenizer):
    """ 
    A generic class that convert text to tokens and tokens to IDs. Supports
    any type of tokenization, be it word, wordpiece, or character-based.
    Based on the ``AutoTokenizer`` from the ``transformers`` library.
    
    Args: 
        name: the identifying name of the tokenizer (see AutoTokenizer,
            https://github.com/huggingface/transformers/blob/master/src/transformers/tokenization_auto.py)
        max_length: if set, will truncate & pad tokens to fit this length
    """

    def __init__(
        self,
        name="bert-base-uncased",
        max_length=256,
        pad_to_length=False,
        use_fast=True,
    ):
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(
            name, use_fast=use_fast
        )
        self.max_length = max_length

    def encode(self, input_text):
        """ Encodes ``input_text``.
        
        ``input_text`` may be a string or a tuple of strings, depending if the
        model takes 1 or multiple inputs. The ``transformers.AutoTokenizer``
        will automatically handle either case.
        """
        encoded_text = self.tokenizer.encode_plus(
            input_text,
            max_length=self.max_length,
            add_special_tokens=True,
            pad_to_max_length=True,
        )
        return encoded_text
    
    def encode_batch(self, input_text_list):
        """ The batch equivalent of ``encode``."""
        return self.tokenizer.encode_batch(input_text_list,
            max_length=self.max_length,
            add_special_tokens=True,
            pad_to_max_length=True,
        )
