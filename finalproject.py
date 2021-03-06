#################### 爬蟲 ####################
from bs4 import BeautifulSoup 
import requests

#################### 畫圖 ####################
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.pyplot import MultipleLocator #用在y軸座標
from matplotlib import animation as animation #animation

#################### 資料整理 ####################
import numpy as np
import copy

#################### 文字處理 ####################
import nltk 
from nltk.corpus import stopwords 
nltk.download('punkt') 
nltk.download("stopwords")
from nltk.tokenize import word_tokenize 

 #################### 載入字體 ####################
font = FontProperties(fname=r'./GenYoGothicTW-Regular.ttf')

 #################### 選模式 ####################
def choose_mode():
    while True: 
        print(' 1. 觀看國內與國外對於相同主題的新聞數量差異','\n','2. 猜測國內不同主題的新聞數量名次','\n',
                '3. 分析新聞標題字詞出現程度','\n','*****離開請輸入000*****\n','-' * 100)
        Mode = eval(input('請輸入想進入的模式:'))
        if Mode == 1 or Mode == 2 or Mode == 3:
            print('=' * 100, '\n')
            break
        elif Mode == 000:
            break
        else:
            print('\n無此模式，請重新輸入')
            print('=' * 100, '\n')
    return Mode

#################### mode1各別主題每小時出現的新聞數量，_1代表英文版，_2代表中文版 ####################
mode1_Dictionary = { 'time' : ['07/21','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00','07/22,00:00','01:00','02:00','03:00',
                    '04:00','05:00','06:00','07:00','08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00'],
                    'taiwan_1' : [44,48,74,25,24,37,55,58,54,58,52,56,64,52,62,52,47,55,48,73,45,46,59,68,56],
                    'taiwan_2' : [57,59,71,58,58,54,47,50,35,23,28,21,23,16,54,63,28,50,50,56,52,64,64,59,50],
                    'covid19_1' : [55,100,87,80,94,100,100,76,81,93,81,82,74,92,100,87,91,100,81,81,88,90,100,82,80],
                    'covid19_2' : [44,66,64,46,56,52,63,52,53,34,51,38,44,35,49,47,50,45,55,51,53,56,66,54,56],
                    'china_1' : [30,70,68,29,48,76,84,59,46,28,37,48,37,56,42,49,51,44,62,63,41,77,67,57,70],
                    'china_2' : [61,78,79,71,80,79,63,68,52,34,34,55,61,33,81,70,43,60,74,75,68,68,63,61,74],
                    'coronavirus_1' : [61,45,86,78,63,87,66,89,71,66,65,75,56,94,52,69,81,73,79,52,65,46,62,55,88],
                    'coronavirus_2' : [23,26,33,39,28,28,25,25,31,12,20,14,34,7,22,37,17,27,28,27,19,31,33,21,34],
                    'trump_1' : [21,39,32,38,29,44,45,39,32,41,38,28,30,32,28,28,24,27,27,27,40,28,22,14,36],
                    'trump_2' : [18,16,15,14,13,16,8,12,12,3,9,1,1,8,11,10,10,16,23,19,15,19,12,21,16],
                    'uk_1' : [33,84,52,29,42,91,60,41,47,91,34,74,41,72,75,62,50,25,51,24,76,81,85,75,73],
                    'uk_2' : [35,44,42,31,38,39,33,27,24,14,15,22,26,14,41,25,17,43,55,47,39,39,39,34,39],
                    'hk_1' : [16,41,41,9,29,35,43,34,13,50,20,38,14,32,33,29,34,23,32,40,30,19,47,62,43],
                    'hk_2' : [61,75,72,72,74,68,75,69,47,42,38,78,84,37,82,52,45,63,84,77,72,70,64,66,67],
                    'election_1' : [19,26,25,32,15,15,26,34,34,32,26,43,4,11,26,25,25,25,27,23,25,25,20,21],
                    'election_2' : [8,13,8,18,9,8,4,7,6,2,6,6,6,1,8,4,6,11,9,4,3,8,4,7,5],
                    'eu_1' : [26,27,50,29,21,36,40,37,41,32,29,35,38,26,23,40,31,25,33,28,29,25,34,47,56],      
                    'eu_2' : [16,23,16,18,13,16,8,15,13,6,7,21,12,8,23,12,16,29,28,22,19,24,16,16,15],
                    'tesla_1' : [13,45,48,25,22,26,19,34,25,15,14,26,10,22,18,23,12,9,11,13,20,10,10,13,25],     
                    'tesla_2' : [12,23,17,19,13,10,16,17,20,11,13,11,7,5,15,17,21,29,29,23,22,16,16,9,14]}

