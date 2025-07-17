import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("2025년 5월 기준 연령별 인구 현황 분석")

# CSV 파일 경로
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding="EUC-KR")

# 컬럼 정리
df.columns = df.columns.str.strip()
age_columns = [col for col in df.columns if col.startswith("2025년05월_계_") and "세" in col]
age_mapping = {col: col.replace("2025년05월_계_", "").replace("세", "") for col in age_columns}
df_renamed = df.rename(columns=age_mapping)
df_renamed["행정구역"] = df_renamed["행정구역"].str.extract(r"([\uAC00-\uD7A3\s]+)")

age_only_columns = list(age_mapping.values())
total_col_name = "총인구수"

# 총인구수 컬럼 확인
if total_col_name not in df_renamed.columns:
    st.error(f"'총인구수' 컬럼이 없습니다.")
    st.stop()

# 숫자 변환
df_renamed[age_only_columns + [total_col_name]] = df_renamed[age_only_columns + [total_col_name]].apply(pd.to_numeric, errors="coerce")

# 상위 5개 지역
top5 = df_renamed.nlargest(5, total_col_name)

# 📍 지도에 표시할 위도/경도 수동 설정 (예시용, 정확한 행정구역 이름에 맞게 조정 가능)
# 실제 서비스 시에는 Geocoding API 사용 추천
location_map = {
    "서울특별시 강남구": [37.5172, 127.0473],
    "경기도 수원시": [37.2636, 127.0286],
    "부산광역시 해운대구": [35.1632, 129.1636],
    "대구광역시 수성구": [35.8562, 128.6304],
    "인천광역시 연수구": [37.4089, 126.6788],
    # 필요 시 다른 지역도 수동으로 추가
}

# 지도 생성
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

for _, row in top5.iterrows():
    region = row["행정구역"]
    pop = row[total_col_name]
    if region in location_map:
        lat, lon = location_map[region]
        folium.Marker(
            location=[lat, lon],
            popup=f"{region} - 총인구수: {int(pop):,}명",
            tooltip=region,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

# Streamlit에 지도 표시
st.subheader("상위 5개 지역 인구 지도 시각화")
st_folium(m, width=700, height=500)

# 선 그래프 (연령별 인구)
st.subheader("상위 5개 지역의 연령별 인구 선 그래프")
line_data = top5.set_index("행정구역")[age_only_columns].T
line_data.index.name = "연령"
line_data.index = line_data.index.astype(int)
line_data = line_data.sort_index()
st.line_chart(line_data)

# 원본 데이터
st.subheader("원본 데이터 (일부 열 생략)")
st.dataframe(df_renamed[["행정구역", total_col_name] + age_only_columns])

for _, row in top5_df.iterrows():
    region = row['행정구역']
    pop = row['총인구수']
    coords = region_coords.get(region)
    if coords:
        folium.Circle(
            location=coords,
            radius=pop / 300,  # 적절한 크기로 조정
            color='Deeppink',
            fill=True,
            fill_color='Lightpink',
            fill_opacity=0.6,
            popup=f"{region} : {pop:,}명",
            tooltip=region
        ).add_to(m)

# 지도 출력
st.subheader("🗺️ 지도에서 상위 5개 행정구역 인구수 확인")
st_folium(m, width=900, height=600)

# 원본 데이터 출력
st.subheader("📊 원본 데이터 (상위 5개 행정구역)")
st.dataframe(top5_df)
