from asyncore import read
import tempfile
import jieba.analyse as analyse
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import colors
from PIL import Image
import numpy as np
import pandas as pd
import imageio as ima  # 读入图片文件
# from snownlp import SnowNLP
from translate import Translator


def read_csv(address):

    data = pd.read_csv(address,
                       error_bad_lines=False, usecols=['正文', '日期'])
    # print(data.info())
    t = np.array(data)
    data = t.tolist()
    print(np.shape(data))

    return data


def merge_by_year(data, year):
    # 将日期截取为年
    for i in data:
        i[1] = int(i[1][0:4])
    sorted(data, key=lambda x: x[1])
    # 将相同年份的数据合并
    dt = list()
    for y in year:
        dt.append([y])

    for j in range(len(dt)):
        s = ''
        for i in data:
            if i[1] == dt[j][0] and type(i[0]) == str and '青年' in i[0]:
                s += i[0]
        dt[j].append(s)

    return dt  # 返回list


def read_stopwords():
    # stopwords
    stop_word = []
    with open(r"./dependence/stopwords.txt", "r", encoding="utf-8") as f:
        for line in f:
            if len(line) > 0:
                stop_word.append(line.strip())  # 进行追加时将字符串前后的空格去掉
    return stop_word


def clean_text(dt, stop_word):
    # 对文本进行分词
    for i in dt:
        i[1] = jieba.lcut(i[1], cut_all=False)  # 使用精确模式进行分词
    # 移除stopwords
    for seg in dt:
        tmp = []
        for word in seg[1]:
            if word not in stop_word and type(word) is str:
                tmp.append(word)
        seg[1] = tmp

    return dt

# 提取关键词


def extract_mainWord(dt):

    for i in range(len(dt)):
        dt[i][1] = " ".join(dt[i][1]).replace("\n", " ")
        # print(dt[i][1])

    # 方式一：
    for i in range(len(dt)):
        x = " ".join(jieba.analyse.textrank(
            dt[i][1], topK=150, withWeight=False))
        dt[i][1] = x  # 关键词追加到列表的最后
        print(dt[i][0])
        print(x)
    # 方式二：
    # for i in range(len(dt)):
    #     x = " ".join(jieba.analyse.extract_tags(
    #         dt[i][1], topK=20, withWeight=True, allowPOS=()))
    #     dt[i].append(x)  # 关键词追加到列表的最后

    return dt


def draw(path_pic, dt):
    background = Image.open(path_pic)
    images = np.array(background)
    wc = WordCloud(font_path='./dependence/msyh.ttc', background_color="white", mask=images,
                   max_words=4000, contour_width=0.5, contour_color="white")
    wc.generate(dt[1])
    # 显示词图云
    plt.imshow(wc)
    # 取消坐标
    plt.clf()
    plt.imshow(wc)
    plt.axis('off')
    plt.title(str(dt[0]))
    plt.show()


def trans(seg):
    # 在任何两种语言之间，中文翻译成英文
    translator = Translator(from_lang="chinese", to_lang="english")
    tmp = list()
    for i in seg:
        translation = translator.translate(i)
        tmp.append(translation)
        print(translation)

    return tmp


if __name__ == '__main__':

    # 读取数据
    address = './weibo/中国青年网/2748597475.csv'
    data = read_csv(address)

    # 年份
    year = [i for i in range(2012, 2023)]
    # 按年份合并数据
    dt = merge_by_year(data, year)

    # 文本分词并去除stopwords
    stop_word = read_stopwords()
    dt = clean_text(dt, stop_word)

    # 关键词提取
    dt = extract_mainWord(dt)

    # 存储为csv
    name = ['year', 'mainwords']
    after = pd.DataFrame(columns=name, data=dt)
    after.to_csv('./after.csv', encoding='utf_8_sig')

    # 词云图
    path_pic = "./dependence/3.jpg"

    # for i in range(len(dt)):
    #     draw(path_pic, dt[i])
