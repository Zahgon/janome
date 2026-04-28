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
import os
import io
import pickle
import gzip
from struct import pack, unpack
import traceback
import logging
import sys
import re
import pkgutil
import zlib
import base64
from functools import lru_cache
from .fst import Matcher, create_minimum_transducer, compileFST

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)
handler = logging.StreamHandler()
handler.setLevel(logging.WARN)
formatter = logging.Formatter('%(asctime)s\t%(name)s - %(levelname)s\t%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

MODULE_FST_DATA = 'fst_data%d.py'
MODULE_ENTRIES_EXTRA = 'entries_extra%d.py'
MODULE_ENTRIES_COMPACT = 'entries_compact%d.py'
MODULE_ENTRIES_BUCKETS = 'entries_buckets.py'
MODULE_CONNECTIONS = 'connections%d.py'
MODULE_CHARDEFS = 'chardef.py'
MODULE_UNKNOWNS = 'unknowns.py'

FILE_USER_FST_DATA = 'user_fst.data'
FILE_USER_ENTRIES_DATA = 'user_entries.data'


def save_fstdata(data, dir, part=0):
    pass


def start_save_entries(dir, bucket_idx, morph_offset):
    pass


def end_save_entries(dir, bucket_idx):
    pass


def save_entry(dir, bucket_idx, morph_id, entry):
    pass


def save_entry_buckets(dir, buckets):
    pass


def save_connections(connections, dir='.'):
    # split whole connections to 2 buckets to reduce memory usage while installing.
    # TODO: find better ways...
    pass


def save_chardefs(chardefs, dir='.'):
    pass


def save_unknowns(unknowns, dir='.'):
    pass


def _save(file, data, compresslevel):
    pass


def _load(file):
    pass


def _load_package_data(package, resource):
    pass


def _save_as_module(file, data, binary=False):
    pass


def _start_entries_as_module(file, morph_id_offset):
    pass


def _end_entries_as_module(file):
    pass


def _save_entry_as_module_compact(file, morph_id, entry):
    pass


def _save_entry_as_module_extra(file, morph_id, entry):
    pass


class Dictionary(ABC):
    """
    Base dictionary class
    """

    @abstractmethod
    def lookup(self, s, matcher):
        pass

    @abstractmethod
    def lookup_extra(self, num):
        pass

    @abstractmethod
    def get_trans_cost(self, id1, id2):
        pass


class RAMDictionary(Dictionary):
    """
    RAM dictionary class
    """

    def __init__(self, entries, connections):
        self.entries = entries
        self.connections = connections

    def lookup(self, s, matcher):
        pass

    def lookup_extra(self, num):
        pass

    def get_trans_cost(self, id1, id2):
        pass


class MMapDictionary(Dictionary):
    """
    MMap dictionary class
    """

    def __init__(self, entries_compact, entries_extra, open_files, connections):
        self.entries_compact = entries_compact
        self.bucket_ranges = entries_compact.keys()
        self.entries_extra = entries_extra
        self.open_files = open_files
        self.connections = connections

    def lookup(self, s, matcher):
        pass

    @lru_cache(maxsize=8192)
    def _find_entry(self, idx):
        pass

    @lru_cache(maxsize=1024)
    def lookup_extra(self, idx):
        pass

    def get_trans_cost(self, id1, id2):
        pass

    def __del__(self):
        for mm, mm_idx in self.entries_compact.values():
            mm.close()
        if self.entries_extra:
            for mm, mm_idx in self.entries_extra.values():
                mm.close()
        for fp in self.open_files:
            fp.close()


class UnknownsDictionary(object):
    """
    Dictionary class for handling unknown words
    """

    def __init__(self, chardefs, unknowns):
        self.char_categories = chardefs[0]
        self.char_ranges = chardefs[1]
        self.unknowns = unknowns

    @lru_cache(maxsize=1024)
    def get_char_categories(self, c):
        pass

    def unknown_invoked_always(self, cate):
        pass

    def unknown_grouping(self, cate):
        pass

    def unknown_length(self, cate):
        pass


class UserDictionary(RAMDictionary):
    """
    User dictionary class (on-the-fly)
    """

    def __init__(self, user_dict, enc, type, connections, progress_handler=None):
        """
        Initialize user defined dictionary object.

        :param user_dict: user dictionary file (CSV format)
        :param enc: character encoding
        :param type: user dictionary type. supported types are 'ipadic' and 'simpledic'
        :param connections: connection cost matrix. expected value is SYS_DIC.connections
        :param progress_handler: handler mainly to indicate progress, implementation of ProgressHandler

        .. seealso:: https://janome.mocobeta.dev/en/#how-to-use-with-user-defined-dictionary
        """
        fst_data, entries = UserDictionary.build_dic(user_dict, enc, type, progress_handler)
        super().__init__(entries, connections)
        self.compiledFST = [fst_data]
        self.matcher = Matcher([fst_data])

    def lookup(self, s):
        pass

    @classmethod
    def line_to_entry_ipadic(cls, line):
        """Convert IPADIC formatted string to an user dictionary entry"""
        pass

    @classmethod
    def line_to_entry_simpledic(cls, line):
        """Convert simpledict formatted string to an user dictionary entry"""
        pass

    @classmethod
    def build_dic(cls, user_dict, enc, dict_type, progress_handler):
        pass

    def save(self, to_dir, compressionlevel=9):
        """
        Save compressed compiled dictionary data.

        :param to_dir: directory to save dictionary data
        :compressionlevel: (Optional) gzip compression level. default is 9
        """
        pass


class CompiledUserDictionary(RAMDictionary):
    """
    User dictionary class (compiled)
    """

    def __init__(self, dic_dir, connections):
        fst_data, entries = CompiledUserDictionary.load_dict(dic_dir)
        super().__init__(entries, connections)
        self.matcher = Matcher([fst_data])

    def lookup(self, s):
        pass

    @classmethod
    def load_dict(cls, dic_dir):
        pass


class LoadingDictionaryError(Exception):
    def __init__(self):
        self.message = 'Cannot load dictionary data. Try mmap mode for very large dictionary.'