#################### mode1畫圖 ####################
def mode1_plot(plt, topic, i):  
    x=mode1_Dictionary['time'][:i]               #把x設定為時間
    y1=mode1_Dictionary['%s_1'%topic][:i]        #把y1設定為英文版
    y2=mode1_Dictionary['%s_2'%topic][:i]        #把y2設定為中文版
    plt.style.use('bmh')
    y_major_locator = MultipleLocator(10)        #把y軸的刻度間隔設置為10 存在變數裡
    ax=plt.gca()                                 #ax為座標軸的實例
    ax.yaxis.set_major_locator(y_major_locator)  #把y軸的主刻度設置為10的倍數
    plt.xticks(rotation=80)                      #把x軸刻度名稱旋轉
    plt.xlim(0,24)                               #固定x軸刻度
    plt.ylim(0,104)                              #固定y軸刻度
    plt.xlabel('Time')                           #設置x軸名稱
    plt.ylabel('number of news')                 #設置y軸名稱
    plt.plot(x, y1, '-o', color='b')             #_1為英文版，線為藍色
    plt.plot(x, y2, '-o', color='r')             #_2為中文版，線為紅色

#################### mode1動畫 ####################
def mode1_animation(topic):
    def animate(i): #update 
        mode1_plot(plt,topic,i)
        plt.legend(labels=['English Version','Chinese Version'],loc='best')
        plt.title('%s'%topic)

    def init(): #inition:空畫布
        plt.legend(labels=['English Version','Chinese Version'],loc='best')
        plt.title('%s'%topic)

    fig, ax=plt.subplots()
    ani=animation.FuncAnimation(fig=fig,    #動畫繪製的figure
                           func=animate,    #自定義動畫函數
                           frames=25,       #動畫長度
                           init_func=init,  #自定義開始幀
                           interval=250,    #更新頻率(以秒計)
                           blit=False)      #更新所有點還是僅更新產生變化的點

    plt.show()

#################### mode2爬標題 ####################
def web_crawler_for_GoogleNews_headlines(url): 
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        stories = soup.find_all('a', class_='DY5T1d')
    return len(stories)

#################### mode2排名 ####################
def GoogleNews_headlines_rank():
    # 順序為肺炎、香港、立法院、高雄市長補選、三倍券、體育、財經
    url = ['https://news.google.com/search?q=%E8%82%BA%E7%82%8E%20when%3A1h&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',
           'https://news.google.com/search?q=%E9%A6%99%E6%B8%AF%20when%3A1h&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',
           'https://news.google.com/search?q=%E7%AB%8B%E6%B3%95%E9%99%A2%20when%3A1h&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',
           'https://news.google.com/search?q=%E9%AB%98%E9%9B%84%E5%B8%82%E9%95%B7%E8%A3%9C%E9%81%B8%20when%3A1h&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',
           'https://news.google.com/search?q=%E4%B8%89%E5%80%8D%E5%88%B8%20when%3A1h&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',
           'https://news.google.com/search?q=%E9%AB%94%E8%82%B2%20when%3A1h&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant',
           'https://news.google.com/search?q=%E8%B2%A1%E7%B6%93%20when%3A1h&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant']
    count, label, rank = [], [], []
    for i in range(7):
        count.append(web_crawler_for_GoogleNews_headlines(url[i]))
    count_copy = copy.deepcopy(count)
    labels = ['Covid-19', 'HK', 'legislature', 'election', 'voucher', 'PE', 'finance']
    count.sort(reverse=True)
    for i in range(len(count)):
        for j in range(7):
            if (count[i] == count_copy[j]) and (count[i] not in label):
                label.append(labels[j])
                rank.append(j + 1)
    return count_copy, labels, rank

#################### mode3找最後一頁的頁數 ####################
def find_end_page_number(): 
    res = requests.get(url_1 + name + url_2 + "1")
    soup = BeautifulSoup(res.text, 'html.parser')
    page_number = 0
    for entry in soup.select('.css-1s4ayab-StyledListItem-PageButtonListItem.e4i2y2x3 div .css-16didf7-StyledButtonContent.e1b2sq420'):
        page_number = str(entry.text.strip()) #不斷將page_number替換掉，直到最後一頁(有些page number和最後一頁share同樣的tag和class name)
    return page_number

