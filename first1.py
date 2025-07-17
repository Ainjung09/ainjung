import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="상위 5개 행정구역 인구 지도", page_icon="🗺️", layout="wide")
st.title("🗺️ 상위 5개 행정구역 인구수 지도 시각화")

# 데이터 불러오기
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

# 행정구역 이름 정리 (괄호 안 숫자 제거)
df['행정구역'] = df['행정구역'].str.replace(r"\s*\(\d+\)", "", regex=True).str.strip()

# 총인구수 숫자형 변환
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

# 연령별 컬럼 정리
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace('2025년05월_계_', '').replace('세', '') + '세')

df_age = df[['행정구역', '총인구수'] + age_columns].copy()
df_age.columns = ['행정구역', '총인구수'] + new_columns

# 총인구수 기준 상위 5개 추출
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5)

# 좌표 수동 매핑 (행정구역 정확히 맞춰야 함)
region_coords = {
    "경기도 수원시": [37.2636, 127.0286],
    "서울특별시 송파구": [37.5145, 127.1056],
    "부산광역시 해운대구": [35.1632, 129.1636],
    "경상남도 창원시": [35.2285, 128.6811],
    "인천광역시 연수구": [37.4089, 126.6788],
}

# 지도 생성
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# folium 원 추가 (pink, 반투명)
for _, row in top5_df.iterrows():
    region = row['행정구역']
    pop = row['총인구수']
    coords = region_coords.get(region)
    if coords:
        folium.Circle(
            location=coords,
            radius=pop / 30,  # 인구수 크기 조절
            color='deeppink',
            fill=True,
            fill_color='pink',
            fill_opacity=0.5,
            popup=f"{region} : {pop:,}명",
            tooltip=region
        ).add_to(m)
    else:
        st.warning(f"위치 정보가 없는 지역입니다: {region}")

# 지도 출력
st.subheader("🗺️ 지도에서 상위 5개 행정구역 인구수 확인")
st_folium(m, width=900, height=600)

# 원본 데이터 표시
st.subheader("📊 원본 데이터 (상위 5개 행정구역)")
st.dataframe(top5_df)

           
