import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="양명여고 진로진학 통합 시스템", page_icon="💖", layout="wide")

# 2. 핑크/옐로우/오렌지 테마 CSS 적용
st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    
    /* 하단 이동 버튼 스타일 (오렌지/핑크 그라데이션) */
    div.stButton > button {
        background: linear-gradient(135deg, #FF69B4 0%, #FFA500 100%);
        color: white;
        border-radius: 15px;
        border: none;
        font-weight: 900;
        padding: 12px 0;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3);
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #FFA500 0%, #FF1493 100%);
        color: white;
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.5);
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
    <div style='text-align: center; margin-top: 30px;'>
        <h3 style='color: #333;'>👇 아래 버튼을 클릭하여 원하는 기능을 바로 실행하세요!</h3>
    </div>
""", unsafe_allow_html=True)

st.write("")

# 4. 클릭 가능한 박스 & 분리된 하단 버튼 레이아웃 (선생님이 선택하신 스타일)
col1, col2, col3, col4 = st.columns([1, 4, 4, 1])

with col2:
    st.markdown("""
    <div style='background-color: #FFFFFF; padding: 30px; border-radius: 15px; border: 3px solid #FFD700; height: 160px; text-align: center; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
        <h3 style='color: #CA8A04; margin-top:0;'>🎓 권장과목 검색기</h3>
        <p style='color: #64748B; font-size: 1rem; margin-top: 15px;'>2028학년도 대학별<br>필수 과목을 빠르게 검색합니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 버튼을 누르면 1번 파일로 이동
    if st.button("🚀 검색기 바로가기", use_container_width=True):
        st.switch_page("pages/1_🎓_권장과목_검색기.py")

with col3:
    st.markdown("""
    <div style='background-color: #FFFFFF; padding: 30px; border-radius: 15px; border: 3px solid #FF1493; height: 160px; text-align: center; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
        <h3 style='color: #FF1493; margin-top:0;'>📋 학교 활동 프로그램 안내</h3>
        <p style='color: #64748B; font-size: 1rem; margin-top: 15px;'>제미나이 AI가 실시간으로<br>전공 맞춤형 세특을 창작합니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 버튼을 누르면 새로 바뀐 2번 파일명으로 이동
    if st.button("🚀 활동 프로그램 바로가기", use_container_width=True):
        st.switch_page("pages/2_📋_학교_활동_프로그램_안내.py")

st.sidebar.info("💖 화면 중앙의 버튼을 누르거나 여기서 메뉴를 선택하세요!")
