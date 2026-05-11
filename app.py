import streamlit as st

# 페이지 탭 이름과 아이콘
st.set_page_config(page_title="양명여고 통합 진로 시스템", page_icon="💖", layout="wide")

# 전체 배경 테마 (핑크 & 옐로우)
st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; }
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; }
</style>
""", unsafe_allow_html=True)

# 메인 대문 화면
st.markdown("""
    <div style='text-align: center; padding: 50px 0;'>
        <div style='font-size: 5rem; margin-bottom: 10px;'>🏫💖💛</div>
        <h1 style='color: #FF1493; font-size: 3.5rem; font-weight: 900;'>양명여자고등학교<br>진로진학 통합 포털</h1>
        <p style='color: #CA8A04; font-size: 1.5rem; margin-top: 20px; font-weight: 600;'>학생들의 꿈과 미래를 잇는 상큼한 통로입니다.</p>
    </div>
    <hr style='border: 1px solid #FFC0CB;'>
    <div style='text-align: center; margin-top: 30px;'>
        <h3 style='color: #333;'>👈 왼쪽 메뉴를 클릭하여 원하는 기능을 실행하세요!</h3>
        <div style='display: flex; justify-content: center; gap: 20px; margin-top: 20px;'>
            <div style='background-color: white; padding: 20px; border-radius: 15px; border: 2px solid #FFD700; width: 300px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
                <h4 style='color: #CA8A04; margin-top:0;'>🎓 권장과목 검색기</h4>
                <p style='color: gray; font-size: 0.9rem;'>2028학년도 대학별<br>필수 과목 빠른 검색</p>
            </div>
            <div style='background-color: white; padding: 20px; border-radius: 15px; border: 2px solid #FF1493; width: 300px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
                <h4 style='color: #FF1493; margin-top:0;'>🎯 AI 생기부 설계기</h4>
                <p style='color: gray; font-size: 0.9rem;'>제미나이 AI 실시간<br>전공 맞춤형 세특 창작</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.info("위에서 원하는 메뉴를 선택해 주세요!")
