# -*- coding: UTF-8 -*-
import os
import sys
import io
import re
import wave

from labformat import tree, show
from labcnp import LabNode, LabGenerator
from pinyin_biaobeiset import pinyinBiaobeiStyle, syllableSeperate
phone_no_syn = ['sp1','sil']

class Data:
    def __init__(self):
        #----------------- origin data ----------------------
        self.name=None
        self.text=None
        self.syn_str=None
        self.times=None
        #----------------------------------------------------

        #----------------- generated data -------------------
        self.words=None
        self.syllables=[]
        self.num_syn=None
        self.rhythms=None
        self.phones=None
        self.pose=None
        self.phs_type=None
        #----------------------------------------------------

class Biaobei:
    def __init__(self, phonelabeling="PhoneLabeling",prosodylabeling="ProsodyLabeling/000001-010000.txt"):
        self.label_data_list = []
        self._readOriginFile(phonelabeling, prosodylabeling)

    def _readProsodyLabeling(self, prosodylabelingtext):
        txtfile=open(prosodylabelingtext)
        prosodylabeling=txtfile.read().decode('gbk')
        txtfile.close()
        prosodylabeling_list=prosodylabeling.splitlines()
        for i in range(len(prosodylabeling_list)/2):
            one = Data()

            # first line
            name_and_text = prosodylabeling_list[2*i].strip().split("\t")
            one.name = name_and_text[0]
            one.text = name_and_text[1]
            # second line
            one.syn_str = prosodylabeling_list[2*i+1].strip()
            one.num_syn = len(one.syn_str.split(" "))
            one.rhythms = re.findall('#\d', one.text)
            
            # one.text still include Chinese character, just change tmp_text to obtain one.words
            tmp_text = one.text            
            for s in [u'（',u'）',u'…', u'；',u'—',u'……',u'？', u'、', u'，', u'。', u'“', u'”', u'-',u':',u'：', u'！']:
                tmp_text = tmp_text.replace(s, u'')
            one.words = re.split('#\d',tmp_text)[:-1]
            
            self.label_data_list.append(one)
        
        print(prosodylabelingtext)


    # read a interval file to get time message
    def _readOneInterval(self, interval_file_path, one_label_data):
        debug = False
        times = []
        phones = []
        
        interval_file = open(interval_file_path)
        contents = interval_file.read()
        interval_file.close()
        contents_list = contents.splitlines()
        i = 0
        for c in contents_list:
            c = c.strip()
        for i in range(len(contents_list)):
            if re.match('"IntervalTier"',contents_list[i]):
                break
        
        if i != 0:
            # phone start index 
            # notice the order: phone_start phone_stop phone
            baseindex = i+5
            file_phone_num = int(contents_list[i+4])
            for i in range(file_phone_num):
                phone_start = contents_list[baseindex + 3*i + 0]
                phone_stop  = contents_list[baseindex + 3*i + 1]
                phone = contents_list[baseindex + 3*i + 2].replace('\"', '')

                if debug:print('phone: %s\tstart: %-20s stop: %-20s'%(phone,phone_start,phone_stop))
                
                times.append([phone_start, phone_stop])
                phones.append(phone)
        else:
            print("error interval file format.")
            sys.exit()
        
        one_label_data.times = times
        one_label_data.phones = phones


    # read all interval file
    def _readPhoneLabeling(self, phonelabeling):
        
        for x in self.label_data_list:
            interval_file_path = os.path.join(phonelabeling, x.name + ".interval")
            self._readOneInterval(interval_file_path, x)
        return


    def _readOriginFile(self, phonelabeling, prosodylabeling):

        self._readProsodyLabeling(prosodylabeling)
        self._readPhoneLabeling(phonelabeling)   
        print("data list length : %d"%len(self.label_data_list))

    def showOneData(self, one_data):

        print("\nname: %s length: %d"%(type(one_data.name),len(one_data.name)))
        print(one_data.name)
        print("\ntext: %s length: %d"%(type(one_data.text),len(one_data.text)))
        print(one_data.text)
        print("\ntimes: %s length: %d"%(type(one_data.times),len(one_data.times)))
        for t in one_data.times:
            print("\t" + str(t))
        print("\nwords: %s length: %d"%(type(one_data.words),len(one_data.words)))
        print(one_data.words)
        print("\nsyllables: %s length: %d"%(type(one_data.syllables),len(one_data.syllables)))
        print(one_data.syllables)
        print("\nsyn_str: %s length: %d"%(type(one_data.syn_str),len(one_data.syn_str)))
        print(one_data.syn_str)
        print("\nrhythms: %s length: %d"%(type(one_data.rhythms),len(one_data.rhythms)))
        print(one_data.rhythms)
        print("\nphones: %s length: %d"%(type(one_data.phones),len(one_data.phones)))
        print(one_data.phones)
        print("\nphs_type: %s length: %d"%(type(one_data.phs_type),len(one_data.phs_type)))
        print(one_data.phs_type)
        print("\n")


    def adjustCheckData(self, tim = True, syl = True, ph = True):
        # TODO mergeing checkDuration and checkPhone to adjustCheckData
        for x in self.label_data_list:
            
            # adjust time format
            forward_time = 0
            phone_inx = 0
            for t in x.times:
                # notice : time point need to time % 50000 == 0
                t[0] = int((float(t[0])*10000000//50000)*50000)
                t[1] = int((float(t[1])*10000000//50000)*50000)
                if t[0] < t[1] and forward_time <= t[0]:
                    pass
                else:
                    print('time message error : %s'%x.name)
                    print('phone: %s t-1[1]: %d  t[0]: %d t[1]: %d'%(x.phones[phone_inx], forward_time, t[0], t[1]))
                    # sys.exit()
                forward_time = t[1]
                phone_inx += 1
            
            # generate phs_type
            x.phs_type = ['a'] * len(x.phones)
            # and prepare tmp_phone that no 'sil' and 'sp1' phones list
            tmp_phone = []
            for i in range(len(x.phones)):
                if not x.phones[i] in phone_no_syn:
                    tmp_phone.append(x.phones[i])
                elif x.phones[i] == 'sil':
                    x.phs_type[i] = 's'
                elif x.phones[i] == 'sp1':
                    x.phs_type[i] = 'd'
            
            # generate syllables
            if tmp_phone[0][-1].isdigit():
                x.syllables.append([tmp_phone[0]])
            i = 0
            while i < len(tmp_phone)-1:
                j = i+1
                if tmp_phone[i][-1].isdigit() and tmp_phone[j][-1].isdigit():
                    x.syllables.append([tmp_phone[j]])
                elif (not tmp_phone[i][-1].isdigit()) and tmp_phone[j][-1].isdigit():
                    x.syllables.append([tmp_phone[i],tmp_phone[j]])
                else:
                    pass
                i += 1
            
            # generate poses
            x.poses = ['n'] * len(x.words)

            # change #2 to #1
            for k in range(len(x.rhythms)):
                if x.rhythms[k] == u'#2':
                    x.rhythms[k] = u'#1'
                # elif x.rhythms[k] == u'#1':
                    # x.rhythms[k] = u'#0'
        print("adjust data done.")

#------------------------------------------------------------------------------ class end



def getTextForTacotron(csv_filename):
    data = Biaobei()
    if os.path.exists(csv_filename):
        os.system("rm " + csv_filename)
    csv_file = open(csv_filename,'a')
    for x in data.label_data_list:
        line = x.name + "|" + x.syn_str + "\n"
        csv_file.write(line)
    csv_file.close()
    print("get biaobei dataset text : %s"%csv_filename)


def drawProgressBar(indx, length, barLen = 20):
    percent = float(indx)/length
    sys.stdout.write("\r")
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "="
        else:
            progress += " "
    sys.stdout.write("[%s] <<< %d/%d (%d%%)" % (progress, indx, length, percent * 100))
    sys.stdout.flush()
    if indx == length: sys.stdout.write('\n')


def generateHTSlabel(labels_dir):
    data = Biaobei()
    data.adjustCheckData()

    if not os.path.exists(labels_dir):
        os.mkdir(labels_dir)
    print("generate...")
    index_for_bar = 0
    for one_data in data.label_data_list[:1]:
        data.showOneData(one_data)
        label = ''    
        phone = tree(one_data.words, one_data.rhythms, one_data.syllables, one_data.poses, one_data.phs_type)
        for ph_list in LabGenerator(phone, one_data.rhythms, one_data.times):
            label += ph_list + '\n'
        current_label_path = os.path.join(labels_dir, one_data.name + ".lab")
        current_label_file = open(current_label_path, "w")
        current_label_file.write(label)
        current_label_file.close()
        index_for_bar += 1
        drawProgressBar(index_for_bar, len(data.label_data_list))
    print("all HTS labels generate done.\n")

def getPhoneDict():
    data = Biaobei()
    data.adjustCheckData()
    phone_constant_set = set()
    phone_yunmu_set = set()
    for one_data in data.label_data_list:
        for phone in one_data.phones:
            if phone[-1].isdigit(): 
                phone_yunmu_set.add(phone[:-1])
            else:
                phone_constant_set.add(phone)
    print(phone_yunmu_set)
    print(phone_constant_set)

def checkpinyin():
    data = Biaobei()
    data.adjustCheckData()
    count = 0
    line = ''
    f = open('debug.txt', 'w')
    for one_data in data.label_data_list:
        text_pinyin = ''
        for w in one_data.words:
            text_pinyin += w
        # print(text_pinyin)
        # print(one_data.syllables)
        pinyin_list = pinyinBiaobeiStyle(text_pinyin)
        # print(pinyin_list)
        phone_r = ['ger','zher','ter','vanr','anr','uor','inr','ongr','iiir','enr','uanr','ingr','iar','ur','ir','our','iangr','ueir','uair','ianr','iour','air','ar','uenr','aor']
        frond_syllable = '   '
        
        for i in range(len(pinyin_list)):
            
            syllables = one_data.syllables
            if i < len(syllables):
                if len(syllables[i]) == 1:
                    set_syllable = syllables[i][0]
                else:
                    set_syllable = syllables[i][0] + syllables[i][1]
            
            if frond_syllable[0:-1] in phone_r:
                syllables.insert(i,[])
                set_syllable = ' '
            elif frond_syllable[1:-1] in phone_r or frond_syllable[2:-1] in phone_r:
                syllables.insert(i,[])
                set_syllable = ' '

            if set_syllable[:-1] != pinyin_list[i][:-1] and set_syllable != ' ':
                if set_syllable[-2] != 'r':
                    count += 1
                    line += text_pinyin[i] + '\t' + set_syllable + '\t' + pinyin_list[i] + '\n'
                    f.write(line.encode('utf8'))
                    print(line.strip())
                    line = ''
            frond_syllable = set_syllable
            
    f.close()
    print(count)

    # one_part = set()
    # for one_data in data.label_data_list:
    #     for syl in one_data.syllables:
    #         if len(syl) == 1:
    #             # print(syl)
    #             one_part.add(syl[0][:-1])

    # phone_set_r = [#'er',
    # 'vanr','anr','uor','inr','ongr','iiir','enr','uanr','ingr','iar','ur','ir','our','iangr','ueir','uair','ianr','iour','air','ar','uenr','aor']
    # for one_data in data.label_data_list:
    #     w = ''
    #     for one_word in one_data.words:
    #         w += one_word
    #     pinyin_list = pinyin(w, style=Style.TONE3)
    #     # print(pinyin_list)
    #     syllables = one_data.syllables
    #     for i in range(len(syllables)):
            
    #         if len(syllables[i]) == 1:
    #             set_syllable = syllables[i][0]
    #         else:
    #             set_syllable = syllables[i][0] + syllables[i][1]

    #         if set_syllable[:-1] in phone_set_r:
    #             print(w[i] + ' ' + set_syllable + ' ' + pinyin_list[i][0])


def checkSyllableSeperate():
    data = Biaobei()
    data.adjustCheckData()
    count = []
    for one_data in data.label_data_list:
        text_pinyin = ''
        for w in one_data.words:
            text_pinyin += w
        print(text_pinyin)
        if len(re.findall(u'儿',text_pinyin)):
            continue
        print(one_data.syllables)
        pinyin_list = pinyinBiaobeiStyle(text_pinyin)
        syllables_sep = []
        for p in pinyin_list:
            syllables_sep.append(syllableSeperate(p))
        print(syllables_sep)
        if len(syllables_sep) != len(one_data.syllables):
            assert False
        for i in range(len(syllables_sep)):
            if len(syllables_sep[i]) != len(one_data.syllables[i]):
                count.append([text_pinyin,syllables_sep,one_data.syllables])
    print('\n\n')
    for c in count:
        print(c[0])
        print(c[1])
        print(c[2])
if __name__ == '__main__':

    # getPhoneDict()

    if True:
        checkSyllableSeperate()
        # generateHTSlabel('labels')
    else:
        getTextForTacotron("metadata.csv")


#-----------------------------------------------------------------------------------------------------


# def checkPhone(question_path, data):
#     question = open(question_path, 'r')
#     questr = str(question.read())
#     # print(questr)
#     phone_set = set()
    
#     for one_data in data.label_data_list:
#         for p in one_data.phones:
#             if p[-1].isdigit():
#                 phone_set.add(p[:-1])
#             else:
#                 phone_set.add(p)
    
#     for p in phone_set:
#         if re.match('[]*' + p + '[]*', questr):
#             pass
#         else:
#             print('err')
#             sys.exit()
    # print(phone_set)

# def checkDuration(wav_dir, data):
   
#     for one_data in data.label_data_list:
#         wav_path = os.path.join(wav_dir, one_data.name + '.wav')
#         wav_file = wave.open(wav_path, 'rb')
#         channels, width, framerate, frames = wav_file.getparams()[:4]
#         wav_duration = int(frames / (framerate*1.0) * 10000000)
#         if one_data.times[-1][1] <= wav_duration:
#             pass
#         else:
#             print('%s label_time %d  wave duration %d'%(one_data.name,one_data.times[-1][1],wav_duration))
#             # one_data.times[-1][1] = wav_duration
        
#         forward_time = 0
#         for t in one_data.times:
#             if t[0] < t[1] and forward_time <= t[0]:
#                 pass
#             else:
#                 print('time message error : %s'%one_data.name)
#                 print('f: %d  t[0]: %d t[1]: %d'%(forward_time, t[0], t[1]))
#             forward_time = t[1]