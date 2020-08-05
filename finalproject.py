from bs4 import BeautifulSoup
import re
import requests
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
import copy
import nltk 
from nltk.corpus import stopwords 
nltk.download('punkt') 
nltk.download("stopwords") 
from nltk.tokenize import word_tokenize 
from matplotlib import animation as animation #animation
import numpy as np

font = FontProperties(fname=r'./GenYoGothicTW-Regular.ttf')  # 中文字體匯入


def chinese_hour(url):  # 爬標題
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        stories = soup.find_all('a', class_='DY5T1d')
    return len(stories)


def new_rank():  # 排名
    # 肺炎、香港、立法院、高雄市長補選、三倍券、體育、財經
    twu = ['https://news.google.com/search?q=%E8%82%BA%E7%82%8E%20when%3A1h&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',
           'https://news.google.com/search?q=%E9%A6%99%E6%B8%AF%20when%3A1h&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',
           'https://news.google.com/search?q=%E7%AB%8B%E6%B3%95%E9%99%A2%20when%3A1h&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',
           'https://news.google.com/search?q=%E9%AB%98%E9%9B%84%E5%B8%82%E9%95%B7%E8%A3%9C%E9%81%B8%20when%3A1h&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',
           'https://news.google.com/search?q=%E4%B8%89%E5%80%8D%E5%88%B8%20when%3A1h&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',
           'https://news.google.com/search?q=%E9%AB%94%E8%82%B2%20when%3A1h&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',
           'https://news.google.com/search?q=%E8%B2%A1%E7%B6%93%20when%3A1h&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant']
    taiwan, label, rank = [], [], []
    for i in range(7):
        taiwan.append(chinese_hour(twu[i]))
    a = copy.deepcopy(taiwan)
    labels = ['Covid-19', 'HK', 'legislature', 'election', 'voucher', 'PE', 'finance']
    taiwan.sort(reverse=True)
    for i in range(len(taiwan)):
        for j in range(7):
            if (taiwan[i] == a[j]) and (taiwan[i] not in label):
                label.append(labels[j])
                rank.append(j + 1)
    taiwan_lab = label  # x軸標籤
    lab_num = np.array(taiwan)  # y軸數據
    plt.xlabel('種類', fontproperties=font, size=12)
    plt.ylabel('新聞量', fontproperties=font, size=12)
    plt.title('新聞量分析圖', fontproperties=font, size=14)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.bar(x=taiwan_lab, height=lab_num,
            color='#084887',
            edgecolor="#FAB419",
            linewidth=2)
    plt.show()
    return taiwan, label, rank


def check_page_number():  # 找最後一頁的頁數
    res = requests.get(url_1 + name + url_2 + "1")
    soup = BeautifulSoup(res.text, 'html.parser')
    for entry in soup.select(
            '.css-1s4ayab-StyledListItem-PageButtonListItem.e4i2y2x3 div .css-16didf7-StyledButtonContent.e1b2sq420'):
        pn = str(entry.text.strip())
    return pn


def web_crawler():  # 爬標題
    i = 1
    while 1:
        res = requests.get(url_1 + name + url_2 + str(i))
        res.encoding = "utf8"  # 解決標點符號亂碼問題
        soup = BeautifulSoup(res.text, 'html.parser')
        for entry in soup.select('.css-johpve-PromoLink.ett16tt7 span'):
            list_1.append(entry.text.strip())
        if i == end_page:
            break
        i = i + 1


def plotdata(plt, data):  # 模式1畫圖-1
    x = [p[0] for p in data]
    y = [p[1] for p in data]
    plt.style.use('bmh')
    plt.yticks([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 120])
    plt.xticks(rotation=80)
    plt.xlim(0,24)
    plt.ylim(0,104)
    plt.xlabel('Time')
    plt.ylabel('number of news')
    plt.plot(x, y, '-o', color='b')

def plotdata1(plt, data):  # 模式1畫圖-2
    x = [p[0] for p in data]
    y = [p[1] for p in data]
    plt.style.use('bmh')
    plt.yticks([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 120])
    plt.xticks(rotation=80)
    plt.xlim(0,24)
    plt.ylim(0,104)
    plt.xlabel('Time')
    plt.ylabel('number of news')
    plt.plot(x, y, '-o', color='r')


