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
            if t in models: return t
        return models[0] if models else "gemini-1.5-flash"
    except: return "gemini-1.5-flash"

# --- 📚 [세부 학과별 특화 DB] 3개 이상의 탐구 주제 ---
MAJOR_DB = {
    "국어국문학과": {
        "topics": ["현대 문학에 나타난 청년 세대의 불안 심리 분석", "한글 창제 원리의 과학성과 언어학적 가치 탐구", "디지털 매체(SNS, 숏폼) 시대의 국어 문법 파괴 현상과 순화 방안", "지역 방언의 소멸 위기와 보존을 위한 문화적 접근"],
        "books": ["언어의 온도", "한국어의 계통"], "links": ["국립국어원", "한국어학회"]
    },
    "심리학과": {
        "topics": ["확증 편향이 디지털 알고리즘과 만났을 때 생기는 사회적 문제", "청소년 우울증 예방을 위한 인지행동치료(CBT)의 학교 적용 방안", "형태주의(Gestalt) 심리학 관점에서 본 시각 디자인 분석", "범죄 심리학 관점에서 본 사이버 폭력 가해자의 심리 기제"],
        "books": ["스키너의 심리상자 열기", "아내를 모자로 착각한 남자"], "links": ["한국심리학회", "마인드포스트"]
    },
    "경영학과": {
        "topics": ["ESG 경영 도입이 기업의 장기적 가치에 미치는 영향 분석", "플랫폼 비즈니스 모델의 수익 구조와 시장 독점 문제 해결 방안", "행동경제학(넛지)을 적용한 긍정적 마케팅 전략 사례 연구", "글로벌 공급망 위기 속에서 한국 기업의 리스크 관리 전략"],
        "books": ["경영의 실제", "마케팅 불변의 법칙"], "links": ["삼성경제연구소(SERI)", "하버드 비즈니스 리뷰"]
    },
    "경제학과": {
        "topics": ["인플레이션 억제를 위한 중앙은행 금리 정책의 딜레마", "가상화폐(암호화폐)의 제도권 편입이 거시 경제에 미치는 영향", "공유 경제 플랫폼이 전통 산업 일자리에 미치는 경제적 파급 효과", "행동경제학 관점에서 본 청년층의 과시적 소비(플렉스) 현상 분석"],
        "books": ["죽은 경제학자의 살아있는 아이디어", "괴짜 경제학"], "links": ["한국은행", "KDI 한국개발연구원"]
    },
    "컴퓨터공학과": {
        "topics": ["양자 컴퓨터(Quantum Computing)의 원리와 기존 암호화 체계의 한계 탐구", "객체 지향 프로그래밍과 함수형 프로그래밍의 패러다임 및 효율성 비교", "클라우드 컴퓨팅 환경에서의 개인정보 보안 최적화 방안", "블록체인 기술을 활용한 공공 기록물 위변조 방지 시스템 설계"],
        "books": ["클린 코드", "컴퓨터 프로그램의 구조와 해석"], "links": ["GitHub", "IEEE Computer Society"]
    },
    "인공지능(AI)학과": {
        "topics": ["생성형 AI(LLM)의 할루시네이션(환각) 현상 원인 및 완화 알고리즘 탐구", "자율주행 자동차의 윤리적 딜레마(트롤리 딜레마) 해결을 위한 가이드라인", "머신러닝 알고리즘에 내재된 데이터 편향성 문제와 공정성 확보 방안", "의료 영상 데이터를 활용한 딥러닝 기반 질병 조기 진단 모델 연구"],
        "books": ["인공지능의 시대", "딥러닝 혁명"], "links": ["AI Hub", "한국인공지능학회"]
    },
    "기계공학과": {
        "topics": ["자율주행차량의 라이다(LiDAR) 센서 한계와 레이더 융합 기술 탐구", "친환경 내연기관 및 수소 연료 전지의 열역학적 효율성 비교", "생체 모방 로봇(Biomimetic Robotics)의 구동 메커니즘 분석", "스마트 팩토리 도입에 따른 제조업 공정 최적화 모델 연구"],
        "books": ["엔지니어의 서재", "기계공학개론"], "links": ["한국기계연구원", "대한기계학회"]
    },
    "생명과학과": {
        "topics": ["유전자 가위(CRISPR-Cas9) 기술의 임상 적용 한계와 생명 윤리적 쟁점", "미세 플라스틱이 해양 생태계 먹이사슬을 거쳐 인체에 미치는 영향", "mRNA 백신의 항원 발현 원리와 차세대 RNA 치료제 전망", "텔로미어(Telomere) 길이에 따른 세포 노화 기전 연구"],
        "books": ["이기적 유전자", "침묵의 봄"], "links": ["생물학연구정보센터(BRIC)", "기초과학연구원(IBS)"]
    },
    "초등교육과": {
        "topics": ["다문화 가정 아동을 위한 이중언어 교육 및 문화 통합 프로그램 기획", "늘봄학교 전면 도입이 초등 공교육 질에 미치는 영향 분석", "에듀테크(Edutech)를 활용한 학습 부진 아동 맞춤형 개별화 교육 방안", "초등학생의 스마트폰 과의존 예방을 위한 자기주도적 미디어 리터러시 교육"],
        "books": ["에밀", "미래 교육의 조건"], "links": ["한국교육과정평가원", "에듀넷"]
    },
    "의예과": {
        "topics": ["디지털 헬스케어 기기를 활용한 만성 질환 관리 시스템의 한계와 개선점", "원격 의료 전면 도입 시 예상되는 의료 서비스의 질적 변화와 법적 쟁점", "인공지능(AI) 기반 신약 개발 가속화가 제약 산업에 미치는 파급 효과", "지역 간 의료 인프라 격차 해소를 위한 공공 의료 시스템 모델 제안"],
        "books": ["숨결이 바람 될 때", "의학의 역사"], "links": ["대한의학회", "PubMed"]
    }
}

