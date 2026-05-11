import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import os

# 1. 페이지 설정
st.set_page_config(page_title="양명여고 학생부 AI 설계기", page_icon="📋", layout="wide")

# 2. 양명여고 전용 화사한 테마 CSS & 📱모바일 반응형 CSS 추가
st.markdown("""
<style>
    /* 기본 화면 스타일 */
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    
    .home-btn > button {
        background-color: #FFFFFF !important; color: #FF1493 !important;
        border: 2px solid #FFC0CB !important; border-radius: 10px !important;
        font-weight: 800 !important; padding: 5px 20px !important;
        transition: all 0.3s ease !important; box-shadow: 0 2px 5px rgba(255, 105, 180, 0.1) !important;
        margin-bottom: 20px !important;
    }
    .home-btn > button:hover { background-color: #FFF0F5 !important; border-color: #FF1493 !important; transform: translateY(-2px) !important; }

    .styled-card {
        background-color: #FFFFFF; border: 3px solid #FFC0CB; border-radius: 20px;
        padding: 30px; box-shadow: 0 8px 20px rgba(255, 105, 180, 0.1); margin-bottom: 25px;
    }

    div.row-widget.stRadio > div { flex-direction: column; gap: 10px; }
    
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

    /* 🖨️ PDF 인쇄 전용 숨김 CSS */
    @media print {
        header { display: none !important; }
        [data-testid="stSidebar"] { display: none !important; }
        .styled-card { display: none !important; }
        .gemini-btn { display: none !important; }
        .home-btn { display: none !important; }
        .stRadio { display: none !important; }
        h1, p { display: none !important; } 
        .stApp { background-color: white !important; }
        .result-box { box-shadow: none !important; border: 1px solid #ccc !important; }
    }

    /* 📱 모바일(스마트폰) 환경 전용 반응형 CSS */
    @media (max-width: 768px) {
        h1.main-title { font-size: 2rem !important; line-height: 1.3 !important; } /* 메인 타이틀 크기 대폭 축소 */
        p.sub-title { font-size: 1rem !important; margin-top: 5px !important; } /* 서브 타이틀 축소 */
        .styled-card { padding: 15px !important; border-radius: 15px !important; } /* 카드 여백 줄이기 */
        .styled-card h3 { font-size: 1.2rem !important; margin-bottom: 10px !important; padding-bottom: 5px !important; } /* 단계별 제목 축소 */
        .gemini-btn > button { font-size: 1.1rem !important; padding: 10px 0 !important; } /* 제미나이 버튼 크기 축소 */
    }
</style>
""", unsafe_allow_html=True)

# API 키 자동 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = None

with st.sidebar:
    st.markdown("### 🤖 제미나이 AI 연결 상태")
    if api_key: st.success("✅ 연결 정상!")
    else: st.error("🚨 API 키 없음!")
    st.markdown("💖 **양명여자고등학교**")

st.markdown('<div class="home-btn">', unsafe_allow_html=True)
if st.button("🏠 메인 화면으로 가기"): st.switch_page("app.py")
st.markdown('</div>', unsafe_allow_html=True)

# 상단 헤더에 클래스 부여 (모바일에서 작아지도록)
st.markdown("""
<div style='text-align: center; padding-bottom: 20px;'>
    <h1 class='main-title' style='color: #FF1493; font-weight: 900; font-size: 3.5rem;'>🤖 실시간 학생부 AI 설계기</h1>
    <p class='sub-title' style='color: #64748B; font-size: 1.2rem; margin-top: 10px;'>계열과 학과를 선택하면 맞춤 활동을 추천하고, AI가 <b>구체적인 활동 전개 방법</b>을 짜드립니다.</p>
</div>
""", unsafe_allow_html=True)

career_data = {
    "인문계열": ["계열 전반 (특정 학과 미정)", "국어국문학과", "영어영문학과", "사학과", "철학과", "심리학과"],
    "사회계열": ["계열 전반 (특정 학과 미정)", "경영학과", "경제학과", "정치외교학과", "사회복지학과", "미디어커뮤니케이션학과", "행정학과"],
    "교육계열": ["계열 전반 (특정 학과 미정)", "초등교육과", "국어교육과", "수학교육과", "영어교육과", "유아교육과", "특수교육과"],
    "공학계열": ["계열 전반 (특정 학과 미정)", "컴퓨터공학과", "인공지능(AI)학과", "기계공학과", "전기전자공학과", "화학공학과"],
    "자연계열": ["계열 전반 (특정 학과 미정)", "수학과", "물리학과", "화학과", "생명과학과", "환경과학과"],
    "의약계열": ["계열 전반 (특정 학과 미정)", "의예과", "치의예과", "한의예과", "약학과", "간호학과"],
    "예체능계열": ["계열 전반 (특정 학과 미정)", "디자인학과", "회화과", "체육학과", "연극영화과"]
}

activities_db = {
    "드림업 프로젝트": "주도형", "학생주도 프로젝트 봉사활동": "주도형", "독서탐구": "주도형",
    "이음 책모임": "주도형", "환경인문독서토론": "주도형", "창의융합 주제탐구 프로젝트": "주도형",
    "스마트폰 이별주간 캠페인": "주도형", "이달의 IB 학습자 상 추천": "주도형",
    "전문직업인 초청 특강": "비주도형", "과천 과학관 실습 프로그램": "비주도형",
    "이공계 진로캠프 (야간 천체 관측)": "비주도형", "금융 리터러시 아카데미": "비주도형"
}

