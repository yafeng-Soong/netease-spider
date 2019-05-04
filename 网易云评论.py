#-*-coding:UTF-8-*-

from urllib import request
from bs4 import BeautifulSoup
import requests
import json
import re
from urllib import parse


a_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
           ,"Referer": "http://music.163.com/discover/artist"
           ,"Origin": "http://music.163.com"
           ,"Host":"music.163.com"
           ,"Cookie":"_iuqxldmzr_=32; _ntes_nnid=9bab5ebb9f8ceee069cb78f0a2981abe,1518338855311; _ntes_nuid=9bab5ebb9f8ceee069cb78f0a2981abe; __utmc=94650624; __utmz=94650624.1518338856.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=94650624.44525748.1518338856.1518338856.1518341295.2; JSESSIONID-WYYY=M%2BRH6YHhfp2cVhqPvhYY8trjkopMxYU3p0mKWwFJaAXHw7UlmXOaYo%5CvvrlS8hQo%2FFydkqEhQUD56EmaA8jdh3fbWXdZ%2BuG7JCt8SeWr08UY8agb%5C%2Fs5Maq3jkD8%2BjcZoxcJtjmwNMSzZUwlTAtFNMYqr3xfWEIO6zDMzqZTx0qDrSS7%3A1518344136402; __utmb=94650624.21.10.1518341295"
           ,"Content-Type":"application/x-www-form-urlencoded"
           ,"Content-Length":"414"
           ,"Connection":"keep-alive"
           ,"Accept-Language":"zh-CN,zh;q=0.9"
           ,"Accept":"*/*"}
s_url="http://music.163.com/artist"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"}

def artist_id():
    url="http://music.163.com/weapi/artist/top?csrf_token="
    data={"params":"uAE0hN7yRCy+plWTUJw7imQQW+wUSFRuVlFD8UTgXNfJTVLzNyqfnLRqSByCjs40san8rbwMfpasdpJRNit6vKkbQE0F7MZEgRPgSEVfXrHIB/wGiyYQ/VIaZnyTql1m",
          "encSecKey":"def9762a8c6ff1f3ae1a7ee23cbc095b3dd6c888f28e974ca00f927fd044a48cfdde49af3138aa99fa7da17fdb97809c7d1abd4ddfc40ab7ef3c0e574e56b2d623c0c23af4d08c629087fd5e1996c961af133140dc81b9fb2322aca668a8079c6cd01a0699fc860b2bb0df47b3887d563f1b18e6585198bb5d9c718a5fa92f04"}
    #用Requests和urlopen解析歌手页面的POST
    post_data = parse.urlencode(data).encode("utf-8")
    req=request.Request(url=url,headers=a_headers)
    res=request.urlopen(req,post_data)
    html=res.read().decode("utf-8")
    #解析所返回的JSON数据
    a_data=json.loads(html)
    a_list=a_data["artists"]#所有歌手的信息储存在artists键中
    id_list=[]#用一个列表储存所有歌手的id和name
    for i in range(len(a_list)):
        a_dict = {}#用一个字典储存一个歌手的id和name
        a_dict["name"]=a_list[i]["name"]
        a_dict["id"]=a_list[i]["id"]
        id_list.append(a_dict)
    return id_list

def song_id(artist_id):
    data={"id":artist_id}#将歌手ID作为params参数传入requests.get()方法
    req=requests.get(url=s_url,headers=headers,params=data)
    req.encoding="utf-8"
    soup=BeautifulSoup(req.text,"lxml")#对返回的数据进行解析
    song_list=soup.find_all("ul",class_="f-hide")#找到class="f-hide"的<ul>标签
    song_soup=BeautifulSoup(str(song_list),"lxml")#将<ul>......</ul>再解析一次，以便使用find_all()方法把所有<a>标签取出来
    song_list=song_soup.find_all("a")
    id_list=[]#存歌曲ID
    name_list=[]#存歌名
    for each in song_list:
        s_id=each.get("href")#歌曲ID在<a>标签href属性中
        s_name=each.string
        s=re.findall(r"\d+",s_id)#用正则找到href中的ID
        id_list.append(s[0])#由于re.findall()返回的是一个列表，所以用下标将ID取出
        name_list.append(s_name)
    return id_list,name_list

def comment_count(song_id):
    url="http://music.163.com/weapi/v1/resource/comments/R_SO_4_"+song_id+"?csrf_token="
    data = {
        "params": "nHfVBsNbW+WCrz7pAbdaq4uW2+4kADa+gNEfGWK7M5n36mWvsmGXsM2KzVUAeR62mhYlsSvc23I58Rf0dvg1Cglxuf5/l1wVRBCRROpjz9WuYSlWdiwXT/x45iud30RmjbTUsMSQuiehO6Ef3vHSdKWHma9pYm/eeYUF7IQ0hXI3HIz42NgwllBj4cy1XlOH",
        "encSecKey": "0587c5b45f3b0771db2b3fe449e7dd9640ab56f679d73a9189096283e776e7a9f749630c6e0fa3f947778f1588b9ec71bd779279006f352e5804036909d5d772c9572c64db575bcce675fcc9055614f1c955abb798eed602cb43945748d8b0a9ecf293cde0ef523e63c3115a1a12b7113be447fba7947090f0d98d2c37cff72a"}
    req=requests.post(url=url,headers=headers,data=data)
    req.encoding="utf-8"
    comment= json.loads(req.text)
    return comment["total"]



if __name__=="__main__":
    f=open("网易云评论.txt","w",encoding="utf-8")
    id_list=artist_id()
    # id_list=[{"name":"周杰伦","id":6452}]
    for artist in id_list:
        total=0
        print("\n\n"+artist["name"])
        f.write("\n\n"+artist["name"]+"热门歌曲以及评论数：")
        song_id_list,name_list=song_id(artist["id"])
        for i in range(len(song_id_list)):
            if(name_list[i]!=None):
                total+=comment_count(song_id_list[i])
                f.write(name_list[i]+":"+str(comment_count(song_id_list[i]))+"条")
        f.write("总计："+str(total)+"条")
        print(artist["name"]+"网易云音乐热门歌曲总评论数："+str(total)+"条")
    print("抓取完毕！")




