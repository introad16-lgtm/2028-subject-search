import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="양명여고 학교 활동 프로그램", page_icon="📋", layout="wide")

# 2. ✨학교 활동 페이지 전용 상큼 테마 CSS✨
st.markdown("""
<style>
    /* 전체 배경 핑크 */
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 

    /* 🏠 메인 홈 버튼 디자인 */
    .home-btn > button {
        background-color: #FFFFFF !important;
        color: #FF1493 !important;
        border: 2px solid #FFC0CB !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        padding: 5px 20px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 5px rgba(255, 105, 180, 0.1) !important;
        margin-bottom: 20px !important;
    }
    .home-btn > button:hover {
        background-color: #FFF0F5 !important;
        border-color: #FF1493 !important;
        transform: translateY(-2px) !important;
    }

    /* 🎯 계열/학과 선택 박스 구역 디자인 */
    .selection-container {
        background-color: #FFFFFF;
        border: 3px solid #FF1493;
        border-radius: 20px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 0 8px 20px rgba(255, 105, 180, 0.1);
    }

    /* 선택창 제목 디자인 */
    .selection-label {
        color: #FF1493;
        font-size: 1.2rem;
        font-weight: 800;
        margin-bottom: 15px;
    }

    /* 셀렉트박스 테두리 디자인 */
    div[data-baseweb="select"] > div {
        border: 2px solid #FFD700 !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# 🏠 메인 홈 버튼
st.markdown('<div class="home-btn">', unsafe_allow_html=True)
if st.button("🏠 메인 화면으로 돌아가기"):
    st.switch_page("app.py")
st.markdown('</div>', unsafe_allow_html=True)

# 3. 상단 헤더
st.markdown("""
<div style='text-align: center; padding-bottom: 40px;'>
    <h1 style='color: #FF1493; font-weight: 900; font-size: 3rem;'>📋 학교 활동 프로그램 안내</h1>
    <p style='color: #64748B; font-size: 1.2rem; margin-top: 10px;'>나의 진로에 딱 맞는 활동은 무엇일까요? 계열과 학과를 선택해 보세요.</p>
</div>
""", unsafe_allow_html=True)

# 4. 계열 및 학과 데이터 구성
# 선생님, 여기에 학과를 더 추가하거나 수정하실 수 있습니다!
career_data = {
    "인문계열": ["국어국문학과", "영어영문학과", "사학사", "철학과", "심리학과"],
    "사회계열": ["경영학과", "경제학과", "정치외교학과", "사회복지학과", "미디어커뮤니케이션학과", "행정학과"],
    "교육계열": ["초등교육과", "국어교육과", "수학교육과", "영어교육과", "유아교육과", "특수교육과"],
    "공학계열": ["컴퓨터공학과", "인공지능(AI)학과", "기계공학과", "전기전자공학과", "화학공학과", "건축학과"],
    "자연계열": ["수학과", "물리학과", "화학과", "생명과학과", "환경학과"],
    "의약계열": ["의예과", "치의예과", "한의예과", "약학과", "간호학과", "수의예과"],
    "예체능계열": ["디자인학과", "회화과", "음악학과", "체육학과", "연극영화과"]
}

# 5. 선택 메뉴 구현
st.markdown("<div class='selection-container'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown("<p class='selection-label'>🌟 1. 희망 계열 선택</p>", unsafe_allow_html=True)
    selected_field = st.selectbox(
        "계열을 선택해 주세요",
        options=list(career_data.keys()),
        index=0,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("<p class='selection-label'>🎓 2. 희망 학과 선택</p>", unsafe_allow_html=True)
    # 선택된 계열에 해당하는 학과 목록만 가져오기
    departments = career_data[selected_field]
    selected_dept = st.selectbox(
        "학과를 선택해 주세요",
        options=departments,
        index=0,
        label_visibility="collapsed"
    )
st.markdown("</div>", unsafe_allow_html=True)

# 선택 결과 확인 (임시 메시지)
st.write("")
st.success(f"📍 현재 **{selected_field} > {selected_dept}** 지망을 선택하셨습니다. 아래에서 맞춤형 활동을 확인하세요!")

# ----------------------------------------------------------------
# 이 아래에 앞으로 활동 프로그램 안내 내용을 채워넣을 예정입니다!
# ----------------------------------------------------------------