recommended_activities = {
    "인문계열": ["드림업 프로젝트", "독서탐구", "이음 책모임", "전문직업인 초청 특강"],
    "사회계열": ["학생주도 프로젝트 봉사활동", "환경인문독서토론", "전문직업인 초청 특강", "금융 리터러시 아카데미"],
    "교육계열": ["학생주도 프로젝트 봉사활동", "이음 책모임", "스마트폰 이별주간 캠페인", "전문직업인 초청 특강"],
    "공학계열": ["과천 과학관 실습 프로그램", "전문직업인 초청 특강", "드림업 프로젝트", "독서탐구"],
    "자연계열": ["이공계 진로캠프 (야간 천체 관측)", "과천 과학관 실습 프로그램", "환경인문독서토론", "독서탐구"],
    "의약계열": ["학생주도 프로젝트 봉사활동", "독서탐구", "전문직업인 초청 특강", "과천 과학관 실습 프로그램"],
    "예체능계열": ["드림업 프로젝트", "스마트폰 이별주간 캠페인", "이달의 IB 학습자 상 추천", "전문직업인 초청 특강"]
}

st.markdown("<div class='styled-card'>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #FF1493; margin-bottom: 20px; border-bottom: 2px solid #FFC0CB; padding-bottom: 10px;'>📝 STEP 1. 계열 및 학과 선택</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1: selected_track = st.selectbox("🌟 희망 계열", list(career_data.keys()))
with col2: selected_major = st.selectbox("🎓 세부 학과", career_data[selected_track])

target_name = selected_major if selected_major != "계열 전반 (특정 학과 미정)" else f"{selected_track} 전반"

st.markdown(f"<h3 style='color: #FF1493; margin-top: 30px; margin-bottom: 20px; border-bottom: 2px solid #FFC0CB; padding-bottom: 10px;'>🎯 STEP 2. 활동 선택 (추천/기타)</h3>", unsafe_allow_html=True)
recs = recommended_activities[selected_track]
all_activities = list(activities_db.keys())

display_options = []
for act in recs: display_options.append(f"🌟 [전공 추천] {act}")
for act in all_activities:
    if act not in recs:
        if act == "창의융합 주제탐구 프로젝트": display_options.append(f"▶ [다른 활동] {act} (🎓3학년 전용)")
        else: display_options.append(f"▶ [다른 활동] {act}")

selected_act_display = st.radio("활동 목록", display_options, label_visibility="collapsed")

if selected_act_display.startswith("🌟 [전공 추천] "): selected_act = selected_act_display.replace("🌟 [전공 추천] ", "")
else: selected_act = selected_act_display.replace("▶ [다른 활동] ", "").replace(" (🎓3학년 전용)", "")

act_type = activities_db.get(selected_act, "주도형")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='styled-card'>", unsafe_allow_html=True)
st.markdown(f"<h3 style='color: #FF1493; margin-bottom: 20px; border-bottom: 2px solid #FFC0CB; padding-bottom: 10px;'>🔍 STEP 3. 세부 정보 입력 ({act_type})</h3>", unsafe_allow_html=True)

custom_title = ""
if act_type == "비주도형":
    st.warning("이 활동은 강연 청취나 정해진 실습을 수행하는 **[비주도형/강의형]** 활동입니다. 제미나이가 **'강연 후 어떻게 심화 후속 활동을 해야 하는지'** 알려드립니다.")
    custom_title = st.text_input("✏️ 수강한 강의/특강/실습의 제목을 적어주세요 (필수)")
else:
    st.success("이 활동은 스스로 탐구하는 **[학생 주도형]** 활동입니다. 제미나이가 **'어떻게 기획하고 실행해야 하는지'** 가이드를 제공합니다.")
    custom_title = st.text_input("💡 (선택) 특별히 다루고 싶은 관심 주제나 읽고 있는 책이 있다면 적어주세요.")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="gemini-btn">', unsafe_allow_html=True)
gemini_btn = st.button("✨ 제미나이 AI 실시간 활동 가이드 생성 ✨", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
st.write("---")

if gemini_btn:
    if not api_key: st.error("🚨 API 키 에러")
    elif act_type == "비주도형" and not custom_title: st.warning("⚠️ 강의 제목을 입력해 주세요.")
    else:
        if act_type == "주도형":
            prompt = f"진로: {target_name}, 활동: {selected_act}, 관심사: {custom_title}. 활동 기획 방법 가이드라인 작성."
        else:
            prompt = f"진로: {target_name}, 강의제목: {custom_title}, 수동적인 강의 청취 후 심화 후속 활동(소논문 등) 가이드라인 작성."
            
        try:
            with st.spinner(f"🌐 가이드 생성 중..."):
                genai.configure(api_key=api_key)
                models = [m.name.replace("models/", "") for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                chosen = models[0]
                for t in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro", "gemini-pro"]:
                    if t in models: chosen = t; break
                model = genai.GenerativeModel(chosen)
                response = model.generate_content(prompt)
                
                st.success(f"✅ 설계 완료! (모델: {chosen})")
                
                st.markdown(f"""
                <div class="result-box" style="background-color: #FFFFFF; border: 3px solid #FFA500; border-radius: 20px; padding: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.08);">
                    <h2 style="color: #CA8A04; text-align: center; border-bottom: 2px dashed #FFD700; padding-bottom: 15px;">🎯 {target_name} 맞춤형 활동 솔루션</h2>
                    <div style="font-size: 1rem; line-height: 1.6; color: #333;">{response.text}</div>
                </div>
                """, unsafe_allow_html=True)
                
                components.html("""<script>function p(){try{window.parent.print();}catch(e){window.print();}}</script><div style="text-align: center; margin-top: 20px;"><button onclick="p()" style="background: #10B981; color: white; border: none; padding: 12px 20px; border-radius: 12px; font-weight: bold; cursor: pointer;">🖨️ PDF 출력</button></div>""", height=80)

        except Exception as e: st.error(f"🚨 통신 오류: {e}")
