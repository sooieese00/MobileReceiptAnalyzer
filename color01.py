import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

# 예제 데이터
category_sum = pd.Series([55, 43, 2, 78,99], index=['aa', 'bb', 'cc', 'dd', 'ee'])

# 테마 색상 설정
themes = {
    "Theme 1": ['#FF5733', '#33FF57', '#3357FF'],  # 빨강, 초록, 파랑
    "Theme 2": ['#FFBD33', '#33FFBD', '#BD33FF'],  # 주황, 민트, 보라
    "Theme 3": ['#FF33A6', '#A6FF33', '#33A6FF'],  # 핑크, 라임, 청록
    "Theme 4": ['#3333FF', '#33FF33', '#FF3333']   # 파랑, 초록, 빨강
}

# 차트 생성 및 이미지 저장 함수
def create_donut_chart(category_sum, colors, theme_name):
    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(
        category_sum,
        labels=category_sum.index,
        startangle=90,
        wedgeprops={'width': 0.4, 'edgecolor': 'w'},
        autopct='%1.1f%%',
        pctdistance=0.85,
        colors=colors
    )
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    plt.legend(
        loc='upper left',
        bbox_to_anchor=(1, 1),
        title="Categories"
    )
    img = io.BytesIO()
    plt.savefig(f"{theme_name}.png", format='png', bbox_inches='tight')
    plt.close()

# 각 테마에 대해 차트 생성
for theme_name, colors in themes.items():
    create_donut_chart(category_sum, colors, theme_name)