# --- 📚 [계열별 공통 DB] 세부 학과가 없을 때 방어용 ---
TRACK_DB = {
    "인문계열": {"topics": ["언어 매체에 나타난 사회적 편견 요소 분석", "고전 문학의 현대적 재해석을 통한 인문학적 가치 탐구", "디지털 인문학: 빅데이터를 활용한 문학 양식 변화 분석"], "books": ["사피엔스", "역사란 무엇인가"], "links": ["한국연구재단", "KCI 학술지"]},
    "사회계열": {"topics": ["현대 사회의 플랫폼 독과점이 시장 경제에 미치는 영향 고찰", "디지털 소외 계층을 위한 보편적 복지 정책 제안", "저출산 고령화 사회의 사회 구조적 원인과 제도적 대안"], "books": ["넛지", "정의란 무엇인가"], "links": ["통계청", "국회예산정책처"]},
    "교육계열": {"topics": ["에듀테크를 활용한 개별화 교육 모델 설계", "IB 교육과정의 국내 공교육 도입 효과 분석", "학업 스트레스 완화를 위한 학교 내 상담 및 멘토링 프로그램"], "books": ["페다고지", "딥러닝의 미래 교육"], "links": ["KERIS 교육학술정보원", "EBS 진로진학"]},
    "공학계열": {"topics": ["지속 가능한 발전을 위한 친환경 에너지 저장 시스템(ESS) 분석", "스마트 시티 구축을 위한 사물인터넷(IoT) 기술의 활용", "웨어러블 로봇 기술이 산업 현장에 미치는 인간공학적 분석"], "books": ["거의 모든 IT의 역사", "공학의 눈으로 미래를 설계하라"], "links": ["KIST", "국가과학기술지식정보서비스"]},
    "자연계열": {"topics": ["수학적 모델링을 활용한 감염병 확산 경로 예측", "기후 변화가 한반도 생물 다양성에 미치는 영향 추적", "양자 역학의 기초 개념과 나노 기술 응용 사례 연구"], "books": ["코스모스", "엔트로피"], "links": ["사이언스온", "Nature Index"]},
    "의약계열": {"topics": ["항생제 내성균(슈퍼박테리아)의 진화 기전과 대체 치료법 탐구", "뇌과학을 활용한 퇴행성 뇌질환 조기 진단 마커 발굴", "제약 공정에서의 품질 관리(QC) 최적화 방안"], "books": ["인수공통 모든 전염병의 열쇠", "닥터스Thinking"], "links": ["국립보건연구원", "식품의약품안전처"]},
    "예체능계열": {"topics": ["AI 생성 예술의 저작권 문제와 창의성 논쟁", "스포츠 데이터 분석을 활용한 경기력 향상 방안 연구", "공공 디자인이 도시 범죄 예방(CPTED)에 미치는 효과"], "books": ["미술의 역사", "스포츠 심리학 개론"], "links": ["한국문화예술위원회", "디자인진흥원"]}
}

