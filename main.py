import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="Global MBTI Explorer", layout="wide")

# 데이터 로드 함수
@st.cache_data
def load_data():
    df = pd.read_csv('countriesMBTI_16types.csv')
    return df

df = load_data()

# 사이드바: 국가 선택
st.sidebar.header("설정")
all_countries = df['Country'].unique()
selected_country = st.sidebar.selectbox("국가를 선택하세요", all_countries)

# 메인 화면 구성
st.title("🌍 국가별 MBTI 분포 시각화")
st.markdown(f"**{selected_country}**의 MBTI 성격 유형 분포를 확인해보세요.")

# 데이터 가공 (선택된 국가의 MBTI 데이터 추출)
country_data = df[df['Country'] == selected_country].drop(columns=['Country']).T
country_data.columns = ['Percentage']
country_data = country_data.sort_values(by='Percentage', ascending=False)

# 1. 단일 국가 분석 차트
col1, col2 = st.columns([2, 1])

with col1:
    fig = px.bar(country_data, 
                 x=country_data.index, 
                 y='Percentage',
                 labels={'index': 'MBTI 유형', 'Percentage': '비율'},
                 color='Percentage',
                 color_continuous_scale='Viridis',
                 title=f"{selected_country} MBTI 분포")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("유형별 순위")
    st.write(country_data.style.format("{:.2%}"))

---

# 2. 국가 간 비교 섹션
st.divider()
st.header("🆚 국가 간 비교")

compare_countries = st.multiselect("비교할 국가들을 선택하세요", all_countries, default=[all_countries[0], all_countries[1]])

if compare_countries:
    compare_df = df[df['Country'].isin(compare_countries)].set_index('Country').T
    
    fig_compare = px.line(compare_df, 
                         labels={'index': 'MBTI 유형', 'value': '비율'},
                         title="국가별 MBTI 패턴 비교",
                         markers=True)
    st.plotly_chart(fig_compare, use_container_width=True)

# 3. MBTI 유형별 랭킹
st.divider()
st.header("🏆 MBTI 유형별 TOP 국가")
selected_mbti = st.selectbox("확인하고 싶은 MBTI 유형을 선택하세요", df.columns[1:])

top_countries = df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=False).head(10)

fig_top = px.bar(top_countries, x='Country', y=selected_mbti, 
                 title=f"{selected_mbti} 비율이 가장 높은 국가 TOP 10",
                 color=selected_mbti)
st.plotly_chart(fig_top, use_container_width=True)
