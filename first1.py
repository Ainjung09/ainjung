import streamlit as st
import pandas as pd

st.title("2025년 5월 기준 연령별 인구 현황 분석")

# 데이터 로드
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding="EUC-KR")

# 모든 컬럼 이름 양쪽 공백 제거
df.columns = df.columns.str.strip()

# 연령 관련 컬럼 필터링
age_columns = [col for col in df.columns if col.startswith("2025년05월_계_") and "세" in col]

# 연령 컬럼 이름을 숫자로 변환
age_mapping = {col: col.replace("2025년05월_계_", "").replace("세", "") for col in age_columns}
df_renamed = df.rename(columns=age_mapping)

# '행정구역' 컬럼 전처리
df_renamed["행정구역"] = df_renamed["행정구역"].str.extract(r"([\uAC00-\uD7A3\s]+)")

# 전처리한 연령 컬럼 리스트
age_only_columns = list(age_mapping.values())

# 총인구수 컬럼 이름을 다시 확인
total_col_name = "총인구수"
if total_col_name not in df_renamed.columns:
    # 유사한 이름을 출력해 도움 주기
    st.error(f"'총인구수' 컬럼이 없습니다. 다음 중 하나일 수 있습니다:\n{[col for col in df_renamed.columns if '총인구수' in col]}")
    st.stop()

# 숫자형으로 변환
convert_cols = age_only_columns + [total_col_name]
df_renamed[convert_cols] = df_renamed[convert_cols].apply(pd.to_numeric, errors="coerce")

# 총인구수 기준 상위 5개 지역
top5 = df_renamed.nlargest(5, total_col_name)

# 연령별 데이터 시각화를 위한 전처리
line_data = top5.set_index("행정구역")[age_only_columns].T
line_data.index.name = "연령"
line_data.index = line_data.index.astype(int)
line_data = line_data.sort_index()

# 시각화
st.subheader("상위 5개 지역의 연령별 인구 선 그래프")
st.line_chart(line_data)

# 원본 데이터 표시
st.subheader("원본 데이터 (일부 열 생략)")
st.dataframe(df_renamed[["행정구역", total_col_name] + age_only_columns])
