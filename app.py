import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="양명여고 진로진학 통합 시스템", page_icon="💖", layout="wide")

# 2. ✨양명여고 핑크/옐로우/오렌지 & 모바일 반응형 완벽 CSS✨
st.markdown("""
<style>
    /* 전체 배경: 은은한 핑크 */
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    
    /* -----------------------------------------------------------
       버튼을 '예쁜 카드'로 만드는 핵심 스타일
    ----------------------------------------------------------- */
    div.stButton > button {
        background-color: white !important;
        border-radius: 20px !important;
        height: 250px !important;
        width: 100% !important;
        box-shadow: 0 8px 15px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        padding: 20px !important;
    }

    div.stButton > button div[data-testid="stMarkdownContainer"] {
        width: 100% !important;
        text-align: center !important;
    }

    /* 제목 (Bold 처리된 부분) 스타일 */
    div.stButton > button strong {
        font-size: 2.2rem !important;
        font-weight: 900 !important;
        display: block !important;
        margin-bottom: 15px !important;
        line-height: 1.3 !important;
    }

    /* 설명글 스타일 */
    div.stButton > button p {
        color: #64748B !important;   
        font-size: 1.1rem !important; 
        font-weight: 600 !important;
        line-height: 1.6 !important;
        margin: 0 !important;
        white-space: pre-wrap !important;
    }

    /* -----------------------------------------------------------
       컬럼별 포인트 색상 강제 주입
    ----------------------------------------------------------- */
    
    /* 💛 1. 권장과목 검색기 (옐로우) */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button { border: 4px solid #FFD700 !important; }
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button strong { color: #CA8A04 !important; }
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button:hover {
        transform: translateY(-10px) !important;
        box-shadow: 0 15px 30px rgba(255, 215, 0, 0.3) !important;
        background-color: #FFFFF8 !important;
        border-color: #FFA500 !important;
    }

    /* 💖 2. 학교 활동 안내 (핫핑크) */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button { border: 4px solid #FF1493 !important; }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button strong { color: #FF1493 !important; }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button:hover {
        transform: translateY(-10px) !important;
        box-shadow: 0 15px 30px rgba(255, 20, 147, 0.3) !important;
        background-color: #FFF9FB !important;
        border-color: #FF69B4 !important;
    }

    /* 🍊 3. 내신 등급 산출기 (오렌지) */
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) button { border: 4px solid #FF8C00 !important; }
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) button strong { color: #EA580C !important; }
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) button:hover {
        transform: translateY(-10px) !important;
        box-shadow: 0 15px 30px rgba(255, 140, 0, 0.3) !important;
        background-color: #FFF5EB !important;
        border-color: #FF7F50 !important;
    }

    /* -----------------------------------------------------------
       📱 모바일 메인 타이틀 반응형 조절
    ----------------------------------------------------------- */
    @media (max-width: 768px) {
        .main-header-title { font-size: 2.2rem !important; line-height: 1.2 !important; }
        .main-header-subtitle { font-size: 1.1rem !important; margin-top: 10px !important; }
        .main-header-dept { font-size: 0.9rem !important; margin-top: 5px !important; }
        div.stButton > button { height: 200px !important; padding: 10px !important; }
        div.stButton > button strong { font-size: 1.5rem !important; }
        div.stButton > button p { font-size: 0.9rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# 3. 메인 타이틀 화면 (반응형 클래스 적용)
st.markdown("""
    <div style='text-align: center; padding: 40px 0;'>
        <div style='font-size: 5rem; margin-bottom: 10px;'>🏫💖💛</div>
        <h1 class='main-header-title' style='color: #FF1493; font-size: 3.5rem; font-weight: 900;'>양명여자고등학교<br>진로진학 통합 포털</h1>
        <p class='main-header-subtitle' style='color: #FF8C00; font-size: 1.5rem; margin-top: 20px; font-weight: 600;'>학생들의 꿈과 미래를 잇는 상큼한 통로입니다.</p>
        <p class='main-header-dept' style='color: #64748B; font-size: 1.1rem; margin-top: 8px; font-weight: 700;'>- 양명여자고등학교 진로진학부 -</p>
    </div>
    <hr style='border: 1px solid #FFC0CB; margin-bottom: 40px;'>
    <div style='text-align: center; margin-bottom: 40px;'>
        <h3 style='color: #333;'>👇 아래 박스를 클릭하면 해당 기능으로 즉시 이동합니다!</h3>
    </div>
""", unsafe_allow_html=True)

# 4. 버튼형 카드 레이아웃
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("**🎓 권장과목 검색기**\n\n2028학년도 대학별 필수 과목을\n빠르고 정확하게 검색합니다.", use_container_width=True):
        st.switch_page("pages/1_🎓_권장과목_검색기.py")

with col2:
    if st.button("**📋 학교 활동 프로그램**\n\n제미나이 AI가 전공 맞춤형 세특을\n실시간으로 설계하고 창작합니다.", use_container_width=True):
        st.switch_page("pages/2_📋_학교_활동_프로그램_안내.py")

with col3:
    if st.button("**📊 내신 등급 산출기**\n\n2028학년도 5등급제 성적을\n대학별 기준에 맞춰 자동 환산합니다.", use_container_width=True):
        st.switch_page("pages/3_📊_내신_등급_산출기.py")

st.sidebar.info("💖 양명여고 학생들의 밝은 미래를 응원합니다!")
