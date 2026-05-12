import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import random  # 💡 클릭 시마다 내용을 다르게 섞어주기 위한 랜덤 모듈

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

# --- 📚 [세부 학과별 특화 DB] 주제와 도서를 대폭 확장 (클릭 시마다 랜덤 추출됨) ---
MAJOR_DB = {
    "반도체공학과": {
        "topics": [
            "차세대 반도체 공정에서의 EUV(극자외선) 노광 기술의 한계와 돌파구 연구",
            "PIM(Processor-In-Memory) 기술을 활용한 AI 연산 효율성 극대화 방안",
            "글로벌 반도체 공급망 재편이 한국 소부장(소재·부품·장비) 산업에 미치는 영향",
            "시스템 반도체 설계를 위한 하드웨어 가속기 구조 분석 및 최적화 탐구",
            "나노 시트(GAA) 구조 도입에 따른 트랜지스터 성능 변화와 전력 효율 연구",
            "메모리 반도체의 고대역폭 메모리(HBM) 기술 발전과 AI 서버 시장 전망"
        ],
        "books": ["반도체 제국의 미래", "칩 워(Chip War)", "물리학을 품은 반도체", "거의 모든 IT의 역사", "엔지니어의 서재"],
        "links": ["한국반도체산업협회", "삼성반도체이야기"]
    },
    "미래자동차공학과": {
        "topics": [
            "자율주행 자동차의 V2X(Vehicle to Everything) 통신 지연 시간 개선 방안",
            "전고체 배터리(Solid-State Battery) 상용화를 위한 기술적 난제와 해결 전략",
            "수소 연료 전지 자동차의 열관리 시스템 효율 향상을 위한 모델링 연구",
            "모빌리티 서비스(MaaS) 도입에 따른 도심 교통 체계 변화 및 탄소 저감 효과",
            "자율주행 알고리즘의 윤리적 판단 기준 설정을 위한 트롤리 딜레마 고찰",
            "전기차 폐배터리 재활용(Recycle) 및 재사용(Reuse)의 경제성 및 환경성 분석"
        ],
        "books": ["미래 자동차 모빌리티", "테슬라 쇼크", "모빌리티의 미래", "자율주행의 시대", "자동차 구조 교과서"],
        "links": ["현대자동차 HMG저널", "한국자동차연구원"]
    },
    "화학공학과": {
        "topics": [
            "탄소 포집 및 활용 기술(CCUS)을 활용한 넷제로(Net Zero) 달성 시나리오 분석",
            "폐플라스틱의 화학적 재활용(열분해) 공정 효율 향상을 위한 촉매 연구",
            "그린 수소 생산을 위한 수전해 기술의 전해질 막 개선 및 경제성 평가",
            "바이오매스 기반 친환경 폴리머 소재의 생분해성 및 물리적 특성 연구",
            "2차 전지 양극재 조성 변화에 따른 에너지 밀도와 안정성 상관관계 분석",
            "정밀 화학 공정에서의 AI 기반 공정 최적화 및 스마트 팩토리 설계 방안"
        ],
        "books": ["화학으로 이루어진 세상", "부분과 전체", "엔트로피", "도구의 인간", "화학의 시대"],
        "links": ["한국화학연구원", "대한화학회"]
    },
    "컴퓨터공학과": {
        "topics": [
            "양자 컴퓨터(Quantum Computing) 알고리즘이 기존 암호 체계에 미치는 영향",
            "마이크로서비스 아키텍처(MSA) 도입 시 데이터 일관성 유지 전략 연구",
            "오픈소스 생태계 기여가 소프트웨어 산업의 기술 혁신에 미치는 파급 효과",
            "엣지 컴퓨팅(Edge Computing)을 활용한 IoT 기기의 데이터 보안 강화 모델",
            "블록체인 기반 탈중앙화 신원증명(DID) 기술의 보안성 및 확장성 분석",
            "대규모 언어 모델(LLM)의 효율적 튜닝을 위한 파라미터 최적화 기법 연구"
        ],
        "books": ["클린 코드", "해커와 화가", "구글 엔지니어는 이렇게 일한다", "알고리즘 산책", "컴퓨터 프로그램의 구조와 해석"],
        "links": ["GitHub", "IEEE Computer Society"]
    },
    "인공지능(AI)학과": {
        "topics": [
            "생성형 AI의 할루시네이션(환각) 방지를 위한 RAG(검색 증강 생성) 기술 연구",
            "설명 가능한 인공지능(XAI) 기법을 활용한 딥러닝 모델의 신뢰성 검증",
            "연합 학습(Federated Learning)을 통한 개인정보 보호형 분산 AI 모델 설계",
            "멀티모달(Multimodal) 학습 기반 시각-언어 데이터 융합 및 분석 최적화",
            "인공지능 알고리즘의 편향성 제거를 위한 데이터셋 구축 가이드라인 설계",
            "강화학습을 활용한 지능형 로봇의 장애물 회피 및 동적 경로 계획 연구"
        ],
        "books": ["인공지능의 시대", "딥러닝 혁명", "AI 마인드", "수학으로 풀어보는 인공지능", "가장 인간적인 인간"],
        "links": ["AI Hub", "한국인공지능학회"]
    },
    "신소재공학과": {
        "topics": [
            "그래핀 기반 나노 복합 소재의 전자파 차폐 효율 및 강도 개선 연구",
            "형상 기억 합금을 활용한 우주 항공 및 의료용 스마트 부품 설계 방안",
            "탄소 나노튜브(CNT)를 적용한 차세대 유연 디스플레이 소자 특성 분석",
            "페로브스카이트 태양전지의 효율 향상과 장기 안정성 확보를 위한 소재 연구",
            "바이오 세라믹 소재를 활용한 인공 뼈 지지체(Scaffold)의 생체 적합성 연구",
            "극저온 환경에서의 고온 초전도체 특성 분석 및 자기 부상 기술 응용"
        ],
        "books": ["사소한 것들의 과학", "신소재의 발견", "재료과학과 공학", "강함의 부드러움", "엔지니어의 시각"],
        "links": ["한국재료연구원", "KCI 학술지"]
    },
    "생명공학과": {
        "topics": [
            "3D 바이오 프린팅 기술을 활용한 맞춤형 인공 장기 제작의 현주소와 과제",
            "개인 맞춤형 정밀 의료를 위한 NGS(차세대 염기서열 분석) 데이터 활용 방안",
            "유전자 가위(CRISPR) 기술을 이용한 희귀 유전 질환 치료의 윤리적 쟁점",
            "합성 생물학을 활용한 미생물 기반 친환경 단백질 소재 생산 공정 최적화",
            "줄기세포 유도 기술을 이용한 퇴행성 뇌 질환 치료 기전 분석 및 연구",
            "디지털 트윈 기반 생체 모델링을 활용한 신약 후보 물질의 독성 예측 연구"
        ],
        "books": ["이기적 유전자", "생명과학, 신에게 도전하다", "바이오해커가 온다", "숨결이 바람 될 때", "호모 데우스"],
        "links": ["생물학연구정보센터(BRIC)", "기초과학연구원(IBS)"]
    },
    "에너지공학과": {
        "topics": [
            "소형 모듈 원자로(SMR)의 안전성 및 경제성 분석과 분산 전원 활용 방안",
            "핵융합 에너지 실현을 위한 초고온 플라즈마 제어 기술의 물리적 원리 탐구",
            "VPP(가상 발전소) 시스템 도입에 따른 재생 에너지 출력 변동성 보완 대책",
            "해상 풍력 발전기의 구조적 안정성 확보를 위한 부유식 구조물 설계 연구",
            "차세대 수소 저장 합금을 이용한 에너지 저장 밀도 및 안전성 향상 연구",
            "스마트 그리드 환경에서의 수요 자원(DR) 관리 알고리즘 및 전력 시장 분석"
        ],
        "books": ["엔트로피", "지속 가능한 에너지", "석유 이후의 세계", "원자력의 진실", "에너지 혁명"],
        "links": ["에너지경제연구원", "한국에너지공단"]
    },
    "산업공학과": {
        "topics": [
            "디지털 트윈(Digital Twin) 기술을 적용한 물류 센터 내 운영 효율 최적화",
            "공급망 관리(SCM)에서의 블록체인 도입이 물류 가시성 및 보안에 미치는 영향",
            "서비스 공학 관점에서의 사용자 경험(UX) 개선을 위한 행동 데이터 분석",
            "제조 현장의 안전 관리를 위한 컴퓨터 비전 기반 실시간 이상 징후 탐지",
            "복잡한 시스템 의사결정을 위한 강화학습 기반 시뮬레이션 모델 설계 연구",
            "생산 계획 및 재고 관리 최적화를 위한 린(Lean) 시스템과 AI 결합 사례"
        ],
        "books": ["경영의 실제", "린 스타트업", "시스템 사고", "생각에 관한 생각", "최적화의 기술"],
        "links": ["대한산업공학회", "산업연구원"]
    }
}

