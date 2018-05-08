from __future__ import print_function
from lexrankr import LexRank

# 이거 아님

lexrank = LexRank()  # can init with various settings
lexrank.summarize('''
경찰이 잠실야구장에서 벌어진 '현대판 노예사건'에 대해 본격 수사에 착수했다. 앞서 서울시장애인인권센터는 이곳 분리수거장에서 A씨(60)를 구조하고, 그가 임금을 받지 못한 채 노예처럼 일해온 것으로 추정된다며 수사를 의뢰했다.

서울 송파경찰서는 A씨를 고용한 고물업체 사장 B씨를 최근 불구속 입건하고 인권센터가 제기한 사기·폭행·가혹행위 등의 의혹에 대해 수사 중이라고 20일 밝혔다.

인권센터와 경찰 등에 따르면 B씨는 지난 17년 동안 A씨에게 제대로 된 임금을 주지 않고 분리수거 업무를 시킨 의혹을 받는다. 

특히 인권센터는 A씨가 떨어진 빵으로 끼니를 채우면서 하루 16시간 동안 일하는 등 노동착취를 당했다고 주장했다. 지적장애를 가진 A씨는 분리수거장 내부 컨테이너에서 지금껏 생활해온 것으로 알려졌다.

현재 경찰은 인권센터와 언론에서 제기한 의혹에 대해 사실관계를 확인하는 중이다. 피해자와 고물업체 사장, 잠실야구장 시설관리자 등에 대해 한차례씩 조사도 진행했다. 

경찰관계자는 "피해자의 계좌 입출금 내역을 분석하고 있다"며 "학대 등의 혐의가 있는지 확인하기 위해 추가로 관계자들을 조사할 계획"이라고 밝혔다. 
''')
summaries = lexrank.probe(1)  # `num_summaries` can be `None` (using auto-detected topics)
for summary in summaries: # 그냥 출력
    print(summary)

from firebase import firebase
firebase = firebase.FirebaseApplication('https://chatbot-c6606.firebaseio.com')

result = firebase.post('/',{'news':summary})
print(result)