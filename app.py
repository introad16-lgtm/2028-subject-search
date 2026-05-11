import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="양명여고 진로진학 통합 시스템", page_icon="💖", layout="wide")

# 2. 스타일 시트 (버튼을 카드처럼 보이게 만들기)
st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; }
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; }
    
    /* 카드형 버튼 스타일 */
    div.stButton > button {
        height: 200px;
        background-color: white;
        border-radius: 20px;
        border: 3px solid #FFD700;
        color: #333;
        font-size: 1.5rem !important;
        font-weight: 900 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: center;
        white-space: pre-line; /* 줄바꿈 허용 */
    }
    
    /* 왼쪽 검색기 카드 스타일 (옐로우 강조) */
    div.stButton:nth-child(1) > button { border-color: #FFD700; color: #CA8A04; }
    
    /* 오른쪽 프로그램 안내 카드 스타일 (핑크 강조) */
    div.stButton:nth-child(2) > button { border-color: #FF1493; color: #FF1493; }

    div.stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(255, 20, 147, 0.2);
        border-color: #FFA500;
        background-color: #FFF9FA;
    }
</style>
""", unsafe_allow_html=True)

# 3. 메인 타이틀
st.markdown("""
    <div style='text-align: center; padding: 40px 0;'>
        <div style='font-size: 5rem; margin-bottom: 10px;'>🏫💖💛</div>
        <h1 style='color: #FF1493; font-size: 3.2rem; font-weight: 900;'>양명여자고등학교<br>진로진학 통합 포털</h1>
        <p style='color: #FF8C00; font-size: 1.4rem; margin-top: 15px; font-weight: 600;'>학생들의 꿈과 미래를 잇는 상큼한 통로입니다.</p>
    </div>
    <div style='text-align: center; margin-bottom: 30px;'>
        <h3 style='color: #333;'>👇 원하는 기능을 클릭하면 바로 이동합니다!</h3>
    </div>
""", unsafe_allow_html=True)

# 4. 카드형 바로가기 레이아웃
col1, col2, col3, col4 = st.columns([1, 4, 4, 1])

with col2:
    # 텍스트와 부가 설명을 포함한 큰 버튼
    if st.button("🎓\n권장과목 검색기\n\n(2028 대학별 필수 과목)", use_container_width=True):
        st.switch_page("pages/1_🎓_권장과목_검색기.py")

with col3:
    if st.button("📋\n학교 활동 프로그램 안내\n\n(특강 및 실습 프로그램)", use_container_width=True):
        st.switch_page("pages/2_🎯_AI_생기부_설계기.py") # 파일명은 그대로 두거나 나중에 바꾸셔도 됩니다.

st.sidebar.info("💖 양명여고 학생들의 성장을 응원합니다!")
