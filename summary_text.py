from __future__ import print_function
from textrankr import TextRank

textrank = TextRank('''
육아의 필수품이 된 물티슈가 알레르기의 원인이 될 수 있다는 연구 결과가 나왔다.

미국 노스웨스턴대학교 연구진은 물티슈로 아기를 닦으면 피부에 남은 비누기(라우릴황산나트륨 등 계면활성제)가 보호막 역할을 하는 기름기(지질)를 없애 아기들에게 알레르기가 생기기 쉽다고 밝혔다.

특히 이번 연구에서 주목할 점은 유전적으로 피부가 약한 아기들에게 물티슈의 화학물질은 식품 알레르기의 원인이 될 수 있다는 것이다.

조앤 쿡 밀스 교수는 '유전자, 먼지와 음식, 그리고 물티슈는 유아 알레르기의 '더 할 수 없이 나쁜 상황(perfect storm)'이다'라고 말했다.

연구에 따르면 알레르기가 있는 아이들은 피부 보호막을 약하게 하는 세 가지 돌연변이 유전자가 있었다. 그러나 해당 유전자를 가졌다고 해서 모두 식품 알레르기 반응을 보인 것은 아니었다.

예컨대 해당 유전자를 가진 실험용 생쥐를 땅콩에 노출해도 별다른 반응이 나타나지 않았던 것. 연구진은 환경적 요인에 주목했다. 실험 끝에 연구진이 식품 알레르기를 유발하는 원인으로 지목한 것 중 하나가 물티슈였다.

연구진은 물티슈의 비누 성분이 피부의 보호막을 약하게 만들어 특히 유전적으로 취약한 아이들에게 나쁜 영향을 미치는 것을 발견했다.

연구진은 유전적 결함이 있는 아기들의 피부가 물티슈의 비누 성분을 접촉했을 때 먼지나 땅콩 등 알레르기 물질이 체내에 유입되기 쉽다고 지적했다. 이 경우 예컨대 땅콩버터 샌드위치를 먹은 누군가가 아기에게 접촉하는 것만으로도 알레르기가 생길 수 있다고 연구진은 경고했다.

연구진은 '신세대 부모들이 물티슈 사용을 줄이는 것이 바람직하다'면서 '가장 좋은 방법은 예전에 부모들이 그랬듯이 물로 씻기는 것'이라고 덧붙였다.
''')
print(textrank.summarize(1))
print(textrank.summarize(1))