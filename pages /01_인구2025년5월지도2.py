import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Streamlit 제목
st.title("📍 2025년 5월 기준 연령별 인구 현황 - 지도 시각화")

# CSV 파일 읽기
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

# 총인구수 전처리
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

# 연령별 컬럼 처리
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace('2025년05월_계_', '').replace('세', '') + '세')

df_age = df[['행정구역', '총인구수'] + age_columns].copy()
df_age.columns = ['행정구역', '총인구수'] + new_columns

# 상위 5개 지역 추출
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5).reset_index(drop=True)

# 지역 이름을 위도/경도로 매핑 (간단한 예시)
# 정확한 좌표는 공식 행정지도 또는 외부 소스를 통해 확보 가능
location_map = {
    '서울특별시': (37.5665, 126.9780),
    '부산광역시': (35.1796, 129.0756),
    '경기도': (37.2752, 127.0095),
    '인천광역시': (37.4563, 126.7052),
    '대구광역시': (35.8722, 128.6025),
    '대전광역시': (36.3504, 127.3845),
    '광주광역시': (35.1595, 126.8526),
    '울산광역시': (35.5384, 129.3114),
    '세종특별자치시': (36.4801, 127.2890),
    '강원도': (37.8228, 128.1555),
    '충청북도': (36.6357, 127.4917),
    '충청남도': (36.5184, 126.8000),
    '전라북도': (35.7175, 127.1530),
    '전라남도': (34.8161, 126.4629),
    '경상북도': (36.4919, 128.8889),
    '경상남도': (35.4606, 128.2132),
    '제주특별자치도': (33.4996, 126.5312)
}

# 지도 생성
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# 지도에 마커 추가
for _, row in top5_df.iterrows():
    region = row['행정구역']
    total_pop = row['총인구수']
    
    if region in location_map:
        lat, lon = location_map[region]
        folium.CircleMarker(
            location=(lat, lon),
            radius=total_pop / 100000,  # 반지름 인구수 비례 조정
            color='blue',
            fill=True,
            fill_opacity=0.4,
            popup=f"{region}<br>총인구수: {total_pop:,}명"
        ).add_to(m)

# 지도 출력
st.subheader("🗺️ 상위 5개 행정구역 인구 분포")
st_data = st_folium(m, width=700, height=500)

