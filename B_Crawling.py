import glob
import multiprocessing as mp
from threading import Thread

def make_list(x):
  # 뉴스링크 텍스트파일을 리스트로만드는 함수
  print(len(x))
  newslist = []
  for i in range(len(x)):
    newslist.extend(open(x[i],'r').read().split('\n'))
  while True:
    try :
      newslist.remove('')
    except :
      break
  print(len(newslist),len(list(set(newslist))))
  newslist = list(set(newslist))
  return newslist


def get_content_from_news_list(news_list,header,saver,thread):
  # 뉴스링크로부터 파싱하는 함수
  if thread==0:
    result = []
    for idx in tqdm(range(len(news_list))):
      response = requests.get(news_list[idx], headers=header)
      try :
        if response.status_code!=200:
          print(f"ERROR {idx} : CODE <{response.status_code}>")
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        # title
        title = soup.find('h3',id='articleTitle').text
        # content
        article_raw = soup.find('div',id='articleBodyContents')
        for get_rid_of in ['span.end_photo_org','div[style]','script']:
          for s in article_raw.select(get_rid_of):
            s.extract()
        content = article_raw.get_text().replace('\n','').replace('\t','')
        result.append([idx,title,content,news_list[idx]])
      except :
        # print(f"ERROR {idx} : link {news_list[idx]}")
        pass
    print("put...",end='')
    saver.put(result)
    return result
  
  else :
    result = []
    for idx in range(len(news_list)):
      response = requests.get(news_list[idx], headers=header)
      try :
        if response.status_code!=200:
          print(f"ERROR {idx} : CODE <{response.status_code}>")
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        # title
        title = soup.find('h3',id='articleTitle').text
        # content
        article_raw = soup.find('div',id='articleBodyContents')
        for get_rid_of in ['span.end_photo_org','div[style]','script']:
          for s in article_raw.select(get_rid_of):
            s.extract()
        content = article_raw.get_text().replace('\n','').replace('\t','')
        result.append([idx,title,content,news_list[idx]])
      except :
        # print(f"ERROR {idx} : link {news_list[idx]}")
        pass
    print("put...",end='')
    saver.put(result)
    return result

def split_by(news_list):
  # 멀티프로세싱을 위해 나눠주는 함수
  n = 10
  k = int(len(news_list)/n)
  news_list_list = []
  for i in range(n):
    if i == n-1 :
      news_list_list.append(news_list[i*k:])
    else :
      news_list_list.append(news_list[i*k:(i+1)*k])
  return news_list_list

def crawling(news_list_list):
  # 멀티쓰레드를 이용한 크롤링함수
  saver = mp.Queue()
  jobs = []
  for thread, nl in enumerate(news_list_list):
    jobs.append(Thread(target=get_content_from_news_list,args=(nl,header,saver,thread)))
  for j in jobs:
    j.start()
  for j in jobs:
    j.join()

  saver.put('stop')
  total = []
  while True:
      tmp = saver.get()
      if tmp == 'stop':
          break
      else:
          total.append(tmp)

  results_gas=[]
  for t in total:
    results_gas.extend(t)


  for i in range(len(results_gas)):
    if type(results_gas[i][2])!=str:
      print(i)
  return results_gas

# 링크 수집
newslist_file = glob.glob("/<yourdir>/*.txt")
newslist_file_2000_2004 = []    # 멀티쓰레드를위해 따로 분리
newslist_file_2005_2009 = []    # 멀티쓰레드를위해 따로 분리
newslist_file_2010_2014 = []    # 멀티쓰레드를위해 따로 분리
num_of_news = 0

for f in newslist_file:
  if f.split('_')[1] in [str(i) for i in range(2000,2005)]:
    newslist_file_2000_2004.append(f)
    num_of_news+=int(f.split('_')[-1].split('.')[0])
  elif f.split('_')[1] in [str(i) for i in range(2005,2010)]:
    newslist_file_2005_2009.append(f)
    num_of_news+=int(f.split('_')[-1].split('.')[0])
  elif f.split('_')[1] in [str(i) for i in range(2010,2015)]:
    newslist_file_2010_2014.append(f)
    num_of_news+=int(f.split('_')[-1].split('.')[0])
  else :
    # print(f)
    pass

newslist_2000_2004 = make_list(newslist_file_2000_2004)
newslist_2005_2009 = make_list(newslist_file_2005_2009)
newslist_2010_2014 = make_list(newslist_file_2010_2014)

newslist_2000_2004 = split_by(newslist_2000_2004)
newslist_2005_2009 = split_by(newslist_2005_2009)
newslist_2010_2014 = split_by(newslist_2010_2014)

results_gas1 = crawling(newslist_2000_2004)
results_gas2 = crawling(newslist_2005_2009)
results_gas3 = crawling(newslist_2010_2014)

# data frame화
df_gas1 = pd.DataFrame(results_gas1, columns=['index','title','content','url']).drop(columns=['index'])
df_gas2 = pd.DataFrame(results_gas2, columns=['index','title','content','url']).drop(columns=['index'])
df_gas3 = pd.DataFrame(results_gas3, columns=['index','title','content','url']).drop(columns=['index'])

# 단순전처리
def preprocessing(txt):
  txt = txt.replace('\r',' ')
  return txt
df_gas1['content']=df_gas1['content'].apply(preprocessing)
df_gas2['content']=df_gas2['content'].apply(preprocessing)
df_gas3['content']=df_gas3['content'].apply(preprocessing)
df_gas1['title']=df_gas1['title'].apply(preprocessing)
df_gas2['title']=df_gas2['title'].apply(preprocessing)
df_gas3['title']=df_gas3['title'].apply(preprocessing)

# merge & save
df_merge = pd.concat([df_gas1,df_gas2,df_gas3])
df_merge = df_merge.reset_index(drop=True)
df_merge.to_csv("/<your dir>.csv", index=False)
