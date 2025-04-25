import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
# 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
columns = [
    "No", "학년", "col2", "이수구분", "col4", "학수번호",
    "col6", "col7", "col8", "col9", "col10", "col11", "col12",
    "교과목명", "col14", "col15", "col16", "col17", "col18", "col19", "col20",
    "col21", "col22", "col23", "col24", "col25", "학점", "이론시간", "실습시간",
    "col29", "강의시간", "분반", "담당교수", "col33"
]
df = pd.read_csv("SOOMIN_timetable.csv", header=1, names=columns)
# 교수 익명화
unique_profs = df['담당교수'].dropna().unique()
prof_mapping = {name: f"교수 {i+1}" for i, name in enumerate(unique_profs)}
df['익명_교수'] = df['담당교수'].map(prof_mapping)


#요일별 강의수
df['강의시간리스트'] = df['강의시간'].astype(str).str.split('\n')
df['요일'] = df['강의시간리스트'].str[0].str.extract(r"([월화수목금토일])")
df['강의실'] = df['강의시간리스트'].str[0].str.extract(r"\((.*?)\)")
# 강의실 익명화
unique_rooms = df['강의실'].dropna().unique()
room_mapping = {name: f"강의실 {i+1}" for i, name in enumerate(unique_rooms)}
df['익명_강의실'] = df['강의실'].map(room_mapping)

# 요일 정제 + 완전 새 컬럼
df['요일_정제'] = df['요일'].astype(str).str.replace("요일", "", regex=False).str.strip()

# 카테고리 순서 지정
요일순서 = ['월', '화', '수', '목', '금', '토', '일']
df['요일_정제'] = pd.Categorical(df['요일_정제'], categories=요일순서, ordered=True)

# 그래프
df['요일_정제'].value_counts().sort_index().plot(kind='bar')
plt.title("요일별 수업 수")
plt.xlabel("요일")
plt.ylabel("수업 수")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
#요일별 강의수 끝

#최다 이용 강의실
top_rooms = df['익명_강의실'].value_counts().head(10)

top_rooms.plot(kind='bar')
plt.title("가장 자주 사용된 강의실 Top 10 (익명)")
plt.xlabel("강의실")
plt.ylabel("사용 횟수")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#최다 이용 강의실 끝

#가장 많은 수업을 맡고 계신 교수님
top_profs = df['익명_교수'].value_counts().head(10)

top_profs.plot(kind='bar')
plt.title("수업을 가장 많이 맡은 교수님 Top 10 (익명)")
plt.xlabel("교수")
plt.ylabel("수업 수")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
plt.show()
#최다 수업 교수님 끝!
#최다 수업하신 교수님의 애용 강의실만 추출
# TOP 10 강의실 (익명 기준)
top_rooms = df['익명_강의실'].value_counts().head(10).index
top_profs = df['익명_교수'].value_counts().head(10).index
# 교수도 익명 top 10, 강의실도 top 10
df_top_both = df[df['익명_교수'].isin(top_profs) & df['익명_강의실'].isin(top_rooms)]
prof_room_table = df_top_both.groupby(['익명_교수', '익명_강의실']).size().unstack(fill_value=0)

plt.figure(figsize=(12, 6))
sns.heatmap(prof_room_table, annot=True, cmap="Blues", linewidths=0.5, fmt="d")
plt.title("TOP 교수 × TOP 강의실 히트맵")
plt.xlabel("강의실")
plt.ylabel("교수")
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()
