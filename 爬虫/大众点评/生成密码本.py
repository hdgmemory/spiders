import requests,re,json

#得到css样式
url = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/shoptextcss/textcss.hHGEFeGyJG.css'

    #自己加： http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/bcc319ec9eeaf4d8da17e0f895f3dff7.svg
response = requests.get(url=url)

#一、找到每个类名标识---fr列表
pattern = re.compile(r'.fr-.*?}')
review_items = pattern.findall(response.text)
# print(review_items)

#二、找到对应的汉字表(address,review)
pattern = re.compile(r'//.*?.svg')
file_svg = pattern.findall(response.text)
# print(file_svg)

#网络请求函数
def get_content(url):
    response = requests.get(url=url)
    return response.text

# 地址编码表和#评论编码表
# address_svg_url = 'http:'+file_svg[0]
review_svg_url = 'http:'+file_svg[1]
# address_str = get_content(address_svg_url)
review_str = get_content(review_svg_url)
# print(review_str)#是xml文档，带格式

#由于拿到的是带格式的内容，所以需要提取一下数据
line_pattern = re.compile(r'class="textStyle">(.*?)</text>')
# review
review_lines = line_pattern.findall(review_str)
review_content =''
for line in review_lines:
    review_content += line
# print(review_content)
#
# # 保存
with open('review_svg.txt', 'w', encoding='utf-8') as fp:
    fp.write(review_content)
# print(len(review_content))#994,和我们之前查的一样
#
# #对应fr-XXXX与汉字的关联，生成密码本
word_dic = {}
for item in review_items:
#
#     #字宽14，高7
#     # 拿位置
    locaton_x = re.compile('background:(.*?)px')
    x_list = locaton_x.findall(item)
    # print(x_list)


    locaton_y = re.compile('px (.*?)px')
    y_list = locaton_y.findall(item)
    print(y_list)
    if len(x_list)>0 and len(y_list)>0:
        x = abs(float(x_list[0]))
        y = abs(float(y_list[0]))

        # print(item[:8],'loc:',x,y)
        #行、列变为一行读取
        #         x   y  index
        # 第一行：0   7    0
        # 第二行：0   37   42
        x_0 = int(x/14)#表示第几列
        y_0 = int(y)//30#表示第几行
        # print('index:',x_0,y_0)
        #                 行  行中第n个字
        word = review_lines[y_0][x_0:x_0+1]
        print(item[:8], word)
#
        #添加到列表当中
        k = item[4:8]
        word_dic[k]=word
# #
data = json.dumps(word_dic,ensure_ascii=False)
with open('review_list.txt','w',encoding='utf-8') as fp:
    fp.write(data)


