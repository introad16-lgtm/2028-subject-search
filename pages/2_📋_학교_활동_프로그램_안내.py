import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 💡 404 에러 & 과부하 방지용 스마트 캐시 함수 ---
@st.cache_data(ttl=3600)
def get_best_model(api_key):
    try:
        genai.configure(api_key=api_key)
        models = [m.name.replace("models/", "") for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for t in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro", "gemini-pro"]:
            if t in models: return t
        return models[0] if models else "gemini-1.5-flash"
    except: return "gemini-1.5-flash"

# --- 📚 [학교 자체 확장 DB] 데이터 구조 ---
# 학과별로 고유한 활동 가이드를 제공하기 위한 데이터베이스입니다.
OFFLINE_DB = {
    "인문계열": {
        "topics": ["언어 매체에 나타난 성차별적 요소 분석", "고전 문학의 현대적 재해석을 통한 인문학적 가치 탐구", "디지털 인문학: 빅데이터를 활용한 문학 양식 변화 분석"],
        "books": ["언어의 온도", "사피엔스", "역사란 무엇인가"],
        "links": ["국립국어원", "한국연구재단 인문학단", "KCI 학술지"]
    },
    "사회계열": {
        "topics": ["행동경제학 관점에서의 소비자 구매 심리 분석", "플랫폼 독과점이 시장 경제에 미치는 영향 고찰", "디지털 소외 계층을 위한 보편적 복지 정책 제안"],
        "books": ["넛지", "죽은 경제학자의 살아있는 아이디어", "정의란 무엇인가"],
        "links": ["KDI 한국개발연구원", "통계청", "국회예산정책처"]
    },
    "교육계열": {
        "topics": ["에듀테크(Edutech)를 활용한 개별화 교육 모델 설계", "다문화 가정 학생을 위한 통합 교육 프로그램 기획", "IB 교육과정의 국내 공교육 도입 효과 분석"],
        "books": ["에밀", "페다고지", "딥러닝의 미래 교육"],
        "links": ["한국교육과정평가원", "KERIS 교육학술정보원", "EBS 진로진학"]
    },
    "공학계열": {
        "topics": ["생성형 AI의 알고리즘 편향성 완화 방안 탐구", "자율주행 자동차의 윤리적 가이드라인 설계", "지속 가능한 발전을 위한 친환경 에너지 저장 시스템(ESS) 분석"],
        "books": ["인공지능의 시대", "거의 모든 IT의 역사", "엔지니어의 서재"],
        "links": ["KIST 한국과학기술연구원", "IEEE Spectrum", "국가과학기술지식정보서비스"]
    },
    "자연계열": {
        "topics": ["수학적 모델링을 활용한 감염병 확산 경로 예측", "미세 플라스틱이 해양 생태계 먹이사슬에 미치는 영향 조사", "양자 역학의 기초 개념과 나노 기술 응용 사례 연구"],
        "books": ["코스모스", "침묵의 봄", "이기적 유전자"],
        "links": ["기초과학연구원(IBS)", "사이언스온", "Nature Index"]
    },
    "의약계열": {
        "topics": ["디지털 헬스케어 기기를 활용한 만성 질환 관리 방안", "유전자 가위(CRISPR) 기술의 임상 적용과 윤리적 쟁점", "지역별 의료 격차 해소를 위한 공공 의료 시스템 개선 제안"],
        "books": ["숨결이 바람 될 때", "인수공통 모든 전염병의 열쇠", "닥터스Thinking"],
        "links": ["국립보건연구원", "식품의약품안전처", "PubMed"]
    },
    "예체능계열": {
        "topics": ["AI 생성 예술의 저작권 문제와 창의성 논쟁", "스포츠 데이터 분석을 활용한 경기력 향상 방안 연구", "공공 디자인이 도시 범죄 예방(CPTED)에 미치는 효과"],
        "books": ["미술의 역사", "예술의 의미", "스포츠 심리학 개론"],
        "links": ["한국문화예술위원회", "디자인진흥원", "국민체육진흥공단"]
    }
}

def show_offline_result(track, major, act_name, title):
    data = OFFLINE_DB.get(track, OFFLINE_DB["인문계열"])
    target = major if major != "계열 전반 (특정 학과 미정)" else f"{track} 전반"
    custom_text = title if title else "선택 활동"

    offline_md = f"""
    ### 💡 1. [{target}] 맞춤형 탐구 주제 제안 (학교 DB)
    * **[심화 주제 A]** {data['topics'][0]} (활동: {act_name} 연계)
    * **[심화 주제 B]** {data['topics'][1]} (주제: {custom_text} 기반)
    
    ### 📚 2. 탐구를 위한 구체적인 활동 전개 팁
    * 활동 과정에서 발생한 의문점을 **{target}** 관점에서 재정의하고, 논문 검색 사이트에서 키워드 교차 확인
    * 실험이나 조사 데이터가 있다면 차트/그래프로 시각화하여 객관성 확보
    
    ### 📖 3. 심화 탐구를 위한 추천 참고 문헌
    * **[추천 도서]** 『{data['books'][0]}』, 『{data['books'][1]}』 외 전공 관련 도서 1권
    * **[논문 키워드]** `#{target}`, `#{custom_text}`, `#융합연구`
    
    ### 🔗 4. [{target}] 전공 탐색 추천 웹사이트
    * **{data['links'][0]}** 및 관련 정부 출연 연구소 보도자료 활용
    * 주요 대학 **{major}** 학과 안내서 및 커뮤니티 탐방
    """
    
    st.markdown(f"""
    <div class="result-box" style="background-color: #F8FAFC; border: 3px solid #10B981; border-radius: 20px; padding: 40px; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
        <h2 style="color: #059669; margin-top: 0; text-align: center; border-bottom: 2px dashed #34D399; padding-bottom: 20px; margin-bottom: 30px;">
            📚 {target} 활동 솔루션 (학교 자체 DB 모드)
        </h2>
        <div style="font-size: 1.1rem; line-height: 1.8; color: #333;">{offline_md}</div>
    </div>
    """, unsafe_allow_html=True)
    
    components.html("""<script>function printResult() { try { window.parent.print(); } catch (e) { window.print(); } }</script><div style="text-align: center; margin-top: 20px;"><button onclick="printResult()" style="background: linear-gradient(135deg, #10B981, #059669); color: white; border: none; padding: 12px 30px; border-radius: 12px; font-weight: 900; cursor: pointer; box-shadow: 0 4px 10px rgba(16,185, 129, 0.3);">🖨️ 결과 화면 PDF 출력</button></div>""", height=100)

# 1. 페이지 설정
st.set_page_config(page_title="양명여고 학생부 설계기", page_icon="📋", layout="wide")

# 2. 디자인 CSS (안전 렌더링 버전)
st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    div.row-widget.stRadio > div { flex-direction: column; gap: 10px; }
    div.stButton > button[kind="secondary"] { background-color: white !important; color: #FF1493 !important; border: 2px solid #FFC0CB !important; border-radius: 10px !important; font-weight: 800; padding: 5px 20px; }
    div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #FF69B4 0%, #FFA500 100%) !important; color: white !important; border: none !important; border-radius: 15px !important; font-weight: 900; font-size: 1.3rem; padding: 12px 0; width: 100%; margin-top: 15px; }
    div[data-baseweb="input"] > div { border: 2.5px solid #FF8C00 !important; background-color: #FFFDF5 !important; border-radius: 10px !important; }
    @media (max-width: 768px) { .main-title { font-size: 2.2rem !important; } }
</style>
""", unsafe_allow_html=True)

try: api_key = st.secrets["GEMINI_API_KEY"]
except: api_key = None

if st.button("🏠 메인 화면으로 가기", type="secondary"): st.switch_page("app.py")

st.markdown("""<div style='text-align: center; padding-bottom: 20px;'><h1 class='main-title' style='color: #FF1493; font-weight: 900; font-size: 3.5rem;'>🤖 실시간 학생부 AI 설계기</h1><p style='color: #64748B; font-size: 1.2rem;'>학과를 선택하면 <b>탐구 주제와 참고 문헌</b>을 실시간으로 안내합니다.</p></div>""", unsafe_allow_html=True)

# 💡 [학과 데이터 대폭 확장] 총 80여 개 학과 구축
career_data = {
    "인문계열": ["계열 전반 (특정 학과 미정)", "국어국문학과", "영어영문학과", "사학과", "철학과", "심리학과", "중어중문학과", "일어일문학과", "문화인류학과", "언어학과", "문헌정보학과"],
    "사회계열": ["계열 전반 (특정 학과 미정)", "경영학과", "경제학과", "정치외교학과", "사회복지학과", "미디어커뮤니케이션학과", "행정학과", "국제통상학과", "회계학과", "관광학과", "사회학과", "도시행정학과"],
    "교육계열": ["계열 전반 (특정 학과 미정)", "초등교육과", "국어교육과", "영어교육과", "역사교육과", "교육학과", "유아교육과", "특수교육과", "지리교육과", "수학교육과", "과학교육과"],
    "공학계열": ["계열 전반 (특정 학과 미정)", "컴퓨터공학과", "인공지능(AI)학과", "기계공학과", "전기전자공학과", "화학공학과", "신소재공학과", "산업공학과", "소프트웨어공학과", "건축학과", "도시공학과", "항공우주공학과"],
    "자연계열": ["계열 전반 (특정 학과 미정)", "수학과", "물리학과", "화학과", "생명과학과", "환경과학과", "지구환경과학과", "해양학과", "통계학과", "식품영양학과"],
    "의약계열": ["계열 전반 (특정 학과 미정)", "의예과", "치의예과", "한의예과", "약학과", "간호학과", "수의예과", "보건행정학과", "물리치료학과", "의생명공학과", "임상병리학과"],
    "예체능계열": ["계열 전반 (특정 학과 미정)", "시각디자인학과", "산업디자인학과", "패션디자인학과", "회화과", "음악학과", "체육학과", "연극영화과", "무용과", "스포츠산업학과"]
}

activities_db = {
    "드림업 프로젝트": "주도형", "학생주도 프로젝트 봉사활동": "주도형", "독서탐구": "주도형",
    "이음 책모임": "주도형", "환경인문독서토론": "주도형", "창의융합 주제탐구 프로젝트": "주도형",
    "스마트폰 이별주간 캠페인": "주도형", "이달의 IB 학습자 상 추천": "주도형",
    "전문직업인 초청 특강": "비주도형", "과천 과학관 실습 프로그램": "비주도형",
    "이공계 진로캠프 (야간 천체 관측)": "비주도형", "금융 리터러시 아카데미": "비주도형"
}

st.markdown("<div style='background-color: white; padding: 15px 25px; border-radius: 15px; border: 2px solid #FFC0CB; margin-bottom: 20px;'><h3 style='color: #FF1493; margin: 0;'>📝 STEP 1. 계열 및 학과 선택</h3></div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1: selected_track = st.selectbox("🌟 희망 계열", list(career_data.keys()))
with col2: selected_major = st.selectbox("🎓 세부 학과", career_data[selected_track])

st.markdown("<div style='background-color: white; padding: 15px 25px; border-radius: 15px; border: 2px solid #FFC0CB; margin-top: 20px; margin-bottom: 15px;'><h3 style='color: #FF1493; margin: 0;'>🎯 STEP 2. 활동 선택</h3></div>", unsafe_allow_html=True)
recs = ["드림업 프로젝트", "독서탐구", "창의융합 주제탐구 프로젝트", "전문직업인 초청 특강", "학생주도 프로젝트 봉사활동", "이음 책모임", "환경인문독서토론", "스마트폰 이별주간 캠페인", "과천 과학관 실습 프로그램", "금융 리터러시 아카데미"]
selected_act = st.radio("활동 선택", recs, label_visibility="collapsed")
act_type = activities_db.get(selected_act, "주도형")

st.markdown(f"<div style='background-color: white; padding: 15px 25px; border-radius: 15px; border: 2px solid #FFC0CB; margin-top: 20px; margin-bottom: 15px;'><h3 style='color: #FF1493; margin: 0;'>🔍 STEP 3. 정보 입력 ({act_type})</h3></div>", unsafe_allow_html=True)
if act_type == "비주도형": custom_title = st.text_input("✏️ 강연/실습 제목 입력 (필수)", placeholder="예: 빅데이터 특강")
else: custom_title = st.text_input("💡 관심 주제/도서 입력 (선택)", placeholder="예: 행동경제학")

engine_choice = st.radio("💡 분석 엔진 선택", ["✨ AI 실시간 분석 (추천)", "📚 학교 DB (안정적/빠름)"], horizontal=True)

if st.button("🚀 활동 가이드 생성", type="primary"):
    if act_type == "비주도형" and not custom_title: st.warning("⚠️ 제목을 입력해 주세요.")
    elif "학교 DB" in engine_choice: show_offline_result(selected_track, selected_major, selected_act, custom_title)
    else:
        if not api_key: show_offline_result(selected_track, selected_major, selected_act, custom_title)
        else:
            try:
                with st.spinner("🌐 AI 설계 중..."):
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(get_best_model(api_key))
                    prompt = f"진로: {selected_major}, 활동: {selected_act}, 주제: {custom_title}. 생기부 예시는 쓰지 말고, 1.주제제안 2.활동팁 3.참고문헌 4.추천웹사이트 형식으로 작성."
                    response = model.generate_content(prompt)
                    st.success("✅ AI 설계 완료!")
                    st.markdown(f'<div class="result-box" style="background:white; border:3px solid #FFA500; border-radius:20px; padding:30px;">{response.text}</div>', unsafe_allow_html=True)
            except: show_offline_result(selected_track, selected_major, selected_act, custom_title)
