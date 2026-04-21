import streamlit as st
import pandas as pd
import os

# 1. 웹 페이지 기본 설정
st.set_page_config(
    page_title="2028학년도 대학별 권장과목 검색기",
    page_icon="🎓",
    layout="centered"
)

# 🌟 메인 화면 학교 문구 추가
st.caption("양명여고 진로진학부")
st.title("🎓 2028 대학별 권장과목 검색")
st.markdown("학생들의 꿈과 진로를 응원합니다. 대학명과 학과를 입력해 권장과목을 확인해 보세요!")

# 데이터 불러오기 함수 (기존과 동일)
@st.cache_data
def load_data():
    if os.path.exists('data.csv'):
        try:
            df = pd.read_csv('data.csv', skiprows=2, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv('data.csv', skiprows=2, encoding='cp949')
    elif os.path.exists('data.xlsx'):
        df = pd.read_excel('data.xlsx', skiprows=2)
    else:
        st.error("데이터 파일(data.csv 또는 data.xlsx)을 찾을 수 없습니다.")
        return pd.DataFrame()
        
    if 'Unnamed: 4' in df.columns:
        df = df.drop(columns=['Unnamed: 4'])
    df.rename(columns={'모집단위\n(계열, 단과대, 학과)': '모집단위', '반영과목': '핵심과목', 'Unnamed: 6': '권장과목'}, inplace=True)
    
    return df.drop(0).reset_index(drop=True).fillna('')

df = load_data()

if not df.empty:
    st.divider()
    
    # 🌟 대학과 학과를 각각 또는 동시에 입력할 수 있는 검색창
    st.subheader("🔍 검색 조건 입력")
    col1, col2 = st.columns(2)
    
    with col1:
        univ_keyword = st.text_input("🏫 대학 이름", placeholder="예: 가톨릭대, 서울대")
    with col2:
        dept_keyword = st.text_input("📚 학과(모집단위)", placeholder="예: 컴퓨터, 의예, 경영")
        
    st.divider()
    
    # 검색 로직
    if univ_keyword or dept_keyword:
        result = df
        
        # 대학명 검색어 처리
        if univ_keyword:
            result = result[result['대학명'].str.contains(univ_keyword, na=False)]
            
        # 학과명 검색어 처리 (동시 입력 시 교집합 검색)
        if dept_keyword:
            result = result[result['모집단위'].str.contains(dept_keyword, na=False)]
            
        if result.empty:
            st.warning("❌ 검색 결과가 없습니다. 검색어를 다시 확인해 주세요.")
        else:
            st.info(f"✅ 총 **{len(result)}건**의 검색 결과를 찾았습니다.")
            for index, row in result.iterrows():
                with st.container():
                    st.markdown(f"#### 🏫 [{row['대학명']}] {row['모집단위']}")
                    if row['핵심과목']: 
                        st.markdown(f"**📌 핵심과목:** {row['핵심과목']}")
                    if row['권장과목']: 
                        st.markdown(f"**💡 권장과목:** {row['권장과목']}")
                    if row['비고'] and row['비고'] != '-': 
                        st.markdown(f"**📝 비고:** {row['비고']}")
                    st.markdown("---")
    else:
        st.info("👆 위 검색창에 대학 이름이나 학과를 입력해 주세요.\n(두 칸을 모두 입력하면 해당 대학의 특정 학과만 찾아볼 수 있습니다.)")

# 하단 푸터 추가
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: gray;
        text-align: center;
        padding: 10px;
        font-size: 12px;
    }
    </style>
    <div class="footer">
        © 2026 양명여자고등학교 진로진학부. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)
