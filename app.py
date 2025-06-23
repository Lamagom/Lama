import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import traceback

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

    # 데이터 로딩 함수 (캐시 적용)
    @st.cache_data
    def load_data():
        data1 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(지역별 발생현황)_20231231.csv", encoding='cp949')
        data2 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(피의자 연령)_20231231.csv", encoding='cp949')
        data3 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(피해자의 특성_성별나이)_20231231.csv", encoding='cp949')
        data4 = pd.read_csv("경찰청_통신매체이용음란_성폭력범죄(사건 처리 기간)_20231231.csv", encoding='cp949')
        data5 = pd.read_csv("한국여성인권진흥원_디지털성범죄피해자지원센터 연령대별 세부 피해 유형 현황_20231231.csv", encoding='cp949')
        return data1, data2, data3, data4, data5

    지역별_피해, 피의자_연령, 피해자_성별연령, 사건처리기간, 피해자_지원 = load_data()

    # --- 분석 1: 지역별 피해 현황 (연도별 컬럼이므로 melt 후 선택) ---
    if selected_analysis == "1. 지역별 피해 현황":
        st.subheader("📍 지역별 피해 발생 건수")

        # 연도별 컬럼 확인 (예시: 2014 ~ 2023년)
        years = [col for col in 지역별_피해.columns if col.isdigit()]
        if not years:
            st.warning("연도별 데이터 컬럼이 없습니다.")
        else:
            selected_year = st.selectbox("연도 선택", sorted(years))
            # melt 처리
            df_long = 지역별_피해.melt(id_vars=['구분'], value_vars=years,
                              var_name='연도', value_name='발생건수')
            # 선택된 연도로 필터링
            df_year = df_long[df_long['연도'] == selected_year]

            st.write(df_year)

            if not df_year.empty:
                fig, ax = plt.subplots(figsize=(10, 6))
                sorted_df = df_year.sort_values('발생건수', ascending=True)
                sns.barplot(x='발생건수', y='구분', data=sorted_df, palette='Reds_r', ax=ax)
                ax.set_xlabel("발생 건수")
                ax.set_ylabel("지역")
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)

    # --- 분석 2: 피의자 연령 분석 (마찬가지로 연도별 선택 가능하게) ---
    elif selected_analysis == "2. 피의자 연령 분석":
        st.subheader("🧑‍⚖️ 피의자 연령 분포")

        # 연도별 컬럼 확인
        years = [col for col in 피의자_연령.columns if col.isdigit()]
        if not years:
            st.warning("연도별 데이터 컬럼이 없습니다.")
        else:
            selected_year = st.selectbox("연도 선택", sorted(years))
            # melt 처리
            df_long = 피의자_연령.melt(id_vars=['구분'], value_vars=years,
                                 var_name='연도', value_name='건수')
            df_year = df_long[df_long['연도'] == selected_year]

            st.write(df_year)

            if not df_year.empty:
                fig, ax = plt.subplots(figsize=(8, 5))
                sns.barplot(x='구분', y='건수', data=df_year, palette='coolwarm', ax=ax)
                ax.set_xlabel('연령대')
                ax.set_ylabel('건수')
                ax.set_title(f"{selected_year}년 피의자 연령 분포")
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)

    # --- 분석 3: 피해자 성별 및 연령 ---
    elif selected_analysis == "3. 피해자 성별 및 연령":
        st.subheader("🚻 피해자 성별 및 연령 분석")

        # 이 데이터는 연도별 컬럼과 성별, 연령대가 같이 있을 가능성 있음
        # 연도별 컬럼 추출
        years = [col for col in 피해자_성별연령.columns if col.isdigit()]
        if not years:
            st.warning("연도별 데이터 컬럼이 없습니다.")
        else:
            selected_year = st.selectbox("연도 선택", sorted(years))
            # melt 처리
            df_long = 피해자_성별연령.melt(id_vars=['구분', '성별'], value_vars=years,
                                var_name='연도', value_name='건수')
            df_year = df_long[df_long['연도'] == selected_year]

            st.write(df_year)

            if not df_year.empty:
                pivot = df_year.pivot_table(index='구분', columns='성별', values='건수', aggfunc='sum').fillna(0)
                fig, ax = plt.subplots(figsize=(10, 6))
                pivot.plot(kind='bar', stacked=True, ax=ax, colormap='pastel')
                ax.set_ylabel('건수')
                ax.set_xlabel('연령대')
                ax.set_title(f"{selected_year}년 피해자 성별 및 연령")
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)

    # --- 분석 4: 사건 처리 기간 분석 ---
    elif selected_analysis == "4. 사건 처리 기간 분석":
        st.subheader("📂 사건 처리 소요 기간 분석")

        # 사건처리기간 데이터에 '구분'과 연도별 컬럼 존재하는 경우 melt 후 연도 선택
        years = [col for col in 사건처리기간.columns if col.isdigit()]
        if not years:
            st.warning("연도별 데이터 컬럼이 없습니다.")
        else:
            selected_year = st.selectbox("연도 선택", sorted(years))
            df_long = 사건처리기간.melt(id_vars=['구분'], value_vars=years,
                               var_name='연도', value_name='건수')
            df_year = df_long[df_long['연도'] == selected_year]

            st.write(df_year)

            if not df_year.empty:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.barplot(x='구분', y='건수', data=df_year, palette='Purples', ax=ax)
                ax.set_title(f"{selected_year}년 사건 처리 기간별 건수")
                ax.set_xlabel('처리 기간 구분')
                ax.set_ylabel('건수')
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)

    # --- 분석 5: 피해자 지원 현황 ---
    elif selected_analysis == "5. 피해자 지원 현황":
        st.subheader("📑 피해자 지원 현황 분석")

        years = [col for col in 피해자_지원.columns if col.isdigit()]
        if not years:
            st.warning("연도별 데이터 컬럼이 없습니다.")
        else:
            selected_year = st.selectbox("연도 선택", sorted(years))
            df_long = 피해자_지원.melt(id_vars=['연령대', '피해유형'], value_vars=years,
                            var_name='연도', value_name='건수')
            df_year = df_long[df_long['연도'] == selected_year]

            st.write(df_year)

            if not df_year.empty:
                pivot = df_year.pivot_table(index='연령대', columns='피해유형', values='건수', aggfunc='sum').fillna(0)
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.heatmap(pivot, annot=True, fmt='g', cmap='YlGnBu', ax=ax)
                ax.set_title(f"{selected_year}년 연령대별 피해 유형 현황")
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)

except Exception:
    st.error("앱 실행 중 오류가 발생했습니다!")
    st.text(traceback.format_exc())
