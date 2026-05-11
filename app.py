import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="양명여고 진로진학 통합 시스템", page_icon="💖", layout="wide")

# 2. ✨전설의 상큼 디자인 완벽 복구✨ CSS
st.markdown("""
<style>
    /* 전체 배경: 은은한 핑크 */
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    
    /* -----------------------------------------------------------
       버튼을 '이전처럼 예쁜 카드'로 만드는 핵심 마법
    ----------------------------------------------------------- */
    div.stButton > button {
        background-color: white !important;
        border-radius: 25px !important; /* 더 둥글고 귀엽게 */
        height: 260px !important; /* 높이를 충분히 확보 */
        width: 100% !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05) !important;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        border: 4px solid transparent !important;
        padding: 30px !important;
    }

    /* 버튼 안의 텍스트 레이아웃 */
    div.stButton > button div[data-testid="stMarkdownContainer"] {
        width: 100% !important;
        text-align: center !important;
    }

    /* 제목 (Bold 처리된 부분) 스타일 */
    div.stButton > button strong {
        font-size: 2.3rem !important;
        font-weight: 900 !important;
        display: block !important;
        margin-bottom: 18px !important;
        line-height: 1.2 !important;
    }

    /* 설명글 스타일 */
    div.stButton > button p {
        color: #64748B !important;   
        font-size: 1.15rem !important; 
        font-weight: 600 !important;
        line-height: 1.6 !important;
        margin: 0 !important;
        white-space: pre-wrap !important;
    }

    /* -----------------------------------------------------------
       컬럼별 고유 색상 및 호버 효과 (떠오르는 효과)
    ----------------------------------------------------------- */
    
    /* 💛 1. 권장과목 검색기 (옐로우/골드) */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button {
        border-color: #FFD700 !important;
    }
    div[data-testid="column"]:nth-of-type(2) div.stButton > button strong {
        color: #CA8A04 !important;
    }
    div[data-testid="column"]:nth-of-type(2) div.stButton > button:hover {
        transform: translateY(-12px) scale(1.02) !important;
        box-shadow: 0 20px 40px rgba(255, 215, 0, 0.25) !important;
        background-color: #FFFFF9 !important;
        border-color: #FFA500 !important;
    }

    /* 💖 2. 학교 활동 안내 (핫핑크) */
    div[data-testid="column"]:nth-of-type(3) div.stButton > button {
        border-color: #FF1493 !important;
    }
    div[data-testid="column"]:nth-of-type(3) div.stButton > button strong {
        color: #FF1493 !important;
    }
    div[data-testid="column"]:nth-of-type(3) div.stButton > button:hover {
        transform: translateY(-12px) scale(1.02) !important;
        box-shadow: 0 20px 40px rgba(255, 20, 147, 0.25) !important;
        background-color: #FFF9FB !important;
        border-color: #FF69B4 !important;
    }

    /* 🍊 3. 내신 등급 산출기 (오렌지) */
    div[data-testid="column"]:nth-of-type(4) div.stButton > button {
        border-color: #FF8C00 !important;
    }
    div[data-testid="column"]:nth-of-type(4) div.stButton > button strong {
        color: #EA580C !important;
    }
    div[data-testid="column"]:nth-of-type(4) div.stButton > button:hover {
        transform: translateY(-12px) scale(1.02) !important;
        box-shadow: 0 20px 40px rgba(255, 140, 0, 0.25) !important;
        background-color: #FFF6F0 !important;
        border-color: #FF7F50 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 메인 타이틀 화면 (이전의 그 느낌 그대로)
st.markdown("""
    <div style='text-align: center; padding: 50px 0;'>
        <div style='font-size: 5.5rem; margin-bottom: 10px;'>🏫💖💛</div>
        <h1 style='color: #FF1493; font-size: 3.8rem; font-weight: 900; letter-spacing: -1px;'>양명여자고등학교<br>진로진학 통합 포털</h1>
        <p style='color: #FF8C00; font-size: 1.6rem; margin-top: 25px; font-weight: 700;'>학생들의 꿈과 미래를 잇는 상큼한 통로입니다.</p>
    </div>
    <hr style='border: 1px solid #FFC0CB; margin-bottom: 40px;'>
    <div style='text-align: center; margin-bottom: 40px;'>
        <h3 style='color: #333; font-weight: 800;'>👇 아래 박스를 클릭하면 해당 기능으로 즉시 이동합니다!</h3>
    </div>
""", unsafe_allow_html=True)

# 4. 3개의 버튼형 카드 레이아웃 (좌우 여백 조절)
col_side1, col1, col2, col3, col_side2 = st.columns([0.2, 3, 3, 3, 0.2])

with col1:
    if st.button("**🎓 권장과목 검색기**\n\n2028학년도 대학별 필수 과목을\n빠르고 정확하게 검색합니다.", key="btn_search"):
        st.switch_page("pages/1_🎓_권장과목_검색기.py")

with col2:
    if st.button("**📋 학교 활동 프로그램**\n\n제미나이 AI가 전공 맞춤형 세특을\n실시간으로 설계하고 창작합니다.", key="btn_activity"):
        st.switch_page("pages/2_📋_학교_활동_프로그램_안내.py")

with col3:
    if st.button("**📊 내신 등급 산출기**\n\n2028학년도 5등급제 성적을\n대학별 기준에 맞춰 자동 환산합니다.", key="btn_grade"):
        st.switch_page("pages/3_📊_내신_등급_산출기.py")

st.sidebar.info("💖 양명여고 학생들의 밝은 미래를 응원합니다!")