def show_offline_result(track, major, act_name, title):
    # 💡 세부 학과 데이터를 먼저 찾고, 없으면 계열 데이터를 가져옵니다.
    data = MAJOR_DB.get(major, TRACK_DB.get(track, TRACK_DB["인문계열"]))
    target = major if major != "계열 전반 (특정 학과 미정)" else f"{track} 전반"
    custom_text = title if title else "관심 주제"

    offline_md = f"""
    ### 💡 1. [{target}] 맞춤형 심층 탐구 주제 제안 (최소 3가지)
    * **[주제 1]** {data['topics'][0]} (활동 연계)
    * **[주제 2]** {data['topics'][1]}
    * **[주제 3]** {data['topics'][2]}
    * **[자율 제안]** '{custom_text}'와 {target} 전공 이론을 접목한 비교 분석 보고서 작성
    
    ### 📚 2. 탐구를 위한 구체적인 활동 전개 팁
    * 활동 과정에서 발생한 의문점을 **{target}** 관점에서 재정의하고, 교과 선생님과 멘토링 진행
    * 탐구한 내용을 단순 요약하지 말고, 시각적 차트(데이터)를 활용하여 객관적인 문제 해결력 어필
    
    ### 📖 3. 심화 탐구를 위한 추천 참고 문헌
    * **[추천 도서]** 『{data['books'][0]}』, 『{data['books'][1]}』 외 {target} 관련 대학 교양 입문서
    * **[논문 검색]** RISS(학술연구정보서비스)에서 `"{target}"`, `"{custom_text}"`, `"융합 연구"` 키워드로 검색
    
    ### 🔗 4. [{target}] 전공 탐색 추천 웹사이트
    * **{data['links'][0]}** 및 관련 보도자료 탐독
    * **{data['links'][1]}** 홈페이지의 최신 연구/학술 동향 파악
    """
    
    st.markdown(f"""
    <div class="result-box" style="background-color: #FFFFFF; border: 3px solid #FFA500; border-radius: 20px; padding: 40px; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
        <h2 style="color: #CA8A04; margin-top: 0; text-align: center; border-bottom: 2px dashed #FFD700; padding-bottom: 20px; margin-bottom: 30px;">
            📚 {target} 활동 솔루션 (학교 자체 DB)
        </h2>
        <div style="font-size: 1.1rem; line-height: 1.8; color: #1E293B;">{offline_md}</div>
    </div>
    """, unsafe_allow_html=True)
    
    components.html("""<script>function printResult() { try { window.parent.print(); } catch (e) { window.print(); } }</script><div style="text-align: center; margin-top: 20px;"><button onclick="printResult()" style="background: linear-gradient(135deg, #FF69B4, #FFA500); color: white; border: none; padding: 12px 30px; border-radius: 12px; font-weight: 900; cursor: pointer; box-shadow: 0 4px 10px rgba(255,105, 180, 0.3);">🖨️ 결과 화면 PDF 출력</button></div>""", height=100)

# 1. 페이지 설정
st.set_page_config(page_title="양명여고 학생부 설계기", page_icon="📋", layout="wide")