while True:  # 防呆&確認模式
    print('1. 觀看國內與國外對於相同主題的新聞數量差異')
    print('2. 猜測國內不同主題的新聞數量名次')
    print('3. 分析新聞標題字詞出現程度')
    print('-' * 100)
    m = eval(input('請輸入想進入的模式:'))
    if m == 1 or m == 2 or m == 3:
        print('=' * 100, '\n')
        break
    else:
        print('\n無此模式，請重新輸入')
        print('=' * 100, '\n')

while m == 1 or m == 2 or m == 3:  # 進入模式
    if m == 1:
        print('歡迎進入模式1：觀看國內與國外對於相同主題的新聞數量差異\n')
        while True:
            print(
                '主題: 1.Taiwan, 2.Covid-19, 3.China, 4.Corona virus, 5.Donald Trump, 6.UK, 7.Hong Kong, 8.Election, 9.EU, 10.Tesla')
            topic = eval(input('請根據以上10個主題代碼，選擇一個你想觀看的主題：'))
            if topic == 1:
                # Taiwan
                taiwan_1=[('07/21',44),('16:00',48),('17:00',74),('18:00',25),('19:00',24),('20:00',37),('21:00',55),('22:00',58),('23:00',54),('07/22,00:00',58),('01:00',52),('02:00',56),
                          ('03:00',64),('04:00',52),('05:00',62),('06:00',52),('07:00',47),('08:00',55),('09:00',48),('10:00',73),('11:00',45),('12:00',46),('13:00',59),('14:00',68),('15:00',56)]

                taiwan_2=[('07/21',57),('16:00',59),('17:00',71),('18:00',58),('19:00',58),('20:00',54),('21:00',47),('22:00',50),('23:00',35),('07/22,00:00',23),('01:00',28),('02:00',21),
                          ('03:00',23),('04:00',16),('05:00',54),('06:00',63),('07:00',28),('08:00',50),('09:00',50),('10:00',56),('11:00',52),('12:00',64),('13:00',64),('14:00',59),('15:00',50)]
               
                fig, ax = plt.subplots()
                
                def animate(i):#update 
                    plotdata(plt,taiwan_1[:i])
                    plotdata1(plt,taiwan_2[:i])
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('Taiwan')

                def init():#inition:空畫布
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('Taiwan')
                    
                ani=animation.FuncAnimation(fig=fig,  #動畫繪製的figure
                           func=animate,              #自定義動畫函數
                           frames=25,                 #動畫長度
                           init_func=init,            #自定義開始幀
                           interval=250,              #更新頻率(以秒計)
                           blit=False)                #更新所有點還是僅更新產生變化的點
                plt.show()
                break

            elif topic == 2:
                # covid19
                covid19_1=[('07/21',55),('16:00',100),('17:00',87),('18:00',80),('19:00',94),('20:00',100),('21:00',100),('22:00',76),('23:00',81),('07/22,00:00',93),('01:00',81),('02:00',82),
                           ('03:00',74),('04:00',92),('05:00',100),('06:00',87),('07:00',91),('08:00',100),('09:00',81),('10:00',81),('11:00',88),('12:00',90),('13:00',100),('14:00',82),('15:00',80)]

                covid19_2=[('07/21',44),('16:00',66),('17:00',64),('18:00',46),('19:00',56),('20:00',52),('21:00',63),('22:00',52),('23:00',53),('07/22,00:00',34),('01:00',51),('02:00',38),
                           ('03:00',44),('04:00',35),('05:00',49),('06:00',47),('07:00',50),('08:00',45),('09:00',55),('10:00',51),('11:00',53),('12:00',56),('13:00',66),('14:00',54),('15:00',56)]
                
                fig, ax = plt.subplots()
                
                def animate(i):#update 
                    plotdata(plt,covid19_1[:i])
                    plotdata1(plt,covid19_2[:i])
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('Covid-19')

                def init():#inition:空畫布
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('Covid-19')
                    
                ani=animation.FuncAnimation(fig=fig,  #動畫繪製的figure
                           func=animate,              #自定義動畫函數
                           frames=25,                 #動畫長度
                           init_func=init,            #自定義開始幀
                           interval=250,              #更新頻率(以秒計)
                           blit=False)                #更新所有點還是僅更新產生變化的點
                plt.show()
                break

            elif topic == 3:
                # china
                china_1=[('07/21',30),('16:00',70),('17:00',68),('18:00',29),('19:00',48),('20:00',76),('21:00',84),('22:00',59),('23:00',46),('07/22,00:00',28),('01:00',37),('02:00',48),
                         ('03:00',37),('04:00',56),('05:00',42),('06:00',49),('07:00',51),('08:00',44),('09:00',62),('10:00',63),('11:00',41),('12:00',77),('13:00',67),('14:00',57),('15:00',70)]

                china_2=[('07/21',61),('16:00',78),('17:00',79),('18:00',71),('19:00',80),('20:00',79),('21:00',63),('22:00',68),('23:00',52),('07/22,00:00',34),('01:00',34),('02:00',55),
                         ('03:00',61),('04:00',33),('05:00',81),('06:00',70),('07:00',43),('08:00',60),('09:00',74),('10:00',75),('11:00',68),('12:00',68),('13:00',63),('14:00',61),('15:00',74)]
                
                fig, ax = plt.subplots()
                
                def animate(i):#update 
                    plotdata(plt,china_1[:i])
                    plotdata1(plt,china_2[:i])
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('China')

                def init():#inition:空畫布
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('China')
                    
                ani=animation.FuncAnimation(fig=fig,  #動畫繪製的figure
                           func=animate,              #自定義動畫函數
                           frames=25,                 #動畫長度
                           init_func=init,            #自定義開始幀
                           interval=250,              #更新頻率(以秒計)
                           blit=False)                #更新所有點還是僅更新產生變化的點
                plt.show()
                break

            elif topic == 4:
                # coronavirus
                coronavirus_1=[('07/21',61),('16:00',45),('17:00',86),('18:00',78),('19:00',63),('20:00',87),('21:00',66),('22:00',89),('23:00',71),('07/22,00:00',66),('01:00',65),('02:00',75),
                               ('03:00',56),('04:00',94),('05:00',52),('06:00',69),('07:00',81),('08:00',73),('09:00',79),('10:00',52),('11:00',65),('12:00',46),('13:00',62),('14:00',55),('15:00',88)]

                coronavirus_2=[('07/21',23),('16:00',26),('17:00',33),('18:00',39),('19:00',28),('20:00',28),('21:00',25),('22:00',25),('23:00',31),('07/22,00:00',12),('01:00',20),('02:00',14),
                               ('03:00',34),('04:00',7),('05:00',22),('06:00',37),('07:00',17),('08:00',27),('09:00',28),('10:00',27),('11:00',19),('12:00',31),('13:00',33),('14:00',21),('15:00',34)]
                
                fig, ax = plt.subplots()
                
                def animate(i):#update 
                    plotdata(plt,coronavirus_1[:i])
                    plotdata1(plt,coronavirus_2[:i])
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('Corona Virus')

                def init():#inition:空畫布
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('Corona Virus')
                    
                ani=animation.FuncAnimation(fig=fig,  #動畫繪製的figure
                           func=animate,              #自定義動畫函數
                           frames=25,                 #動畫長度
                           init_func=init,            #自定義開始幀
                           interval=250,              #更新頻率(以秒計)
                           blit=False)                #更新所有點還是僅更新產生變化的點
                plt.show()
                break

            elif topic == 5:
                # trump
                trump_1=[('07/21',21),('16:00',39),('17:00',32),('18:00',38),('19:00',29),('20:00',44),('21:00',45),('22:00',39),('23:00',32),('07/22,00:00',41),('01:00',38),('02:00',28),
                         ('03:00',30),('04:00',32),('05:00',28),('06:00',28),('07:00',24),('08:00',27),('09:00',27),('10:00',27),('11:00',40),('12:00',28),('13:00',22),('14:00',14),('15:00',36)]

                trump_2=[('07/21',18),('16:00',16),('17:00',15),('18:00',14),('19:00',13),('20:00',16),('21:00',8),('22:00',12),('23:00',12),('07/22,00:00',3),('01:00',9),('02:00',1),
                         ('03:00',1),('04:00',8),('05:00',11),('06:00',10),('07:00',10),('08:00',16),('09:00',23),('10:00',19),('11:00',15),('12:00',19),('13:00',12),('14:00',21),('15:00',16)]
                
                fig, ax = plt.subplots()
                
                def animate(i):#update 
                    plotdata(plt,trump_1[:i])
                    plotdata1(plt,trump_2[:i])
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('Donald Trump')

                def init():#inition:空畫布
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('Donald Trump')
                    
                ani=animation.FuncAnimation(fig=fig,  #動畫繪製的figure
                           func=animate,              #自定義動畫函數
                           frames=25,                 #動畫長度
                           init_func=init,            #自定義開始幀
                           interval=250,              #更新頻率(以秒計)
                           blit=False)                #更新所有點還是僅更新產生變化的點
                plt.show()
                break

            elif topic == 6:
                # uk
                uk_1=[('07/21',33),('16:00',84),('17:00',52),('18:00',29),('19:00',42),('20:00',91),('21:00',60),('22:00',41),('23:00',47),('07/22,00:00',91),('01:00',34),('02:00',74),
                      ('03:00',41),('04:00',72),('05:00',75),('06:00',62),('07:00',50),('08:00',25),('09:00',51),('10:00',24),('11:00',76),('12:00',81),('13:00',85),('14:00',75),('15:00',73)]

                uk_2=[('07/21',35),('16:00',44),('17:00',42),('18:00',31),('19:00',38),('20:00',39),('21:00',33),('22:00',27),('23:00',24),('07/22,00:00',14),('01:00',15),('02:00',22),
                      ('03:00',26),('04:00',14),('05:00',41),('06:00',25),('07:00',17),('08:00',43),('09:00',55),('10:00',47),('11:00',39),('12:00',39),('13:00',39),('14:00',34),('15:00',39)]
                
                fig, ax = plt.subplots()
                
                def animate(i):#update 
                    plotdata(plt,uk_1[:i])
                    plotdata1(plt,uk_2[:i])
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('UK')

                def init():#inition:空畫布
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('UK')
                    
                ani=animation.FuncAnimation(fig=fig,  #動畫繪製的figure
                           func=animate,              #自定義動畫函數
                           frames=25,                 #動畫長度
                           init_func=init,            #自定義開始幀
                           interval=250,              #更新頻率(以秒計)
                           blit=False)                #更新所有點還是僅更新產生變化的點
                plt.show()
                break

            elif topic == 7:
                # hk
                hk_1=[('07/21',16),('16:00',41),('17:00',41),('18:00',9),('19:00',29),('20:00',35),('21:00',43),('22:00',34),('23:00',13),('07/22,00:00',50),('01:00',20),('02:00',38),
                      ('03:00',14),('04:00',32),('05:00',33),('06:00',29),('07:00',34),('08:00',23),('09:00',32),('10:00',40),('11:00',30),('12:00',19),('13:00',47),('14:00',62),('15:00',43)]

                hk_2=[('07/21',61),('16:00',75),('17:00',72),('18:00',72),('19:00',74),('20:00',68),('21:00',75),('22:00',69),('23:00',47),('07/22,00:00',42),('01:00',38),('02:00',78),
                      ('03:00',84),('04:00',37),('05:00',82),('06:00',52),('07:00',45),('08:00',63),('09:00',84),('10:00',77),('11:00',72),('12:00',70),('13:00',64),('14:00',66),('15:00',67)]
                
                fig, ax = plt.subplots()
                
                def animate(i):#update 
                    plotdata(plt,hk_1[:i])
                    plotdata1(plt,hk_2[:i])
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('Hong Kong')

                def init():#inition:空畫布
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('Hong Kong')
                    
                ani=animation.FuncAnimation(fig=fig,  #動畫繪製的figure
                           func=animate,              #自定義動畫函數
                           frames=25,                 #動畫長度
                           init_func=init,            #自定義開始幀
                           interval=250,              #更新頻率(以秒計)
                           blit=False)                #更新所有點還是僅更新產生變化的點
                plt.show()
                break

            elif topic == 8:
                # election
                election_1=[('07/21',19),('16:00',26),('17:00',25),('18:00',32),('19:00',15),('20:00',15),('21:00',26),('22:00',34),('23:00',34),('07/22,00:00',32),('01:00',26),('02:00',43),
                            ('03:00',49),('04:00',4),('05:00',11),('06:00',26),('07:00',25),('08:00',25),('09:00',25),('10:00',27),('11:00',23),('12:00',25),('13:00',25),('14:00',20),('15:00',21)]

                election_2=[('07/21',8),('16:00',13),('17:00',8),('18:00',18),('19:00',9),('20:00',8),('21:00',4),('22:00',7),('23:00',6),('07/22,00:00',2),('01:00',6),('02:00',6),
                            ('03:00',6),('04:00',1),('05:00',8),('06:00',4),('07:00',6),('08:00',11),('09:00',9),('10:00',4),('11:00',3),('12:00',8),('13:00',4),('14:00',7),('15:00',5)]
                
                fig, ax = plt.subplots()
                
                def animate(i):#update 
                    plotdata(plt,election_1[:i])
                    plotdata1(plt,election_2[:i])
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('Election')

                def init():#inition:空畫布
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('Election')
                    
                ani=animation.FuncAnimation(fig=fig,  #動畫繪製的figure
                           func=animate,              #自定義動畫函數
                           frames=25,                 #動畫長度
                           init_func=init,            #自定義開始幀
                           interval=250,              #更新頻率(以秒計)
                           blit=False)                #更新所有點還是僅更新產生變化的點
                plt.show()
                break

            elif topic == 9:
                # eu
                eu_1=[('07/21',26),('16:00',27),('17:00',50),('18:00',29),('19:00',21),('20:00',36),('21:00',40),('22:00',37),('23:00',41),('07/22,00:00',32),('01:00',29),('02:00',35),
                      ('03:00',38),('04:00',26),('05:00',23),('06:00',40),('07:00',31),('08:00',25),('09:00',33),('10:00',28),('11:00',29),('12:00',25),('13:00',34),('14:00',47),('15:00',56)]
      
                eu_2=[('07/21',16),('16:00',23),('17:00',16),('18:00',18),('19:00',13),('20:00',16),('21:00',8),('22:00',15),('23:00',13),('07/22,00:00',6),('01:00',7),('02:00',21),
                      ('03:00',12),('04:00',8),('05:00',23),('06:00',12),('07:00',16),('08:00',29),('09:00',28),('10:00',22),('11:00',19),('12:00',24),('13:00',16),('14:00',16),('15:00',15)]
                
                fig, ax = plt.subplots()
                
                def animate(i):#update 
                    plotdata(plt,eu_1[:i])
                    plotdata1(plt,eu_2[:i])
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('EU')

                def init():#inition:空畫布
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('EU')
                    
                ani=animation.FuncAnimation(fig=fig,  #動畫繪製的figure
                           func=animate,              #自定義動畫函數
                           frames=25,                 #動畫長度
                           init_func=init,            #自定義開始幀
                           interval=250,              #更新頻率(以秒計)
                           blit=False)                #更新所有點還是僅更新產生變化的點
                plt.show()
                break

            elif topic == 10:
                # tesla
                tesla_1=[('07/21',13),('16:00',45),('17:00',48),('18:00',25),('19:00',22),('20:00',26),('21:00',19),('22:00',34),('23:00',25),('07/22,00:00',15),('01:00',14),('02:00',26),
                         ('03:00',10),('04:00',22),('05:00',18),('06:00',23),('07:00',12),('08:00',9),('09:00',11),('10:00',13),('11:00',20),('12:00',10),('13:00',10),('14:00',13),('15:00',25)]
      
                tesla_2=[('07/21',12),('16:00',23),('17:00',17),('18:00',19),('19:00',13),('20:00',10),('21:00',16),('22:00',17),('23:00',20),('07/22,00:00',11),('01:00',13),('02:00',11),
                         ('03:00',7),('04:00',5),('05:00',15),('06:00',17),('07:00',21),('08:00',29),('09:00',29),('10:00',23),('11:00',22),('12:00',16),('13:00',16),('14:00',9),('15:00',14)]
                
                fig, ax = plt.subplots()
                
                def animate(i):#update 
                    plotdata(plt,tesla_1[:i])
                    plotdata1(plt,tesla_2[:i])
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('Tesla')

                def init():#inition:空畫布
                    plt.legend(labels=['English Version','Chinese Version'],loc='best')
                    plt.title('Tesla')
                    
                ani=animation.FuncAnimation(fig=fig,  #動畫繪製的figure
                           func=animate,              #自定義動畫函數
                           frames=25,                 #動畫長度
                           init_func=init,            #自定義開始幀
                           interval=250,              #更新頻率(以秒計)
                           blit=False)                #更新所有點還是僅更新產生變化的點
                plt.show()
                break
            else:
                print('錯誤輸入！', '\n', '-' * 100, '\n')

        print('-' * 100)
        print('1. 觀看國內與國外對於相同主題的新聞數量差異')
        print('2. 猜測國內不同主題的新聞數量名次')
        print('3. 分析新聞標題字詞出現程度')
        m = eval(input('\n繼續觀看其他主題請輸入1, 前往其他模式請輸入該模式代碼, 離開請輸入其他任意數字:'))
        if m == 1 or m == 2 or m == 3:
            print('=' * 100)
    elif m == 2:
        print('歡迎進入模式2：猜測國內不同主題的新聞數量名次\n')
        while True:
            print(
                '主題: 1.肺炎(Covid-19), 2.香港(HK), 3.立法院(legislature), 4.高雄市長補選(election), 5.三倍券(voucher), 6.體育(PE), 7.財經(finance)')
            choose = eval(input('請根據以上7個主題代碼，猜測一個你認為過去一小時內數量最多者：'))
            kind = [1, 2, 3, 4, 5, 6, 7]
            if choose in kind:
                taiwan, label, rank = new_rank()
                print('')
                for i in range(7):
                    if choose == rank[i] and i == 0:
                        print('\n超棒！完美的follow最新時事！٩(●˙▿˙●)۶…⋆ฺ\n')
                        break
                    elif choose == rank[i] and i < 4:
                        print('\n好可惜差了一點點！(￣▽￣)~*\n')
                        break
                    elif choose == rank[i] and i < 7:
                        print('\n不優！沒事多看看新聞吧！Σ( ° △ °|||)\n')
                        break
                break
            else:
                print('錯誤輸入！', '\n', '-' * 100, '\n')

        print('-' * 100)
        print('1. 觀看國內與國外對於相同主題的新聞數量差異')
        print('2. 猜測國內不同主題的新聞數量名次')
        print('3. 分析新聞標題字詞出現程度')
        m = eval(input('\n再挑戰一次輸入2, 前往其他模式請輸入該模式代碼, 離開請輸入其他任意數字:'))
        if m == 1 or m == 2 or m == 3:
            print('=' * 100)
    elif m == 3:
        print('歡迎進入模式3：分析新聞標題字詞出現程度')
        url_1 = "https://www.bbc.co.uk/search?q="
        name = input("請輸入關鍵字(如果超過一個字請用+號連接):")
        url_2 = "&page="

        end_page = int(check_page_number())
        list_1 = []

        web_crawler()  # 執行爬蟲

        # 從爬回來的所有標題提煉單字
        dataset = []
        for entry in list_1:
            word = word_tokenize(entry)
            for i in word:
                dataset.append(i)

        #移除stopwords
        my_stopwords = stopwords.words('english')
        newly_added_stopwords=["-",'?',':',',',"'s",".","!",";","/","'","What","The","&","How"]
        for each_element in newly_added_stopwords:
            my_stopwords.append(each_elemnet)

        dataset_clean = [word for word in dataset if not word in my_stopwords]
        #print(dataset_clean)
        # 計算字出現頻率
        dictionary = {}
        for i in dataset_clean:
            dictionary[i] = dictionary.get(i, 0) + 1

        # 排序
        list_dictionary = []
        for i in dictionary:
            e = (i, dictionary[i])
            list_dictionary.append(e)
        # 需要再恢復 print(list_dictionary)
        list_dictionary.sort(reverse=True, key=lambda list_dictionary: list_dictionary[1])

        # 使用者輸入介面
        while 1:
            print("模式輸入", 1, "：觀看出現頻率大於等於輸入次數的單詞")
            print("模式輸入", 2, "：顯示出現頻率前十高的單詞的標準化出現頻率")
            print("模式輸入", 3, "：顯示任一單詞的標準化出現頻率")
            mode = int(input("請輸入模式："))
            if mode == 1:
                # 秀出出現頻率大於等於輸入次數的單字
                n = int(input("請輸入最小出現頻率："))
                i = 0
                taiwan_lab = []
                lab_num = []
                while 1:
                    if list_dictionary[i][1] < n:
                        break
                    print(list_dictionary[i][0], ":", list_dictionary[i][1], "次")
                    taiwan_lab.append(list_dictionary[i][0])  # x軸字串
                    lab_num.append(list_dictionary[i][1])
                    i = i + 1
                plt.xlabel('種類', fontproperties=font, size=12)
                plt.ylabel('出現次數', fontproperties=font, size=12)
                plt.title('觀看出現頻率圖', fontproperties=font, size=14)
                plt.xticks(rotation=45,fontsize=10)
                plt.yticks(fontsize=10)
                plt.bar(x=taiwan_lab, height=lab_num,
                        color='#084887',
                        edgecolor="#FAB419",
                        linewidth=2)
                plt.show()
            if mode == 2:
                # 計算出現頻率前十高的單詞的標準化出現頻率
                total = len(list_dictionary)
                frequency_total = 0
                for i in range(total):
                    frequency_total = frequency_total + int(list_dictionary[i][1])
                avg = frequency_total / total
                # sum of squares of deviations
                sum_sqr_dev = 0
                for i in range(total):
                    sum_sqr_dev = sum_sqr_dev + (list_dictionary[i][1] - avg) ** 2
                    # standard deviation
                sd = (sum_sqr_dev / total) ** (0.5)
                # 標準化頻率
                standard_frequency = []  # 可由此變數擷取標準化資料
                for i in range(10):
                    standard_frequency.append(round((list_dictionary[i][1] - avg) / sd, 3))
                    print("出現頻率第", str(i + 1), "高的標準化頻率:", standard_frequency[i], "\t", list_dictionary[i][0])

                taiwan_lab = []
                lab_num = []
                for i in range(0, 10, 1):
                    taiwan_lab.append(list_dictionary[i][0])  # x軸字串
                    lab_num.append(standard_frequency[i])  # y軸數據
                print(taiwan_lab, lab_num)
                plt.xlabel('種類', fontproperties=font, size=12)
                plt.ylabel('頻率', fontproperties=font, size=12)
                plt.title('出現頻率前10高的標準化頻率', fontproperties=font, size=14)
                plt.xticks(fontsize=6.5)
                plt.yticks(fontsize=10)
                plt.bar(x=taiwan_lab, height=lab_num,
                        color='#084887',
                        edgecolor="#FAB419",
                        linewidth=2)
                plt.show()
            if mode == 3:
                # 計算任一單詞的標準化出現頻率
                total = len(list_dictionary)
                frequency_total = 0
                for i in range(total):
                    frequency_total = frequency_total + int(list_dictionary[i][1])
                avg = frequency_total / total
                # sum of squares of deviations
                sum_sqr_dev = 0
                for i in range(total):
                    sum_sqr_dev = sum_sqr_dev + (list_dictionary[i][1] - avg) ** 2
                    # standard deviation
                sd = (sum_sqr_dev / total) ** (0.5)

                flag = 0  # 用以跳出多層迴圈
                while 1:
                    word_interest = input("請輸入想搜尋的單詞：")
                    for i in range(total):
                        if word_interest == str(list_dictionary[i][0]):
                            sf_specific = list_dictionary[i][1]
                            flag = flag + 1
                            break
                        if word_interest == str(0000):
                            flag = flag + 1
                            break
                    if flag == 0:
                        print("此單字並未出現在標題中")
                    if flag == 1:
                        break
                sf_specific = round((sf_specific - avg) / sd, 3)
                print("出現頻率的標準化頻率:", sf_specific)

            print('-' * 100)
            print('1. 觀看國內與國外對於相同主題的新聞數量差異')
            print('2. 猜測國內不同主題的新聞數量名次')
            print('3. 分析新聞標題字詞出現程度')
            m = eval(input('\n再一次請輸入3, 前往其他模式請輸入該模式代碼, 離開請輸入其他任意數字:'))
            if m == 3:
                print("")
                k = eval(input("替換關鍵字請輸入0,不需要則輸入其他任意數字:"))
                if k == 0:
                    print("-" * 100)
                    break
                else:
                    print('')
            else:
                print('=' * 100)
                break
                