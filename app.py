import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="양명여고 진로진학 통합 시스템", page_icon="💖", layout="wide")

# 2. 핑크/옐로우 테마 & ✨투명 유리 버튼 마법 CSS✨
st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    
    /* 각 칸(컬럼)을 기준으로 겹치기 준비 */
    div[data-testid="column"] {
        position: relative !important;
    }
    
    /* ✨핵심✨ 진짜 클릭 버튼은 '완전 투명'하게 만들어서 디자인 위에 덮어씌우기 */
    div.stButton {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        opacity: 0 !important; /* 투명하게 숨김! */
        z-index: 999 !important; /* 제일 위로 끌어올림 */
    }
    div.stButton > button {
        width: 100% !important;
        height: 100% !important;
        cursor: pointer !important;
    }

    /* 디자인 박스에 마우스 올렸을 때 애니메이션 */
    .my-card {
        transition: all 0.3s ease;
    }
    div[data-testid="column"]:hover .my-card {
        transform: translateY(-8px);
        box-shadow: 0 15px 25px rgba(0,0,0,0.1) !important;
    }
    div[data-testid="column"]:nth-of-type(2):hover .my-card { background-color: #FFFFF0 !important; border-color: #FFA500 !important; }
    div[data-testid="column"]:nth-of-type(3):hover .my-card { background-color: #FFF0F5 !important; border-color: #FF69B4 !important; }

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

# 4. 완벽한 디자인 + 보이지 않는 투명 버튼 레이아웃
col1, col2, col3, col4 = st.columns([1, 4, 4, 1])

with col2:
    # 화면에 보이는 '완벽하고 큼직한 디자인 박스' (선생님이 원하셨던 그대로!)
    st.markdown("""
    <div class="my-card" style='background-color: white; border: 4px solid #FFD700; border-radius: 20px; padding: 40px 20px; text-align: center; height: 220px; box-shadow: 0 8px 15px rgba(0,0,0,0.05);'>
        <h3 style='color: #CA8A04; font-size: 2.2rem; margin: 0; font-weight: 900;'>🎓 권장과목 검색기</h3>
        <p style='color: #64748B; font-size: 1.1rem; margin-top: 15px; font-weight: 600;'>2028학년도 대학별 필수 과목을<br>빠르게 검색합니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 기능만 담당하는 '보이지 않는 투명 버튼' (위의 박스를 덮고 있음)
    if st.button("검색기 이동", key="btn1"):
        st.switch_page("pages/1_🎓_권장과목_검색기.py")

with col3:
    # 화면에 보이는 '완벽하고 큼직한 디자인 박스'
    st.markdown("""
    <div class="my-card" style='background-color: white; border: 4px solid #FF1493; border-radius: 20px; padding: 40px 20px; text-align: center; height: 220px; box-shadow: 0 8px 15px rgba(0,0,0,0.05);'>
        <h3 style='color: #FF1493; font-size: 2.2rem; margin: 0; font-weight: 900;'>📋 학교 활동 프로그램 안내</h3>
        <p style='color: #64748B; font-size: 1.1rem; margin-top: 15px; font-weight: 600;'>제미나이 AI가 전공 맞춤형 세특을<br>실시간으로 창작합니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 기능만 담당하는 '보이지 않는 투명 버튼'
    if st.button("활동 안내 이동", key="btn2"):
        st.switch_page("pages/2_📋_학교_활동_프로그램_안내.py")

st.sidebar.info("💖 화면 중앙의 박스를 직접 누르거나, 여기서 메뉴를 선택하세요!")
