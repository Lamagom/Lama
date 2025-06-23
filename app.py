import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 기본 설정 ---
st.set_page_config(page_title="Last Banana - 디지털 성범죄 분석", layout="wide")
st.title("📊 Last Banana")
st.markdown("### AI 발전과 디지털성범죄의 연관성")
st.markdown("---")

# --- 분석 주제 선택 ---
analysis_options = [
    "1. 지역별 피해 현황",
    "2. 피의자 연령 분석",
    "3. 피해자 성별 및 연령",
    "4. 사건 처리 기간 분석",
    "5. 피해자 지원 현황"
]
selected_analysis = st.selectbox("🗂️ 분석 주제를 선택하세요:", analysis_options)

# --- 데이터 로딩 함수 ---
def load_data():
    data1 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(지역별 발생현황)_20231231.csv", encoding='cp949')
    data2 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(피의자 연령)_20231231.csv", encoding='cp949')
    data3 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(피해자의 특성_성별나이)_20231231.csv", encoding='cp949')
    data4 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(사건 처리 기간)_20231231.csv", encoding='cp949')
    data5 = pd.read_csv("한국여성인권진흥원_디지털성범죄피해자지원센터 연령대별 세부 피해 유형 현황_20231231.csv", encoding='cp949')
    return data1, data2, data3, data4, data5

지역별_피해, 피의자_연령, 피해자_성별연령, 사건처리기간, 피해자_지원 = load_data()

# --- 분석 1: 지역별 피해 현황 (선 그래프) ---
if selected_analysis == "1. 지역별 피해 현황":
    st.subheader("📍 지역별 피해 발생 건수")
    st.write(지역별_피해)

    if '지역' in 지역별_피해.columns and '발생건수' in 지역별_피해.columns:
        sorted_df = 지역별_피해.sort_values('발생건수', ascending=True)
        
        fig, ax = plt.subplots(figsize=(12, 7))
        ax.plot(sorted_df['발생건수'], sorted_df['지역'], marker='o', linestyle='-', color='crimson', linewidth=2)
        ax.set_xlabel("발생 건수", fontsize=12)
        ax.set_ylabel("지역", fontsize=12)
        ax.invert_yaxis()  # 위에서 아래로 정렬
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig)

# --- 분석 2: 피의자 연령 분석 (영역 그래프) ---
elif selected_analysis == "2. 피의자 연령 분석":
    st.subheader("🧑‍⚖️ 피의자 연령 분포")
    st.write(피의자_연령)

    if '연령대' in 피의자_연령.columns and '건수' in 피의자_연령.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.fill_between(피의자_연령['연령대'], 피의자_연령['건수'], color='mediumblue', alpha=0.3)
        ax.plot(피의자_연령['연령대'], 피의자_연령['건수'], marker='o', color='mediumblue', linewidth=2)
        ax.set_xlabel('연령대', fontsize=12)
        ax.set_ylabel('건수', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        st.pyplot(fig)

# --- 분석 3: 피해자 성별 및 연령 (누적 선 그래프) ---
elif selected_analysis == "3. 피해자 성별 및 연령":
    st.subheader("🚻 피해자 성별 및 연령 분석")
    st.write(피해자_성별연령)

    if '성별' in 피해자_성별연령.columns and '연령대' in 피해자_성별연령.columns:
        df = 피해자_성별연령.copy()
        counts = df.groupby(['연령대', '성별']).size().unstack().fillna(0)
        counts_norm = counts.divide(counts.sum(axis=1), axis=0)  # 비율
        
        fig, ax = plt.subplots(figsize=(12, 7))
        counts_norm.plot(kind='line', marker='o', linewidth=3, ax=ax)
        ax.set_ylabel('비율', fontsize=12)
        ax.set_xlabel('연령대', fontsize=12)
        ax.set_title("연령대별 피해자 성별 비율", fontsize=14)
        ax.grid(True, linestyle='--', alpha=0.6)
        plt.legend(title='성별', fontsize=11)
        plt.tight_layout()
        st.pyplot(fig)

# --- 분석 4: 사건 처리 기간 분석 (누적 히스토그램) ---
elif selected_analysis == "4. 사건 처리 기간 분석":
    st.subheader("📂 사건 처리 소요 기간 분석")
    st.write(사건처리기간)

    if '처리기간' in 사건처리기간.columns:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.hist(사건처리기간['처리기간'], bins=20, cumulative=True, color='purple', alpha=0.7)
        ax.set_xlabel('처리 기간 (일)', fontsize=12)
        ax.set_ylabel('누적 건수', fontsize=12)
        ax.set_title('사건 처리 기간 누적 분포', fontsize=14)
        ax.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        st.pyplot(fig)

# --- 분석 5: 피해자 지원 현황 (다중 선 그래프) ---
elif selected_analysis == "5. 피해자 지원 현황":
    st.subheader("📑 피해자 지원 현황 분석")
    st.write(피해자_지원)

    if '연령대' in 피해자_지원.columns and '피해유형' in 피해자_지원.columns:
        pivot = 피해자_지원.pivot_table(index='연령대', columns='피해유형', values='건수', aggfunc='sum').fillna(0)
        
        fig, ax = plt.subplots(figsize=(14, 7))
        pivot.plot(ax=ax, marker='o', linewidth=2)
        ax.set_ylabel('건수', fontsize=12)
        ax.set_title('연령대별 피해 유형 현황', fontsize=14)
        ax.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        st.pyplot(fig)
