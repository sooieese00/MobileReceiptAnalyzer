import datetime
from collections import defaultdict

# 과거 구매 데이터 예시
purchase_history = [
    {"구매일자": "2022-01-01", "품목": "우유/유제품", "수량": 2},
    {"구매일자": "2022-01-14", "품목": "우유/유제품", "수량": 1},
    {"구매일자": "2022-01-27", "품목": "우유/유제품", "수량": 3},
    {"구매일자": "2022-02-09", "품목": "우유/유제품", "수량": 2},
    {"구매일자": "2022-01-05", "품목": "채소", "수량": 1},
    {"구매일자": "2022-01-20", "품목": "채소", "수량": 1},
    {"구매일자": "2022-02-04", "품목": "채소", "수량": 1},
    {"구매일자": "2022-02-19", "품목": "채소", "수량": 1},
    {"구매일자": "2022-01-10", "품목": "정육/계란류", "수량": 2},
    {"구매일자": "2022-01-25", "품목": "정육/계란류", "수량": 1},
    {"구매일자": "2022-02-09", "품목": "정육/계란류", "수량": 3},
    {"구매일자": "2022-02-24", "품목": "정육/계란류", "수량": 2},
    {"구매일자": "2022-01-07", "품목": "수산물/건해산", "수량": 1},
    {"구매일자": "2022-01-28", "품목": "수산물/건해산", "수량": 2},
    {"구매일자": "2022-02-18", "품목": "수산물/건해산", "수량": 1},
    {"구매일자": "2022-03-11", "품목": "수산물/건해산", "수량": 3},
    {"구매일자": "2022-01-03", "품목": "생수/음료/주류", "수량": 3},
    {"구매일자": "2022-01-27", "품목": "생수/음료/주류", "수량": 2},
    {"구매일자": "2022-02-20", "품목": "생수/음료/주류", "수량": 1},
    {"구매일자": "2022-03-16", "품목": "생수/음료/주류", "수량": 4},
    {"구매일자": "2022-01-01", "품목": "청소/생활용품", "수량": 2},
    {"구매일자": "2022-03-02", "품목": "청소/생활용품", "수량": 1},
    {"구매일자": "2022-05-01", "품목": "청소/생활용품", "수량": 1},
    {"구매일자": "2022-07-01", "품목": "청소/생활용품", "수량": 2}
]

# 구매 주기 계산 함수
def calculate_purchase_cycle(purchase_history):
    # 품목별 구매 데이터 정리
    items = defaultdict(list)
    for purchase in purchase_history:
        date = datetime.datetime.strptime(purchase["구매일자"], "%Y-%m-%d")
        items[purchase["품목"]].append({"구매일자": date, "수량": purchase["수량"]})

    # 주기 계산
    item_cycles = {}
    for 품목, purchases in items.items():
        purchases.sort(key=lambda x: x["구매일자"])  # 날짜순 정렬
        total_quantity = sum(p["수량"] for p in purchases[:-1])  # 마지막 구매 수량 제외
        weighted_sum = 0

        for i in range(1, len(purchases)):
            days_between = (purchases[i]["구매일자"] - purchases[i-1]["구매일자"]).days
            weighted_sum += days_between * purchases[i-1]["수량"]

        if total_quantity > 0:  # 분모가 0이 되는 경우를 방지
            purchase_cycle = weighted_sum / total_quantity
        else:
            purchase_cycle = 0  # 혹시나 모든 수량이 마지막 구매에 해당하면 0으로 설정

        item_cycles[품목] = purchase_cycle

    return item_cycles

# 구매 주기 계산
item_cycles = calculate_purchase_cycle(purchase_history)
print("구매 주기:", item_cycles)

import itertools

# 주기 데이터를 정렬된 리스트로 변환
sorted_cycles = sorted(item_cycles.items(), key=lambda x: x[1])

# 각 구매 주기 간 차이가 7 이하인 품목들을 그룹화
def group_cycles(sorted_cycles, max_diff=7):
    groups = []
    group = [sorted_cycles[0]]

    for i in range(1, len(sorted_cycles)):
        if sorted_cycles[i][1] - group[0][1] <= max_diff:
            group.append(sorted_cycles[i])
        else:
            groups.append(group)
            group = [sorted_cycles[i]]

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
    
groups = group_cycles(sorted_cycles)
averages = calculate_group_averages(groups)

# 결과 출력
for group_name, average in averages.items():
    print(f"그룹: {group_name}, 평균 구매 주기: {average:.2f}일")

# 그룹별 마지막 구매 일자 계산
def get_last_purchase_dates(groups, purchase_history):
    last_purchase_dates = {}
    for group in groups:
        group_name = ", ".join([item[0] for item in group])
        last_dates = []
        for item in group:
            for purchase in purchase_history:
                if purchase["품목"] == item[0]:
                    last_dates.append(datetime.datetime.strptime(purchase["구매일자"], "%Y-%m-%d"))
        last_purchase_dates[group_name] = max(last_dates) if last_dates else None
    return last_purchase_dates

# 그룹별 다음 구매 일자 도출 함수
def recommend_next_purchase_dates(averages, last_purchase_dates):
    recommendations = []
    for group_name, average in averages.items():
        if last_purchase_dates[group_name]:
            next_purchase_date = last_purchase_dates[group_name] + datetime.timedelta(days=round(average))
            recommendations.append(f"{next_purchase_date.strftime('%Y년 %m월 %d일')}은 {group_name} 사는 날입니다")
    return recommendations

# 그룹화 및 평균 계산
groups = group_cycles(sorted_cycles)
averages = calculate_group_averages(groups)

# 그룹별 마지막 구매 일자 계산
last_purchase_dates = get_last_purchase_dates(groups, purchase_history)

# 다음 구매 일자 추천
recommendations = recommend_next_purchase_dates(averages, last_purchase_dates)

# 결과 출력
for recommendation in recommendations:
    print(recommendation)