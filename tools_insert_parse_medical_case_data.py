import json
import time
import os
from pypinyin import pinyin, lazy_pinyin

# path = "medical_case_data_txt"
path = "other"
log = "log.txt"


def get_current_time():
    return time.strftime('%Y-%m-%d %X', time.localtime(time.time()))


def clean(s):
    return s.replace("\\", "\\\\").replace("\"", "\\\"").replace("\r", "").replace(",", "，")


def get_val(dict, key):
    if key in dict.keys() and clean(dict[key]) != "缺":
        return clean(dict[key])
    else:
        return ""


def get_name_gender_birthday(s):
    arr = s.split(" ")
    ret_arr = []
    for item in arr:
        if item.strip() != "":
            ret_arr.append(item)
    # it's a triky here
    while len(ret_arr) < 3:
        ret_arr.append(" ")

    return ret_arr


def get_acronym(case_title):
    """
    获取字符串的首字母
    :param str_data: 字符串
    :return: 字符串
    """
    return "".join([i[0][0] for i in pinyin(case_title)])


def load_log(log):
    f_s = set()
    if os.path.exists(log):
        with open(log) as indata:
            for line in indata:
                f_s.add(line.strip().split()[0])
    return f_s


def write_into_file(f, content):
    with open(f, 'a+') as f:
        f.write("%s\n" % content)


print(path)

# print(path)
# logf = load_log(log)
for root, dirs, files in os.walk(path):
    for file in files:
        # if file in logf:
        #	continue
        jsonfile = os.path.join(root, file)
        print(jsonfile)

        # exit(0)
        cnt = 0
        values_str = ""
        # jsonfile = "医案+曹玉山.txt"
        with open(jsonfile, 'r', encoding='UTF-8') as indata:
            # print(indata.read())
            json_dict = json.load(indata)
            # print("total records: %s" % len(json_dict))

            for key, rcd in json_dict.items():
                # print(rcd)

                t = get_current_time()
                case_title = rcd['医案标题']
                doctor_name = rcd['医生姓名']
                department = rcd['科别']
                patient_name = ""
                gender = ""
                birth_day = ""
                patient_name, gender, birth_day = get_name_gender_birthday(rcd['医案']['患者姓名'])

                treatment_time = get_val(rcd['医案'], '就诊时间')
                solar_term = get_val(rcd['医案'], '节气')
                patient_description = get_val(rcd['医案'], '主诉')
                current_illness_history = get_val(rcd['医案'], '现病史')
                tongue_symptom = "%s; %s" % (get_val(rcd['医案'], '舌质'), get_val(rcd['医案'], '舌苔'))
                pulse_symptom = get_val(rcd['医案'], '脉象')
                current_symptom = get_val(rcd['医案'], '刻下症')
                illness_history = get_val(rcd['医案'], '既往史')
                personal_history = get_val(rcd['医案'], '个人史')
                allergy_history = get_val(rcd['医案'], '过敏史')
                marriage_history = get_val(rcd['医案'], '婚育史')
                family_history = get_val(rcd['医案'], '家族史')
                assist_exam = get_val(rcd['医案'], '辅助检查')
                symptom_analysis = get_val(rcd['医案'], '辨证分析')
                tcm_diagnosis = get_val(rcd['医案'], '中医诊断')
                wm_diagnosis = get_val(rcd['医案'], '西医诊断')
                tcm_syndrome = get_val(rcd['医案'], '中医证候')
                therapeutic = get_val(rcd['医案'], '治则治法')
                prescription = get_val(rcd['医案'], '方名')
                composition = get_val(rcd['医案'], '组成')
                usages = get_val(rcd['医案'], '用法')
                doctor_comments = get_val(rcd['医案'], '医嘱')
                acupuncture = get_val(rcd['医案'], '针灸')
                point_select = get_val(rcd['医案'], '选穴')
                massage = get_val(rcd['医案'], '推拿')

                # "医生姓名": "蔡小荪",
                # "科别": "妇科",
                # "中医诊断": "滑胎,经行吐衄",

                # print(doctor_name + '_' + department + '_' + tcm_diagnosis)

                title_department_tcm_diagnosis = case_title + '_' + department + '_' + tcm_diagnosis

                # print(case_title)    # 标题
                # print("中医诊断：", tcm_diagnosis, ",", "方名：", prescription, ",", "组成：", composition, "\n")      # 中医诊断、方名、组成


                a = composition.split('，')


                import re

                # 序号_标题_科别
                # 001_crkbygsyxhxqffzlbbf_其他
                number = str(cnt + 1).zfill(3)
                case_title = re.sub('[^a-zA-Z]', '', get_acronym(case_title))

                final1 = number + '_' + case_title + '_' + department

                # 患病节气_主诉_舌质_舌苔_脉象_刻下症_既往史（字符串结尾的中文符号未删除掉）
                # cfhd5t_zctmbbbyyy_红_少苔_弦细_左侧头面部白斑，无明显自觉症状，平素偏食，易腹痛、便溏。_无肝炎及结核病史，无系统性疾病。
                solar_term = get_acronym(solar_term)
                patient_description = re.sub('[^a-zA-Z0-9]', '', get_acronym(patient_description))
                tongue_symptom = tongue_symptom.replace('; ', '_')

                final2 = solar_term + '_' + patient_description + '_' + tongue_symptom + '_' + pulse_symptom + '_' + \
                         current_symptom + '_' + illness_history

                # 中/西医诊断(中/西医诊断病名拼接)_中医证候(病状)_治则治法(患病部位_治疗方法)_方名(处方名)_组成(处方方剂组成成分及分量)_用法
                # 白驳风/白癜风_肝肾不足_患病部位_补益肝肾，养血活血祛风_自拟方_补骨脂9g，沙苑子9g，菟丝子9g，丹参20g，煅自然铜6g，北沙参9g，玉竹9g，首乌9g，黑芝麻9g，浮萍6g，刺蒺藜9g，生甘草6g_40剂，水煎服
                # 从治则法治提取患病部位，需要构造字典
                #print(a)
                str1 = ""
                for i in a:
                    i1 = re.findall(r'[^0-9a-z，]+', i)
                    # print(i1)
                    if len(i1) > 0:
                        str1 += i1[0] + " "
                    # #for j in i1:
                    #     # print(j, end=" ")
                    #     composition = j
                    #     #print(composition)
                    #     str += composition + ";"
                #print(str)
                # composition = re.sub(r'[0-9a-z]', '', str(a))

                final3 = tcm_diagnosis + '/' + wm_diagnosis + '_' + tcm_syndrome + '_' + 'ERROR患病部位' '_' + therapeutic + '_' + \
                             prescription + '_' + str1 + '_' + usages

                # print(final3)

                final = final1 + '\t\t' + final2 + '\t\t' + final3
                print(final)








                # final = final1 + '\t\t' + final2 + '\t\t' + final3
                # with open(r"other\data.txt", "w") as f:
                #     f.write(final)




                # print(title_department_tcm_diagnosis, b)
                cnt += 1
                # exit(0)


            print("get records: %s" % cnt)

    # log this file
    # write_into_file(log, "%s %s" % (file, cnt))
