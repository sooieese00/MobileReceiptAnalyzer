import pandas as pd
import datetime
from collections import defaultdict

# 엑셀 파일 경로
file_path = 'C:/Users/soo/Desktop/soo/2024/dx/receipts/Account.xlsx'

# 엑셀 파일을 읽어서, 헤더가 5번째 행(B6, C6, F6)에 있다고 지정
data = pd.read_excel(file_path, sheet_name='지출리스트', header=5, usecols='B,C,F')

# '날짜' 열을 datetime 형식으로 변환
data['날짜'] = pd.to_datetime(data['날짜'], errors='coerce')

# 결측치가 있는 행 제거
cleaned_data = data.dropna()

# 데이터를 dictionary 리스트 형태로 변환
purchase_history = [
    {"날짜": row['날짜'], "분류": row['분류'], "수량": row['수량']}
    for _, row in cleaned_data.iterrows()
]

# 가장 최근의 날짜 구하기
latest_date = cleaned_data['날짜'].max()

# 구매 주기 계산 함수
def calculate_purchase_cycle(purchase_history):
    # 분류별 구매 데이터 정리
    items = defaultdict(list)
    for purchase in purchase_history:
        date = purchase["날짜"]
        items[purchase["분류"]].append({"날짜": date, "수량": purchase["수량"]})

    # 주기 계산
    item_cycles = {}
    for 분류, purchases in items.items():
        if len(purchases) < 2:
            # 구매 기록이 하나뿐인 경우 주기를 계산할 수 없음
            item_cycles[분류] = 0
            continue

        purchases.sort(key=lambda x: x["날짜"])  # 날짜순 정렬
        total_quantity = sum(p["수량"] for p in purchases[:-1])  # 마지막 구매 수량 제외
        weighted_sum = 0

        for i in range(1, len(purchases)):
            days_between = (purchases[i]["날짜"] - purchases[i-1]["날짜"]).days
            weighted_sum += days_between * purchases[i-1]["수량"]

        if total_quantity > 0:  # 분모가 0이 되는 경우를 방지
            purchase_cycle = weighted_sum / total_quantity
        else:
            purchase_cycle = 0  # 혹시나 모든 수량이 마지막 구매에 해당하면 0으로 설정

        item_cycles[분류] = purchase_cycle

    return item_cycles

# 구매 주기 계산
item_cycles = calculate_purchase_cycle(purchase_history)
print("구매 주기:", item_cycles)

# 주기 데이터를 정렬된 리스트로 변환
sorted_cycles = sorted(item_cycles.items(), key=lambda x: x[1])

# 각 구매 주기 간 차이가 7 이하인 분류들을 그룹화
def group_cycles(sorted_cycles, max_diff=7):
    groups = []
    group = []

    for i in range(len(sorted_cycles)):
        if sorted_cycles[i][1] == 0:
            continue
        if not group or sorted_cycles[i][1] - group[0][1] <= max_diff:
            group.append(sorted_cycles[i])
        else:
            groups.append(group)
            group = [sorted_cycles[i]]

    if group:
        groups.append(group)

    # 그룹 내에서 가장 큰 값과 가장 작은 값의 차이가 7 이하인지 확인
    final_groups = []
    for group in groups:
        if max(group, key=lambda x: x[1])[1] - min(group, key=lambda x: x[1])[1] <= max_diff:
            final_groups.append(group)

    return final_groups

# 각 그룹의 단순 평균 계산
def calculate_group_averages(groups):
    averages = {}
    for group in groups:
        group_name = ", ".join([item[0] for item in group])
        group_average = sum(item[1] for item in group) / len(group)
        averages[group_name] = group_average
    return averages

# 그룹화 및 평균 계산
groups = group_cycles(sorted_cycles)
averages = calculate_group_averages(groups)

# 그룹별 마지막 구매 일자 계산
def get_last_purchase_dates(groups, purchase_history):
    last_purchase_dates = {}
    for group in groups:
        group_name = ", ".join([item[0] for item in group])
        last_dates = []
        for item in group:
            for purchase in purchase_history:
                if purchase["분류"] == item[0]:
                    last_dates.append(purchase["날짜"])
        last_purchase_dates[group_name] = max(last_dates) if last_dates else None
    return last_purchase_dates

last_purchase_dates = get_last_purchase_dates(groups, purchase_history)

# 그룹별 다음 구매 일자 도출 함수
def recommend_next_purchase_dates(averages, last_purchase_dates, num_recommendations=3):
    recommendations = []
    for group_name, average in averages.items():
        if last_purchase_dates[group_name]:
            next_purchase_date = last_purchase_dates[group_name] + datetime.timedelta(days=round(average))
            while next_purchase_date <= latest_date:
                next_purchase_date += datetime.timedelta(days=round(average))
            for _ in range(num_recommendations):
                recommendations.append(f"{next_purchase_date.strftime('%Y년 %m월 %d일')}은 {group_name} 사는 날입니다")
                next_purchase_date += datetime.timedelta(days=round(average))
    return recommendations

# 다음 구매 일자 추천
recommendations = recommend_next_purchase_dates(averages, last_purchase_dates)

# 결과 출력
for recommendation in recommendations:
    print(recommendation)
