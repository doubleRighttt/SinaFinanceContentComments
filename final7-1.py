import jieba
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from snownlp import SnowNLP


data = pd.read_csv("newscomment.csv")
data.head()
#情感划分 赞大于300的给1 赞小于三百的给0
def make_label(agree):
 if agree > 300:
    return 1
 else:
    return 0

data['sentiment'] = data.agree.apply(make_label)

print(data)


#结巴分词
def chinese_word_cut(mytext):
 return " ".join(jieba.cut(mytext))

data['cut_comment'] = data.comment.apply(chinese_word_cut)

#划分数据集
X = data['cut_comment']
y = data.sentiment

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=22)


#数据处理
def get_custom_stopwords(stop_words_file):
 with open(stop_words_file,'r',encoding='utf-8') as f:
    stopwords = f.read()
    stopwords_list = stopwords.split('\n')
    custom_stopwords_list = [i for i in stopwords_list]
 return custom_stopwords_list

stop_words_file = '哈工大停用词表.txt'
stopwords = get_custom_stopwords(stop_words_file)

vect = CountVectorizer(max_df = 0.8,
                       min_df = 3,
                       token_pattern=u'(?u)\\b[^\\d\\W]\\w+\\b',
                       stop_words=frozenset(stopwords))

test = pd.DataFrame(vect.fit_transform(X_train).toarray(), columns=vect.get_feature_names())
test.head()


#训练模式  朴素贝叶斯算法
from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()

X_train_vect = vect.fit_transform(X_train)
nb.fit(X_train_vect, y_train)
train_score = nb.score(X_train_vect, y_train)
#print(train_score)

#测试数据
X_test_vect = vect.transform(X_test)
#print(nb.score(X_test_vect, y_test))

#使用snownlp插件包
data = open("newscomment.txt",encoding='utf-8')
s = data.read()
snownlp = SnowNLP(s)
print(snownlp.sentiments)