# --- 📚 [계열별 공통 DB] 데이터 보강 ---
TRACK_DB = {
    "인문계열": {
        "topics": ["언어 매체에 나타난 사회적 편견 요소 분석", "고전 문학의 현대적 재해석을 통한 인문학적 가치 탐구", "디지털 인문학: 빅데이터를 활용한 문학 양식 변화 분석", "다문화 시대의 역사 인식의 변화", "철학적 관점에서 본 기술 만능주의 비판"], 
        "books": ["사피엔스", "역사란 무엇인가", "정의란 무엇인가", "호모 데우스"], 
        "links": ["한국연구재단", "KCI 학술지"]
    },
    "사회계열": {
        "topics": ["현대 사회의 플랫폼 독과점이 시장 경제에 미치는 영향 고찰", "디지털 소외 계층을 위한 보편적 복지 정책 제안", "저출산 고령화 사회의 사회 구조적 원인과 제도적 대안", "뉴미디어 시대의 확증 편향과 사회 양극화", "도시 빈민 문제와 주거 환경 개선 정책"], 
        "books": ["넛지", "총, 균, 쇠", "팩트풀니스", "죽은 경제학자의 살아있는 아이디어"], 
        "links": ["통계청", "국회예산정책처"]
    },
    "공학계열": {
        "topics": ["지속 가능한 발전을 위한 친환경 에너지 저장 시스템(ESS) 분석", "스마트 시티 구축을 위한 사물인터넷(IoT) 기술의 활용", "웨어러블 로봇 기술이 산업 현장에 미치는 인간공학적 분석", "생체 모방 공학을 활용한 신소재 개발 연구", "자율주행 기술의 센서 융합 및 오차 보정 알고리즘"], 
        "books": ["거의 모든 IT의 역사", "공학의 눈으로 미래를 설계하라", "엔지니어의 서재", "테크놀로지의 제국"], 
        "links": ["KIST 한국과학기술연구원", "국가과학기술지식정보서비스"]
    }
}

