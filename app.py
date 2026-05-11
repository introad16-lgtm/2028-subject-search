import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="양명여고 진로진학 통합 시스템", page_icon="💖", layout="wide")

# 2. 핑크/옐로우 테마 및 '처음 느낌 그대로' 버튼 크기/색상 대폭 확대
st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    
    /* 버튼을 거대한 카드처럼 예쁘게 꾸미기 */
    div.stButton > button {
        background-color: #FFFFFF !important;
        border-radius: 20px !important;
        height: 220px !important; /* 박스 높이 넉넉하게 */
        width: 100% !important;
        box-shadow: 0 8px 15px rgba(0,0,0,0.08) !important;
        transition: all 0.3s ease !important;
        white-space: pre-wrap !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        line-height: 1.6 !important;
    }
    
    /* ========================================= */
    /* 💛 왼쪽 검색기 카드 (옐로우 테마)         */
    /* ========================================= */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button {
        border: 4px solid #FFD700 !important; /* 테두리 굵고 진하게 */
    }
    
    /* 첫 번째 줄 (제목) : 엄청 크게, 진한 노란색 */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button p::first-line {
        color: #CA8A04 !important;
        font-size: 2.2rem !important; 
        font-weight: 900 !important;
    }
    
    /* 전체 텍스트 (설명) : 회색, 적당한 크기 */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button p {
        color: #64748B !important;
        font-size: 1.1rem !important; 
        font-weight: 600 !important;
        margin: 0 !important;
    }
    
    /* 마우스 올렸을 때 애니메이션 */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button:hover {
        transform: translateY(-8px) !important;
        box-shadow: 0 15px 25px rgba(255, 215, 0, 0.3) !important;
        background-color: #FFFFF0 !important;
        border-color: #FFA500 !important;
    }

    /* ========================================= */
    /* 💖 오른쪽 프로그램 안내 카드 (핑크 테마)  */
    /* ========================================= */
    div[data-testid="column"]:nth-of-type(3) div.stButton > button {
        border: 4px solid #FF1493 !important; /* 테두리 굵고 진하게 */
    }
    
    /* 첫 번째 줄 (제목) : 엄청 크게, 진한 핑크색 */
    div[data-testid="column"]:nth-of-type(3) div.stButton > button p::first-line {
        color: #FF1493 !important;
        font-size: 2.2rem !important; 
        font-weight: 900 !important;
    }
    
    /* 전체 텍스트 (설명) : 회색, 적당한 크기 */
    div[data-testid="column"]:nth-of-type(3) div.stButton > button p {
        color: #64748B !important;
        font-size: 1.1rem !important; 
        font-weight: 600 !important;
        margin: 0 !important;
    }
    
    /* 마우스 올렸을 때 애니메이션 */
    div[data-testid="column"]:nth-of-type(3) div.stButton > button:hover {
        transform: translateY(-8px) !important;
        box-shadow: 0 15px 25px rgba(255, 20, 147, 0.3) !important;
        background-color: #FFF0F5 !important;
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
    <div style='text-align: center; margin-top: 30px; margin-bottom: 30px;'>
        <h3 style='color: #333;'>👇 아래 박스를 클릭하면 바로 해당 기능으로 이동합니다!</h3>
    </div>
""", unsafe_allow_html=True)

# 4. 박스형 바로가기 버튼 레이아웃
col1, col2, col3, col4 = st.columns([1, 4, 4, 1])

with col2:
    # 띄어쓰기(\n)를 기준으로 위는 제목, 아래는 설명으로 디자인이 나뉩니다.
    if st.button("🎓 권장과목 검색기\n\n2028학년도 대학별 필수 과목을 빠르게 검색합니다.", use_container_width=True):
        st.switch_page("pages/1_🎓_권장과목_검색기.py")

with col3:
    if st.button("📋 학교 활동 프로그램 안내\n\n제미나이 AI가 전공 맞춤형 세특을 창작합니다.", use_container_width=True):
        st.switch_page("pages/2_📋_학교_활동_프로그램_안내.py")

st.sidebar.info("💖 화면 중앙의 박스를 직접 누르거나, 여기서 메뉴를 선택하세요!")
