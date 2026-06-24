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

# 🔑 트리플 API 키 가져오기
try: api_key_1 = st.secrets["GEMINI_API_KEY_1"]
except: api_key_1 = None

try: api_key_2 = st.secrets["GEMINI_API_KEY_2"]
except: api_key_2 = None

try: api_key_3 = st.secrets["GEMINI_API_KEY_3"]
except: api_key_3 = None

with st.sidebar:
    st.markdown("### 🔐 교사 전용 모드 (트리플 엔진)")
    
    key_choice = st.radio("사용할 AI 계정 선택:", ["계정 1 (메인)", "계정 2 (예비 1)", "계정 3 (예비 2)"])
    
    if key_choice == "계정 1 (메인)":
        api_key = api_key_1
    elif key_choice == "계정 2 (예비 1)":
        api_key = api_key_2
    else:
        api_key = api_key_3
        
    if api_key: 
        st.success(f"✅ {key_choice} 연결 정상!")
    else: 
        st.error(f"🚨 {key_choice}의 API 키가 올바르지 않거나 없습니다.")
        
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
    raw_student_text = extract_text_from_pdf(student_file)
    final_student_record = anonymize_text(raw_student_text)
    st.success("✅ 학생 생기부 로드 및 개인정보 블라인드 처리 완료!")

if target_major:
    admission_stats_text = get_local_admission_stats(EXCEL_FILE_PATH, target_univ, target_major)
    if admission_stats_text and "오류" not in admission_stats_text and "존재하지 않습니다" not in admission_stats_text:
        with st.expander(f"📊 '{target_major}' 관련 합불 통계 미리보기"):
            st.text(admission_stats_text)

st.markdown("</div>", unsafe_allow_html=True)

TEACHER_SYSTEM_PROMPT = """
당신은 '양명여자고등학교 선생님을 위한 전담 대입 컨설팅 전문가'입니다. 

[Core Evaluation Principles (5대 절대 준수 원칙)]
1. 기록의 패러다임: '참여 사실' 나열은 최하점, '학생의 주도적 확장 + 교사의 전문적 평가' 결합을 최우수로 평가.
2. 탐구 알고리즘 (4단계): [①교과 개념 발제 → ②독서/논문 심화 → ③전공 현상 적용 → ④한계 인식 및 환류] 구조 점검.
3. 철학적 사유와 초융합: 인문/철학적 질문을 자연과학/공학의 원리로 증명하는 창의적 융합 확인.
4. 도구 교과의 무기화: 수학, 정보(AI/코딩)를 활용한 데이터 시각화, 정량적 산출물 유무 점검.
5. 표현의 구체성: '분석하다, 증명하다, 모델링하다' 등 능동적이고 학술적인 행동동사 중심 분석.

[Security & Exception Handling (보안 및 맥락 관리 절대 수칙)]
1. 분석 대상의 명확한 고정: [우수 생기부 참조 데이터]와 [양명여고 합불 통계]는 오직 '평가 기준'으로만 사용하며, [분석 대상 학생 생기부]의 내용과 절대 섞지 마십시오.
2. 출력 헤더 표기: 답변 최상단에 "[현재 분석 대상: 학생 A]" 라고 명시할 것.
3. 완전한 익명화: 출력물에는 반드시 '학생 A'라는 가명만 사용할 것. 

[Execution Tasks & Strict Output Templates]
서술형 텍스트는 모두 불릿 포인트(*)를 사용해 개조식으로 작성하세요.

1. 총평 및 대입 3대 핵심 역량 평가 (표 사용)
- 평가영역(학업/진로/공동체), 등급(S/A/B/C), 구체적 성취, 강점/약점

2. 전략적 지원 학과 추천 (표 사용)
- 메인 전공, 틈새 전공, 융합 전공 추천 및 추천 사유

3. 수시 6장 지원 대학 포트폴리오 (표 사용)
* 매우 중요: 제공된 [양명여고 최근 3년 합불 통계 데이터]와 [학생의 내신 성적]을 엄격하게 비교 분석하여 가장 현실적인 상향/적정/안정 카드를 설계하세요. 합불 통계에 없는 대학은 일반적인 입시 결과를 바탕으로 추론하세요.
- 상향 2장, 적정 2장, 안정 2장 추천 및 합격 가능성 분석

4. 남은 학기 맞춤형 후속 탐구(Follow-up Project) 기획 (표 사용)
- 창체 자율, 창체 진로, 교과 세특 영역별 탐구 주제, 4단계 수행 과정(발제/심화/적용/환류), 기대효과

5. [양명여고 특화] 심화 융합 탐구 마스터 플랜 (표 사용)
- 융합 프로젝트 주제명 2가지, 연계 교과, 4단계 수행 과정

6. 핵심 상담 포인트 (2~3줄 요약)

7. 정밀 분석을 위한 사전 질문 (아래 텍스트 그대로 출력)
- 📊 성적 확인: 위에서 입력하신 내신 등급 외에 수능 최저 충족 가능성은 어떻게 되나요?
- 🎯 추가 선호: 학생의 2지망 학과나 피하고 싶은 대학이 있나요?
- 🎤 면접 대비: 학생의 말하기 자신감이나 모의면접 경험 여부는 어떠한가요?
"""

# 👇 변경된 부분: 버튼 텍스트를 "🚀 AI 생기부 분석"으로 교체하고 전체 너비(use_container_width=True) 적용!
if st.button("🚀 AI 생기부 분석", type="primary", use_container_width=True):
    if not student_file:
        st.warning("⚠️ 분석할 학생의 생기부 PDF 파일을 업로드해 주세요.")
    elif not api_key:
        st.error("🚨 선택된 계정의 API 키가 설정되지 않았습니다. 좌측 사이드바를 확인해 주세요.")
    else:
        with st.spinner(f"🌐 {key_choice} 엔진으로 합불 통계와 우수 사례 바탕 정밀 분석 중입니다..."):
            try:
                genai.configure(api_key=api_key)
                chosen_model = get_best_model(api_key)
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
                
                [분석 대상 학생 생기부 (평가 대상)]
                {final_student_record}
                
                위 [분석 대상 학생 생기부]의 정성적 수준과 [합불 통계]의 정량적 데이터를 융합하여 지정된 포맷으로 완벽한 분석 리포트를 작성해 주세요.
                """
                
                if "chat_session" not in st.session_state:
                    st.session_state.chat_session = model.start_chat(history=[])
                
                response = st.session_state.chat_session.send_message(user_prompt)
                st.success(f"✅ {key_choice} 엔진으로 심층 분석 리포트가 완성되었습니다!")
                
                st.markdown("<div class='report-box'>", unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"🚨 분석 중 오류가 발생했습니다: {str(e)}")

st.write("---")
if "chat_session" in st.session_state:
    st.markdown("### 💬 AI 컨설턴트와 정밀 상담 진행")
    st.info("리포트 하단의 '사전 질문'에 대한 답변을 입력하거나, 수시 전략 수정 등을 요구해 보세요.")
    
    user_msg = st.chat_input("질문이나 추가 정보를 입력하세요...")
    if user_msg:
        with st.chat_message("user"):
            st.markdown(user_msg)
            
        with st.spinner("전문가가 답변을 작성 중입니다..."):
            try:
                response = st.session_state.chat_session.send_message(user_msg)
                with st.chat_message("assistant"):
                    st.markdown(response.text)
            except Exception as e:
                st.error("답변 생성 중 오류가 발생했습니다.")
