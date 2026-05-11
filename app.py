import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="양명여고 진로진학 통합 시스템", page_icon="💖", layout="wide")

# 2. 핑크/옐로우/오렌지 테마 CSS 및 '박스형 버튼' 스타일 적용
st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    
    /* 기존 박스 디자인을 그대로 버튼에 입히는 마법의 CSS */
    div.stButton > button {
        background-color: #FFFFFF !important;
        border-radius: 15px !important;
        height: 160px !important; /* 기존 박스 높이와 동일하게 */
        width: 100% !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease !important;
        white-space: pre-line !important; /* 글자 줄바꿈 허용 */
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        line-height: 1.6 !important;
    }
    
    /* 왼쪽 첫 번째 버튼 (권장과목 검색기 - 옐로우 테마) */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button {
        border: 3px solid #FFD700 !important;
        color: #CA8A04 !important;
        font-size: 1.3rem !important;
        font-weight: 900 !important;
    }
    
    /* 마우스 올렸을 때 애니메이션 */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 10px 25px rgba(255, 215, 0, 0.2) !important;
        border-color: #FFA500 !important;
        background-color: #FFF9FA !important;
    }

    /* 오른쪽 두 번째 버튼 (학교 활동 프로그램 안내 - 핑크 테마) */
    div[data-testid="column"]:nth-of-type(3) div.stButton > button {
        border: 3px solid #FF1493 !important;
        color: #FF1493 !important;
        font-size: 1.3rem !important;
        font-weight: 900 !important;
    }

    div[data-testid="column"]:nth-of-type(3) div.stButton > button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 10px 25px rgba(255, 20, 147, 0.2) !important;
        border-color: #FF69B4 !important;
        background-color: #FFF9FA !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 메인 타이틀 화면
st.markdown("""
    <div style='text-align: center; padding: 50px 0;'>
        <div style='font-size: 5rem; margin-bottom: 10px;'>🏫💖💛</div>
        <h1 style='color: #FF1493; font-size: 3.5rem; font-weight: 900;'>양명여자고등학교<br>진로진학 통합 포털</h1>
        <p style='color: #FF8C00; font-size: 1.5rem; margin-top: 20px; font-weight: 600;'>학생들의 꿈과 미래를 잇는 상큼한 통로입니다.</p>
    </div>
    <hr style='border: 1px solid #FFC0CB;'>
    <div style='text-align: center; margin-top: 30px; margin-bottom: 30px;'>
        <h3 style='color: #333;'>👇 아래 박스를 클릭하면 바로 해당 기능으로 이동합니다!</h3>
    </div>
""", unsafe_allow_html=True)

# 4. 박스형 바로가기 버튼 레이아웃
col1, col2, col3, col4 = st.columns([1, 4, 4, 1])

with col2:
    # 박스 디자인과 텍스트를 하나로 합친 버튼
    if st.button("🎓 권장과목 검색기\n\n(2028학년도 대학별 필수 과목을 빠르게 검색합니다)", use_container_width=True):
        st.switch_page("pages/1_🎓_권장과목_검색기.py")

with col3:
    # 박스 디자인과 텍스트를 하나로 합친 버튼
    if st.button("📋 학교 활동 프로그램 안내\n\n(제미나이 AI가 전공 맞춤형 세특을 창작합니다)", use_container_width=True):
        st.switch_page("pages/2_📋_학교_활동_프로그램_안내.py")

st.sidebar.info("💖 화면 중앙의 박스를 직접 누르거나, 여기서 메뉴를 선택하세요!")
