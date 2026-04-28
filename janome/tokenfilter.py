# Copyright 2015 moco_beta
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Iterator, List, Dict, Tuple, Any

from .tokenizer import Token


class TokenFilter(ABC):
    """
    Base TokenFilter class.

    A TokenFilter modifies or transforms the input token sequence according to the rule described in apply() method.
    Subclasses must implement apply() method.

    Added in *version 0.3.4*
    """

    @abstractmethod
    def apply(self, tokens: Iterator[Token]) -> Iterator[Any]:
        pass

    def __call__(self, tokens: Iterator[Token]) -> Iterator[Any]:
        return self.apply(tokens)


class LowerCaseFilter(TokenFilter):
    """
    A LowerCaseFilter converts the surface and base_form of tokens to lowercase.

    Added in *version 0.3.4*
    """

    def apply(self, tokens: Iterator[Token]) -> Iterator[Token]:
        pass


class UpperCaseFilter(TokenFilter):
    """
    An UpperCaseFilter converts the surface and base_form of tokens to uppercase.

    Added in *version 0.3.4*
    """

    def apply(self, tokens: Iterator[Token]) -> Iterator[Token]:
        pass


class POSStopFilter(TokenFilter):
    u"""
    A POSStopFilter removes tokens associated with part-of-speech tags
    listed in the stop tags list and keeps other tokens.

    Tag matching rule is prefix-matching. e.g., if '動詞' is given as a stop tag,
    '動詞,自立,*,*' and '動詞,非自立,*,*' (or so) are removed.

    Added in *version 0.3.4*
    """

    def __init__(self, pos_list: List[str]):
        """
        Initialize POSStopFilter object.

        :param pos_list: stop part-of-speech tags list.
        """
        self.pos_list = pos_list

    def apply(self, tokens: Iterator[Token]) -> Iterator[Token]:
        pass


class POSKeepFilter(TokenFilter):
    """
    A POSKeepFilter keeps tokens associated with part-of-speech tags
    listed in the keep tags list and removes other tokens.

    Tag matching rule is prefix-matching. e.g., if '動詞' is given as a keep tag,
    '動詞,自立,*,*' and '動詞,非自立,*,*' (or so) are kept.

    Added in *version 0.3.4*
    """

    def __init__(self, pos_list: List[str]):
        """
        Initialize POSKeepFilter object.

        :param pos_list: keep part-of-speech tags list.
        """
        self.pos_list = pos_list

    def apply(self, tokens: Iterator[Token]) -> Iterator[Token]:
        pass


class CompoundNounFilter(TokenFilter):
    """
    A CompoundNounFilter generates compound nouns.

    This Filter joins contiguous nouns.
    For example, '形態素解析器' is splitted three noun tokens '形態素/解析/器' by Tokenizer and then re-joined by this filter.
    Generated tokens are associated with the special part-of-speech tag '名詞,複合,*,*'

    Added in *version 0.3.4*
    """

    def apply(self, tokens: Iterator[Token]) -> Iterator[Token]:
        pass


class ExtractAttributeFilter(TokenFilter):
    """
    An ExtractAttributeFilter extracts a specified attribute of Token.

    **NOTES** This filter must placed the last of token filter chain because return values are not tokens but strings.

    Added in *version 0.3.4*
    """

    def __init__(self, att: str):
        """
        Initialize ExtractAttributeFilter object.

        :param att: attribute name should be extraced from a token. valid values for *att* are 'surface',
                    'part_of_speech', 'infl_type', 'infl_form', 'base_form', 'reading' and 'phonetic'.
        """
        if att not in ['surface', 'part_of_speech', 'infl_type', 'infl_form', 'base_form', 'reading', 'phonetic']:
            raise Exception(f'Unknown attribute name: {att}')
        self.att = att

    def apply(self, tokens: Iterator[Token]) -> Iterator[str]:
        pass


class TokenCountFilter(TokenFilter):
    """
    An TokenCountFilter counts word frequencies in the input text. Here, 'word' means an attribute of Token.

    This filter generates word-frequency pairs.
    When `sorted` option is set to True, pairs are sorted in descending order of frequency.

    **NOTES** This filter must placed the last of token filter chain because return values are not tokens
    but string-integer tuples.

    Added in *version 0.3.5*
    """

    def __init__(self, att: str = 'surface', sorted: bool = False):
        """
        Initialize TokenCountFilter object.

        :param att: attribute name should be extraced from a token. valid values for *att* are 'surface',
                    'part_of_speech', 'infl_type', 'infl_form', 'base_form', 'reading' and 'phonetic'.
        :param sorted: sort items by term frequency
        """
        if att not in ['surface', 'part_of_speech', 'infl_type', 'infl_form', 'base_form', 'reading', 'phonetic']:
            raise Exception(f'Unknown attribute name: {att}')
        self.att = att
        self.sorted = sorted

    def apply(self, tokens: Iterator[Token]) -> Iterator[Tuple[str, int]]:
        pass
