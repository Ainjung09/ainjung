import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# 데이터 로드
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding="EUC-KR")

# 컬럼명 정리
df.columns = df.columns.str.strip()

# '2025년05월_계_연령' 형태의 열만 추출 및 숫자 연령으로 변환
age_columns = [col for col in df.columns if col.startswith("2025년05월_계_") and "세" in col]
age_mapping = {col: col.replace("2025년05월_계_", "").replace("세", "") for col in age_columns}
df_renamed = df.rename(columns=age_mapping)

# '행정구역' 컬럼을 분리 (예: '서울특별시 강남구(11680)' → '서울특별시 강남구')
df_renamed["행정구역"] = df_renamed["행정구역"].str.extract(r"([\uAC00-\uD7A3\s]+)")

# 숫자로 변환 가능한 컬럼만 필터링
age_only_columns = list(age_mapping.values())
df_renamed[age_only_columns + ["총인구수"]] = df_renamed[age_only_columns + ["총인구수"]].apply(pd.to_numeric, errors="coerce")

# 총인구수 상위 5개 행정구역 선택
top5 = df_renamed.nlargest(5, "총인구수")

# 연령별 인구 그래프 그리기
st.subheader("상위 5개 지역의 연령별 인구 선 그래프")
line_data = top5.set_index("행정구역")[age_only_columns].T
line_data.index.name = "연령"
line_data.index = line_data.index.astype(int)
line_data = line_data.sort_index()

st.line_chart(line_data)

# 원본 데이터 표시
st.subheader("원본 데이터 (일부 열 생략)")
st.dataframe(df_renamed[["행정구역", "총인구수"] + age_only_columns])