# --- 📚 학교 자체 오프라인 DB 출력 함수 ---
def show_offline_result(track, target_name, selected_act, custom_title, act_type):
    # 1. 데이터 가져오기
    data = MAJOR_DB.get(target_name, TRACK_DB.get(track, TRACK_DB["공학계열"]))
    custom_text = custom_title if custom_title else "관련 심화 주제"
    
    # 💡 2. 매번 버튼을 누를 때마다 다르게 나오도록 무작위(Random)로 3개, 2개씩 섞어서 뽑기
    try:
        selected_topics = random.sample(data['topics'], 3)
    except:
        selected_topics = data['topics'][:3]
        
    try:
        selected_books = random.sample(data['books'], 2)
    except:
        selected_books = data['books'][:2]

    # 💡 3. 활동 팁(조언) 역시 3가지 버전 중 하나를 랜덤 출력!
    lead_advices = [
        f"선택하신 **[{selected_act}]**은 스스로 기획하고 탐구하는 **학생 주도형 활동**입니다. 위의 주제 중 하나를 선택해 본인만의 가설을 세우고, 자료 조사부터 결론 도출까지의 과정을 생기부에 구체적으로 녹여내세요.",
        f"**[{selected_act}]** 활동의 핵심은 '자기주도성'입니다. 제시된 탐구 주제를 바탕으로 스스로 질문을 던지고, 전공 지식을 활용해 문제 해결 과정을 생기부에 깊이 있게 서술해 보세요.",
        f"단순한 참여를 넘어 **[{selected_act}]** 과정에서 마주한 학문적 호기심을 전공과 연결하세요. 위 주제들을 참고하여 스스로 실험이나 조사를 설계하고 주도적으로 결론을 도출하는 것이 중요합니다."
    ]
    
    passive_advices = [
        f"선택하신 **[{selected_act}]**은 강연 청취 중심의 **비주도형 활동**입니다. 수동적인 소감에 그치지 말고, 배운 내용을 바탕으로 위 주제와 연결하여 **'추가 문헌 조사 및 심층 소논문 작성'** 등 후속 탐구를 전개하세요.",
        f"**[{selected_act}]**과 같은 활동은 '후속 심화 탐구'가 생명입니다. 강연이나 실습에서 알게 된 사실을 위의 추천 주제와 엮어 자신만의 심화 보고서를 작성하며 전공에 대한 열정을 증명해 보세요.",
        f"주어진 내용을 그대로 받아들이지 말고, **[{selected_act}]**에서 배운 점을 비판적으로 수용하세요. 위 주제를 바탕으로 RISS 등에서 관련 논문을 찾아 읽고 전공 지식을 능동적으로 확장하는 후속 활동이 필수적입니다."
    ]

    act_advice = random.choice(lead_advices if act_type == "주도형" else passive_advices)

    offline_md = f"""
    ### 💡 1. [{target_name}] 맞춤형 심층 탐구 주제 제안 (랜덤 셔플)
    * **[주제 1]** {selected_topics[0]}
    * **[주제 2]** {selected_topics[1]}
    * **[주제 3]** {selected_topics[2]}
    * **[응용 제안]** '{custom_text}'의 실제 사례를 {target_name} 전공의 기초 이론과 대조하여 분석하는 심층 보고서 작성
    
    ### 🎯 2. [{selected_act}] 구체적인 활동 전개 팁
    * {act_advice}
    * 관련 통계 자료(통계청, KOSIS 등)나 객관적 데이터를 활용하여 주장의 설득력을 높일 것
    
    ### 📖 3. 심화 탐구를 위한 추천 참고 문헌
    * **[추천 도서]** 『{selected_books[0]}』, 『{selected_books[1]}』 외 {target_name} 분야의 융합적 시각을 다룬 대학 교양 수준 입문서 자율 탐독
    * **[논문 검색]** RISS(학술연구정보서비스) 또는 DBpia에서 `"{custom_text}"`, `"{target_name} 융합 연구"` 키워드로 KCI 등재지 논문 리뷰
    
    ### 🔗 4. 전공 탐색 추천 웹사이트
    * 주요 4년제 대학 **{target_name} 학과 홈페이지** 및 커리큘럼(전공 기초/심화 과목) 분석
    * 진로와 연관된 **국가 연구소 (예: KDI, KIST, STEPI 등)** 홈페이지의 최신 연구 동향(Press Release) 확인 및 {data['links'][0]} 참조
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


# ==========================================
# 메인 프로그램 UI
# ==========================================

st.set_page_config(page_title="양명여고 학생부 설계기", page_icon="📋", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    div.row-widget.stRadio > div { flex-direction: column; gap: 10px; }
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
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #FF69B4 0%, #FFA500 100%) !important;
        color: white !important; border: none !important; border-radius: 15px !important;
        font-weight: 900 !important; font-size: 1.4rem !important; padding: 15px 0 !important;
        box-shadow: 0 6px 15px rgba(255, 105, 180, 0.4) !important; transition: all 0.3s ease !important;
        width: 100%; margin-top: 15px !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-5px) !important; box-shadow: 0 10px 25px rgba(255, 215, 0, 0.5) !important;
        background: linear-gradient(135deg, #FFA500 0%, #FF1493 100%) !important;
    }
    div[data-baseweb="input"] > div {
        border: 2.5px solid #FF8C00 !important; background-color: #FFFDF5 !important; border-radius: 10px !important;
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

if st.button("🏠 메인 화면으로 가기", type="secondary"): 
    st.switch_page("app.py")

st.markdown("""
<div style='text-align: center; padding-bottom: 20px;'>
    <h1 class='main-title' style='color: #FF1493; font-weight: 900; font-size: 3.5rem;'>🤖 실시간 학생부 AI 설계기</h1>
    <p class='sub-title' style='color: #64748B; font-size: 1.2rem; margin-top: 10px;'>학과를 선택하면 맞춤 활동을 추천하고, <b>구체적인 활동 전개 방법과 추천 문헌</b>을 짜드립니다.</p>
