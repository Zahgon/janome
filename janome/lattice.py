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

import os


class NodeType:
    SYS_DICT = "SYS_DICT"
    USER_DICT = "USER_DICT"
    UNKNOWN = "UNKNOWN"


class Node(object):
    """
    Standard Node class
    """
    __slots__ = [
        'pos', 'index', 'surface', 'left_id', 'right_id', 'cost',
        'part_of_speech', 'infl_type', 'infl_form',
        'base_form', 'reading', 'phonetic', 'node_type',
        'min_cost', 'back_pos', 'back_index'
    ]

    def __init__(self, dict_entry, node_type=NodeType.SYS_DICT):
        self.pos = 0
        self.index = 0
        self.min_cost = 2147483647  # int(pow(2,31)-1)
        self.back_pos = -1
        self.back_index = -1
        self.surface, self.left_id, self.right_id, self.cost, \
            self.part_of_speech, self.infl_type, self.infl_form, self.base_form, \
            self.reading, self.phonetic = dict_entry
        self.node_type = node_type

    def __str__(self):
        return f"({self.surface}, {self.left_id}, {self.right_id}, {self.cost}, {self.part_of_speech}, \
                  {self.infl_type}, {self.infl_form}, {self.base_form}, {self.reading}, {self.phonetic}) \
                      [back_pos = {self.back_pos}, back_index = {self.back_index}]"

    def node_label(self):
        pass


class SurfaceNode(object):
    """
    Node class with surface form only.
    """
    __slots__ = [
        'pos', 'index', 'min_cost', 'back_pos', 'back_index',
        'num', 'surface', 'left_id', 'right_id', 'cost', 'node_type'
    ]

    def __init__(self, dict_entry, node_type=NodeType.SYS_DICT):
        self.pos = 0
        self.index = 0
        self.min_cost = 2147483647  # int(pow(2,31)-1)
        self.back_pos = -1
        self.back_index = -1
        self.num, self.surface, self.left_id, self.right_id, self.cost = dict_entry
        self.node_type = node_type

    def node_label(self):
        pass


class BOS(object):
    """
    BOS node
    """
    __slots__ = [
        'pos', 'index', 'min_cost', 'back_pos', 'back_index',
        'right_id', 'cost'
    ]

    def __init__(self):
        self.pos = 0
        self.index = 0
        self.min_cost = 0
        self.back_pos = -1
        self.back_index = -1
        self.right_id = 0
        self.cost = 0

    def __str__(self):
        return '__BOS__'

    def node_label(self):
        pass


class EOS(object):
    """
    EOS node
    """
    __slots__ = [
        'pos', 'index', 'min_cost', 'back_pos', 'back_index',
        'left_id', 'cost'
    ]

    def __init__(self, pos):
        self.pos = pos
        self.index = 0
        self.min_cost = 2147483647  # int(pow(2,31)-1)
        self.back_pos = -1
        self.back_index = -1
        self.cost = 0
        self.left_id = 0

    def __str__(self):
        return f'__EOS__ [back_pos={self.back_pos}]'

    def node_label(self):
        pass


class Lattice(object):
    def __init__(self, size, dic):
        self.snodes = [[BOS()]] + [[] for i in range(0, size + 1)]
        self.enodes = [[], [BOS()]] + [[] for i in range(0, size + 1)]
        self.conn_costs = [[]]
        self.p = 1
        self.dic = dic

    def add(self, node):
        pass

    def forward(self):
        pass

    def end(self):
        pass

    def backward(self):
        pass

    # generate Graphviz dot file
    def generate_dotfile(self, filename='lattice.gv'):
        def is_unknown(node):
            pass
        pass

    def __open_file(self, filename, mode, encoding):
        pass

    def __str__(self):
        return '\n'.join(','.join(str(node) for node in nodes) for nodes in self.snodes)
