import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import traceback

# 한글 폰트 설정 (Windows 환경 기준)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 페이지 기본 설정
st.set_page_config(page_title="Last Banana - 디지털 성범죄 분석", layout="wide")

try:
    st.title("📊 Last Banana")
    st.markdown("### AI 발전과 디지털성범죄의 연관성")
    st.markdown("---")

    # 분석 주제 선택
    analysis_options = [
        "1. 지역별 피해 현황",
        "2. 피의자 연령 분석",
        "3. 피해자 성별 및 연령",
        "4. 사건 처리 기간 분석",
        "5. 피해자 지원 현황"
    ]
    selected_analysis = st.selectbox("🗂️ 분석 주제를 선택하세요:", analysis_options)

    # 데이터 로딩 함수
    @st.cache_data
    def load_data():
        data1 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(지역별 발생현황)_20231231.csv", encoding='cp949')
        data2 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(피의자 연령)_20231231.csv", encoding='cp949')
        data3 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(피해자의 특성_성별나이)_20231231.csv", encoding='cp949')
        data4 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(사건 처리 기간)_20231231.csv", encoding='cp949')
        data5 = pd.read_csv("한국여성인권진흥원_디지털성범죄피해자지원센터 연령대별 세부 피해 유형 현황_20231231.csv", encoding='cp949')
        return data1, data2, data3, data4, data5

    지역별_피해, 피의자_연령, 피해자_성별연령, 사건처리기간, 피해자_지원 = load_data()

    # 분석 1: 지역별 피해 현황
    if selected_analysis == "1. 지역별 피해 현황":
        st.subheader("📍 지역별 피해 발생 건수")
        year_options = [col for col in 지역별_피해.columns if str(col).isdigit()]
        selected_year = st.selectbox("연도 선택", year_options)
        data = 지역별_피해[['구분', selected_year]].rename(columns={'구분': '지역', selected_year: '발생건수'})

        fig, ax = plt.subplots(figsize=(10, 6))
        data = data.sort_values('발생건수', ascending=True)
        sns.barplot(x='발생건수', y='지역', data=data, palette='Reds_r', ax=ax)
        ax.set_xlabel("발생 건수")
        ax.set_ylabel("지역")
        st.pyplot(fig, use_container_width=True)

    # 분석 2: 피의자 연령 분석
    elif selected_analysis == "2. 피의자 연령 분석":
        st.subheader("🧑‍⚖️ 피의자 연령 분포")
        year_options = [col for col in 피의자_연령.columns if str(col).isdigit()]
        selected_year = st.selectbox("연도 선택", year_options)
        data = 피의자_연령[['구분', selected_year]].rename(columns={'구분': '연령대', selected_year: '건수'})
        data = data[data['건수'].notna()]

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='건수', y='연령대', data=data.sort_values('건수', ascending=False), palette='coolwarm', ax=ax)
        ax.set_xlabel("건수")
        ax.set_ylabel("연령대")
        st.pyplot(fig, use_container_width=True)

    # 분석 3: 피해자 성별 및 연령
    elif selected_analysis == "3. 피해자 성별 및 연령":
        st.subheader("🚻 피해자 성별 및 연령 분석")
        if '성별' in 피해자_성별연령.columns and '연령대' in 피해자_성별연령.columns:
            df = 피해자_성별연령.copy()
            total_by_age = df.groupby('연령대').size()
            counts = df.groupby(['연령대', '성별']).size().unstack().fillna(0)
            percent_df = counts.divide(total_by_age, axis=0)

            fig, ax = plt.subplots(figsize=(10, 6))
            percent_df.plot(kind='bar', stacked=True, ax=ax, colormap='pastel')
            ax.set_ylabel('비율')
            ax.set_xlabel('연령대')
            st.pyplot(fig, use_container_width=True)
        else:
            st.warning("성별과 연령대 정보가 누락되었습니다.")

    # 분석 4: 사건 처리 기간 분석
    elif selected_analysis == "4. 사건 처리 기간 분석":
        st.subheader("📂 사건 처리 소요 기간 분석")
        if '처리기간' in 사건처리기간.columns:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [4, 1]})
            sns.histplot(사건처리기간['처리기간'], bins=20, kde=True, color='purple', ax=ax1)
            ax1.set_title("사건 처리 기간 분포")
            sns.boxplot(x=사건처리기간['처리기간'], color='purple', ax=ax2)
            st.pyplot(fig, use_container_width=True)
        else:
            st.warning("처리기간 컬럼이 없습니다.")

    # 분석 5: 피해자 지원 현황
    elif selected_analysis == "5. 피해자 지원 현황":
        st.subheader("📑 피해자 지원 현황 분석")
        if '연령대' in 피해자_지원.columns and '피해유형' in 피해자_지원.columns:
            pivot = 피해자_지원.pivot_table(index='연령대', columns='피해유형', values='피해건수', aggfunc='sum').fillna(0)
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.heatmap(pivot, annot=True, fmt='g', cmap='YlGnBu', ax=ax)
            ax.set_title('연령대별 피해 유형 현황')
            st.pyplot(fig, use_container_width=True)
        else:
            st.warning("피해유형 및 연령대 컬럼이 없습니다.")

except Exception:
    st.error("앱 실행 중 오류가 발생했습니다!")
    st.text(traceback.format_exc())