# 2. 디자인 CSS (화사한 핑크/옐로우/오렌지 양명여고 전용 테마 복구)
st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    div.row-widget.stRadio > div { flex-direction: column; gap: 10px; }
    
    /* 서브 버튼 (홈 가기 등) */
    div.stButton > button[kind="secondary"] { background-color: white !important; color: #FF1493 !important; border: 2px solid #FFC0CB !important; border-radius: 10px !important; font-weight: 800; padding: 5px 20px; box-shadow: 0 2px 5px rgba(255, 105, 180, 0.1); }
    div.stButton > button[kind="secondary"]:hover { background-color: #FFF0F5 !important; border-color: #FF1493 !important; transform: translateY(-2px); }
    
    /* 메인 분석 버튼 */
    div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #FF69B4 0%, #FFA500 100%) !important; color: white !important; border: none !important; border-radius: 15px !important; font-weight: 900; font-size: 1.3rem; padding: 12px 0; width: 100%; margin-top: 15px; box-shadow: 0 6px 15px rgba(255, 105, 180, 0.4); }
    div.stButton > button[kind="primary"]:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(255, 215, 0, 0.5); background: linear-gradient(135deg, #FFA500 0%, #FF1493 100%) !important; }
    
    /* 입력창 오렌지 포인트 */
    div[data-baseweb="input"] > div { border: 2.5px solid #FF8C00 !important; background-color: #FFFDF5 !important; border-radius: 10px !important; }
    div[data-baseweb="input"] > div:focus-within { border-color: #FF1493 !important; box-shadow: 0 0 10px rgba(255, 20, 147, 0.3) !important; }

    @media print {
        header, [data-testid="stSidebar"], .stButton, .stRadio, h1, p { display: none !important; } 
        .stApp { background-color: white !important; }
        .result-box { box-shadow: none !important; border: 1px solid #E2E8F0 !important; }
    }
    @media (max-width: 768px) { .main-title { font-size: 2.2rem !important; } }
</style>
""", unsafe_allow_html=True)

try: api_key = st.secrets["GEMINI_API_KEY"]
except: api_key = None

with st.sidebar:
    st.markdown("### 🤖 시스템 연결 상태")
    if api_key: st.success("✅ AI 서버 연결 정상!")
    else: st.warning("⚠️ 오프라인 DB 모드 동작 중")
    st.markdown("💖 **양명여자고등학교 진로진학부**")

if st.button("🏠 메인 화면으로 가기", type="secondary"): st.switch_page("app.py")

st.markdown("""<div style='text-align: center; padding-bottom: 20px;'><h1 class='main-title' style='color: #FF1493; font-weight: 900; font-size: 3.5rem;'>🤖 실시간 학생부 AI 설계기</h1><p style='color: #64748B; font-size: 1.2rem;'>세부 학과를 선택하면 <b>3가지 이상의 심층 탐구 주제와 문헌</b>을 실시간으로 설계합니다.</p></div>""", unsafe_allow_html=True)

# 💡 학과 리스트 유지
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
target_name = selected_major if selected_major != "계열 전반 (특정 학과 미정)" else f"{selected_track} 전반"

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
                    prompt = f"진로: {target_name}, 활동: {selected_act}, 주제: {custom_title}. 생기부 예시는 쓰지 말고, 1.[{target_name}] 맞춤형 탐구 주제 제안(최소 3가지 이상 상세히) 2.활동팁 3.참고문헌 4.추천웹사이트 형식으로 작성."
                    response = model.generate_content(prompt)
                    st.success("✅ AI 설계 완료!")
                    st.markdown(f'<div class="result-box" style="background:white; border:3px solid #FFA500; border-radius:20px; padding:30px;"><h2 style="color: #CA8A04; text-align: center; border-bottom: 2px dashed #FFD700; padding-bottom: 20px; margin-bottom: 30px;">🎯 {target_name} 맞춤형 활동 솔루션 (AI)</h2>{response.text}</div>', unsafe_allow_html=True)
            except: show_offline_result(selected_track, selected_major, selected_act, custom_title)