</div>
""", unsafe_allow_html=True)

# 💡 학과 리스트를 대폭 확장 (공학계열 세분화 및 반도체 추가)
career_data = {
    "인문계열": ["계열 전반 (특정 학과 미정)", "국어국문학과", "영어영문학과", "사학과", "철학과", "심리학과", "중어중문학과", "일어일문학과", "문헌정보학과"],
    "사회계열": ["계열 전반 (특정 학과 미정)", "경영학과", "경제학과", "정치외교학과", "사회복지학과", "미디어커뮤니케이션학과", "행정학과", "국제통상학과", "관광학과"],
    "교육계열": ["계열 전반 (특정 학과 미정)", "초등교육과", "국어교육과", "수학교육과", "영어교육과", "역사교육과", "유아교육과", "특수교육과"],
    "공학계열": ["계열 전반 (특정 학과 미정)", "컴퓨터공학과", "인공지능(AI)학과", "반도체공학과", "신소재공학과", "기계공학과", "전기전자공학과", "화학공학과", "에너지공학과", "미래자동차공학과", "산업공학과", "건축공학과", "항공우주공학과", "생명공학과", "환경공학과"],
    "자연계열": ["계열 전반 (특정 학과 미정)", "수학과", "물리학과", "화학과", "생명과학과", "환경과학과", "지구환경과학과", "통계학과", "천문우주학과"],
    "의약계열": ["계열 전반 (특정 학과 미정)", "의예과", "치의예과", "약학과", "간호학과", "수의예과", "물리치료학과", "임상병리학과"],
    "예체능계열": ["계열 전반 (특정 학과 미정)", "디자인학과", "시각디자인학과", "회화과", "음악학과", "체육학과", "연극영화과", "무용과", "스포츠산업학과"]
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

st.markdown("<div style='background-color: white; padding: 15px 25px; border-radius: 15px; border: 2px solid #FFC0CB; margin-bottom: 20px;'><h3 style='color: #FF1493; margin: 0;'>📝 STEP 1. 계열 및 학과 선택</h3></div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1: selected_track = st.selectbox("🌟 희망 계열", list(career_data.keys()))
with col2: selected_major = st.selectbox("🎓 세부 학과", career_data[selected_track])

target_name = selected_major if selected_major != "계열 전반 (특정 학과 미정)" else f"{selected_track} 전반"

st.markdown("<div style='background-color: white; padding: 15px 25px; border-radius: 15px; border: 2px solid #FFC0CB; margin-top: 30px; margin-bottom: 20px;'><h3 style='color: #FF1493; margin: 0;'>🎯 STEP 2. 활동 선택</h3></div>", unsafe_allow_html=True)
recs = recommended_activities[selected_track]
all_activities = list(activities_db.keys())
display_options = [f"🌟 [전공 추천] {act}" for act in recs] + [f"▶ [다른 활동] {act}" for act in all_activities if act not in recs]
selected_act_display = st.radio("활동 목록", display_options, label_visibility="collapsed")
selected_act = selected_act_display.split("] ")[1]
act_type = activities_db.get(selected_act, "주도형")

st.markdown(f"<div style='background-color: white; padding: 15px 25px; border-radius: 15px; border: 2px solid #FFC0CB; margin-top: 30px; margin-bottom: 20px;'><h3 style='color: #FF1493; margin: 0;'>🔍 STEP 3. 정보 입력 ({act_type})</h3></div>", unsafe_allow_html=True)
if act_type == "비주도형": custom_title = st.text_input("✏️ 수강/참가한 강의/특강/실습의 제목을 입력해 주세요 (필수)", placeholder="예: 반도체 공정 특강, 자율주행 알고리즘 실습")
else: custom_title = st.text_input("💡 (선택) 특별히 다루고 싶은 관심 주제나 읽고 있는 책이 있다면 적어주세요.")

st.write("---")
engine_choice = st.radio("💡 분석 엔진 선택", ["✨ 제미나이 AI 실시간 분석 (추천)", "📚 학교 자체 데이터베이스 (안정적/빠름)"], horizontal=True)

if st.button("🚀 활동 가이드 생성", type="primary"):
    if act_type == "비주도형" and not custom_title: st.warning("⚠️ 강의/실습 제목을 반드시 입력해 주세요.")
    elif "학교 자체" in engine_choice: show_offline_result(selected_track, target_name, selected_act, custom_title, act_type)
    else:
        if not api_key: show_offline_result(selected_track, target_name, selected_act, custom_title, act_type)
        else:
            try:
                with st.spinner(f"🌐 제미나이 AI가 '{target_name}' 진로에 맞춰 설계 중..."):
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(get_best_model(api_key))
                    prompt = f"진로: {target_name}, 활동: {selected_act} ({act_type}), 주제: {custom_title}. 생기부 예시안 출력 금지. 1.탐구주제 3개 2.활동팁 3.참고문헌 4.추천웹사이트 형식으로 작성."
                    response = model.generate_content(prompt)
                    st.success("✅ AI 설계 완료!")
                    st.markdown(f'<div class="result-box" style="background:white; border:3px solid #FFA500; border-radius:20px; padding:30px;"><h2 style="color: #CA8A04; text-align: center; border-bottom: 2px dashed #FFD700; padding-bottom: 20px; margin-bottom: 30px;">🎯 {target_name} 맞춤형 활동 솔루션 (AI)</h2><div style="font-size: 1.1rem; line-height: 1.8; color: #333;">{response.text}</div></div>', unsafe_allow_html=True)
                    components.html("""<script>function printResult() { try { window.parent.print(); } catch (e) { window.print(); } }</script><div style="text-align: center; margin-top: 20px;"><button onclick="printResult()" style="background: linear-gradient(135deg, #10B981, #059669); color: white; border: none; padding: 12px 30px; border-radius: 12px; font-weight: 900; cursor: pointer; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);">🖨️ 결과 화면 PDF 출력</button></div>""", height=100)
            except Exception as e:
                st.warning("⏳ AI 서버 과부하로 학교 자체 데이터베이스로 자동 전환합니다!")
                show_offline_result(selected_track, target_name, selected_act, custom_title, act_type)
