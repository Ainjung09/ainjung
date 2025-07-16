import streamlit as st
import pandas as pd

# 앱 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# CSV 파일 경로 (업로드된 파일 경로 사용)
file_path = "/mnt/data/202505_202505_연령별인구현황_월간.csv"

# CSV 파일 읽기 (EUC-KR 인코딩)
df = pd.read_csv(file_path, encoding="euc-kr")

# '2025년05월_계_'로 시작하는 컬럼만 추출 + '총인구수' 유지
age_prefix = "2025년05월_계_"
total_col = "총인구수"

age_cols = [col for col in df.columns if col.startswith(age_prefix)]
rename_dict = {col: col.replace(age_prefix, "") for col in age_cols}

# 필요한 열만 선택하고 열 이름 전처리
df = df[["행정구역", total_col] + age_cols].rename(columns=rename_dict)

# 총인구수 기준 상위 5개 행정구역 추출
top5_df = df.sort_values(by=total_col, ascending=False).head(5)

# 연령별 인구 데이터 변형: 연령을 세로축으로, 각 행정구역을 열로
plot_df = top5_df.set_index("행정구역").loc[:, rename_dict.values()].T
plot_df.index.name = "연령"

# 선 그래프 출력
st.subheader("상위 5개 행정구역의 연령별 인구 선 그래프")
st.line_chart(plot_df)

# 원본 데이터 표출
st.subheader("원본 데이터 (상위 5개 행정구역)")
st.dataframe(top5_df)
