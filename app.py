import streamlit as st
import pandas as pd
import os

# 1. 웹 페이지 기본 설정
st.set_page_config(
    page_title="2028학년도 대학별 권장과목 검색기",
    page_icon="🎓",
    layout="centered"
)

# 🌟 학교 이름을 크고 강조되게 변경 (HTML 사용)
st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🏫 양명여고 진로진학부</h2>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>2028 대학별 권장과목 검색</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>대학명과 학과를 각각 또는 동시에 입력하여 필요한 과목을 찾아보세요.</p>", unsafe_allow_html=True)

# 데이터 불러오기 함수
@st.cache_data
def load_data():
    # 파일 이름을 data.csv 또는 data.xlsx로 맞춰주세요.
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
    st.write("") # 간격 조절
    
    # 🌟 하나만 써도, 둘 다 써도 검색되는 스마트 검색창
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            univ_keyword = st.text_input("🏫 대학 이름으로 검색", placeholder="예: 서울대, 가톨릭대")
        with col2:
            dept_keyword = st.text_input("📚 학과 이름으로 검색", placeholder="예: 컴퓨터, 의학, 경영")
    
    st.divider()
    
    # 검색 로직 (둘 중 하나만 입력해도 작동하며, 둘 다 입력하면 더 정확하게 필터링됩니다)
    if univ_keyword or dept_keyword:
        result = df
        
        # 대학명 입력 시 필터링
        if univ_keyword:
            result = result[result['대학명'].str.contains(univ_keyword, na=False)]
            
        # 학과명 입력 시 필터링 (동시 입력 시 교집합 결과)
        if dept_keyword:
            result = result[result['모집단위'].str.contains(dept_keyword, na=False)]
            
        if result.empty:
            st.warning("❌ 검색 결과가 없습니다. 검색어를 다시 확인해 주세요.")
        else:
            st.success(f"✅ 총 **{len(result)}건**의 검색 결과를 찾았습니다.")
            for index, row in result.iterrows():
                # 결과물 디자인을 카드 형태로 보기 좋게 출력
                with st.expander(f"🏫 [{row['대학명']}] {row['모집단위']}", expanded=True):
                    if row['핵심과목']: 
                        st.markdown(f"**📌 핵심과목:** {row['핵심과목']}")
                    if row['권장과목']: 
                        st.markdown(f"**💡 권장과목:** {row['권장과목']}")
                    if row['비고'] and row['비고'] != '-': 
                        st.markdown(f"**📝 비고:** {row['비고']}")
    else:
        st.info("💡 대학 이름이나 학과 중 하나만 입력해도 검색이 시작됩니다.\n두 칸을 모두 입력하면 해당 대학의 특정 학과만 정확히 찾아낼 수 있습니다.")

# 하단 푸터
st.markdown(
    """
    <hr>
    <div style='text-align: center; color: gray; font-size: 0.8em;'>
        © 2026 양명여자고등학교 진로진학부 | 학생들의 미래를 응원합니다.
    </div>
    """,
    unsafe_allow_html=True
)
