# -- encoding: utf-8 --
from __future__ import unicode_literals
import re
import copy
from sys import exit
from labcnp import LabNode, LabGenerator
import pdb
rhythm_map = ['ph', 'syl', '#0', '#1', '#3', '#4'] # '#2'


def tree_per_word(word, cur_rhythm, tree_init, syllables, poses):
    def get_list(rhythm):
        return tree_init[rhythm]

    assert cur_rhythm in rhythm_map
    current_rhythm_list = get_list(cur_rhythm)

    if cur_rhythm == u'ph':
        pass

    elif cur_rhythm == u'syl':
        smaller_rhythm = u'ph'
        syllable = syllables.pop(0)
        for phones in syllable:
            tree_per_word(phones, smaller_rhythm, tree_init, syllables, poses)

    elif cur_rhythm == u'#0':
        smaller_rhythm = u'syl'
        for syllable in syllables[0:len(word)]:
            tree_per_word(''.join(syllable), smaller_rhythm, tree_init,
                          syllables, poses)

    elif cur_rhythm == u'#1':
        smaller_rhythm = u'#0'
        tree_per_word(word, smaller_rhythm, tree_init, syllables, poses)

#-----------------------------------------------------------------------------
    # elif cur_rhythm == u'#2':
    #     smaller_rhythm = u'#1'
    #     tree_per_word(word, smaller_rhythm, tree_init, syllables, poses)
    
    # elif cur_rhythm == u'#3':
    #     smaller_rhythm = u'#2'
    #     tree_per_word(word, smaller_rhythm, tree_init, syllables, poses)
#-----------------------------------------------------------------------------
    elif cur_rhythm == u'#3':
        smaller_rhythm = u'#1'
        tree_per_word(word, smaller_rhythm, tree_init, syllables, poses)
#-----------------------------------------------------------------------------

    elif cur_rhythm == u'#4':
        smaller_rhythm = u'#3'
        tree_per_word(word, smaller_rhythm, tree_init, syllables, poses)

    else:
        raise ValueError('rhythm {} is not correct'.format(cur_rhythm))

    # 创建节点
    if cur_rhythm == u'ph':
        newNode = LabNode(
            txt=word, index=len(current_rhythm_list) + 1, rhythm=cur_rhythm)

    else:
        smaller_rhythm_list = get_list(smaller_rhythm)
        newNode = LabNode(
            sons=smaller_rhythm_list,
            txt=word,
            index=len(current_rhythm_list) + 1,
            rhythm=cur_rhythm)
        if len(smaller_rhythm_list) > 0:
            tree_init['assist'][smaller_rhythm] = smaller_rhythm_list[-1]
        else:
            tree_init['assist'][smaller_rhythm] = []
        # 清空此节点下的子节点list，以便新节点重建子节点list
        tree_init[smaller_rhythm] = []

    # 设置词性
    if cur_rhythm == u'#0':
        newNode.pos = poses.pop(0)

    # 设置左右brother
    if len(current_rhythm_list) > 0:
        newNode.lbrother = current_rhythm_list[-1]
        current_rhythm_list[-1].rbrother = newNode
    elif tree_init['assist'][cur_rhythm]:
        # 设置非同树枝下的树叶连成一块
        newNode.lbrother = tree_init['assist'][cur_rhythm]
        tree_init['assist'][cur_rhythm].rbrother = newNode

    # 加入新节点到current_rhythm_list
    current_rhythm_list.append(newNode)


def show(tree_list, shift=0):
    for item in tree_list:
        print('|\t' * shift + str(item.index) + '\t' + item.txt + '\t' +
              item.rhythm + '\t' + str(item.sons_num) + '\t' + item.pos)
        show(item.sons, shift + 1)


def get_first_node_of_tree(root_node):
    """root_node's rhythm is #4"""
    return root_node.sons[0].sons[0].sons[0].sons[0].sons[0]


def add_head_middle_tail_silence(root_node, phs_type):
    """Add a 'sil' tree node at the head or middle or tail of tree according to
    the phs_type"""
    fphone = get_first_node_of_tree(root_node)

    if phs_type[0] == u's':
        newNode = LabNode(txt='sil', rhythm='ph')
        newNode.rbrother = fphone
        fphone.lbrother = newNode
        fphone = newNode
    phone = fphone
    assert phone is not None
    for ptype in phs_type[1:-1]:
        if ptype in ['s', 'd']:
            if ptype == u's':
                newNode = LabNode(txt='pau', rhythm='ph')
            else:
                newNode = LabNode(txt='sp', rhythm='ph')
            newNode.rbrother = phone.rbrother
            newNode.lbrother = phone
            phone.rbrother = newNode
            newNode.rbrother.lbrother = newNode
            phone = newNode
        else:
            assert phone is not None
            phone = phone.rbrother
    assert phone is not None
    if phs_type[-1] in ['s', 'd']:
        phone.rbrother = LabNode(txt='sil', rhythm='ph')
        phone.rbrother.lbrother = phone
    return fphone


def tree(words, rhythms, syllables, poses, phs_type=None):
    assert len(words) == len(rhythms)
    assert len(words) == len(poses)
    tree_init = {'assist': {}}
    for rhythm in rhythm_map:
        tree_init[rhythm] = []
        tree_init['assist'][rhythm] = None

    syllables_copy = copy.deepcopy(syllables)
    poses_copy = copy.deepcopy(poses)
    for word, rhythm in zip(words, rhythms):
        tree_per_word(word, rhythm, tree_init, syllables_copy, poses_copy)
    # 增加一个#5，是多个#4句子的集合
    newNode = LabNode(sons=tree_init['#4'], index=1, rhythm='#5')
    """
    if phs_type:
        newNode.adjust()
    """

    # print('----show tree----')
    # show(tree_init['#4'], 0)

    root_node = tree_init['#4'][0]
    return add_head_middle_tail_silence(root_node, phs_type) # use phs_type mark add silence
    # return get_first_node_of_tree(root_node)