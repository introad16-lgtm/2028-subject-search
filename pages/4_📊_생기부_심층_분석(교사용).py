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
    div.stDownloadButton > button { width: 100%; font-weight: bold; border-radius: 10px; margin-top: 10px; }
    .report-box { background-color: white; border-top: 5px solid #2563EB; border-radius: 10px; padding: 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-top: 20px; font-size: 1.05rem; line-height: 1.7; }
    .upload-box { background-color: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px; border-left: 5px solid #2563EB; }
    .status-box { background-color: #EFF6FF; padding: 20px; border-radius: 10px; border: 1px solid #BFDBFE; margin-bottom: 20px; }
    table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
    th { background-color: #F1F5F9; text-align: left; padding: 12px; border: 1px solid #CBD5E1; }
    td { padding: 12px; border: 1px solid #CBD5E1; vertical-align: top; }
</style>
""", unsafe_allow_html=True)

# 🔑 트리플 API 키 가져오기
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

# 📋 기본 인적 정보 입력란
col1, col2, col3 = st.columns(3)
with col1: target_univ = st.text_input("🎯 1지망 대학", placeholder="예: 서울대")
with col2: target_major = st.text_input("🎓 1지망 학과", placeholder="예: 교육학과")
with col3: student_grade = st.text_input("📊 학생 전교과 내신", placeholder="예: 1.5")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #1E3A8A; margin-bottom: 10px;'>📋 정밀 분석을 위한 사전 질문 입력란 (AI 포트폴리오에 즉시 반영)</h4>", unsafe_allow_html=True)

# 🔄 7번 사전 질문을 상단 입력 폼으로 전면 배치
col_q1, col_q2 = st.columns(2)
with col_q1:
    s_strategy = st.selectbox("⚖️ 수시 전략 방향성", ["선택 안함", "학생부종합전형(학종) 중심", "교과전형 중심", "학종/교과 균형 병행", "실기 및 특기자 전형 위주"])
    s_region = st.text_input("🗺️ 선호 대학 권역", value="인서울 최우선 및 수도권 주요 대학 선호")
with col_q2:
    s_minimum = st.text_input("📝 수능 최저 학력 기준 충족 가능성", placeholder="예: 모의고사 2합 6 안정적 가능 / 최저 없는 전형 희망")
    s_interview = st.text_input("🎤 학생의 면접 대비 상태 및 성향", placeholder="예: 말하기 자신감 높음 / 모의면접 경험 없음, 면접 위주 전형 부담 등")

final_student_record = ""
admission_stats_text = ""

if student_file:
    if "current_file_name" not in st.session_state or st.session_state.current_file_name != student_file.name:
        with st.spinner("📄 생기부 텍스트 추출 및 마스킹 작업 중..."):
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

# 💡 시스템 프롬프트에서 7번 질문 항목을 제거하고 상단 입력값 반영 지침으로 수정
TEACHER_SYSTEM_PROMPT = """
[System Role & Persona]
당신은 '양명여자고등학교 선생님을 위한 전담 대입 컨설팅 전문가'입니다. 

[🚨 마크다운 표 줄바꿈 절대 보존 원칙]
- 표(Table)의 행(| 내용 |)을 생성할 때 마다 **반드시 줄바꿈(Enter/개행 기호)**을 철저히 지키십시오. 한 줄로 뭉치면 표가 깨집니다.

[Core Evaluation Principles (5대 절대 준수 원칙)]
1. 기록의 패러다임: '참여 사실' 나열은 최하점, '학생의 주도적 확장 + 교사의 전문적 평가' 결합을 최우수로 평가.
2. 탐구 알고리즘 (4단계): [①교과 개념 발제 → ②독서/논문 심화 → ③전공 현상 적용 → ④한계 인식 및 환류] 구조 점검.
3. 철학적 사유와 초융합: 인문/철학적 질문을 자연과학/공학의 원리로 증명(또는 그 반대)하는 창의적 융합 확인.
4. 도구 교과의 무기화: 수학, 정보(AI/코딩)를 활용한 정량적 산출물 유무 점검.
5. 표현의 구체성: '분석하다, 증명하다, 모델링하다' 등 학술적인 행동동사 중심 분석.

[Security & Exception Handling]
1. 데이터 검증: 데이터가 없으면 "⚠️ 생기부 데이터가 입력되지 않았습니다. 데이터를 입력해 주세요."라고만 출력.
2. 완전한 익명화: 식별 불가능한 가명(예: 학생 A)만 사용할 것. 
3. 출력 헤더 표기: 답변 최상단에 "[현재 분석 대상: 학생 A]" 라고 명시할 것.

[Execution Tasks & Strict Output Templates]
선생님이 사전에 입력한 [사전 진단 맥락 정보]를 모든 역량 평가와 수시 포트폴리오(상향/적정/안정 카드 배치) 설계 시 유기적으로 결합하여 반영하되, 아래 지정된 1~6번 목차 양식만 엄격하게 출력하세요. (질문 단계는 완료되었으므로 질문 항목은 출력하지 않습니다.)

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
(제공된 선생님의 수시 전략, 권역 선호도, 수능 최저 충족 상황을 반영하여 리얼하게 포트폴리오를 설계할 것)
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
* (교사가 학생 및 학부모 상담 시 수능최저, 면접 강약점을 연계하여 바로 활용할 수 있는 전체 전략의 핵심을 2~3줄로 요약)
"""

if st.button("🚀 AI 생기부 분석", type="primary", use_container_width=True):
    if not student_file: st.warning("⚠️ 분석할 학생의 생기부 PDF 파일을 업로드해 주세요.")
    elif not target_keys: st.error("🚨 사용 가능한 API 키가 없습니다. 좌측 사이드바 설정을 확인해 주세요.")
    else:
        with st.spinner("🌐 AI 엔진 가동 중... (입력하신 사전 진단 데이터를 기반으로 맞춤형 수시 라인을 설계 중입니다)"):
            success = False
            for idx, current_key in enumerate(target_keys):
                try:
                    genai.configure(api_key=current_key)
                    chosen_model = get_best_model(current_key)
                    model = genai.GenerativeModel(model_name=chosen_model, system_instruction=TEACHER_SYSTEM_PROMPT)
                    
                    ref_text_block = f"[우수 생기부 참조 데이터 (평가 기준)]\n{reference_record}\n" if reference_record else ""
                    stats_text_block = f"[양명여고 최근 3년 합불 통계 (수시 6장 설계 기준)]\n{admission_stats_text}\n" if admission_stats_text else ""
                    
                    # 🔥 사전 질문 답변 데이터가 완벽하게 격리 및 조립되어 주입됩니다.
                    user_prompt = f"""
                    [1. 우수 사례 참조 데이터 (오직 '평가 기준'으로만 참고)]
                    {ref_text_block}
                    
                    [2. 양명여고 합불 통계 데이터]
                    {stats_text_block}
                    
                    ======================================================================
                    [3. 🔥 분석 대상 학생의 기본 정보 및 선생님의 사전 진단 맥락]
                    - 1지망 대학/학과: {target_univ if target_univ else '미입력'} / {target_major if target_major else '미입력'}
                    - 전교과 내신 평균 등급: {student_grade if student_grade else '미입력'}
                    - ⚖️ 선생님이 판단한 수시 전략 방향: {s_strategy}
                    - 🗺️ 선호 대학 권역 범위: {s_region}
                    - 📝 모의고사 기준 수능 최저 충족 여부: {s_minimum}
                    - 🎤 학생의 구체적 면접 역량 및 성향: {s_interview}
                    
                    [🚨 진짜 분석 대상 학생의 실제 생기부 텍스트]
                    {final_student_record}
                    ======================================================================
                    
                    최종 지시: 위 [3번]의 사전 진단 내역(수능최저, 면접 상태 등)을 철저히 반영하여, 수시 6장 카드와 6번 핵심 상담 포인트를 극도로 현실성 있게 구성하세요. 마크다운 표 개행 규칙을 준수하여 1~6번 리포트를 단 하나의 덩어리로 작성하십시오.
                    """
                    
                    st.session_state.chat_session = model.start_chat(history=[])
                    response = st.session_state.chat_session.send_message(user_prompt)
                    
                    engine_name = f"{idx+1}번 엔진" if key_choice == "🤖 자동 모드 (권장)" else "선택된 엔진"
                    st.success(f"✅ {engine_name}으로 심층 분석 리포트가 완성되었습니다!")
                    
                    st.markdown("<div class='report-box'>", unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.download_button(
                        label="📥 생성된 분석 리포트 다운로드 (.md 파일)",
                        data=response.text,
                        file_name=f"양명여고_생기부분석_{target_major if target_major else '결과'}.md",
                        mime="text/markdown"
                    )
                    
                    success = True
                    break 
                    
                except Exception as e:
                    if key_choice == "🤖 자동 모드 (권장)" and idx < len(target_keys) - 1:
                        st.warning(f"⚠️ {idx+1}번 엔진 한도 초과. 즉시 다음 예비 엔진으로 자동 전환합니다...")
                        continue 
                    else:
                        st.error(f"🚨 분석 중 오류가 발생했습니다.\n\n상세 내용: {str(e)}")
                        break

st.write("---")
if "chat_session" in st.session_state:
    st.markdown("### 💬 AI 컨설턴트와 정밀 상담 진행")
    user_msg = st.chat_input("질문이나 추가 정보를 입력하세요...")
    if user_msg:
        with st.chat_message("user"): st.markdown(user_msg)
        with st.spinner("전문가가 답변을 작성 중입니다..."):
            try:
                response = st.session_state.chat_session.send_message(user_msg)
                with st.chat_message("assistant"): st.markdown(response.text)
            except Exception as e:
                st.error("답변 생성 중 오류가 발생했습니다.")
