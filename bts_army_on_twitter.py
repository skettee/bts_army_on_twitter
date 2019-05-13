#%% [markdown]
# ## BTS 아미 트윗 🤖
# ### 방탄소년단 아미의 트윗을 모아주는 봇입니다.
# 
# ### 개발 환경 만들기
# 
#  봇을 개발하기 위해서는 몇가지 소프트웨어를 설치하고 환경을 설정해야 합니다. 
#  [개발 환경 만들기](https://github.com/moabogey/docs/wiki/개발환경만들기)를 참조 하세요.
# 
# ### 코드 실행
# 
#  - 터미널 실행
#    1. 🖼  Windows PowerShell을 실행한다.
#    2. 🍎 Terminal을 실행한다.
# 
#  - 작업할 폴더를 생성한다.
# 
#  ```
#  mkdir MyWork
#  ```
# 
#  - 작업할 폴더로 이동한다.
#  
#  ```
#  cd MyWork
#  ```
# 
#  - 깃 클론 (Git Clone)을 수행한다.
# 
#  ```
#  git clone https://github.com/skettee/bts_army_on_twitter.git
#  ```
# 
#  - 복사한 코드의 폴더로 이동한다.
# 
#  ```
#  cd bts_army_on_twitter
#  ```
# 
#  - VSCode를 실행한다.
# 
#  ```
#  code .
#  ```
# 
#  - 왼쪽 EXPLORE에서 `bas_army_on_twitter.py`를 선택한다.
# 
#  - 하단 바에 `Python3.7.3 64-bit('base':conda)`를 누른다.
# 
#  - `Python 3.6.8 64-bit ('moabogey':conda)`를 선택한다.
# 
#  - 소스 코드에 RunCell | Run Below에서 `Run Below`를 누른다.
# 
#  - 데이터가 정상적으로 수집이 되는지 오른쪽 Python Interactive에서 확인한다. 
#    
#
# ### 코드 분석
# 
#  bts_army_on_twitter.py를 분석합니다.  
#  봇의 소스 코드는 크게 세단계로 나눌 수 있습니다.  
# 
#  1. 사이트의 HTML에서 데이터를 수집
# 
#  2. 포스트의 HTML에서 데이터를 수집
# 
#  3. 데이터 저장
#  
# **사이트의 HTML에서 데이터를 수집**
#  
#    - 데이터를 수집할 사이트의 정보와 주소를 설정합니다. 예제에서는 https://twitter.com/BTS_ARMY 에서 데이터를 수집합니다.
# 
#    - requests와 beautifulsoup4를 이용해서 사이트의 HTML을 가져오고 파일로 저장합니다.
# 
#    - 저장된 HTML파일 (예제에서는 twitter_source.html)을 열어 봅니다. 여기서 우리는 "포스트의 리스트"를 표현하는 구간을 찾을 것입니다. ***포스트***는 제목, 내용, 이미지, 작성자, 작성 날짜 및 페이지 위치(URL)를 가지고 있는 하나의 문서(여기서는 트윗)를 나타내는 용어로 사용합니다.
# 
#    ```
#    +-------------+  +-->   <div class="content">
#    |   Post 1    
#    |  (Tweet 1)   
#    +-------------+  +-->   </div>
#    
#    +-------------+  +-->   <div class="content">
#    |   Post 2    
#    |  (Tweet 2)  
#    +-------------+  +-->   </div>
#    
#    +-------------+  +-->  <div class="content">
#    |   Post3     
#    |  (Tweet 3)
#    +-------------+  +-->   </div>
#    ```
#  
#    - 예제에서 각각의 포스트는 `<div class="content">` 에서 시작 되고 `</div>`로 끝난다는 것을 알아내는 것이 중요합니다. 이것은 사이트마다 다르기 때문에 이것을 찾아내는 것은 약간의 경험이 필요합니다.
# 
#    - 발견한 포스트에서 아래와 같이 작성자, 올린 시간 및 포스트 위치(URL)을 찾습니다.
# 
#    ```
#    +-------------+
#    |   Post 1    
#    +-------------+
#    |  createdBy  +-->  <strong class="fullname...> </strong>
#    |             
#    |  post URL   +-->  <a class="tweet-timestamp... href=...>
#    |             
#    |  createdAt  +-->  <a class="tweet-timestamp... title=...>
#    |             
#    +-------------+
#    ```
#  
#    - 나머지 데이터를 수집하기 위해서 포스트 HTML로 이동합니다.
#  
# **포스트의 HTML에서 데이터를 수집**
# 
#    - 데이터를 수집할 포스트의 주소를 설정합니다.
# 
#    - requests와 beautifulsoup4를 이용해서 사이트의 HTML을 가져오고 파일로 저장합니다.
# 
#    - 저장된 HTML파일 (예제에서는 twitter_post_source.html)을 열어 봅니다. 여기서 우리는 포스트의 제목, 요약, 이미지, 사이트 이름, 포스트 주소(URL), 수집 날짜 및 시간 데이터를 수집할 것입니다.
#  
# **Open Graph Protocol**
# 
#    - 대부분의 사이트들은 우리가 수집할 데이터를 사이트의 첫머리에 미리 모아 놓고 있습니다. 이 규약(Protocol)은 사이트를 모두 분석하지 않고도 사이트의 내용을 파악하는데 도움이 됩니다.
# 
#    - 아래와 같은 메타 태그를 사용합니다.
# 
#   ```html
#   <head>
#   ...
#       <meta content="..." property="og:url"/>
#       <meta content="..." property="og:title"/>
#       <meta content="..." property="og:image"/>
#       <meta content="..." property="og:description"/>
#       <meta content="..." property="og:site_name"/>
#   ...
#   </head>
#   ```
# 
#    - 메타 태그에서 데이터를 수집합니다.
#  
# **데이터 저장**
# 
#    - 수집한 데이터를 선별해서 중복되는 것을 제외하고 데이터베이스에 저장합니다. 모아보기 봇은 하루에 24번 이상 동작 하도록 되어 있기 때문에 한번에 모든 데이터를 수집하지 않고 가장 최근의 데이터 1~2개를 수집하는 것이 원칙입니다. 여기서는 데이터를 수집한 날짜와 동일한 날에 등록된 포스트만 수집하도록 프로그래밍되어 있습니다.
#  
#
# ### 참고 사이트
#  
# - [개발 환경 만들기](https://github.com/moabogey/docs/wiki/개발환경만들기)
#
# - [예제 코드 실행](https://github.com/moabogey/docs/wiki/예제코드실행)
#
# - [코딩을 하기 전에](https://github.com/moabogey/docs/wiki/코딩하기전에)
#
# - [예제 코드 분석](https://github.com/moabogey/docs/wiki/예제코드분석)
#
# - [봇 개발 하기](https://github.com/moabogey/docs/wiki/봇개발하기)

