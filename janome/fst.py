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

import copy
from struct import pack, unpack
from collections import OrderedDict
import logging
import threading
from functools import lru_cache

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)
handler = logging.StreamHandler()
handler.setLevel(logging.WARN)
formatter = logging.Formatter('%(asctime)s\t%(name)s - %(levelname)s\t%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# bit flags to represent class of arcs
# refer to Apache Lucene FST's implementation
FLAG_FINAL_ARC = 1 << 0             # 1
FLAG_LAST_ARC = 1 << 1              # 2
FLAG_TARGET_NEXT = 1 << 2           # 4  TODO: not used. can be removed?
FLAG_STOP_NODE = 1 << 3             # 8  TODO: not used. can be removed?
FLAG_ARC_HAS_OUTPUT = 1 << 4        # 16
FLAG_ARC_HAS_FINAL_OUTPUT = 1 << 5  # 32

# all characters
CHARS = set()


def set_fst_log_level(level):
    pass


class State(object):
    """
    State Class
    """
    __slots__ = ['id', 'final', 'trans_map', 'final_output']

    def __init__(self, id=None):
        self.id = id
        self.final = False
        self.trans_map = {}
        self.final_output = set()

    def is_final(self):
        pass

    def set_final(self, final):
        pass

    def transition(self, char):
        pass

    def set_transition(self, char, state):
        pass

    def state_output(self):
        pass

    def set_state_output(self, output):
        pass

    def clear_state_output(self):
        pass

    def output(self, char):
        pass

    def set_output(self, char, out):
        pass

    def clear(self):
        pass

    def __eq__(self, other):
        if other is None or not isinstance(other, State):
            return False
        else:
            return \
                self.final == other.final and \
                self.trans_map == other.trans_map and \
                self.final_output == other.final_output

    def __hash__(self):
        return hash(str(self.final) + str(self.trans_map) + str(self.final_output))


def copy_state(src, id):
    pass


class FST(object):
    """
    FST (final dictionary) class
    """
    MAX_SIZE = 300000

    def __init__(self):
        # must preserve inserting order
        self.dictionary = OrderedDict()

    def size(self):
        pass

    def member(self, state):
        pass

    def insert(self, state):
        pass

    def remove(self, state):
        pass

    def exceed_max_size(self):
        pass

    def print_dictionary(self):
        pass


# naive implementation for building fst
# http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.24.3698
def create_minimum_transducer(inputs, on_progress=None):
    def find_minimized(state):
        pass
    def prefix_len(s1, s2):
        pass
    pass


def compileFST(fst):
    """
    convert FST to byte array representing arcs
    """
    pass


class Matcher(object):
    def __init__(self, dict_data, max_cache_size=1024, max_cached_word_len=8):
        if dict_data:
            self.dict_data = dict_data
            self.dict_len = len(dict_data)
            # bytes -> (position, final_outputs, outputs)
            self.cache = [OrderedDict() for _ in range(len(dict_data))]
            self.max_cache_size = max_cache_size
            self.max_cached_word_len = max_cached_word_len
            self.lock = threading.Lock()

    def run(self, word, common_prefix_match=True):
        pass

    def _run(self, word, data_num, common_prefix_match):
        pass

    @lru_cache(maxsize=4096)
    def next_arc(self, data, addr):
        pass


if __name__ == '__main__':
    inputs1 = [
        ('apr'.encode('utf8'), '30'),
        ('aug'.encode('utf8'), '31'),
        ('dec'.encode('utf8'), '31'.encode('utf8')),
        ('feb'.encode('utf8'), '28'.encode('utf8')),
        ('feb'.encode('utf8'), '29'.encode('utf8')),
        ('jan'.encode('utf8'), '31'.encode('utf8')),
        ('jul'.encode('utf8'), '31'.encode('utf8')),
        ('jun'.encode('utf8'), '30'.encode('utf8'))
    ]
    processed, fst = create_minimum_transducer(inputs1)
    data = compileFST(fst)

    m = Matcher([data])
    # print(m.run('apr'))
    print(m.run('apr'.encode('utf8')))
    print(m.run('aug'.encode('utf8')))
