import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import random  # 💡 클릭 시마다 내용을 다르게 섞어주기 위한 랜덤 모듈 추가

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
    "국어국문학과": {
        "topics": [
            "K-콘텐츠 확산에 따른 한국어 교육 모델 및 현지화 전략 설계", 
            "디지털 매체(숏폼, SNS) 시대의 국어 문법 파괴 현상과 순화 방안", 
            "고전문학의 메타버스 플랫폼 구현 방안과 인문학적 가치 탐구",
            "다문화 사회 진입에 따른 이중언어 아동을 위한 맞춤형 국어 교육 정책",
            "현대시와 대중가요 가사의 문학적 상관관계 분석 및 서정성 연구",
            "지역 방언의 소멸 위기와 보존을 위한 문화적/제도적 접근 방안"
        ],
        "books": ["언어의 온도", "한국어의 계통", "생각하는 힘, 노자 인문학", "말의 그릇", "우리말 어원 사전"], 
        "links": ["국립국어원", "한국어학회"]
    },
    "심리학과": {
        "topics": [
            "확증 편향이 디지털 알고리즘과 만났을 때 생기는 사회적 문제와 대안", 
            "청소년 우울증 예방을 위한 학교 내 인지행동치료(CBT) 적용 방안", 
            "범죄 심리학 관점에서 본 사이버 폭력 가해자의 심리 기제",
            "가스라이팅과 그루밍 범죄의 심리학적 메커니즘 분석",
            "현대인의 완벽주의와 번아웃 증후군의 상관관계 및 회복 탄력성",
            "집단 극화 현상이 팬덤 문화와 마녀사냥에 미치는 영향"
        ],
        "books": ["스키너의 심리상자 열기", "아내를 모자로 착각한 남자", "생각에 관한 생각", "프레임", "설득의 심리학"], 
        "links": ["한국심리학회", "마인드포스트"]
    },
    "경영학과": {
        "topics": [
            "ESG 경영 도입이 기업의 장기적 재무 가치에 미치는 실증적 분석", 
            "플랫폼 비즈니스 모델의 시장 독점 문제와 벤처 생태계 조성 방안", 
            "행동경제학(넛지)을 적용한 긍정적 마케팅 및 소비 촉진 사례 연구",
            "구독 경제(Subscription) 모델의 수익성 다각화 전략 및 한계점",
            "엔터테인먼트 산업의 글로벌 마케팅 성공 요인과 현지화 전략",
            "스타트업의 데스밸리(Death Valley) 극복을 위한 재무 및 조직 관리 전략"
        ],
        "books": ["경영의 실제", "마케팅 불변의 법칙", "트렌드 코리아", "블루오션 전략", "원씽(The One Thing)"], 
        "links": ["삼성경제연구소(SERI)", "하버드 비즈니스 리뷰"]
    },
    "경제학과": {
        "topics": [
            "글로벌 인플레이션 억제를 위한 중앙은행 금리 정책의 딜레마 분석", 
            "가상화폐(암호화폐)의 제도권 편입이 거시 경제에 미치는 영향", 
            "공유 경제 플랫폼이 전통 산업 일자리에 미치는 경제적 파급 효과",
            "기본소득 제도의 경제적 타당성과 근로 의욕 변화 모델링",
            "보호무역주의 부활이 한국 수출 경제에 미치는 타격과 대응책",
            "탄소 배출권 거래제의 경제적 실효성 및 시장 메커니즘 분석"
        ],
        "books": ["죽은 경제학자의 살아있는 아이디어", "괴짜 경제학", "자본주의", "넛지", "국부론"], 
        "links": ["한국은행", "KDI 한국개발연구원"]
    },
    "컴퓨터공학과": {
        "topics": [
            "양자 컴퓨팅(Quantum Computing)의 원리와 기존 암호화 체계의 한계 탐구", 
            "클라우드 컴퓨팅 환경에서의 개인정보 보안 최적화 및 분산 처리 방안", 
            "오픈소스 생태계가 소프트웨어 산업 발전에 미치는 영향 및 기여 방안",
            "블록체인을 활용한 전자 투표 시스템의 무결성 검증 및 한계점",
            "엣지 컴퓨팅(Edge Computing)을 통한 자율주행 데이터 응답 속도 개선 사례",
            "생체 인식 기술의 발전이 야기하는 프라이버시 침해 문제와 보안 모델"
        ],
        "books": ["클린 코드", "컴퓨터 프로그램의 구조와 해석", "알고리즘 산책", "해커와 화가", "구글 엔지니어는 이렇게 일한다"], 
        "links": ["GitHub", "IEEE Computer Society"]
    },
    "인공지능(AI)학과": {
        "topics": [
            "생성형 AI(LLM)의 할루시네이션(환각) 현상 원인 및 완화 알고리즘 탐구", 
            "머신러닝 알고리즘에 내재된 데이터 편향성 문제와 공정성 확보 방안", 
            "의료 영상 데이터를 활용한 딥러닝 기반 질병 조기 진단 모델 연구",
            "자연어 처리(NLP)를 활용한 혐오 표현 탐지 및 감정 분석 모델 설계",
            "강화학습을 적용한 스마트 시티 교통 제어 시스템 최적화 방안",
            "딥페이크(Deepfake) 탐지 AI 모델의 원리와 기술적 한계 돌파 방안"
        ],
        "books": ["인공지능의 시대", "딥러닝 혁명", "AI 마인드", "수학으로 풀어보는 인공지능", "인공지능과 뇌"], 
        "links": ["AI Hub", "한국인공지능학회"]
    },
    "생명과학과": {
        "topics": [
            "유전자 가위(CRISPR-Cas9) 기술의 임상 적용 한계와 생명 윤리적 쟁점", 
            "미세 플라스틱이 해양 생태계 먹이사슬을 거쳐 인체에 미치는 면역학적 영향", 
            "mRNA 백신의 항원 발현 원리와 차세대 RNA 표적 치료제 전망",
            "마이크로바이옴(장내 미생물)이 인간의 면역 및 신경계에 미치는 영향",
            "합성 생물학을 이용한 인공 세포 제작의 현주소와 윤리적 딜레마",
            "기후 변화가 유발하는 식물 병해충 확산 메커니즘과 식량 안보"
        ],
        "books": ["이기적 유전자", "침묵의 봄", "생명과학, 신에게 도전하다", "코스모스", "바이오해커가 온다"], 
        "links": ["생물학연구정보센터(BRIC)", "기초과학연구원(IBS)"]
    },
    "의예과": {
        "topics": [
            "디지털 치료제(DTx)의 임상적 유효성 검증과 제도적 한계 분석", 
            "인공지능(AI) 기반 신약 개발 가속화가 제약 산업에 미치는 파급 효과", 
            "초고령 사회 대비 지역 간 의료 인프라 격차 해소를 위한 공공 의료 모델 제안",
            "수면 부족이 청소년의 뇌 인지 기능 및 발달에 미치는 의학적 분석",
            "항암제 내성 발생 원인과 다제내성 극복을 위한 표적 치료 방안",
            "플라시보 효과의 뇌신경학적 메커니즘 및 임상 적용의 윤리성 연구"
        ],
        "books": ["숨결이 바람 될 때", "의학의 역사", "아프다, 의사도", "질병의 탄생", "아내를 모자로 착각한 남자"], 
        "links": ["대한의학회", "PubMed"]
    }
}