#################### mode3爬標題 ####################
def web_crawler_for_BBCNews_headlines(headlines):
    i = 1
    while 1:
        res = requests.get(url_1 + name + url_2 + str(i))
        res.encoding = "utf8"  # 解決標點符號亂碼問題
        soup = BeautifulSoup(res.text, 'html.parser')
        for entry in soup.select('.css-johpve-PromoLink.ett16tt7 span'):
            headlines.append(entry.text.strip())
        if i == end_page:
            break
        i = i + 1

#################### mode3提取單詞 ####################
def separate_word_in_headlines(all_separate_words):
    for each in headlines:
        word = word_tokenize(each)
        for i in word:
            all_separate_words.append(i)

#################### mode3移除虛詞 ####################
def remove_stopwords(all_separate_words):
    my_stopwords = stopwords.words('english')
    newly_added_stopwords=["-",'?',':',',',"'s",".","!",";","/","'","’","What","The","&","How"]
    for each_element in newly_added_stopwords:
        my_stopwords.append(each_element)
    all_separate_words_clean = [word for word in all_separate_words if not word in my_stopwords]
    return all_separate_words_clean

#################### mode3依出現頻率排序 ####################
def sort_with_frequency(list_dictionary,dictionary):
    for i in dictionary:
        e = (i, dictionary[i])
        list_dictionary.append(e)
    # print(list_dictionary) #for check
    list_dictionary.sort(reverse=True, key=lambda list_dictionary: list_dictionary[1])
    return list_dictionary

#################### mode3計算標準化頻率 ####################
def get_standard_frequency(list_dictionary,index_of_the_word):
    total = len(list_dictionary)
    frequency_total = 0
    for i in range(total):
        frequency_total = frequency_total + int(list_dictionary[i][1])
    average = frequency_total / total
    sum_sqr_dev = 0 # sum of squares of deviations
    for i in range(total):
        sum_sqr_dev = sum_sqr_dev + (list_dictionary[i][1] - average) ** 2
    sd = (sum_sqr_dev / total) ** (0.5) # standard deviation
    # 標準化頻率
    index_of_the_word=int(index_of_the_word)
    standard_frequency=round((list_dictionary[index_of_the_word][1] - average) / sd, 3)
    if sd==0:
        standard_frequency=0
    return standard_frequency

#################### mode2跟mode3畫圖 ####################
def draw_bar(news_type,news_num,draw_mode):  #畫圖
            label_y=['新聞量', '頻率', '頻率']
            title=['新聞量分析圖', '觀看出現頻率圖', '出現頻率前10高的標準化頻率']
            plt.xlabel('種類', fontproperties=font, size=12)
            plt.ylabel('%s'%label_y[draw_mode], fontproperties=font, size=12)
            plt.title('%s'%title[draw_mode], fontproperties=font, size=14)
            plt.xticks(fontsize=6.5)
            plt.yticks(fontsize=10)
            plt.bar(x=news_type, height=news_num,
                    color='#084887',
                    edgecolor="#FAB419",
                    linewidth=2)
            plt.show()

#################### 程式運行 ####################
# 防呆&確認模式
while True:  
    Mode = choose_mode()
    if Mode in [1, 2, 3, 000]:
        break

