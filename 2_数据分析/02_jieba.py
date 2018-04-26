# coding=utf-8

import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 读取文件，
file = open(u'file/诛仙.txt', 'rb').read(1000).decode('gbk')


wordcloud = WordCloud(background_color="white",width=1000, height=860, margin=2).generate(file)


plt.imshow(wordcloud)
plt.axis("off")
plt.show()

wordcloud.to_file('test.png')