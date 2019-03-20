# -*- coding: UTF-8 -*-
import copy
from labformat import tree, show
from labcnp import LabNode, LabGenerator
from biaobei import Data

# generate HTS label for test synthesis by herb
# 2019.1.12

def generateHTSlabel(one_data, labels_path):

    label = ''    
    phone = tree(one_data.words, one_data.rhythms, one_data.syllables, one_data.poses, one_data.phs_type)
    one_data.times = [[0,0]] * len(one_data.phones)
    # print(one_data.times)
    for ph_list in LabGenerator(phone, one_data.rhythms, one_data.times):
        label += ph_list + '\n'
    print(label)
    current_label_file = open(labels_path, "w")
    current_label_file.write(label)
    current_label_file.close()
    print("all HTS labels generate done.\n")

if __name__ == "__main__":
    data = []
    one_data = Data()

    one_data.phones = ['x','in1','j','iang1','d','a4','x','ue2','h','uan1','ing2','n','in2']
    one_data.words = [u'新疆',u'大学',u'欢迎',u'您']
    one_data.rhythms = ['#1','#3','#1','#4']
    one_data.syllables = [['x','in1'],['j','iang1'],['d','a4'],['x','ue2'],['h','uan1'],['ing2'],['n','in2']]
    one_data.poses = ['n'] * len(one_data.rhythms)
    one_data.phs_type = ['a'] * len(one_data.phones)

    data.append(one_data)

    sec_data = Data()
    sec_data.phones = [ 'sil','x','in1','j','iang1','sh','i4','zh','ong2','g','uo2','l','u4','d','i4','m',
                        'ian4','j','i5','z','uei4','d','a4','d','e5','sh','eng3','j','i2','x','ing2',
                        'zh','eng4','q','v1','sp1','zh','an4','zh','ong1','g','uo2','g','uo2','t','u3','m',
                        'ian4','j','i5','l','iou4','f','en1','zh','i1','i1','sil']
    sec_data.words = [u'新疆',u'是',u'中国',u'陆地',u'面积',u'最大',u'的',u'省级',u'行政区',u'占',u'中国',u'国土',u'面积',u'六分之一']
    sec_data.rhythms = ['#1', '#1',  '#1',  '#1',   '#1',   '#1',  '#3', '#1',     '#4',  '#1',  '#1',  '#1',  '#1',     '#4']
    sec_data.syllables =[['x','in1'],['j','iang1'],['sh','i4'],['zh','ong2'],['g','uo2'],['l','u4'],['d','i4'],['m',
                        'ian4'],['j','i5'],['z','uei4'],['d','a4'],['d','e5'],['sh','eng3'],['j','i2'],['x','ing2'],
                        ['zh','eng4'],['q','v1'],['zh','an4'],['zh','ong1'],['g','uo2'],['g','uo2'],['t','u3'],['m',
                        'ian4'],['j','i5'],['l','iou4'],['f','en1'],['zh','i1'],['i1']]
    sec_data.poses = ['n'] * len(sec_data.rhythms)
    sec_data.phs_type = ['a'] * len(sec_data.phones)

    for r in sec_data.rhythms[-1]:
        r = '#1'

    data.append(sec_data)
    
    label_name_index = 1
    for a_data in data:

        for i in range(len(a_data.phones)):
            if a_data.phones[i] == 'sil':
                a_data.phs_type[i] = 's'
            elif a_data.phones[i] == 'sp1':
                a_data.phs_type[i] = 'd'

        generateHTSlabel(a_data, "test-label-%05d.lab"%label_name_index)
        label_name_index += 1

#############################################################################################################
    phone_1 = ['ch', 'zh', 'r', 'pl', 'sil', 'c', 'b', 'd', 'g', 'f', 'h',
                'k', 'j', 'm', 'l', 'n', 'q', 'p', 's', 'sh', 't', 'x', 'z']
    phone_2 = ['uen', 'ei', 've', 'ai', 'vanr', 'in', 'ong', 'ao', 'an', 
                'uai', 'en', 'iong', 'anr', 'uan', 'ia', 'uei', 'ing', 'ie',
                'er', 'uor', 'iao', 'ian', 'van', 'inr', 'eng', 'iang', 'ongr', 
                'iiir', 'ng', 'enr', 'ang', 'uanr', 'ingr', 'iar', 'ur', 'ir',
                'io', 'our', 'iou', 'iangr', 'ueir', 'vn', 'uair', 'iii', 
                'uang', 'a', 'ii', 'ianr', 'ueng', 'e', 'i', 'iyl', 'sp', 'iour',
                'o', 'air', 'uo', 'ar', 'u', 'uenr', 'v', 'ou', 'ua', 'aor']

