import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# 사용할 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows의 Malgun Gothic 폰트 경로
font_prop = fm.FontProperties(fname=font_path)

# 샘플 데이터
labels = ['항목1', '항목2', '항목3', '항목4', '항목5', '항목6', '항목7', '항목8']
sizes = [15, 20, 30, 10, 5, 10, 5, 5]
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6', '#c4e17f', '#76d7c4']

# 파이 차트 그리기
plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, textprops={'fontproperties': font_prop})
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# 제목 추가
plt.title('테마2 - 파이 차트', fontproperties=font_prop)

# 플롯 저장
theme_name = 'theme2'
plt.savefig(f"{theme_name}.png", format='png', bbox_inches='tight')

# 플롯 보여주기
plt.show()
