import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from datetime import datetime, timedelta
from math import cos, sin, radians


# 엑셀 파일 경로
file_path = 'C:/Users/soo/Desktop/soo/2024/dx/receipts/Account.xlsx'

# 엑셀 파일에서 데이터 읽기, 헤더가 6번째 행에 있음
df = pd.read_excel(file_path, sheet_name='지출리스트', header=5, usecols='B:G')

# '날짜' 열을 datetime 형식으로 변환
df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')

# 가장 큰 날짜 (가장 최근 날짜)
latest_date = df['날짜'].max()

# 최근 3개월 동안의 데이터 필터링
three_months_ago = latest_date - timedelta(days=90)
filtered_df = df[df['날짜'] >= three_months_ago]

# 1) 분류별로 금액을 더해서 도넛모양파이차트 생성
category_sum = filtered_df.groupby('분류')['금액'].sum()

# 한글 폰트 설정 (예: 맑은 고딕)
font_path = "C:/Windows/Fonts/malgun.ttf"  # 윈도우 시스템에서의 맑은 고딕 폰트 경로
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# 도넛 차트 생성
fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts = ax.pie(category_sum, startangle=90, wedgeprops=dict(width=0.3, edgecolor='w'))

# 각 파이 조각 위에 분류 이름과 퍼센티지를 표시
total = sum(category_sum)
for i, (wedge, label) in enumerate(zip(wedges, category_sum.index)):
    angle = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
    x = wedge.r * 0.7 * cos(radians(angle))
    y = wedge.r * 0.7 * sin(radians(angle))
    percent = f'{100 * category_sum[i] / total:.1f}%'
    ax.text(x, y, f"{label}\n{percent}", ha='center', va='center', fontsize=10, weight="bold", color="black")



# 범례에 분류 이름 옆에 합계 가격 표시
max_label_length = max(len(cat) for cat in category_sum.index)
legend_labels = [f"{cat.ljust(max_label_length)} ({val:.0f}원)" for cat, val in zip(category_sum.index, category_sum)]
ax.legend(wedges, legend_labels, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
plt.title('분류별 금액 합계 (최근 3개월)')
plt.show()

# 2) 품목별로 수량을 합쳐서 가장 많이 구매한 품목 5가지를 출력
top_items = filtered_df.groupby('품목')['수량'].sum().sort_values(ascending=False).head(5).astype(int)
print("가장 많이 구매한 품목 5가지")
for item, quantity in top_items.items():
    print(f"{item} ##{quantity}개")