import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import traceback

# 📌 Streamlit 페이지 설정
st.set_page_config(page_title="Last Banana - 디지털 성범죄 분석", layout="wide")

# ✅ 스타일 설정
sns.set_theme(style="whitegrid")
plt.rcParams['axes.unicode_minus'] = False

# ✅ 데이터 로딩 함수
@st.cache_data
def load_data():
    data1 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(지역별 발생현황)_20231231.csv", encoding='cp949')
    data2 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(피의자 연령)_20231231.csv", encoding='cp949')
    data3 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(피해자의 특성_성별나이)_20231231.csv", encoding='cp949')
    data4 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(사건 처리 기간)_20231231.csv", encoding='cp949')
    data5 = pd.read_csv("한국여성인권진흥원_디지털성범죄피해자지원센터 연령대별 세부 피해 유형 현황_20231231.csv", encoding='cp949')
    return data1, data2, data3, data4, data5

# ✅ 연도 컬럼 자동 추출
def get_year_columns(df):
    return [col for col in df.columns if str(col).isdigit() and len(str(col)) == 4]

# ✅ 메인 실행 블록
try:
    st.title("📊 Last Banana")
    st.markdown("### AI 발전과 디지털성범죄의 연관성")
    st.markdown("---")

    분석_항목 = [
        "1. 지역별 피해 현황",
        "2. 피의자 연령 분석",
        "3. 피해자 성별 및 연령",
        "4. 사건 처리 기간 분석",
        "5. 피해자 지원 현황"
    ]
    선택 = st.selectbox("🔍 분석 항목을 선택하세요:", 분석_항목)

    지역별_피해, 피의자_연령, 피해자_성별연령, 사건처리기간, 피해자_지원 = load_data()

    # 1. 지역별 피해
    if 선택 == "1. 지역별 피해 현황":
        st.subheader("📍 지역별 피해 현황")
        연도들 = get_year_columns(지역별_피해)
        선택연도 = st.selectbox("연도를 선택하세요", 연도들)
        st.dataframe(지역별_피해[['구분', 선택연도]])

        fig, ax = plt.subplots(figsize=(10, 6))
        sorted_df = 지역별_피해[['구분', 선택연도]].sort_values(by=선택연도, ascending=True)
        sns.barplot(data=sorted_df, x=선택연도, y='구분', palette='Reds_r', ax=ax)
        ax.set_title(f"{선택연도}년 지역별 피해 건수")
        st.pyplot(fig, use_container_width=True)

    # 2. 피의자 연령 분석
    elif 선택 == "2. 피의자 연령 분석":
        st.subheader("🧑‍⚖️ 피의자 연령 분포")
        연도들 = get_year_columns(피의자_연령)
        선택연도 = st.selectbox("연도를 선택하세요", 연도들)
        st.dataframe(피의자_연령[['구분', 선택연도]])

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=피의자_연령, x='구분', y=선택연도, palette="Blues_d", ax=ax)
        ax.set_ylabel("건수")
        ax.set_xlabel("연령대")
        plt.xticks(rotation=45)
        st.pyplot(fig, use_container_width=True)

    # 3. 피해자 성별 및 연령
    elif 선택 == "3. 피해자 성별 및 연령":
        st.subheader("🚻 피해자 성별 및 연령")
        st.dataframe(피해자_성별연령)

        if '성별' in 피해자_성별연령.columns:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.countplot(data=피해자_성별연령, x='성별', palette='Set2', ax=ax)
            ax.set_title("피해자 성별 분포")
            st.pyplot(fig, use_container_width=True)

    # 4. 사건 처리 기간 분석
    elif 선택 == "4. 사건 처리 기간 분석":
        st.subheader("⏳ 사건 처리 기간")
        st.dataframe(사건처리기간)

        if '처리기간' in 사건처리기간.columns:
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.histplot(사건처리기간['처리기간'], bins=20, kde=True, color='purple', ax=ax)
            ax.set_title("사건 처리 기간 분포")
            st.pyplot(fig, use_container_width=True)

    # 5. 피해자 지원 현황
    elif 선택 == "5. 피해자 지원 현황":
        st.subheader("📑 피해자 지원 현황")
        st.dataframe(피해자_지원)

        if {'연령대', '피해유형', '건수'}.issubset(피해자_지원.columns):
            pivot = 피해자_지원.pivot_table(index='연령대', columns='피해유형', values='건수', aggfunc='sum').fillna(0)
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.heatmap(pivot, annot=True, fmt='g', cmap='YlGnBu', ax=ax)
            ax.set_title("연령대별 피해 유형 분포")
            st.pyplot(fig, use_container_width=True)

except Exception:
    st.error("❌ 앱 실행 중 오류가 발생했습니다!")
    st.text(traceback.format_exc())
