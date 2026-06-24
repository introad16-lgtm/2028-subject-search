import streamlit as st
import google.generativeai as genai
import PyPDF2
import re
import pandas as pd
import os

# --- 💡 스마트 캐시 함수 ---
@st.cache_data(ttl=3600)
def get_best_model(api_key):
    try:
        genai.configure(api_key=api_key)
        models = [m.name.replace("models/", "") for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for t in ["gemini-1.5-pro", "gemini-1.5-flash"]: 
            if t in models: 
                return t
        return models[0] if models else "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

# --- 🛡️ 강력한 개인정보 자동 블라인드(마스킹) 함수 ---
def anonymize_text(text):
    text = re.sub(r'\d{6}\s*-\s*\d{7}', '******-*******', text) 
    text = re.sub(r'(성명\s*:\s*)[가-힣]{2,5}', r'\1OOO', text) 
    text = re.sub(r'(주소\s*:\s*).*?(?=\n|$)', r'\1[주소 자동 블라인드 처리됨]', text) 
    text = re.sub(r'010\s*-\s*\d{3,4}\s*-\s*\d{4}', '010-****-****', text) 
    text = re.sub(r'\b([1-3])(0[1-9]|1[0-9])([0-3][0-9]|40)\b', r'\1****', text) 
    text = re.sub(r'(졸업 대장 번호\s*\|?\s*)\d+', r'\1[번호 삭제됨]', text) 
    return text

def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    except Exception as e:
        st.error(f"학생 PDF 파일 읽기 오류: {e}")
    return text

@st.cache_data
def load_local_pdf(file_path):
    text = ""
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as e:
            pass 
    return text

@st.cache_data
def get_local_admission_stats(file_path, target_univ, target_major):
    if not os.path.exists(file_path):
        return ""
    try:
        df = pd.read_excel(file_path, sheet_name=0)
        filtered_df = df.copy()
        
        if target_univ:
            filtered_df = filtered_df[filtered_df['대학명'].str.contains(target_univ, na=False)]
        if target_major:
            filtered_df = filtered_df[filtered_df['지원학과(모집단위)'].str.contains(target_major, na=False)]
        
        if filtered_df.empty and target_major:
             filtered_df = df[df['지원학과(모집단위)'].str.contains(target_major, na=False)]

        if filtered_df.empty:
            return "해당 대학/학과에 대한 최근 양명여고 합불 데이터가 존재하지 않습니다."
        
        stats = filtered_df.groupby(['대학명', '전형명', '최종합불결과'])['전교과_내신평균'].agg(['count', 'mean', 'min', 'max']).reset_index()
        stats.columns = ['대학명', '전형명', '결과', '지원건수', '평균내신', '최고내신(min)', '최저내신(max)']
        
        stats_str = f"📈 [양명여고 최근 3년 '{target_univ} {target_major}' 관련 지원 통계]\n\n"
        for index, row in stats.iterrows():
            stats_str += f"- 대학/전형: {row['대학명']} ({row['전형명']})\n"
            stats_str += f"  결과: {row['결과']} ({row['지원건수']}건)\n"
            stats_str += f"  내신: 평균 {row['평균내신']:.2f} (최고 {row['최고내신(min)']:.2f} ~ 최저 {row['최저내신(max)']:.2f})\n\n"
            
        return stats_str
    except Exception as e:
        return f"엑셀 데이터 분석 중 오류 발생: {e}"

# --- 1. 페이지 설정 및 디자인 ---
st.set_page_config(page_title="양명여고 생기부 분석기", page_icon="📊", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; } 
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 2px solid #3B82F6; }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: white !important; border: none !important; border-radius: 10px !important;
        font-weight: 900 !important; font-size: 1.2rem !important; padding: 15px 0 !important;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3) !important; width: 100%; margin-top: 15px !important;
    }
    div.stButton > button[kind="primary"]:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 15px rgba(29, 78, 216, 0.4) !important; }
    .report-box { background-color: white; border-top: 5px solid #2563EB; border-radius: 10px; padding: 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-top: 20px; font-size: 1.05rem; line-height: 1.7; }
    .upload-box { background-color: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px; border-left: 5px solid #2563EB; }
    .status-box { background-color: #EFF6FF; padding: 20px; border-radius: 10px; border: 1px solid #BFDBFE; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# 🔑 트리플 API 키 가져오기 및 리스트화
keys_list = []
try: 
    if st.secrets["GEMINI_API_KEY_1"]: keys_list.append(st.secrets["GEMINI_API_KEY_1"])
except: pass
try: 
    if st.secrets["GEMINI_API_KEY_2"]: keys_list.append(st.secrets["GEMINI_API_KEY_2"])
except: pass
try: 
    if st.secrets["GEMINI_API_KEY_3"]: keys_list.append(st.secrets["GEMINI_API_KEY_3"])
except: pass

with st.sidebar:
    st.markdown("### 🔐 교사 전용 모드 (트리플 엔진)")
    key_choice = st.radio("사용할 AI 계정 선택:", ["🤖 자동 모드 (권장)", "계정 1 (메인)", "계정 2 (예비 1)", "계정 3 (예비 2)"])
    
    if key_choice == "🤖 자동 모드 (권장)": target_keys = keys_list; st.success(f"✅ 자동 모드 가동 중! (가용 엔진: {len(keys_list)}개)")
    elif key_choice == "계정 1 (메인)" and len(keys_list) >= 1: target_keys = [keys_list[0]]; st.success("✅ 계정 1 수동 연결!")
    elif key_choice == "계정 2 (예비 1)" and len(keys_list) >= 2: target_keys = [keys_list[1]]; st.success("✅ 계정 2 수동 연결!")
    elif key_choice == "계정 3 (예비 2)" and len(keys_list) >= 3: target_keys = [keys_list[2]]; st.success("✅ 계정 3 수동 연결!")
    else: target_keys = []; st.error("🚨 선택한 계정의 API 키가 없습니다.")
        
    st.markdown("---")
    st.markdown("**양명여자고등학교 진로진학부**")

if st.button("🏠 메인 화면으로 가기"): st.switch_page("app.py")

st.markdown("""
<div style='text-align: center; padding-bottom: 20px;'>
    <h1 style='color: #1E3A8A; font-weight: 900; font-size: 3rem;'>📊 3학년 생기부 심층 분석기</h1>
    <p style='color: #64748B; font-size: 1.1rem;'>우수 생기부와 <b>합불 엑셀 데이터</b>를 융합하여 완벽한 수시 전략을 설계합니다.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='status-box'>
    <h4 style='color: #1D4ED8; margin-top: 0; margin-bottom: 15px;'>⚙️ 학교 DB 자동 연동 상태</h4>
    ✅ <b>우수 생기부 평가 기준</b> (우수생기부통합.pdf) : 백그라운드 로드 완료<br>
    ✅ <b>양명여고 합불 통계</b> (양명여고_합불데이터(2022_2025).xlsx) : 분석 엔진 대기 중
</div>
""", unsafe_allow_html=True)

REF_PDF_PATH = "우수생기부통합.pdf"
EXCEL_FILE_PATH = "양명여고_합불데이터(2022_2025).xlsx"
reference_record = load_local_pdf(REF_PDF_PATH)

st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #2563EB; margin-top: 0;'>👤 [분석 대상] 학생 생기부 (PDF)</h3>", unsafe_allow_html=True)
st.info("💡 분석할 학생의 나이스 생기부 PDF 파일을 올려주세요. 개인정보는 100% 자동 삭제됩니다.")
student_file = st.file_uploader("학생 생기부 파일 업로드", type=["pdf"], key="stu_upload", label_visibility="collapsed")

col1, col2, col3 = st.columns(3)
with col1: target_univ = st.text_input("🎯 1지망 대학 (예: 서울대)")
with col2: target_major = st.text_input("🎓 1지망 학과 (예: 교육)")
with col3: student_grade = st.text_input("📊 학생 전교과 내신 (예: 1.5)")

final_student_record = ""
admission_stats_text = ""

if student_file:
    if "current_file_name" not in st.session_state or st.session_state.current_file_name != student_file.name:
        with st.spinner("📄 생기부 텍스트 추출 및 마스킹 작업 중... (최초 1회만 진행되며 약 5~10초 소요됩니다)"):
            raw_student_text = extract_text_from_pdf(student_file)
            st.session_state.final_student_record = anonymize_text(raw_student_text)
            st.session_state.current_file_name = student_file.name
            st.success("✅ 학생 생기부 로드 및 개인정보 블라인드 처리 완료!")
    else:
        st.success("⚡ 메모리에서 학생 생기부를 즉시 불러왔습니다!")
    final_student_record = st.session_state.final_student_record

if target_major:
    admission_stats_text = get_local_admission_stats(EXCEL_FILE_PATH, target_univ, target_major)
    if admission_stats_text and "오류" not in admission_stats_text and "존재하지 않습니다" not in admission_stats_text:
        with st.expander(f"📊 '{target_major}' 관련 합불 통계 미리보기"): st.text(admission_stats_text)

st.markdown("</div>", unsafe_allow_html=True)

# 💡 선생님이 작성해주신 완벽한 시스템 프롬프트가 여기에 박힙니다!
TEACHER_SYSTEM_PROMPT = """
[System Role & Persona]
당신은 '양명여자고등학교 선생님을 위한 전담 대입 컨설팅 전문가'입니다. 일반계 고등학교인 양명여고 학생들의 특성을 깊이 이해하고 있으며, 교사의 진학 지도 업무를 체계적이고 객관적으로 지원합니다. 당신의 모든 답변은 아래의 원칙과 지정된 표 형식(Markdown Table)을 100% 엄격하게 준수해야 합니다.

[Core Evaluation Principles (5대 절대 준수 원칙)]
1. 기록의 패러다임: '참여 사실' 나열은 최하점, '학생의 주도적 확장 + 교사의 전문적 평가' 결합을 최우수로 평가.
2. 탐구 알고리즘 (4단계): [①교과 개념 발제 → ②독서/논문 심화 → ③전공 현상 적용 → ④한계 인식 및 환류(비판적 사유)] 구조 점검.
3. 철학적 사유와 초융합: 인문/철학적 질문을 자연과학/공학의 원리로 증명(또는 그 반대)하는 창의적 융합 확인.
4. 도구 교과의 무기화: 수학, 정보(AI/코딩/통계)를 활용한 데이터 시각화, 정량적 산출물 유무 점검.
5. 표현의 구체성: '분석하다, 증명하다, 모델링하다, 시각화하다' 등 능동적이고 학술적인 행동동사 중심 분석.

[대학 입학사정관 평가 루브릭 (절대 기준)]
서류평가요소 (학업역량)
- 기초학업역량: 학업성취도 / 교과목이수현황 / 고교교육환경.
- 심화학업역량: 지원계열교과목이수현황 / 지원계열관련과목성취도.
- 주요 평가질문: 대학에서의 수학을 위한 기본과목 성적은? 진로선택과목 이수내역은 적절한가? 소속고교의 교육과정과 난이도는? 지원계열 관련 과목 이수 정도와 성취수준은? 도전적 과제 수행 노력은?

서류평가요소 (학교활동의 우수성)
- 지식탐구역량: 탐구능력 / 학업태도 및 학업의지.
- 창의융합역량: 창의력 / 문제해결능력 / 지원계열탐색노력.
- 주요 평가질문: 탐구활동에 적극 참여하고 결과물을 산출했는가? 교과 연계 탐구인가? 자발적 성취동기가 있는가? 지원계열에 대한 관심과 이해로 지식의 깊이를 더했는가? 융합적 활용과 문제해결 경험이 있는가?

서류평가요소 (발전가능성)
- 공동체역량: 리더십 / 협업능력 / 의사소통능력.
- 성장잠재력: 성실성 및 책임감 / 자기주도성 / 성장가능성.
- 주요 평가질문: 주도적 노력으로 리더십을 발휘했는가? 공동 목표를 위해 협업하고 타인을 존중하는가? 출결 등 의무를 다했는가? 목표를 위해 능동적으로 도전하고 외연을 확장했는가? 희망학교 인재상으로 성장할 잠재력이 있는가?

[Security & Exception Handling (보안 및 예외 처리)]
1. 데이터 검증: [학생 데이터 입력란]이 비어있거나 데이터가 불충분할 경우, 임의로 분석을 지어내지 말고 즉시 중단한 뒤 "⚠️ 생기부 데이터가 입력되지 않았습니다. 데이터를 입력해 주세요."라고만 출력할 것.
2. 완전한 익명화: 출력물에는 반드시 식별 불가능한 가명(예: 학생 A)만 사용할 것. 민감 정보 발견 시 즉시 익명 처리.
3. 분석 대상의 명확한 고정: 우수 사례 데이터는 오직 '평가 기준'으로만 사용하며, 주 분석 대상의 내용과 섞지 말 것.
4. 출력 헤더 표기: 답변 최상단에 "[현재 분석 대상: 학생 A]" 라고 명시할 것.

[Execution Tasks & Strict Output Templates (수행 과제 및 지정 출력 포맷)]
입력된 학생 데이터를 분석하여, 반드시 아래에 지정된 목차와 표(Table) 형식을 단 하나도 빠짐없이 그대로 사용하여 출력하세요. 서술형 텍스트는 모두 불릿 포인트(*)를 사용해 개조식으로 작성하세요.

1. 총평 및 대입 3대 핵심 역량 평가
* 총평: (사정관 시각에서 초안의 핵심 경쟁력과 보완점을 2~3줄로 요약)
| 평가 영역 | 평가 등급 | 생기부 기반 구체적 성취 수준 및 정성 평가 (개조식) | 돋보이는 강점 및 보완 요망 약점 |
| :--- | :---: | :--- | :--- |
| 학업 역량 | [S/A/B/C] | * 내용 | * 강점: <br> * 약점: |
| 진로 역량 | [S/A/B/C] | * 내용 | * 강점: <br> * 약점: |
| 공동체 역량 | [S/A/B/C] | * 내용 | * 강점: <br> * 약점: |

2. 전략적 지원 학과 추천
| 추천 방향성 | 추천 학과(전공) | 생기부 기반 추천 사유 및 타당성 (개조식) |
| :--- | :--- | :--- |
| ① 메인 전공 (정면 돌파) | | * 내용 |
| ② 틈새 전공 (전략적 우회) | | * 내용 |
| ③ 융합 전공 (미래 유망) | | * 내용 |

3. 수시 6장 지원 대학 포트폴리오
| 지원 전략 | 추천 대학 | 추천 전형 (교과/종합/논술) | 추천 사유 및 합격 가능성 분석 (개조식) |
| :--- | :--- | :--- | :--- |
| 상향 (도전) 1 | | | * 내용 |
| 상향 (도전) 2 | | | * 내용 |
| 적정 1 | | | * 내용 |
| 적정 2 | | | * 내용 |
| 안정 1 | | | * 내용 |
| 안정 2 | | | * 내용 |

4. 남은 학기 맞춤형 후속 탐구(Follow-up Project) 기획
| 영역 | 제안 탐구 주제명 | 제안 배경 및 근거 | 4단계 수행 과정 (발제 → 심화 → 적용 → 환류) | 기대 효과 및 어필 역량 |
| :--- | :--- | :--- | :--- | :--- |
| 창체 자율 | | * 내용 | * 1단계(발제): <br> * 2단계(심화): <br> * 3단계(적용): <br> * 4단계(환류): | * 내용 |
| 창체 진로 | | * 내용 | * 1단계(발제): <br> * 2단계(심화): <br> * 3단계(적용): <br> * 4단계(환류): | * 내용 |
| 교과 세특 | | * 내용 | * 1단계(발제): <br> * 2단계(심화): <br> * 3단계(적용): <br> * 4단계(환류): | * 내용 |

5. [양명여고 특화] 심화 융합 탐구 마스터 플랜
| 융합 프로젝트 주제명 | 연계 대상 (교과 및 창체) | 4단계 수행 과정 (발제 → 심화 → 적용 → 환류) |
| :--- | :--- | :--- |
| 주제 1 | | * 1단계: <br> * 2단계: <br> * 3단계: <br> * 4단계: |
| 주제 2 | | * 1단계: <br> * 2단계: <br> * 3단계: <br> * 4단계: |

6. 핵심 상담 포인트
* (전체 전략의 핵심을 2~3줄로 요약)

7. 정밀 분석을 위한 사전 질문
- 📊 성적 입력: 현재까지의 전체 평균 등급 및 주요 과목 성적은 어떻게 되나요?
- 🎯 학생 선호: 학생 A의 실제 1지망 학과 및 학교는 어디인가요?
- ⚖️ 수시 전략: 학종 중심인지, 교과를 병행할 예정인지 방향성이 있나요?
- 🗺️ 대학 권역: 인서울 최우선인지, 경기/인천 등 수도권까지 허용 가능한가요?
- 📝 수능 최저 충족: 모의고사 점수 또는 수능 최저 학력 기준 충족 가능성을 알려주세요.
- 🎤 면접 대비: 학생의 말하기 자신감이나 모의면접 경험 여부는 어떠한가요?
"""

if st.button("🚀 AI 생기부 분석", type="primary", use_container_width=True):
    if not student_file: st.warning("⚠️ 분석할 학생의 생기부 PDF 파일을 업로드해 주세요.")
    elif not target_keys: st.error("🚨 사용 가능한 API 키가 없습니다. 좌측 사이드바 설정을 확인해 주세요.")
    else:
        with st.spinner("🌐 AI 엔진 가동 중... (분석에 약 20~40초가 소요되며, 자동 모드 시 오류가 발생하면 예비 엔진으로 즉시 전환됩니다)"):
            success = False
            for idx, current_key in enumerate(target_keys):
                try:
                    genai.configure(api_key=current_key)
                    chosen_model = get_best_model(current_key)
                    model = genai.GenerativeModel(model_name=chosen_model, system_instruction=TEACHER_SYSTEM_PROMPT)
                    
                    ref_text_block = f"[우수 생기부 참조 데이터 (평가 기준)]\n{reference_record}\n" if reference_record else ""
                    stats_text_block = f"[양명여고 최근 3년 합불 통계 (수시 6장 설계 기준)]\n{admission_stats_text}\n" if admission_stats_text else ""
                    
                    user_prompt = f"""
                    {ref_text_block}
                    {stats_text_block}
                    
                    --------------------------------------------------
                    [분석 대상 학생 정보]
                    - 1지망 대학: {target_univ if target_univ else '미입력'}
                    - 1지망 학과: {target_major if target_major else '미입력'}
                    - 전교과 내신 평균: {student_grade if student_grade else '미입력'}
                    
                    [학생 데이터 입력란]
                    {final_student_record}
                    
                    위 [학생 데이터 입력란]의 정성적 수준과 [합불 통계]의 정량적 데이터를 융합하여, 당신의 시스템 프롬프트에 지정된 [Execution Tasks & Strict Output Templates]의 1~7번 목차와 표 형식을 단 하나도 빠짐없이, 형태 변형 없이 100% 엄격하게 적용하여 완벽한 분석 리포트를 작성해 주세요.
                    """
                    
                    st.session_state.chat_session = model.start_chat(history=[])
                    response = st.session_state.chat_session.send_message(user_prompt)
                    
                    engine_name = f"{idx+1}번 엔진" if key_choice == "🤖 자동 모드 (권장)" else "선택된 엔진"
                    st.success(f"✅ {engine_name}으로 심층 분석 리포트가 완성되었습니다!")
                    
                    st.markdown("<div class='report-box'>", unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    success = True
                    break 
                    
                except Exception as e:
                    if key_choice == "🤖 자동 모드 (권장)" and idx < len(target_keys) - 1:
                        st.warning(f"⚠️ {idx+1}번 엔진 응답 지연/한도 초과. 즉시 다음 예비 엔진으로 자동 전환합니다...")
                        continue 
                    else:
                        st.error(f"🚨 분석 중 오류가 발생했습니다.\n\n상세 내용: {str(e)}")
                        break

st.write("---")
if "chat_session" in st.session_state:
    st.markdown("### 💬 AI 컨설턴트와 정밀 상담 진행")
    st.info("리포트 하단의 '사전 질문'에 대한 답변을 입력하거나, 수시 전략 수정 등을 요구해 보세요.")
    user_msg = st.chat_input("질문이나 추가 정보를 입력하세요...")
    if user_msg:
        with st.chat_message("user"): st.markdown(user_msg)
        with st.spinner("전문가가 답변을 작성 중입니다..."):
            try:
                response = st.session_state.chat_session.send_message(user_msg)
                with st.chat_message("assistant"): st.markdown(response.text)
            except Exception as e:
                st.error("답변 생성 중 오류가 발생했습니다.")
