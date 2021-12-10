from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import re

## 키워드 검색, 뉴스 원문 링크 리스트로 반환

def get_news_list(query,sort,ds,de,max_num):
  ds_ = re.sub('\.','',ds)
  de_ = re.sub('\.','',de)
  news_url_list = set()
  for page in tqdm(range(1,max_num,10)):
    source_url = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={query}&sort={sort}&ds={ds}&de={de}&nso=so:r,p:from{ds_}to{de_},a:all&start={page}"
    response = requests.get(source_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # 네이버뉴스 링크만 가져옴
    news_url = soup.find_all('a',attrs={'class':"info"})
    for n_url in news_url:
      if n_url['class']==['info']:
        news_url_list.add(n_url['href'])
  news_url_list = [s for s in list(news_url_list) if 'sports.news' not in s]
  return news_url_list

sort = "0"
ds_d = ".01.01"
de_d = ".12.31"
max_num = 4000 # 3991건까지 제공함

keyword = ['가스','에너지','원자력','수소','천연가스','그린수소','탄소중립','CCS기술','액화수소','탄소 네거티브','도시가스','신재생에너지','친환경','KOGAS','가스공사']

news_list = []
for y in range(2017,2021):
  ds = str(y)+ds_d
  de = str(y)+de_d
  for kw in keyword :
    print(f"{y} : {kw}")
    news_list = get_news_list(kw,sort,ds,de,max_num)
    f = open(f"/<your dir>/LinkList_{y}_{kw}_{len(news_list)}.txt", 'w')
    f.write('\n'.join(news_list))
    f.close()

    