# 進入模式
while Mode == 1 or Mode == 2 or Mode == 3:  
    #################### mode1 ####################
    if Mode == 1:
        print('歡迎進入模式1：觀看國內與國外對於相同主題的新聞數量差異\n')
        while True:
            print('主題: 1.Taiwan, 2.Covid-19, 3.China, 4.Corona virus, 5.Donald Trump, 6.UK, 7.Hong Kong, 8.Election, 9.EU, 10.Tesla')
            topic = ['taiwan','covid19','china','coronavirus','trump','uk','hk','election','eu','tesla']  #設定主題
            topic_number = eval(input('請根據以上10個主題代碼，選擇一個你想觀看的主題：'))                    #讓使用者輸入想觀看的主題代碼
            if topic_number in range(1,11):             #確定輸入的主題代碼正確
                mode1_animation(topic[topic_number-1])  #畫出動畫
                print("")
                break                                   #跳出迴圈，重新詢問使用者
            else:
                print('錯誤輸入！', '\n', '-' * 100, '\n')
        
        Mode=choose_mode()

    #################### mode2 ####################
    elif Mode == 2:
        print('歡迎進入模式2：猜測國內不同主題的新聞數量名次\n')
        while True:
            print(
                '主題: 1.肺炎(Covid-19), 2.香港(HK), 3.立法院(legislature), 4.高雄市長補選(election), 5.三倍券(voucher), 6.體育(PE), 7.財經(finance)')
            choose = eval(input('請根據以上7個主題代碼，猜測一個你認為過去一小時內數量最多者：'))
            kind = [1, 2, 3, 4, 5, 6, 7]
            if choose in kind:
                count, label, rank = GoogleNews_headlines_rank()
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
                draw_mode=0
                draw_bar(label,count,draw_mode)
                print("")
                break
            else:
                print('錯誤輸入！', '\n', '-' * 100, '\n')

        Mode=choose_mode()

    #################### mode3 ####################
    elif Mode == 3:
        print('歡迎進入模式3：分析新聞標題字詞出現程度')
        url_1 = "https://www.bbc.co.uk/search?q="
        name = input("請輸入關鍵字(如果超過一個字請用+號連接):")
        url_2 = "&page="

        end_page = int(find_end_page_number())
        if end_page == 0:
            end_page = 1 #若搜尋結果只有一頁，不會顯示下方頁碼標籤，因此找不到，故為預設值0
        
        # 執行爬蟲
        headlines = []
        web_crawler_for_BBCNews_headlines(headlines)  #將標題存到headlines這個list

        #################### 資料處理 ####################
        # 從爬回來的所有標題提煉單字
        all_separate_words = []
        separate_word_in_headlines(all_separate_words)

        #移除stopwords
        all_separate_words_clean=remove_stopwords(all_separate_words)
        #print(all_separate_words_clean) #for check
        
        # 計算字出現頻率
        dictionary = {}
        for i in all_separate_words_clean:
            dictionary[i] = dictionary.get(i, 0) + 1

        # 排序
        list_dictionary = []
        list_dictionary = sort_with_frequency(list_dictionary,dictionary)
        #################################################

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
                x_axis_type = []
                y_axis_num = []
                while 1:
                    if list_dictionary[i][1] < n:
                        break
                    print(list_dictionary[i][0], ":", list_dictionary[i][1], "次")
                    x_axis_type.append(list_dictionary[i][0])  # x軸字串
                    y_axis_num.append(list_dictionary[i][1])
                    i = i + 1
                draw_mode=1
                draw_bar(x_axis_type,y_axis_num,draw_mode)
            if mode == 2:
                # 計算出現頻率前十高的單詞的標準化出現頻率
                standard_frequency_top_10 = []  
                for index_of_the_word in range(10):
                    standard_frequency_top_10.append(get_standard_frequency(list_dictionary,index_of_the_word))
                    print("出現頻率第", str(index_of_the_word+ 1), "高的標準化頻率:", standard_frequency_top_10[index_of_the_word], "\t", list_dictionary[index_of_the_word][0])
                x_axis_type = []
                y_axis_num = []
                for i in range(0, 10, 1):
                    x_axis_type.append(list_dictionary[i][0])  # x軸字串
                    y_axis_num.append(standard_frequency_top_10[i])  # y軸數據
                print(x_axis_type, y_axis_num)
                draw_mode=2
                draw_bar(x_axis_type,y_axis_num,draw_mode)
            if mode == 3:
                # 計算任一單詞的標準化出現頻率
                flag = 0  # 用以跳出多層迴圈
                total = len(list_dictionary)
                while 1:
                    word_interest = input("請輸入想搜尋的單詞,若想停止搜尋請輸入0000\n：")
                    for i in range(total):
                        if word_interest == str(list_dictionary[i][0]):
                            standard_frequency_of_specific_word=get_standard_frequency(list_dictionary,i)
                            flag = flag + 1
                            break
                        if word_interest == str(0000):
                            flag = flag + 1
                            break
                    if flag == 0:
                        print("此單字並未出現在標題中")
                    if flag == 1:
                        break
                print("出現頻率的標準化頻率:", standard_frequency_of_specific_word)

            print("")
            Mode=choose_mode()

            if mode in [1, 2, 3] and Mode==3:
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