import streamlit as st
import pandas as pd

# 페이지 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드해주세요", type=["csv"])

if uploaded_file is not None:
    # CSV 파일 읽기 (EUC-KR 인코딩)
    df = pd.read_csv(uploaded_file, encoding='euc-kr')

    # 원본 데이터 표시
    st.subheader("원본 데이터")
    st.dataframe(df)

    # 전처리
    df = df.copy()
    # '행정구역' 컬럼에서 지역명만 추출 (예: '서울특별시 종로구 (11110)' → '서울특별시 종로구')
    df['행정구역'] = df['행정구역'].str.extract(r'([\uAC00-\uD7A3\s]+)')

    # 연령별 컬럼 추출 (예: '2025년05월_계_0세', ..., '2025년05월_계_100세 이상')
    age_columns = [col for col in df.columns if '2025년05월_계_' in col and '세' in col]

    # '총인구수' 컬럼은 따로 유지
    df_total = df[['행정구역', '총인구수'] + age_columns].copy()

    # 총인구수 기준 상위 5개 행정구역 추출
    top5_df = df_total.sort_values(by='총인구수', ascending=False).head(5)

    # 연령별 데이터 정리 (컬럼명을 숫자 연령으로 변경)
    rename_dict = {col: col.replace('2025년05월_계_', '').replace('세', '') for col in age_columns}
    top5_df = top5_df.rename(columns=rename_dict)

    # 데이터 재구성: 연령을 행으로, 각 행정구역을 열로
    line_chart_df = top5_df.set_index('행정구역').drop(columns='총인구수').T
    line_chart_df.index.name = '연령'
    line_chart_df = line_chart_df.reset_index()
    line_chart_df['연령'] = line_chart_df['연령'].str.replace(' 이상', '')  # '100세 이상' 처리
    line_chart_df['연령'] = line_chart_df['연령'].astype(str)

    # 시각화
    st.subheader("상위 5개 행정구역 연령별 인구 추이")
    st.line_chart(line_chart_df.set_index('연령'))

    # 분석한 데이터도 함께 제공
    st.subheader("상위 5개 행정구역 연령별 인구 데이터")
    st.dataframe(line_chart_df)
else:
    st.info("먼저 CSV 파일을 업로드해주세요.")

