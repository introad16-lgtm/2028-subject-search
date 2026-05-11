import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="양명여고 진로진학 통합 시스템", page_icon="💖", layout="wide")

# 2. 핑크/옐로우 테마 및 ✨글자색 완벽 복구✨ 네이티브 버튼 CSS
st.markdown("""
<style>
    /* 전체 배경 핑크 */
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    
    /* -----------------------------------------------------------
       버튼을 거대한 디자인 카드(박스)로 탈바꿈 시키는 핵심 CSS
    ----------------------------------------------------------- */
    div.stButton > button {
        background-color: white !important;
        border-radius: 20px !important;
        height: 240px !important; /* 높이를 조금 더 여유있게 조정 */
        width: 100% !important;
        box-shadow: 0 8px 15px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        /* 기본 설명 텍스트 스타일 */
        color: #64748B !important;   
        font-size: 1.1rem !important; 
        font-weight: 600 !important;
        line-height: 1.5 !important;
        padding: 20px !important;
    }

    /* 버튼 내부의 텍스트 정렬 */
    div.stButton > button div[data-testid="stMarkdownContainer"] {
        width: 100% !important;
        text-align: center !important;
    }

    /* ✨ 제목 부분(Bold처리된 부분)만 골라서 색상과 크기를 크게! */
    div.stButton > button strong {
        font-size: 2.3rem !important; /* 제목 크기 대폭 확대 */
        font-weight: 900 !important;
        display: block !important;
        margin-bottom: 20px !important; /* 제목과 설명 사이 간격 */
    }

    /* -----------------------------------------------------------
       💛 왼쪽 검색기 카드 전용 스타일 (옐로우-골드)
    ----------------------------------------------------------- */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button {
        border: 4px solid #FFD700 !important; /* 옐로우 테두리 */
    }
    div[data-testid="column"]:nth-of-type(2) div.stButton > button strong {
        color: #CA8A04 !important; /* 진한 골드색 제목 */
    }
    div[data-testid="column"]:nth-of-type(2) div.stButton > button:hover {
        transform: translateY(-10px) !important;
        box-shadow: 0 15px 30px rgba(255, 215, 0, 0.3) !important;
        background-color: #FFFFF8 !important;
        border-color: #FFA500 !important;
    }

    /* -----------------------------------------------------------
       💖 오른쪽 활동 안내 카드 전용 스타일 (핑크)
    ----------------------------------------------------------- */
    div[data-testid="column"]:nth-of-type(3) div.stButton > button {
        border: 4px solid #FF1493 !important; /* 핑크 테두리 */
    }
    div[data-testid="column"]:nth-of-type(3) div.stButton > button strong {
        color: #FF1493 !important; /* 핫핑크색 제목 */
    }
    div[data-testid="column"]:nth-of-type(3) div.stButton > button:hover {
        transform: translateY(-10px) !important;
        box-shadow: 0 15px 30px rgba(255, 20, 147, 0.3) !important;
        background-color: #FFF9FB !important;
        border-color: #FF69B4 !important;
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
    <div style='text-align: center; margin-top: 30px; margin-bottom: 40px;'>
        <h3 style='color: #333;'>👇 아래 박스를 클릭하면 해당 기능으로 즉시 이동합니다!</h3>
    </div>
""", unsafe_allow_html=True)

# 4. 버튼형 카드 레이아웃
col1, col2, col3, col4 = st.columns([1, 4, 4, 1])

with col2:
    # **별표**로 감싸진 부분이 CSS 마법을 통해 '색상이 들어간 거대 제목'이 됩니다!
    if st.button("**🎓 권장과목 검색기**\n\n2028학년도 대학별 필수 과목을\n빠르고 정확하게 검색합니다.", use_container_width=True):
        st.switch_page("pages/1_🎓_권장과목_검색기.py")

with col3:
    if st.button("**📋 학교 활동 프로그램 안내**\n\n제미나이 AI가 전공 맞춤형 세특을\n실시간으로 설계하고 창작합니다.", use_container_width=True):
        st.switch_page("pages/2_📋_학교_활동_프로그램_안내.py")

st.sidebar.info("💖 양명여고 학생들의 밝은 미래를 응원합니다!")
