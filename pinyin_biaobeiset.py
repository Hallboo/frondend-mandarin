# -*- encoding: UTF-8 -*-
import sys
import re
from pypinyin import pinyin, Style

consonant_list = ['b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k',
                  'h', 'j', 'q', 'x', 'zh', 'ch', 'sh', 'r', 'z',
                  'c', 's', 'y', 'w']

# phone_1 = ['ch', 'zh', 'r', 'pl', 'sil', 'c', 'b', 'd', 'g', 'f', 'h',
#             'k', 'j', 'm', 'l', 'n', 'q', 'p', 's', 'sh', 't', 'x', 'z']
# phone_2 = ['uen', 'ei', 've', 'ai', 'vanr', 'in', 'ong', 'ao', 'an', 
#             'uai', 'en', 'iong', 'anr', 'uan', 'ia', 'uei', 'ing', 'ie',
#             'er', 'uor', 'iao', 'ian', 'van', 'inr', 'eng', 'iang', 'o    ngr', 
#             'iiir', 'ng', 'enr', 'ang', 'uanr', 'ingr', 'iar', 'ur', 'ir',
#             'io', 'our', 'iou', 'iangr', 'ueir', 'vn', 'uair', 'iii', 
#             'uang', 'a', 'ii', 'ianr', 'ueng', 'e', 'i', 'iyl', 'sp', 'iour',
#             'o', 'air', 'uo', 'ar', 'u', 'uenr', 'v', 'ou', 'ua', 'aor']

phone_3 = ['er','vanr','anr','uor','inr','ongr','iiir','enr','uanr','ingr',
          'iar','ur','ir','our','iangr','ueir','uair','ianr','iour','air','ar','uenr','aor']

CONSONANT_DICT = {'w':'u','y':'i'}
VOWEL_DICT = {'un':'uen','ui':'uei','iu':'iou','ioung':'iong','ue':'ve'}#'uan':'van'}
SYLLABLE_FULL_DICT = {'yo':'iou',#'en':'ng',#'de':'di',
                    'ci':'cii','si':'sii','zi':'zii','ri':'riii',
                    'zhi':'zhiii','chi':'chiii','shi':'shiii','shei':'shuei',}
SYLLABLE_DICT = {'yu':'v','wu':'u','yi':'i','qu':'qv','ju':'jv',#'xuan':'xvan',
                'xu':'xv',
                'io':"iou",}

def convertSyllable(syllable):
    '''seprate syllable to consonant + ' ' + vowel '''
    if not syllable[-1].isdigit():
        syllable += '5'
    # print(syllable)
    syllable_ = syllable[:-1]
    if syllable_ in SYLLABLE_FULL_DICT:
        syllable = syllable.replace(syllable_, SYLLABLE_FULL_DICT[syllable_])
        return syllable

    for key in SYLLABLE_DICT:
        if key in syllable:
            syllable = syllable.replace(key, SYLLABLE_DICT[key])

    consonant = ''
    vowel = ''
    if syllable[0:2] in consonant_list:
        consonant = syllable[0:2]
        vowel = syllable[2:-1]
    elif syllable[0] in consonant_list:
        consonant = syllable[0]
        vowel = syllable[1:-1]
    else:
        pass
        # print("there are phone exclude list : %s"%syllable)

    # print(syllable + '\t' + consonant + '\t' + vowel)

    if consonant in CONSONANT_DICT:
        syllable = syllable.replace(consonant, CONSONANT_DICT[consonant])
    if vowel in VOWEL_DICT:
        syllable = syllable.replace(vowel, VOWEL_DICT[vowel])

    return syllable        

def syllableSeperate(syllable):
    '''seprate syllable to consonant + ' ' + vowel '''
    if not syllable[-1].isdigit():
        syllable += '5'

    if syllable[0:2] in consonant_list:
        return [syllable[0:2], syllable[2:]]
    elif syllable[0] in consonant_list and not syllable[1].isdigit():
        return [syllable[0], syllable[1:]]
    else:
        # print("there are phone exclude list : %s"%syllable)
        return [syllable]

def adjustPinyin(pinyin_list):
    
    syllable_list = []
    for item in pinyin_list:
        syllable_list.append(convertSyllable(item[0]))
    return syllable_list

def pinyinBiaobeiStyle(text):

    syllable_list = []
    pinyin_list = pinyin(text, style=Style.TONE3)
    for item in pinyin_list:
        syllable_list.append(convertSyllable(item[0]))
    return syllable_list