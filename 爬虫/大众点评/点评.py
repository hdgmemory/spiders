import requests
from fake_useragent import UserAgent

ua = UserAgent()

headers = {
    'User-Agent':ua.random
}
#获取页面信息
response = requests.get('http://www.dianping.com/shop/102284990',headers=headers)
content = response.text
with open('dianping.html','w',encoding='utf-8') as fp:
    fp.write(response.text)
print(response.text)

#在编程的时候可能会频繁的访问，可能会对我们的ip进行禁止，
# 前期我们先写规则，后面有时间再用代理完成反反爬
with open('dianping.html','r',encoding='utf-8') as fp:
    content1 = fp.read()
# print(content1)



#解析数据--例如：在附<span class="fr-5exP"></span>办事....
import re
pattern = re.compile(r'<p class="desc">(.*?)</p>')
comments = pattern.findall(content)
# for c in comments:
#     print(c)


#读取密码本
import json
fp = open('review_list.txt','r',encoding='utf-8')
review_dict = json.load(fp)
# print(review_dict)

#进行替换
#最终结果存放的位置
result = []

for c in comments:
    pattern = re.compile(r'<span class="fr-(.*?)"></span>')
    span_list = pattern.findall(c)
    # print(span_list)

    c_copy = c
    for k in span_list:

        try:#有时候密码本上没有对应的键值

            #替换
            #找到要被替换的内容
            old_value = '<span class="fr-%s"></span>'%(k)

            new_value = review_dict[k]#value为替换的内容

            c_copy = c_copy.replace(old_value, new_value)
            # print(c_copy)

        except:
            pass
    result.append(c_copy)

#验证结果
for c in result:
    print(c)