# --- 📚 [계열별 공통 DB] 세부 학과가 없을 때 방어용 (마찬가지로 확장) ---
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
        selected_topics = data['topics'][:3] # 혹시 주제가 3개 미만일 경우를 대비한 안전장치
        
    try:
        selected_books = random.sample(data['books'], 2)
    except:
        selected_books = data['books'][:2]

    # 💡 3. 활동 팁(조언) 역시 고정되지 않게 3가지 버전 중 하나를 랜덤 출력!
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

    if act_type == "주도형":
        act_advice = random.choice(lead_advices)
    else:
        act_advice = random.choice(passive_advices)

    # 4. 화면 출력용 마크다운 텍스트 조립
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
    
    # 💡 선생님의 완벽한 핑크/그린/오렌지 원본 디자인 그대로 유지!
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
# 메인 프로그램 UI (디자인 변경 없음!)
# ==========================================

# 1. 페이지 설정
st.set_page_config(page_title="양명여고 학생부 설계기", page_icon="📋", layout="wide")

# 2. 에러 원천 차단형 안전 CSS (선생님 원본 디자인 100% 유지)
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
            show_offline_result(selected_track, target_name, selected_act, custom_title, act_type)
            
        else:
            if not api_key:
                st.warning("⏳ AI 서버 키가 설정되지 않아 **[학교 자체 데이터베이스]** 모드로 자동 전환합니다!")
                show_offline_result(selected_track, target_name, selected_act, custom_title, act_type)
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
                        show_offline_result(selected_track, target_name, selected_act, custom_title, act_type)
                    else:
                        st.error("🚨 알 수 없는 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.")
