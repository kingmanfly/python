import itchat
from wxpy import *  #wxpy 在 itchat 的基础上，通过大量接口优化提升了模块的易用性，并进行丰富的功能扩展。
import matplotlib.pyplot as plt
import pandas as pd
import numpy
import re
import io
import jieba
import numpy as np
from wordcloud import WordCloud,ImageColorGenerator
from scipy.misc import imread
import PIL

def write_txt_file(path, txt):
    '''
    写入txt文本
    '''
    with open(path, 'a', encoding='utf-8', newline='') as f:
        f.write(txt)

def read_txt_file(path):
    '''
    读取txt文本
    '''
    with open(path, 'r', encoding='utf-8', newline='') as f:
        return f.read()

def login():
    # 初始化机器人，扫码登陆
    bot = Bot(cache_path=True)

    # 获取所有好友
    my_friends = bot.friends()

    # print(type(my_friends))
    return my_friends

def draw_sex_ratio(datas,count):
    for key in datas.keys():
        plt.bar(key, datas[key])
    plt.legend()
    plt.xlabel('sex')
    plt.ylabel('rate')
    plt.title('The number of my friends is ' + str(count))
    plt.show()

def show_sex_ratio(friends):
    # 使用一个字典统计好友男性和女性的数量
    total = len(friends[1:])
    print("好友总数：" + str(total))
    if total == 0:
        return
    
    sex_dict = {'male': 0, 'female': 0, 'other': 0}

    for friend in friends[1:]:
        # 统计性别
        if friend.sex == 1:
            sex_dict['male'] += 1
        elif friend.sex == 2:
            sex_dict['female'] += 1
        else:
            sex_dict['other'] += 1

    print(sex_dict)
    print("男性好友：%.2f%%" % (float(sex_dict['male']) / total * 100) + "\n" +
        "女性好友：%.2f%%" % (float(sex_dict['female']) / total * 100) + "\n" +
        "不明性别的好友：%.2f%%" % (sex_dict['other'] / total * 100) + "\n"
    )
    # draw_sex_ratio(sex_dict,total)

def show_area_distribution(friends):
    # 使用一个字典统计各省好友数量
    province_dict = {'北京': 0, '上海': 0, '天津': 0, '重庆': 0,
        '河北': 0, '山西': 0, '吉林': 0, '辽宁': 0, '黑龙江': 0,
        '陕西': 0, '甘肃': 0, '青海': 0, '山东': 0, '福建': 0,
        '浙江': 0, '台湾': 0, '河南': 0, '湖北': 0, '湖南': 0,
        '江西': 0, '江苏': 0, '安徽': 0, '广东': 0, '海南': 0,
        '四川': 0, '贵州': 0, '云南': 0,
        '内蒙古': 0, '新疆': 0, '宁夏': 0, '广西': 0, '西藏': 0,
        '香港': 0, '澳门': 0}

    # 统计省份
    for friend in friends:
        if friend.province in province_dict.keys():
            province_dict[friend.province] += 1

    # 为了方便数据的呈现，生成JSON Array格式数据
    data = []
    for key, value in province_dict.items():
        data.append({'name': key, 'value': value})

    print(data)

def parse_signature(friends):
    siglist = []
    for friend in friends[1:]:
        # 过滤掉不要的
        # signature = friend.signature.strip().replace("span", "").replace("class", "").replace("emoji","")
        # rep = re.compile("1f\d+w*|[<>/=]")
        # signature = rep.sub("", signature)
        # siglist.append(signature)

        # 只要需要的汉字
        # 对数据进行清洗，将标点符号等对词频统计造成影响的因素剔除
        pattern = re.compile(r'[一-龥]+')
        filterdata = re.findall(pattern, friend.signature)
        siglist.append(" ".join(filterdata))

    text = "".join(siglist)
    with io.open('signatures.txt', 'a', encoding='utf-8') as f:
        wordlist = jieba.cut(text, cut_all=True)
        word_space_split = " ".join(wordlist)
        f.write(word_space_split)
        f.close()

def draw_signature():
    text = open(u'signatures.txt', encoding='utf-8').read()
    # bg_pic = imread('girl.jpg')
    alice_mask = np.array(PIL.Image.open('man.png'))
    my_wordcloud = WordCloud( background_color="white",
            mask = alice_mask,
            max_words = 2000,
            max_font_size = 60,
            font_path="C:\\Windows\\Fonts\\STFANGSO.ttf",#不加这一句显示口字形乱码
            scale = 2).generate(text)
    # image_colors = ImageColorGenerator(alice_mask)
    # plt.imshow(my_wordcloud.recolor(color_func=image_colors))
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()
    my_wordcloud.to_file('output.png')

def main():
    friends = login()
    show_sex_ratio(friends)
    show_area_distribution(friends)
    parse_signature(friends)
    draw_signature()

if __name__ == '__main__':
    '''
    入口
    '''
    main()