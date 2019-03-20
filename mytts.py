#
#
import os


import jieba
from pinyin_biaobeiset import pinyinBiaobeiStyle, syllableSeperate
from labformat import tree, show
from labcnp import LabNode, LabGenerator


def generateHTSlabel(text):
    pinyin_list = pinyinBiaobeiStyle(text)
    print(pinyin_list)
    words_jieba = jieba.cut(text)
    words = "".join(words_jieba)
    print(words)
    rhythms = ['#1'] * len(words)
    rhythms[-1] = '#4'

    syllables_ = pinyinBiaobeiStyle(text)
    syllables = []
    for p in syllables_:
        syllables.append(syllableSeperate(p))
    
    phones = []
    for s in syllables:
        for cv in s:
            phones.append(cv)
    
    poses = ['n'] * len(rhythms)

    phs_type = ['a'] * len(phones)

    label = ''    
    f_phone = tree(words, rhythms, syllables, poses, phs_type)
    times = [[0,0]] * len(phones)
    # print(times)
    for ph_list in LabGenerator(f_phone, rhythms, times):
        label += ph_list + '\n'
    # print(label)
    return label

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="convert text file to HTS label.")
    parser.add_argument(
        "txtfile",
        help="text file, it's text of need synthesis. one line refer to a sentence."
    )
    parser.add_argument(
        "output_path",
        help="Full path to output directory, will be created if it doesn't exist"
        )
    args = parser.parse_args()
    print("Start generate HTS label:"+'\ntext:'+args.txtfile+'\noutput:'+args.output_path + '\n')

    os.makedirs(args.output_path, exist_ok=True)

    tfile = open(args.txtfile, 'r')
    all_text = tfile.read()
    all_text_list = all_text.splitlines()

    for text in all_text_list:
        label_name = text.split('\t')[0]
        text = text.split('\t')[1]
        one_label = generateHTSlabel(text)
        one_label_file_path = os.path.join(args.output_path, label_name + '.lab')
        lab_file = open(one_label_file_path, 'w')
        lab_file.write(one_label)
        lab_file.close()
        print('text:' + text)
        print('file:' + one_label_file_path)
        print(one_label)