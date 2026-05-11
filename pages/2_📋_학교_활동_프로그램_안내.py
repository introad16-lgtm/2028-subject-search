import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(page_title="양명여고 학교 활동 프로그램", page_icon="📋", layout="wide")

# 2. ✨학교 활동 페이지 전용 CSS✨
st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 

    /* 홈 버튼 */
    .home-btn > button {
        background-color: #FFFFFF !important;
        color: #FF1493 !important;
        border: 2px solid #FFC0CB !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        padding: 5px 20px !important;
        transition: all 0.3s ease !important;
        margin-bottom: 20px !important;
    }
    .home-btn > button:hover {
        background-color: #FFF0F5 !important;
        border-color: #FF1493 !important;
    }

    /* 선택 구역 박스 */
    .selection-container {
        background-color: #FFFFFF;
        border: 3px solid #FF1493;
        border-radius: 20px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 0 8px 20px rgba(255, 105, 180, 0.1);
    }
    .selection-label {
        color: #FF1493;
        font-size: 1.2rem;
        font-weight: 800;
        margin-bottom: 15px;
    }
    div[data-baseweb="select"] > div {
        border: 2px solid #FFD700 !important;
        border-radius: 12px !important;
    }
    
    /* ✨ 제미나이 버튼 전용 화려한 스타일 ✨ */
    .gemini-btn > button {
        background: linear-gradient(135deg, #FF69B4 0%, #FFA500 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        padding: 15px 0 !important;
        box-shadow: 0 6px 15px rgba(255, 105, 180, 0.4) !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    .gemini-btn > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 20px rgba(255, 215, 0, 0.5) !important;
        background: linear-gradient(135deg, #FFA500 0%, #FF1493 100%) !important;
    }
</style>
""", unsafe_allow_html=True)

# 홈 버튼
st.markdown('<div class="home-btn">', unsafe_allow_html=True)
if st.button("🏠 메인 화면으로 돌아가기"):
    st.switch_page("app.py")
st.markdown('</div>', unsafe_allow_html=True)

# 3. 상단 헤더
st.markdown("""
<div style='text-align: center; padding-bottom: 30px;'>
    <h1 style='color: #FF1493; font-weight: 900; font-size: 3rem;'>📋 학교 활동 프로그램 안내</h1>
    <p style='color: #64748B; font-size: 1.2rem; margin-top: 10px;'>계열과 학과를 선택하고, 양명여고의 맞춤형 활동을 제미나이 AI로 분석해 보세요.</p>
</div>
""", unsafe_allow_html=True)

# 4. 계열 및 학과 데이터
career_data = {
    "인문계열": ["국어국문학과", "영어영문학과", "사학과", "철학과", "심리학과"],
    "사회계열": ["경영학과", "경제학과", "정치외교학과", "사회복지학과", "미디어커뮤니케이션학과", "행정학과"],
    "교육계열": ["초등교육과", "국어교육과", "수학교육과", "영어교육과", "유아교육과", "특수교육과"],
    "공학계열": ["컴퓨터공학과", "인공지능(AI)학과", "기계공학과", "전기전자공학과", "화학공학과", "건축학과"],
    "자연계열": ["수학과", "물리학과", "화학과", "생명과학과", "환경학과"],
    "의약계열": ["의예과", "치의예과", "한의예과", "약학과", "간호학과", "수의예과"],
    "예체능계열": ["디자인학과", "회화과", "음악학과", "체육학과", "연극영화과"]
}

# 💡 양명여고 대표 활동을 계열별로 자동 매칭!
activity_data = {
    "인문계열": ["아침 독서 프로그램", "창의융합 주제탐구", "독서 토론 캠프", "드림업 프로젝트"],
    "사회계열": ["전문직업인 특강", "금융 리터러시 아카데미", "학생 주도 봉사활동", "창의융합 주제탐구"],
    "교육계열": ["학생 주도 봉사활동", "독서 토론 캠프", "진로 검사 및 상담", "스마트폰 이별주간 캠페인"],
    "공학계열": ["융합과학캠프", "창의융합 주제탐구", "전문직업인 특강 (IT분야)", "과천과학관 실습"],
    "자연계열": ["융합과학캠프", "과천과학관 실습", "창의융합 주제탐구", "아침 독서 (과학분야)"],
    "의약계열": ["학생 주도 봉사활동", "융합과학캠프", "생명과학 주제탐구", "전문직업인 특강 (의료분야)"],
    "예체능계열": ["체육 및 예술 축제 기획", "드림업 프로젝트", "전문직업인 특강", "학생 주도 봉사활동"]
}

# 5. 선택 메뉴
st.markdown("<div class='selection-container'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown("<p class='selection-label'>🌟 1. 희망 계열 선택</p>", unsafe_allow_html=True)
    selected_field = st.selectbox("계열 선택", options=list(career_data.keys()), label_visibility="collapsed")

with col2:
    st.markdown("<p class='selection-label'>🎓 2. 희망 학과 선택</p>", unsafe_allow_html=True)
    selected_dept = st.selectbox("학과 선택", options=career_data[selected_field], label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

# 6. 추천 활동 선택 영역 
st.write("")
st.markdown(f"### 💡 **{selected_dept}** 지망 학생을 위한 양명여고 맞춤 추천 활동")

# 계열에 맞는 맞춤 활동을 가져옵니다.
recommended_activities = activity_data.get(selected_field, ["창의융합 주제탐구", "진로 탐색 활동"])
selected_activity = st.radio(
    "아래 활동 중 하나를 선택하여 제미나이 AI에게 세특 가이드를 요청해 보세요:",
    recommended_activities,
    horizontal=True
)

st.write("---")

# 7. 제미나이 AI 연동 영역 
st.markdown("### 🤖 제미나이 AI 맞춤형 생기부 설계기")
st.info(f"**[{selected_dept}]** 진학을 위한 **[{selected_activity}]** 활동에 대해 제미나이 AI가 맞춤형 기록 예시를 창작합니다.")

# 제미나이 버튼을 화면 중앙에 예쁘게 배치
empty1, gemini_col, empty2 = st.columns([1, 2, 1])
with gemini_col:
    st.markdown('<div class="gemini-btn">', unsafe_allow_html=True)
    gemini_clicked = st.button("✨ 제미나이 AI 생기부 생성하기 ✨")
    st.markdown('</div>', unsafe_allow_html=True)

# 제미나이 버튼을 눌렀을 때의 동작 (로딩 애니메이션 + 결과)
if gemini_clicked:
    with st.spinner("제미나이 AI가 양명여고 학생의 역량을 돋보이게 할 내용을 작성 중입니다..."):
        # 여기에 추후 선생님의 실제 Gemini API 코드를 연결하면 됩니다.
        time.sleep(2) # 생각하는 척 2초 대기!
        
        st.success("✅ 제미나이 AI의 맞춤형 가이드 작성이 완료되었습니다!")
        st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #FF1493; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <h4 style="color: #FF1493;">📚 세부능력 및 특기사항 (작성 예시)</h4>
            <p style="color: #333; line-height: 1.8; font-size: 1.1rem;">
            <b>[{selected_activity}]</b>에 주도적으로 참여하여 <b>{selected_dept}</b> 분야에 대한 깊은 학업적 호기심을 입증함. 
            해당 활동에서 습득한 개념과 원리를 자신의 진로와 논리적으로 연계하여 분석하는 능력이 돋보임. 
            특히 양명여고의 자기주도적 학습 환경을 적극적으로 활용하여 심화 자료를 능동적으로 탐색하였으며, 
            팀원들과의 협력 과정에서 갈등을 조율하고 대안을 제시하는 훌륭한 리더십을 발휘함. 
            향후 <b>{selected_dept}</b> 전공에 진학하여 공동체에 선한 영향력을 미칠 수 있는 탁월한 잠재력을 지닌 학생임.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.caption("※ 본 내용은 제미나이 AI가 생성한 가이드라인 예시이며, 실제 API를 연동하여 학생의 개별적인 키워드를 추가할 수 있습니다.")
