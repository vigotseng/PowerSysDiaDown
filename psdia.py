import requests
from bs4 import BeautifulSoup

base_url = 'http://10:8080'
# 列别获取url
query_url = base_url + '/QJDmis/SysAdmin_Doc.dmis'
url_list = []

def get_html(query_url):
    # 如果存在两小时以内获取过的html数据，则从本地读取html数据文件进行网址扫描
    # 如果不存在文件，或者两小时内没有或去过html数据，就开始请求获取html数据，并保存到本地
    # 请求获得html数据，并保存到本地
    
    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Length':'1189',
            'Content-Type':'application/x-www-form-urlencoded',
            'Cookie':'',
            'Host':'10.181.200.130:8080',
            'Origin':'http://10:8080',
            'Referer':'http://10:8080/QJDmis/SysAdmin_Doc.dmis',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

    formdata = {'SplitPage':'true',
            'NUMPERPAGE':'10000',
            'CURPAGE':'1',
            'ViewState':'',
            'Forward':'queryFileDone',
            'ext5':'',
            'title':'(unable to decode value)'}
    # 获得下载网页
    r = requests.post(query_url,headers=headers,data=formdata,timeout=1)
    # save_html_file(r)
    return r

# def save_html_file(res):
#     soup = BeautifulSoup(res.text,'lxml')
#     # print(soup.prettify())
#     html_pre_file = open('html_pre_file.html','w',encoding='UTF-8')
#     html_pre_file.write(soup.prettify())
#     html_pre_file.close

def get_down_url(res):
    org_soup = BeautifulSoup(res.text,'lxml')
    soup = BeautifulSoup(org_soup.prettify(),'lxml')
    tr_li = soup.find_all('tr',attrs={'class':'td4'})
    # print(tr_li[4])
    for tr in tr_li:
        td = tr.find_all('td')
        # print(td[1].string.split(),td[2].string.split(),td[4].string.split(),td[5].string.split())
        file_sub = td[1].string.strip()
        file_name = td[2].string.strip()
        file_date = td[4].string.strip()
        file_url = base_url + td[5].find('a').get('href').strip()
        # print(file_sub,file_name,file_date,file_url)
        url_list.append([file_sub,file_name,file_date,file_url])
        # print(url_list)

def down_list(url_list):
    cnt = 1
    for urls in url_list:
        # print(urls)
        r = requests.get(urls[3])
        save_file_name ='psdiadoc/' + urls[0] + urls[1]
        with open(save_file_name, "wb+") as code:
            code.write(r.content)
            print(cnt,'-',urls[1])
        cnt = cnt + 1
        
def main():
    print('downloading......')
    res = get_html(query_url)
    get_down_url(res)
    down_list(url_list)
    # save_html_file(res)
    # print(res.text)
   
if __name__ == '__main__':
    main()