#%%
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
from datetime import timedelta

if __debug__:
    import os.path

# 모아보기 컴포넌트를 가져온다.
import moabogey_database as moabogey
from moabogey_id import *

# 사이트 이름
site_name = 'twitter'
# 사이트에서 가져올 주제
subject_name = 'BTS_ARMY'
# 사이트 주소
site_url = 'https://twitter.com/BTS_ARMY'
if __debug__:
    print('🤟{}🤟 데이터 수집 중... ⚙️'.format(site_url))

# 사이트의 HTML을 가져온다.
try:
    response = requests.get(site_url)
    # 에러가 발생 했을 경우 에러 내용을 출력하고 종료한다.
    response.raise_for_status()
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')
else:
    html_source = response.text
    
    # BeautifulSoup 오브젝트를 생성한다.
    soup = BeautifulSoup(html_source, 'html.parser')
    
    # HTML을 분석하기 위해서 페이지의 소스를 파일로 저장한다.
    if __debug__:
        file_name = site_name + '_source.html'
        if not os.path.isfile(file_name):
            print('file save: ', file_name)
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
       
    # 데이터를 저장할 데이터베이스를 생성한다. 
    # bot_id는 moabogey_id에서 가져온 값이다.
    db_name = subject_name + '_on_' + site_name 
    my_db = moabogey.Dbase(db_name, bot_id)
            
    # 반복해서 포스트의 목록을 하나씩 검색하며 데이터를 수집한다.
    for post in soup.find_all('div', class_='content'):
        # 포스트를 올린 작성자를 수집한다.
        moa_createBy = post.find('strong', class_='fullname').text.strip()
        #print('createdBy: ', moa_createBy)

        # 포스트의 주소를 수집한다.
        href = post.find('a', {"class": "tweet-timestamp", "href": True})
        if href:
            href = href['href'] 
            href_url = 'https://twitter.com' + href
            #print('href: ', href_url)

            # 포스트를 올린 날짜를 수집한다.
            if __debug__:
                # LANGUAGE KOREA CASE
                post_time = post.find('a', class_="tweet-timestamp")['title'].replace('오전', 'AM').replace('오후', 'PM')
                # 시간 형식 - AM 2:27 - 2019년 3월 11일
                moa_createdAt = datetime.strptime(post_time, '%p %I:%M - %Y년 %m월 %d일')
            else:
                # LANGUAGE UNDEFINED CASE
                post_time = post.find('a', class_="tweet-timestamp")['title']
                # 시간 형식 - 8:01 PM - 30 Mar 2019
                moa_createdAt = datetime.strptime(post_time, '%I:%M %p - %d %b %Y')

            # 시간을 보정한다. UTC (+7) ?
            moa_createdAt = moa_createdAt + timedelta(hours=7)

            # 포스트의 HTML을 가져온다.
            try:
                response =  requests.get(href_url)
                response.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            except Exception as err:
                print(f'Other error occurred: {err}')
            else:
                subhtml_source = response.text
                # BeautifulSoup 오브젝트를 생성한다.
                post = BeautifulSoup(subhtml_source, 'html.parser')

                # HTML을 분석하기 위해서 포스트의 소스를 파일로 저장한다.
                if __debug__:
                    file_name = site_name + '_post_source.html'
                    if not os.path.isfile(file_name):
                        print('file save: ', file_name)
                        with open(file_name, 'w', encoding='utf-8') as f:
                            f.write(post.prettify())

                # 포스트 제목을 수집/가공 한다.
                #moa_title = post.find('meta', property="og:title")
                moa_title = post.find('meta', property="og:description")
                if moa_title:
                    moa_title = moa_title['content'].splitlines()[0]
                
                # 포스트 요약을 수집/가공한다.
                moa_desc = post.find('meta', property="og:description")
                if moa_desc:
                    moa_desc = ''.join(moa_desc['content'].splitlines()[1:])
                
                # 대표 이미지의 주소를 수집한다.
                moa_image = post.find('meta', property="og:image")
                if moa_image:
                    moa_image = moa_image['content']
                
                # 사이트 이름을 수집한다.
                moa_site_name = post.find('meta', property="og:site_name")
                if moa_site_name:
                    moa_site_name = moa_site_name['content']
                
                # 포스트의 주소를 수집한다.
                moa_url = href_url
                
                # 현재 날짜와 시간을 수집한다.
                moa_timeStamp = datetime.now()

                # 오늘 발행된 포스트만 선택한다.
                delta = moa_timeStamp - moa_createdAt + timedelta(hours=9)
                if delta.days <=0:
                
                    # 데이터베이스에 있는 포스트와 중복되는지를 확인한다.
                    if my_db.isNewItem('title', moa_title):
                        # 데이터 타입을 확인한다.
                        assert type(moa_title) == str, 'title: type error'
                        assert type(moa_desc) == str, 'desc: type error'
                        assert type(moa_url) == str, 'url: type error'
                        assert type(moa_image) == str, 'image: type error'
                        assert type(moa_site_name) == str, 'siteName: type error'
                        assert type(moa_createBy) == str, 'createBy: type error'
                        assert type(moa_createdAt) == datetime, 'createdAt: type error'
                        assert type(moa_timeStamp) == datetime, 'timeStamp: type error'
                        
                        # JSON형식으로 수집한 데이터를 변환한다.
                        db_data = { 'title': moa_title, 
                            'desc': moa_desc,
                            'url': moa_url,
                            'image': moa_image,
                            'siteName': moa_site_name,
                            'createdBy': moa_createBy,
                            'createdAt': moa_createdAt,
                            'timeStamp': moa_timeStamp
                        }

                        if __debug__:
                            # 디버그를 위해서 수집한 데이터를 출력한다.
                            temp_data = db_data.copy()
                            temp_data['desc'] = temp_data['desc'][:20] + '...'
                            print('📀 수집한 json data: ')
                            print(json.dumps(temp_data, indent=4, ensure_ascii=False, default=str))

                        # 수집한 데이터를 데이터베이스에 전송한다.
                        my_db.insertTable(db_data)

    # 데이터 베이스에 저장된 데이터를 디스플레이 한다.
    if __debug__:
        my_db.displayHTML()

    # 데이터 베이스를 닫는다.
    my_db.close()
    
