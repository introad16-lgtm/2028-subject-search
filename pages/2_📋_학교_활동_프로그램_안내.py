import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# --- 💡 스마트 캐시 함수 ---
@st.cache_data(ttl=3600)
def get_best_model(api_key):
    try:
        genai.configure(api_key=api_key)
        models = [m.name.replace("models/", "") for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for t in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro", "gemini-pro"]:
            if t in models: 
                return t
        return models[0] if models else "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

# --- 📚 학교 자체 오프라인 DB 출력 함수 ---
def show_offline_result(target_name, selected_act, custom_title):
    custom_text = custom_title if custom_title else "관련 심화 주제"
    
    offline_md = f"""
    ### 💡 1. [{target_name}] 맞춤형 탐구 주제 제안 (학교 DB)
    * **[현장-이론 교차 분석]** 학교 활동 중 다룬 **[{custom_text}]**의 실제 사례를 {target_name} 전공의 기초 이론과 대조하여 분석하는 심층 보고서 작성
    * **[사회적 딜레마 고찰]** **[{custom_text}]** 과정에서 파생될 수 있는 윤리적/구조적 문제점을 파악하고, 이를 극복하기 위한 정책적 대안 제시
    
    ### 📚 2. 탐구를 위한 구체적인 활동 전개 팁
    * 단편적인 소감문 작성을 지양하고, **[{custom_text}]**에 대한 질문을 최소 3가지 이상 만들어 교과 선생님이나 전문가에게 질의응답 시도
    * 관련 통계 자료(통계청, KOSIS 등)나 객관적 데이터를 활용하여 주장의 설득력을 높일 것
    
    ### 📖 3. 심화 탐구를 위한 추천 참고 문헌
    * **[추천 도서]** {target_name} 분야의 융합적 시각을 다룬 대학 교양 수준의 입문서 1~2권 자율 탐독
    * **[논문 검색]** RISS(학술연구정보서비스) 또는 DBpia에서 `"{custom_text} 전망"`, `"{target_name} 융합 연구"` 키워드로 KCI 등재지 논문 리뷰
    
    ### 🔗 4. 전공 탐색 추천 웹사이트
    * 주요 4년제 대학 **{target_name} 학과 홈페이지** 및 커리큘럼(전공 기초/심화 과목) 분석
    * 진로와 연관된 **국가 연구소 (예: KDI, KIST, STEPI 등)** 홈페이지의 최신 연구 동향(Press Release) 확인
    """
    
    st.markdown(f"""
    <div class="result-box" style="background-color: #F8FAFC; border: 3px solid #10B981; border-radius: 20px; padding: 40px; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
        <h2 style="color: #059669; margin-top: 0; text-align: center; border-bottom: 2px dashed #34D399; padding-bottom: 20px; margin-bottom: 30px;">
            📚 {target_name} 맞춤형 활동 솔루션 (학교 자체 DB)
        </h2>
        <div style="font-size: 1.1rem; line-height: 1.8; color: #333;">
            {offline_md}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    components.html("""
    <script>function printResult() { try { window.parent.print(); } catch (e) { window.print(); } }</script>
    <div style="text-align: center; margin-top: 20px;">
        <button onclick="printResult()" style="background: linear-gradient(135deg, #10B981, #059669); color: white; border: none; padding: 12px 30px; border-radius: 12px; font-weight: 900; font-size: 1.1rem; cursor: pointer; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3); transition: all 0.2s;">
            🖨️ 결과 화면 PDF로 출력하기 (인쇄)
        </button>
    </div>
    """, height=100)


# 1. 페이지 설정
st.set_page_config(page_title="양명여고 학생부 설계기", page_icon="📋", layout="wide")

# 2. 에러 원천 차단형 안전 CSS
st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    
    div.row-widget.stRadio > div { flex-direction: column; gap: 10px; }

    /* 🏠 홈 버튼 스타일 (Secondary Button) */
    div.stButton > button[kind="secondary"] {
        background-color: #FFFFFF !important; color: #FF1493 !important;
        border: 2px solid #FFC0CB !important; border-radius: 10px !important;
        font-weight: 800 !important; padding: 5px 20px !important;
        transition: all 0.3s ease !important; box-shadow: 0 2px 5px rgba(255, 105, 180, 0.1) !important;
        margin-bottom: 20px !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #FFF0F5 !important; border-color: #FF1493 !important; transform: translateY(-2px) !important;
    }

    /* 🚀 AI 분석 메인 버튼 스타일 (Primary Button) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #FF69B4 0%, #FFA500 100%) !important;
        color: white !important; border: none !important; border-radius: 15px !important;
        font-weight: 900 !important; font-size: 1.4rem !important; padding: 15px 0 !important;
        box-shadow: 0 6px 15px rgba(255, 105, 180, 0.4) !important; transition: all 0.3s ease !important;
        width: 100%;
        margin-top: 15px !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-5px) !important; box-shadow: 0 10px 25px rgba(255, 215, 0, 0.5) !important;
        background: linear-gradient(135deg, #FFA500 0%, #FF1493 100%) !important;
    }

    /* ✨ 입력창 오렌지 테두리 강조 CSS */
    div[data-baseweb="input"] > div {
        border: 2.5px solid #FF8C00 !important;
        background-color: #FFFDF5 !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="input"] > div:focus-within {
        border-color: #FF1493 !important;
        box-shadow: 0 0 10px rgba(255, 20, 147, 0.3) !important;
    }

    @media print {
        header, [data-testid="stSidebar"], .stButton, .stRadio, h1, p { display: none !important; } 
        .stApp { background-color: white !important; }
        .result-box { box-shadow: none !important; border: 1px solid #ccc !important; }
    }

    @media (max-width: 768px) {
        h1.main-title { font-size: 2rem !important; line-height: 1.3 !important; }
        p.sub-title { font-size: 1rem !important; margin-top: 5px !important; }
        div.stButton > button[kind="primary"] { font-size: 1.1rem !important; padding: 10px 0 !important; }
    }
</style>
""", unsafe_allow_html=True)

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = None

with st.sidebar:
    st.markdown("### 🤖 시스템 연결 상태")
    if api_key: st.success("✅ AI 서버 연결 정상!")
    else: st.warning("⚠️ 학교 오프라인 DB 모드 동작 중")
    st.markdown("💖 **양명여자고등학교 진로진학부**")

# 홈 버튼 (Secondary 타입으로 설정하여 위 CSS 적용)
if st.button("🏠 메인 화면으로 가기", type="secondary"): 
    st.switch_page("app.py")

st.markdown("""
<div style='text-align: center; padding-bottom: 20px;'>
    <h1 class='main-title' style='color: #FF1493; font-weight: 900; font-size: 3.5rem;'>🤖 실시간 학생부 AI 설계기</h1>
    <p class='sub-title' style='color: #64748B; font-size: 1.2rem; margin-top: 10px;'>계열과 학과를 선택하면 맞춤 활동을 추천하고, <b>구체적인 활동 전개 방법과 추천 문헌</b>을 짜드립니다.</p>
</div>
""", unsafe_allow_html=True)

career_data = {
    "인문계열": ["계열 전반 (특정 학과 미정)", "국어국문학과", "영어영문학과", "사학과", "철학과", "심리학과"],
    "사회계열": ["계열 전반 (특정 학과 미정)", "경영학과", "경제학과", "정치외교학과", "사회복지학과", "미디어커뮤니케이션학과", "행정학과"],
    "교육계열": ["계열 전반 (특정 학과 미정)", "초등교육과", "국어교육과", "수학교육과", "영어교육과"],
    "공학계열": ["계열 전반 (특정 학과 미정)", "컴퓨터공학과", "인공지능(AI)학과", "기계공학과", "전기전자공학과", "화학공학과"],
    "자연계열": ["계열 전반 (특정 학과 미정)", "수학과", "물리학과", "화학과", "생명과학과", "환경과학과"],
    "의약계열": ["계열 전반 (특정 학과 미정)", "의예과", "치의예과", "약학과", "간호학과", "수의예과"],
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
    "교육계열": ["학생주도 프로젝트 봉사활동", "이음 책모임", "스마트폰 이별주간 캠페인"],
    "공학계열": ["과천 과학관 실습 프로그램", "전문직업인 초청 특강", "드림업 프로젝트"],
    "자연계열": ["이공계 진로캠프 (야간 천체 관측)", "과천 과학관 실습 프로그램", "환경인문독서토론"],
    "의약계열": ["학생주도 프로젝트 봉사활동", "독서탐구", "과천 과학관 실습 프로그램"],
    "예체능계열": ["드림업 프로젝트", "스마트폰 이별주간 캠페인", "전문직업인 초청 특강"]
}

# --- STEP 1 ---
st.markdown("""
<div style='background-color: white; padding: 15px 25px; border-radius: 15px; border: 2px solid #FFC0CB; box-shadow: 0 4px 10px rgba(255, 105, 180, 0.05); margin-bottom: 20px;'>
    <h3 style='color: #FF1493; margin: 0; padding-bottom: 5px;'>📝 STEP 1. 계열 및 학과 선택</h3>
</div>
""", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1: selected_track = st.selectbox("🌟 희망 계열", list(career_data.keys()))
with col2: selected_major = st.selectbox("🎓 세부 학과", career_data[selected_track])

target_name = selected_major if selected_major != "계열 전반 (특정 학과 미정)" else f"{selected_track} 전반"

# --- STEP 2 ---
st.markdown("""
<div style='background-color: white; padding: 15px 25px; border-radius: 15px; border: 2px solid #FFC0CB; box-shadow: 0 4px 10px rgba(255, 105, 180, 0.05); margin-top: 30px; margin-bottom: 20px;'>
    <h3 style='color: #FF1493; margin: 0; padding-bottom: 5px;'>🎯 STEP 2. 활동 선택 (추천/기타)</h3>
</div>
""", unsafe_allow_html=True)
recs = recommended_activities[selected_track]
all_activities = list(activities_db.keys())

display_options = []
for act in recs: display_options.append(f"🌟 [전공 추천] {act}")
for act in all_activities:
    if act not in recs:
        if act == "창의융합 주제탐구 프로젝트": display_options.append(f"▶ [다른 활동] {act} (🎓3학년 전용)")
        else: display_options.append(f"▶ [다른 활동] {act}")

selected_act_display = st.radio("활동 목록", display_options, label_visibility="collapsed")
selected_act = selected_act_display.split("] ")[1].replace(" (🎓3학년 전용)", "")
act_type = activities_db.get(selected_act, "주도형")

# --- STEP 3 ---
st.markdown(f"""
<div style='background-color: white; padding: 15px 25px; border-radius: 15px; border: 2px solid #FFC0CB; box-shadow: 0 4px 10px rgba(255, 105, 180, 0.05); margin-top: 30px; margin-bottom: 20px;'>
    <h3 style='color: #FF1493; margin: 0; padding-bottom: 5px;'>🔍 STEP 3. 세부 정보 입력 ({act_type})</h3>
</div>
""", unsafe_allow_html=True)

custom_title = ""
if act_type == "비주도형":
    st.warning("이 활동은 강연 청취나 정해진 실습을 수행하는 **[비주도형/강의형]** 활동입니다. 강연 후 심화 후속 활동 방향을 알려드립니다.")
    custom_title = st.text_input("✏️ 수강/참가한 강의/특강/실습의 제목을 입력해 주세요 (필수)", placeholder="예: 화학, AI 윤리, 분광기 실습")
else:
    st.success("이 활동은 스스로 탐구하는 **[학생 주도형]** 활동입니다. 기획하고 실행하는 가이드를 제공합니다.")
    custom_title = st.text_input("💡 (선택) 특별히 다루고 싶은 관심 주제나 읽고 있는 책이 있다면 적어주세요.")

st.write("---")
engine_choice = st.radio(
    "💡 분석 엔진 선택", 
    ["✨ 제미나이 AI 실시간 분석 (추천/창의적안)", "📚 학교 자체 데이터베이스 (빠름/안정적)"], 
    horizontal=True
)

# 분석 버튼 (Primary 타입으로 설정하여 위 CSS 적용)
gemini_btn = st.button("🚀 선택한 엔진으로 활동 가이드 생성", type="primary", use_container_width=True)
st.write("---")

if gemini_btn:
    if act_type == "비주도형" and not custom_title: 
        st.warning("⚠️ 강의/실습 제목을 반드시 입력해 주셔야 맞춤형 가이드가 나옵니다.")
    else:
        if "학교 자체" in engine_choice:
            st.success("✅ 학교 자체 데이터베이스 엔진으로 신속하게 결과를 생성했습니다!")
            show_offline_result(target_name, selected_act, custom_title)
            
        else:
            if not api_key:
                st.warning("⏳ AI 서버 키가 설정되지 않아 **[학교 자체 데이터베이스]** 모드로 자동 전환합니다!")
                show_offline_result(target_name, selected_act, custom_title)
            else:
                prompt = f"""
                당신은 고등학교 진로진학 전문 교사입니다.
                - 진로/학과: {target_name}
                - 활동: {selected_act} ({act_type})
                - 관심사/주제: {custom_title if custom_title else '자유 제안'}
                
                이 학생이 '{target_name}' 진학을 위해 이 활동을 어떻게 기획/실행/후속 심화할지 가이드라인을 작성하세요.
                주의: 생기부 기록 예시안은 절대 출력하지 마세요.
                
                양식:
                ### 💡 1. [{target_name}] 맞춤형 탐구 주제 제안 (2가지)
                ### 📚 2. 탐구를 위한 구체적인 활동 전개 팁
                ### 📖 3. 심화 탐구를 위한 추천 참고 문헌 (책 2권 및 RISS 키워드)
                ### 🔗 4. [{target_name}] 전공 탐색 추천 웹사이트
                """
                try:
                    with st.spinner(f"🌐 제미나이 AI가 실시간으로 가이드를 창작 중입니다..."):
                        chosen_model = get_best_model(api_key)
                        model = genai.GenerativeModel(chosen_model)
                        response = model.generate_content(prompt)
                        
                        st.success(f"✅ 제미나이 AI가 창의적 설계를 완료했습니다! (모델: {chosen_model})")
                        st.markdown(f"""
                        <div class="result-box" style="background-color: #FFFFFF; border: 3px solid #FFA500; border-radius: 20px; padding: 40px; box-shadow: 0 10px 25px rgba(0,0,0,0.08);">
                            <h2 style="color: #CA8A04; margin-top: 0; text-align: center; border-bottom: 2px dashed #FFD700; padding-bottom: 20px; margin-bottom: 30px;">
                                🎯 {target_name} 맞춤형 활동 솔루션 (AI)
                            </h2>
                            <div style="font-size: 1.1rem; line-height: 1.8; color: #333;">{response.text}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        components.html("""<script>function printResult() { try { window.parent.print(); } catch (e) { window.print(); } }</script><div style="text-align: center; margin-top: 20px;"><button onclick="printResult()" style="background: linear-gradient(135deg, #10B981, #059669); color: white; border: none; padding: 12px 30px; border-radius: 12px; font-weight: 900; cursor: pointer; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);">🖨️ 결과 화면 PDF 출력</button></div>""", height=100)

                except Exception as e:
                    error_msg = str(e).lower()
                    if "429" in error_msg or "quota" in error_msg or "exhausted" in error_msg:
                        st.warning("⏳ 현재 다른 친구들이 AI를 많이 사용 중입니다. **[학교 자체 데이터베이스]** 모드로 즉시 전환하여 결과를 보여드립니다! 💖")
                        show_offline_result(target_name, selected_act, custom_title)
                    else:
                        st.error("🚨 알 수 없는 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.")
