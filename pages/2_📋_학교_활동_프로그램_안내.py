import streamlit as st
import google.generativeai as genai
import time

# 1. 페이지 설정
st.set_page_config(page_title="양명여고 학생부 AI 설계기", page_icon="📋", layout="wide")

# 2. 양명여고 전용 화사한 테마 CSS
st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    
    /* 🏠 메인 홈 버튼 디자인 */
    .home-btn > button {
        background-color: #FFFFFF !important; color: #FF1493 !important;
        border: 2px solid #FFC0CB !important; border-radius: 10px !important;
        font-weight: 800 !important; padding: 5px 20px !important;
        transition: all 0.3s ease !important; box-shadow: 0 2px 5px rgba(255, 105, 180, 0.1) !important;
        margin-bottom: 20px !important;
    }
    .home-btn > button:hover {
        background-color: #FFF0F5 !important; border-color: #FF1493 !important; transform: translateY(-2px) !important;
    }

    /* 카드형 컨테이너 디자인 */
    .styled-card {
        background-color: #FFFFFF; border: 3px solid #FFC0CB; border-radius: 20px;
        padding: 30px; box-shadow: 0 8px 20px rgba(255, 105, 180, 0.1); margin-bottom: 25px;
    }

    /* 추천 활동 라디오 버튼 스타일 수정 */
    div.row-widget.stRadio > div { flex-direction: column; gap: 10px; }
    
    /* ✨ 화려한 제미나이 버튼 ✨ */
    .gemini-btn > button {
        background: linear-gradient(135deg, #FF69B4 0%, #FFA500 100%) !important;
        color: white !important; border: none !important; border-radius: 15px !important;
        font-weight: 900 !important; font-size: 1.4rem !important; padding: 15px 0 !important;
        box-shadow: 0 6px 15px rgba(255, 105, 180, 0.4) !important; transition: all 0.3s ease !important;
        width: 100%;
    }
    .gemini-btn > button:hover {
        transform: translateY(-5px) !important; box-shadow: 0 10px 25px rgba(255, 215, 0, 0.5) !important;
        background: linear-gradient(135deg, #FFA500 0%, #FF1493 100%) !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 사이드바 (API 키 입력 및 설정)
with st.sidebar:
    st.markdown("### 🔑 제미나이 AI 설정")
    st.info("이 프로그램은 실시간으로 AI를 구동합니다. 구글 Gemini API 키를 입력해 주세요.")
    api_key = st.text_input("Gemini API Key 입력", type="password")
    st.write("---")
    st.markdown("💖 **양명여자고등학교 진로진학부**")

# 홈 버튼
st.markdown('<div class="home-btn">', unsafe_allow_html=True)
if st.button("🏠 메인 화면으로 돌아가기"):
    st.switch_page("app.py")
st.markdown('</div>', unsafe_allow_html=True)

# 4. 상단 헤더
st.markdown("""
<div style='text-align: center; padding-bottom: 30px;'>
    <h1 style='color: #FF1493; font-weight: 900; font-size: 3.5rem;'>🤖 실시간 학생부 AI 설계기</h1>
    <p style='color: #64748B; font-size: 1.2rem; margin-top: 10px;'>계열과 학과를 선택하면 맞춤 활동을 추천하고, 제미나이 AI가 <b>구체적인 활동 전개 방법</b>을 즉석에서 짜드립니다.</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# [데이터 세팅] 학과 및 활동 분류
# -------------------------------------------------------------
career_data = {
    "인문계열": ["국어국문학과", "영어영문학과", "사학과", "철학과", "심리학과"],
    "사회계열": ["경영학과", "경제학과", "정치외교학과", "사회복지학과", "미디어커뮤니케이션학과", "행정학과"],
    "교육계열": ["초등교육과", "국어교육과", "수학교육과", "영어교육과", "유아교육과", "특수교육과"],
    "공학계열": ["컴퓨터공학과", "인공지능(AI)학과", "기계공학과", "전기전자공학과", "화학공학과", "건축학과"],
    "자연계열": ["수학과", "물리학과", "화학과", "생명과학과", "환경학과"],
    "의약계열": ["의예과", "치의예과", "한의예과", "약학과", "간호학과", "수의예과"],
    "예체능계열": ["디자인학과", "회화과", "음악학과", "체육학과", "연극영화과"]
}

# 양명여고 대표 활동 (주도형 / 비주도형 명확히 분류)
activities_db = {
    "드림업 프로젝트": "주도형",
    "학생주도 프로젝트 봉사활동": "주도형",
    "독서탐구": "주도형",
    "이음 책모임": "주도형",
    "환경인문독서토론": "주도형",
    "창의융합 주제탐구 프로젝트": "주도형",
    "스마트폰 이별주간 캠페인": "주도형",
    "이달의 IB 학습자 상 추천": "주도형",
    "전문직업인 초청 특강": "비주도형",
    "과천 과학관 실습 프로그램": "비주도형",
    "이공계 진로캠프 (야간 천체 관측)": "비주도형",
    "금융 리터러시 아카데미": "비주도형"
}

# 계열별 맞춤형 추천 활동 매핑
recommended_activities = {
    "인문계열": ["드림업 프로젝트", "독서탐구", "이음 책모임", "전문직업인 초청 특강"],
    "사회계열": ["학생주도 프로젝트 봉사활동", "환경인문독서토론", "전문직업인 초청 특강", "금융 리터러시 아카데미"],
    "교육계열": ["학생주도 프로젝트 봉사활동", "이음 책모임", "스마트폰 이별주간 캠페인", "전문직업인 초청 특강"],
    "공학계열": ["창의융합 주제탐구 프로젝트", "전문직업인 초청 특강", "과천 과학관 실습 프로그램", "드림업 프로젝트"],
    "자연계열": ["창의융합 주제탐구 프로젝트", "이공계 진로캠프 (야간 천체 관측)", "과천 과학관 실습 프로그램", "독서탐구"],
    "의약계열": ["학생주도 프로젝트 봉사활동", "창의융합 주제탐구 프로젝트", "전문직업인 초청 특강", "과천 과학관 실습 프로그램"],
    "예체능계열": ["드림업 프로젝트", "스마트폰 이별주간 캠페인", "이달의 IB 학습자 상 추천", "전문직업인 초청 특강"]
}

# -------------------------------------------------------------
# STEP 1. 진로 및 추천 활동 선택 
# -------------------------------------------------------------
st.markdown("<div class='styled-card'>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #FF1493; margin-bottom: 20px; border-bottom: 2px solid #FFC0CB; padding-bottom: 10px;'>📝 STEP 1. 계열 및 학과 선택</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    selected_track = st.selectbox("🌟 희망 계열", list(career_data.keys()))
with col2:
    selected_major = st.selectbox("🎓 세부 학과", career_data[selected_track])

st.markdown("<h3 style='color: #FF1493; margin-top: 30px; margin-bottom: 20px; border-bottom: 2px solid #FFC0CB; padding-bottom: 10px;'>🎯 STEP 2. 전공 맞춤 추천 활동 선택</h3>", unsafe_allow_html=True)
st.info(f"💡 **{selected_major}** 진학을 목표로 하는 학생들에게 아래 활동들을 추천합니다. 하나를 선택해 보세요!")

recs = recommended_activities[selected_track]
selected_act = st.radio("추천 활동 목록", recs, label_visibility="collapsed")
act_type = activities_db.get(selected_act, "주도형")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# STEP 3. 활동 성격에 따른 동적 입력창 (주도형 vs 비주도형)
# -------------------------------------------------------------
st.markdown("<div class='styled-card'>", unsafe_allow_html=True)
st.markdown(f"<h3 style='color: #FF1493; margin-bottom: 20px; border-bottom: 2px solid #FFC0CB; padding-bottom: 10px;'>🔍 STEP 3. 세부 정보 입력 ({act_type})</h3>", unsafe_allow_html=True)

custom_title = ""

if act_type == "비주도형":
    st.warning("이 활동은 강연 청취나 정해진 실습을 수행하는 **[비주도형/강의형]** 활동입니다. 수동적인 참여에 그치지 않도록, 제미나이가 **'강연 후 어떻게 심화 후속 활동을 해야 하는지'** 알려드립니다.")
    custom_title = st.text_input("✏️ 수강한 강의/특강/실습의 구체적인 제목을 적어주세요 (필수)", placeholder="예: 빅데이터와 AI 윤리 특강, 과천과학관 DNA 추출 실습")
else:
    st.success("이 활동은 스스로 주제를 정해 탐구하는 **[학생 주도형]** 활동입니다. 제미나이가 **'어떻게 기획하고 실행해야 하는지'** 구체적인 전개 가이드를 제공합니다.")
    custom_title = st.text_input("💡 (선택) 특별히 다루고 싶은 관심 주제나 읽고 있는 책이 있다면 적어주세요.", placeholder="예: 행동경제학, 플랫폼 독과점 문제 (없으면 비워두셔도 됩니다)")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# STEP 4. 제미나이 실행 버튼 및 AI 로직
# -------------------------------------------------------------
st.markdown("<h3 style='color: #CA8A04; text-align: center; margin-bottom: 20px;'>🚀 STEP 4. AI에게 분석 요청하기</h3>", unsafe_allow_html=True)

st.markdown('<div class="gemini-btn">', unsafe_allow_html=True)
gemini_btn = st.button("✨ 제미나이 AI 실시간 활동 가이드 생성 ✨", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

if gemini_btn:
    if not api_key:
        st.error("🚨 화면 왼쪽 사이드바에 Gemini API Key를 먼저 입력해 주세요!")
    elif act_type == "비주도형" and not custom_title:
        st.warning("⚠️ 비주도형 활동의 경우, 후속 활동을 기획하기 위해 반드시 '강의 제목'을 입력해 주셔야 합니다.")
    else:
        # 프롬프트 동적 생성 (핵심 로직)
        if act_type == "주도형":
            prompt = f"""
            당신은 대한민국 최고 수준의 고등학교 진로진학 전문 교사입니다.
            - 학생 희망 학과: {selected_major}
            - 선택한 학교 활동: {selected_act} (학생 주도형 활동)
            - 학생의 세부 관심사: {custom_title if custom_title else '학과 특성에 맞춰 자유롭게 제안'}
            
            요청: 이 학생이 '{selected_major}' 진학을 위해 이 주도형 활동을 '어떻게 기획하고 실행하면 좋을지' 가이드라인을 제시해 주세요.
            단순히 주제만 던져주지 말고, 어떤 책/논문을 찾아보고, 어떤 방식으로 탐구 결과물을 낼지 구체적인 '행동 가이드'를 작성해야 합니다.
            
            아래 마크다운 양식에 맞춰 예쁘게 작성하세요:
            ### 💡 1. [희망 학과] 맞춤형 탐구 주제 제안 (2가지)
            ### 📚 2. 탐구를 위한 구체적인 활동 전개 팁 (자료 조사 방법, 결과물 형태 등)
            ### 🎓 3. 생기부 과세특/창체 기록 예시안 (이 활동을 성공적으로 마쳤을 때 기록될 4~5줄)
            """
        else:
            prompt = f"""
            당신은 대한민국 최고 수준의 고등학교 진로진학 전문 교사입니다.
            - 학생 희망 학과: {selected_major}
            - 선택한 학교 활동: {selected_act} (비주도형/강의 청취형 활동)
            - 수강한 강의/특강 제목: {custom_title}
            
            요청: 이 학생이 '{custom_title}'라는 수동적인 강의/특강을 들은 후, '{selected_major}' 전공과 연계하여 
            '어떤 심화 후속 활동'을 스스로 진행하면 생기부에 주도성을 어필할 수 있을지 가이드라인을 제시해 주세요.
            강연 내용을 전공과 엮어 비판적으로 성찰하거나, 추가 독서, 소논문 작성 등으로 확장하는 전략이 필요합니다.
            
            아래 마크다운 양식에 맞춰 예쁘게 작성하세요:
            ### 🔍 1. 강의 내용과 [희망 학과]의 연결 고리 (강의 내용을 어떻게 전공의 시각으로 바라볼 것인가)
            ### 🏃‍♂️ 2. 주도성 어필을 위한 후속 심화 활동 가이드 (추가로 무엇을 읽고, 어떤 보고서를 써야 할지)
            ### 🎓 3. 생기부 과세특/창체 기록 예시안 (단순 강연 청취가 아닌, 후속 탐구까지 완료했을 때 기록될 4~5줄)
            """
            
        try:
            with st.spinner(f"🌐 제미나이 AI가 '{selected_major}' 전공에 맞춰 실시간으로 가이드를 생성 중입니다..."):
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                
                st.success("✅ 제미나이 AI의 실시간 맞춤형 설계가 완료되었습니다!")
                
                st.markdown(f"""
                <div style="background-color: #FFFFFF; border: 3px solid #FFA500; border-radius: 20px; padding: 40px; box-shadow: 0 10px 25px rgba(0,0,0,0.08);">
                    <h2 style="color: #CA8A04; margin-top: 0; text-align: center; border-bottom: 2px dashed #FFD700; padding-bottom: 20px; margin-bottom: 30px;">
                        🎯 {selected_major} 맞춤형 활동 솔루션
                    </h2>
                    <div style="font-size: 1.1rem; line-height: 1.8; color: #333;">
                        {response.text}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"🚨 제미나이 통신 중 오류가 발생했습니다. API 키가 정확한지 확인해 주세요. (에러 내용: {e})")
