import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json
import requests
import pandas as pd



#存入本地txt
def write_article(data,flag):
    if flag == 1:
        file_name = 'newscontent.txt'
        f = open(file_name, 'a', encoding='utf-8')
        f.write(data)
        f.write("\n\n")
        f.close()
    elif flag == 2:
        file_name = 'newscomment.csv'
        name = ['comment','agree']
        comments = pd.DataFrame(list(zip(*data)),columns=name)
        comments.to_csv(file_name)
    else:
        file_name = 'newscomment.txt'
        f = open(file_name, 'a', encoding='utf-8')
        f.write(data)
        f.write("\n\n")
        f.close()


def get_content(url):
    try:
        html = urllib.request.urlopen(url)
    except HTTPError as e:
        return None
    try:
        obj = BeautifulSoup(html.read(),"html.parser")
    except HTTPError as f:
        return None
    nameList = obj.findAll("div", {"class": "article"})
    for name in nameList:
        print(name.get_text())
        str = name.get_text()
        write_article(str,1)
get_content("https://finance.sina.com.cn/chanjing/gsnews/2019-12-11/doc-iihnzahi6659560.shtml")



#定义空数组 用来存放评论和评论获赞的数量
listAll=[]
listComments = []
listAgree = []

#获取当前页的评论 最多三条热门
comments = requests.get("https://comment.sina.com.cn/page/info?version=1&format=json&channel=cj&newsid=comos-ihnzahi6659560&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1&uid=unlogin_user")
comments.encoding=('utf-8')
comments.text
jd = json.loads(comments.text)
#print(jd)
for x in range(3):
    print(jd['result']['hot_list'][x]['content'])
    str1 = jd['result']['hot_list'][x]['content']
    str2 = jd['result']['hot_list'][x]['agree']
    write_article(str1,3)
    listComments.append(str1)
    listAgree.append(str2)




#打开更多评论查看全部评论
comments2 = requests.get("http://comment.sina.com.cn/page/info?version=1&format=json&channel=cj&newsid=comos-ihnzahi6659560&group=0&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=10&t_size=3&h_size=3&thread=1&uid=unlogin_user")
comments2.encoding=('utf-8')
comments.text
jd1 = json.loads(comments2.text)
count = jd1['result']['count']['thread_show']
#print(jd1)

#-5防止下标越界
for x in range(count-5):
    print(jd1['result']['cmntlist'][x]['content'])
    str1 = jd1['result']['cmntlist'][x]['content']
    str2 = jd1['result']['cmntlist'][x]['agree']
    write_article(str1,3)
    listComments.append(str1)
    listAgree.append(str2)

#把评论和赞放到一个数组里面
listAll.append(listComments)
listAll.append(listAgree)


#将评论写入cvs文件
#print(listAll)
write_article(listAll,2)