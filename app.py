import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os
import traceback

# 페이지 설정
st.set_page_config(page_title="Last Banana - 디지털 성범죄 분석", layout="wide")

# 한글 폰트 설정
font_url = "https://github.com/naver/nanumfont/blob/master/ttf/NanumGothic.ttf?raw=true"
font_path = "./NanumGothic.ttf"

if not os.path.exists(font_path):
    import urllib.request
    urllib.request.urlretrieve(font_url, font_path)

fontprop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = fontprop.get_name()
plt.rcParams['axes.unicode_minus'] = False

try:
    st.title("📊 Last Banana")
    st.markdown("### AI 발전과 디지털성범죄의 연관성")
    st.markdown("---")

    analysis_options = [
        "1. 지역별 피해 현황",
        "2. 피의자 연령 분석",
        "3. 피해자 성별 및 연령",
        "4. 사건 처리 기간 분석",
        "5. 피해자 지원 현황"
    ]
    selected_analysis = st.selectbox("🗂️ 분석 주제를 선택하세요:", analysis_options)

    @st.cache_data
    def load_data():
        data1 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(지역별 발생현황)_20231231.csv", encoding='cp949')
        data2 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(피의자 연령)_20231231.csv", encoding='cp949')
        data3 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(피해자의 특성_성별나이)_20231231.csv", encoding='cp949')
        data4 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(사건 처리 기간)_20231231.csv", encoding='cp949')
        data5 = pd.read_csv("한국여성인권진흥원_디지털성범죄피해자지원센터 연령대별 세부 피해 유형 현황_20231231.csv", encoding='cp949')
        return data1, data2, data3, data4, data5

    data1, data2, data3, data4, data5 = load_data()

    # 유틸 함수: 연도 컬럼 추출
    def get_year_columns(df):
        return [col for col in df.columns if str(col).isdigit() and len(str(col)) == 4]

    # 분석별 처리
    if selected_analysis == "1. 지역별 피해 현황":
        st.subheader("📍 지역별 피해 발생 건수")
        st.dataframe(data1)
        years = get_year_columns(data1)
        year = st.selectbox("연도를 선택하세요", years)

        if year in data1.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            sorted_df = data1.sort_values(by=year, ascending=True)
            sns.barplot(x=year, y='구분', data=sorted_df, palette='Reds_r', ax=ax)
            ax.set_xlabel("발생 건수")
            ax.set_ylabel("지역")
            st.pyplot(fig)

    elif selected_analysis == "2. 피의자 연령 분석":
        st.subheader("🧑‍⚖️ 피의자 연령 분포")
        st.dataframe(data2)
        years = get_year_columns(data2)
        year = st.selectbox("연도를 선택하세요", years)

        if year in data2.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            plot_df = data2[['구분', year]].dropna()
            plot_df = plot_df.rename(columns={year: '건수'})
            sns.barplot(data=plot_df, x='건수', y='구분', palette='coolwarm', ax=ax)
            ax.set_title(f"{year}년 피의자 연령 분포")
            st.pyplot(fig)

    elif selected_analysis == "3. 피해자 성별 및 연령":
        st.subheader("🚻 피해자 성별 및 연령")
        st.dataframe(data3)
        years = get_year_columns(data3)
        year = st.selectbox("연도를 선택하세요", years)

        if year in data3.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            plot_df = data3[['구분', year]].dropna().rename(columns={year: '건수'})
            sns.barplot(data=plot_df, x='건수', y='구분', palette='pastel', ax=ax)
            ax.set_title(f"{year}년 피해자 성별 및 연령")
            st.pyplot(fig)

    elif selected_analysis == "4. 사건 처리 기간 분석":
        st.subheader("📂 사건 처리 기간 분석")
        st.dataframe(data4)
        years = get_year_columns(data4)
        year = st.selectbox("연도를 선택하세요", years)

        if year in data4.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            plot_df = data4[['구분', year]].dropna().rename(columns={year: '건수'})
            sns.barplot(data=plot_df, x='건수', y='구분', palette='Purples', ax=ax)
            ax.set_title(f"{year}년 사건 처리 기간")
            st.pyplot(fig)

    elif selected_analysis == "5. 피해자 지원 현황":
        st.subheader("📑 피해자 지원 현황")
        st.dataframe(data5)
        if '연령대' in data5.columns and '피해건수' in data5.columns:
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(data=data5, x='피해건수', y='연령대', palette='YlGnBu', ax=ax)
            ax.set_title('연령대별 피해 유형 건수')
            st.pyplot(fig)

except Exception:
    st.error("앱 실행 중 오류가 발생했습니다!")
    st.text(traceback.format_exc())
