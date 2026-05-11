import streamlit as st

st.set_page_config(page_title="양명여고 통합 진로 시스템", page_icon="💖", layout="wide")

# 전체 배경 테마 (핑크 & 옐로우)
st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; }
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; padding: 50px 0;'>
        <div style='font-size: 5rem; margin-bottom: 10px;'>🏫💖💛</div>
        <h1 style='color: #FF1493; font-size: 3.5rem; font-weight: 900;'>양명여자고등학교<br>진로진학 통합 포털</h1>
        <p style='color: #CA8A04; font-size: 1.5rem; margin-top: 20px; font-weight: 600;'>학생들의 꿈과 미래를 잇는 상큼한 통로입니다.</p>
    </div>
    <hr style='border: 1px solid #FFC0CB;'>
    <div style='text-align: center; margin-top: 30px;'>
        <h3 style='color: #333;'>👈 왼쪽 메뉴를 클릭하여 원하는 기능을 실행하세요!</h3>
        <p style='color: gray;'>1. 대학별 권장과목 검색 | 2. AI 기반 생기부 설계</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.info("원하는 기능을 위에서 선택해주세요!")
