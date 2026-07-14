import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import PyPDF2
import re
import pandas as pd
import os

# --- 💡 양명여고 전용 5등급 -> 9등급 자동 환산 엔진 ---
def calculate_9_grade(g5_raw):
    try:
        val = float(g5_raw)
    except ValueError:
        return None
        
    # 1. 양명여고 특별 보정
    avg5 = val - 0.050
    if avg5 < 1.0: avg5 = 1.0
    if avg5 > 5.0: avg5 = 5.0
    
    # 2. 선형 보간법 (구간 매칭)
    points = [
        (1.0, 1.0), (1.1, 1.35), (1.2, 1.65), (1.31, 1.99), 
        (1.478, 2.345), (1.715, 2.753), (2.004, 3.261), 
        (3.0, 6.0), (5.0, 9.0)
    ]
    
    if avg5 <= 1.0: return 1.0
    if avg5 >= 5.0: return 9.0
    
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        if x1 <= avg5 <= x2:
            return y1 + (avg5 - x1) / (x2 - x1) * (y2 - y1)
    return 9.0

# --- 💡 스마트 캐시 함수 ---
@st.cache_data(ttl=3600)
def get_best_model(api_key):
    try:
        genai.configure(api_key=api_key)
        models = [m.name.replace("models/", "") for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for t in ["gemini-1.5-pro", "gemini-1.5-flash"]: 
            if t in models: return t
        return models[0] if models else "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

# --- 🛡️ 2차 정규식 개인정보 자동 블라인드 함수 ---
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
            if extracted: text += extracted + "\n"
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
                    if extracted: text += extracted + "\n"
        except Exception: pass 
    return text

# --- 📊 양명여고 합불 통계 검색 ---
@st.cache_data
def get_local_admission_stats(file_path, target_univ, target_major):
    if not os.path.exists(file_path): return ""
    try:
        df = pd.read_excel(file_path, sheet_name=0)
        filtered_df = df.copy()
        
        if target_univ: filtered_df = filtered_df[filtered_df['대학명'].str.contains(target_univ, na=False)]
        if target_major: filtered_df = filtered_df[filtered_df['지원학과(모집단위)'].str.contains(target_major, na=False)]
        
        is_fallback = False
        if filtered_df.empty and target_major:
             filtered_df = df[df['지원학과(모집단위)'].str.contains(target_major, na=False)]
             is_fallback = True

        if filtered_df.empty:
            return f"❌ 최근 3개년(2022~2025) 양명여고 데이터에 '{target_major}' 관련 기록이 존재하지 않습니다."
        
        stats = filtered_df.groupby(['대학명', '전형명', '최종합불결과'])['전교과_내신평균'].agg(['count', 'mean', 'min', 'max']).reset_index()
        stats.columns = ['대학명', '전형명', '결과', '지원건수', '평균내신', '최고내신(min)', '최저내신(max)']
        
        if is_fallback and target_univ:
            stats_str = f"💡 [참고] '{target_univ} {target_major}' 데이터가 없어 타 대학교의 '{target_major}' 통계를 출력합니다.\n\n"
        else:
            stats_str = f"📈 [양명여고 최근 3년 '{target_univ} {target_major}' 지원 통계]\n\n"
            
        for index, row in stats.iterrows():
            stats_str += f"- {row['대학명']}({row['전형명']}): {row['결과']}({row['지원건수']}건) / 내신평균 {row['평균내신']:.2f}\n"
        return stats_str
    except Exception as e: return f"데이터 분석 오류: {e}"

# --- 📚 대학 공식 권장과목 검색 ---
@st.cache_data
def get_recommended_subjects(file_path, target_univ, target_major):
    if not os.path.exists(file_path): return ""
    try:
        df = pd.read_excel(file_path, skiprows=2, engine='openpyxl')
        df['대학명'] = df.iloc[:, 2].fillna('').astype(str)
        df['모집단위'] = df.iloc[:, 3].fillna('').astype(str) + " " + df.iloc[:, 4].fillna('').astype(str)
        df['핵심과목'] = df.iloc[:, 5].fillna('-').astype(str)
        df['권장과목'] = df.iloc[:, 6].fillna('-').astype(str) if len(df.columns) > 6 else '-'
        df['비고'] = df.iloc[:, 7].fillna('-').astype(str) if len(df.columns) > 7 else '-'
        
        result = df.copy()
        if target_univ: result = result[result['대학명'].str.contains(target_univ, na=False, case=False)]
        if target_major: result = result[result['모집단위'].str.contains(target_major, na=False, case=False)]
        
        if result.empty and target_major:
             result = df[df['모집단위'].str.contains(target_major, na=False, case=False)]
             
        if result.empty: return ""
        
        rec_str = "📚 [대학 공식 발표 핵심/권장 이수 과목 데이터]\n"
        for _, row in result.head(3).iterrows():
            rec_str += f"- {row['대학명']} {row['모집단위'].strip()} : [핵심] {row['핵심과목']} / [권장] {row['권장과목']}\n"
        return rec_str
    except Exception: return ""

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
    .status-box { background-color: #EFF6FF; padding: 20px; border-radius: 10px; border: 1px solid #BFDBFE; margin-bottom: 20px; }
    table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
    th { background-color: #F1F5F9; text-align: left; padding: 12px; border: 1px solid #CBD5E1; }
    td { padding: 12px; border: 1px solid #CBD5E1; vertical-align: top; }
    @media print {
        [data-testid="stSidebar"], [data-testid="stHeader"], div[data-testid="stToolbar"] { display: none !important; }
        .stButton, .stDownloadButton, .status-box, iframe, .element-container:has(input) { display: none !important; }
        .stApp { background-color: white !important; }
        .report-box { border: none !important; box-shadow: none !important; margin: 0 !important; padding: 0 !important; width: 100% !important; }
    }
</style>
""", unsafe_allow_html=True)

# ========= 🔒 교사 전용 보안 (비밀번호) 시스템 =========
if "teacher_authenticated" not in st.session_state:
    st.session_state.teacher_authenticated = False

if not st.session_state.teacher_authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔒 교사용 컨설팅 시스템 접근 인증</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("💡 학생들의 민감한 성적 및 생기부 데이터를 다루는 교사 전용 메뉴입니다. 진로진학부 전용 비밀번호를 입력해 주세요.")
        pwd = st.text_input("🔑 비밀번호", type="password", placeholder="비밀번호를 입력하세요")
        
        if st.button("입장하기", type="primary", use_container_width=True):
            if pwd == "ymgh17147":  
                st.session_state.teacher_authenticated = True
                st.rerun()  
            else:
                st.error("❌ 비밀번호가 일치하지 않습니다.")
                
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🏠 메인 화면으로 돌아가기", use_container_width=True):
            st.switch_page("app.py")
            
    st.stop()  
# ==========================================================

# API 키 세팅
keys_list = []
for i in range(1, 4):
    try: 
        if st.secrets[f"GEMINI_API_KEY_{i}"]: keys_list.append(st.secrets[f"GEMINI_API_KEY_{i}"])
    except: pass

with st.sidebar:
    st.markdown("### 🔐 교사 전용 모드 (트리플 엔진)")
    key_choice = st.radio("사용할 AI 계정 선택:", ["🤖 자동 모드 (권장)", "계정 1 (메인)", "계정 2 (예비 1)", "계정 3 (예비 2)"])
    if key_choice == "🤖 자동 모드 (권장)": target_keys = keys_list
    elif key_choice == "계정 1 (메인)" and len(keys_list) >= 1: target_keys = [keys_list[0]]
    elif key_choice == "계정 2 (예비 1)" and len(keys_list) >= 2: target_keys = [keys_list[1]]
    elif key_choice == "계정 3 (예비 2)" and len(keys_list) >= 3: target_keys = [keys_list[2]]
    else: target_keys = []
    
    st.markdown("---")
    if st.button("🔓 로그아웃 (비밀번호 잠금)", use_container_width=True):
        st.session_state.teacher_authenticated = False
        st.rerun()
        
    st.markdown("---")
    st.markdown("**양명여자고등학교 진로진학부**")
    
if st.button("🏠 메인 화면으로 가기"): st.switch_page("app.py")

st.markdown("<h1 style='text-align: center; color: #1E3A8A; font-weight: 900; font-size: 3rem;'>📊 생기부 심층 분석기 (학년 통합)</h1>", unsafe_allow_html=True)

# 📌 학년 선택 라디오 버튼 (✨ 4가지 옵션 유지)
selected_grade = st.radio(
    "👨‍🏫 분석할 학생의 학년을 선택하세요", 
    [
        "1학년 (진로 탐색 및 기초 설계)", 
        "2학년 (전공 심화 및 빌드업)", 
        "3학년 (수시 실전 포트폴리오)", 
        "3학년 (수시 6장 정밀 설계)"
    ], 
    horizontal=True
)

REF_PDF_PATH = "우수생기부통합.pdf"
EXCEL_FILE_PATH = "양명여고_합불데이터(2022_2025).xlsx"
REC_SUBJECTS_FILE_PATH = "data.xlsx"  
reference_record = load_local_pdf(REF_PDF_PATH)

st.markdown("---")
st.markdown("<h3 style='color: #2563EB; margin-top: 0;'>👤 생기부 업로드 및 사전 진단</h3>", unsafe_allow_html=True)

# 🔥 1차 방어막: 학생 실명 원천 차단 입력창
mask_name = st.text_input("🛡️ 텍스트 원천 차단용 학생 이름 (선택)", placeholder="예: 홍길동 (입력 시 생기부 텍스트에서 이름이 완벽히 삭제된 후 AI로 전송됩니다)")
student_file = st.file_uploader("나이스 생기부 PDF 업로드", type=["pdf"])

# 🔄 학년별 동적 입력 폼
target_univ, target_major, admission_stats_text, rec_subjects_text, final_student_record = "", "", "", "", ""
user_context = ""

if "1학년" in selected_grade:
    col1, col2, col3 = st.columns(3)
    with col1:
        g1_track = st.text_input("🎯 희망 진로/계열", placeholder="예: 미디어/언론 계열")
        g1_grade = st.text_input("📊 5등급제 내신 평균", placeholder="예: 1.528")
    with col2:
        g1_trend = st.text_input("📉 중학교 대비 성취도 변화 및 멘탈", placeholder="예: 첫 시험 수학 4등급으로 하락해 불안해함")
    with col3:
        g1_favorite = st.text_input("✨ 흥미 과목 / 2학년 선택 희망", placeholder="예: 국어 / 윤리와사상 고민 중")
    
    calc_msg = ""
    if g1_grade:
        g9_val = calculate_9_grade(g1_grade)
        if g9_val: calc_msg = f" (양명여고 산출기 기준 9등급제 환산: {g9_val:.3f}등급)"
        
    user_context = f"- 희망 진로 계열: {g1_track}\n- 5등급 내신: {g1_grade}{calc_msg}\n- 성취도 변화/상태: {g1_trend}\n- 관심 과목: {g1_favorite}"
    target_major = g1_track

elif "2학년" in selected_grade:
    col1, col2 = st.columns(2)
    with col1:
        target_univ = st.text_input("🎯 1지망 희망 대학 (통계용)", placeholder="예: 건국대")
        target_major = st.text_input("🎓 희망 학과 (통계용)", placeholder="예: 미디어학과")
        g2_grade = st.text_input("📊 5등급제 내신 평균", placeholder="예: 1.528")
    with col2:
        g2_trend = st.text_input("📉 1학년 대비 성적 추이", placeholder="예: 전체적으로 상승세, 국어 특히 우수")
        g2_subject = st.text_input("📚 3학년 선택 과목 고민", placeholder="예: 심화수학을 할지 말지 고민 중")
    
    calc_msg = ""
    if g2_grade:
        g9_val = calculate_9_grade(g2_grade)
        if g9_val: calc_msg = f" (양명여고 산출기 기준 9등급제 환산: {g9_val:.3f}등급)"
        
    user_context = f"- 1지망 대학/학과: {target_univ} / {target_major}\n- 5등급 내신: {g2_grade}{calc_msg}\n- 1학년 대비 추이: {g2_trend}\n- 3학년 선택 고민 과목: {g2_subject}"

else: # 3학년 (두 가지 모드 모두 동일한 입력창 사용)
    col1, col2, col3 = st.columns(3)
    with col1: target_univ = st.text_input("🎯 1지망 대학", placeholder="예: 서울대")
    with col2: target_major = st.text_input("🎓 1지망 학과", placeholder="예: 교육학과")
    with col3: student_grade = st.text_input("📊 전교과 내신", placeholder="예: 1.5")
    
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        s_strategy = st.selectbox("⚖️ 수시 전략", ["학생부종합(학종) 중심", "교과전형 중심", "학종/교과 병행", "실기/특기자 위주"])
        s_region = st.text_input("🗺️ 선호 권역", value="인서울 및 수도권")
    with col_q2:
        s_minimum = st.text_input("📝 수능 최저 충족 가능성", placeholder="예: 2합 6 안정")
        s_interview = st.text_input("🎤 면접 상태 및 성향", placeholder="예: 말하기 자신감 높음")
    user_context = f"- 1지망 대학/학과: {target_univ} / {target_major}\n- 내신: {student_grade}\n- 전략: {s_strategy} / {s_region}\n- 수능 최저: {s_minimum}\n- 면접: {s_interview}"

# 🔥 PDF 텍스트 추출 및 원천 마스킹 로직
if student_file:
    if "current_file" not in st.session_state or st.session_state.current_file != student_file.name or st.session_state.get("last_mask_name") != mask_name:
        with st.spinner("📄 텍스트 추출 및 개인정보 원천 차단 작업 중..."):
            raw_text = extract_text_from_pdf(student_file)
            
            if mask_name:
                mask_name = mask_name.strip()
                raw_text = raw_text.replace(mask_name, "학생 A")
                if len(mask_name) >= 3: 
                    first_name = mask_name[1:]
                    raw_text = raw_text.replace(first_name, "학생 A")
            
            st.session_state.final_text = anonymize_text(raw_text)
            st.session_state.current_file = student_file.name
            st.session_state.last_mask_name = mask_name
            
    final_student_record = st.session_state.final_text

if target_major:
    # 1. 합불 통계 로드
    admission_stats_text = get_local_admission_stats(EXCEL_FILE_PATH, target_univ, target_major)
    if admission_stats_text and "오류" not in admission_stats_text:
        with st.expander(f"📊 '{target_major}' 양명여고 합불 통계 미리보기"): st.text(admission_stats_text)
    
    # 2. 1, 2학년일 경우 대학 권장과목 데이터 로드
    if "1학년" in selected_grade or "2학년" in selected_grade:
        rec_subjects_text = get_recommended_subjects(REC_SUBJECTS_FILE_PATH, target_univ, target_major)
        if rec_subjects_text:
            with st.expander(f"📚 '{target_major}' 관련 대학 공식 권장과목 미리보기"): st.text(rec_subjects_text)

# 🔥 공통 보안 지침 
COMMON_SECURITY_PROMPT = """
[Security & Exception Handling (🚨 초강력 개인정보 보호 절대 원칙)]
1. 🚨 실명 노출 절대 금지(Kill Switch): 입력된 생기부 본문 텍스트 안에 실수로 학생의 '실명'이 남아 있더라도, 절대로 실명을 출력하지 마십시오.
2. 강제 개명: 무조건 '학생 A' 또는 '해당 학생'으로 지칭할 것.
3. 출력 헤더 표기: 답변 최상단에 "[현재 분석 대상: 학생 A]" 라고 명시할 것.
"""

# 🔥 환산 내신 절대 준수 규칙
GRADE_CONVERT_PROMPT = """
[🚨 내신 환산 절대 규칙 및 데이터 예외 처리 (환각 방지)]
1. 학생 데이터에 '양명여고 산출기 기준 9등급제 환산' 점수가 주어지면, AI는 절대 임의로 5등급 백분위를 추정하지 마십시오. 반드시 제공된 9등급제 환산 점수를 100% 신뢰하여 과거 입결 데이터 비교 및 대학 라인 산정의 '절대 기준점'으로 삼으십시오.
2. 내신 점수나 대학 정보가 비어있어도 생기부 텍스트가 존재하면 절대 멈추지 말고 분석을 진행하십시오.
"""

# 🔥 마크다운 표 생성 필수 규칙 (공통)
TABLE_FORMAT_PROMPT = """
[🚨 절대 규칙 - 마크다운 표(Table) 깨짐 완벽 방지]
1. 표를 생성할 때 각 행(Row)이 끝날 때마다 반드시 엔터(줄바꿈)를 하십시오. 전체를 한 줄로 이어 쓰면 안 됩니다.
2. 표의 '셀(Cell) 내부'에서 텍스트를 줄바꿈할 때만 무조건 `<br>` 태그를 사용하십시오.
3. 1번 문항 등급 판정 시 S/A/B/C 중 하나를 반드시 입력하세요.
"""

# 🔥 2022 개정 교육과정 과목명 절대 준수 (1, 2학년 전용)
CURRICULUM_2022_PROMPT = """
[🚨 2022 개정 교육과정 과목명 준수 절대 규칙]
학생에게 2·3학년 선택 과목을 추천할 때, 과거 2015 교육과정의 명칭(예: 물리학Ⅱ, 화학Ⅱ, 생명과학Ⅱ, 지구과학Ⅱ 등)을 절대 사용하지 마십시오. 반드시 아래의 2022 개정 교육과정 '진로 선택' 및 '융합 선택' 과목명을 사용해야 합니다.
- 물리: 역학과 에너지, 전자기와 양자
- 화학: 물질과 에너지, 화학 반응의 세계
- 생명: 세포와 물질대사, 생물의 유전
- 지구: 지구시스템과학, 행성우주과학
- 융합: 과학의 역사와 문화, 기후변화와 환경생태, 융합과학 탐구
"""

# ----------------- 1학년 프롬프트 -----------------
PROMPT_1 = f"""
[System Persona] 당신은 '양명여자고등학교 1학년 전담 대입 컨설팅 전문가'입니다. 2022 개정 교육과정 세대입니다.

{COMMON_SECURITY_PROMPT}
{GRADE_CONVERT_PROMPT}
{TABLE_FORMAT_PROMPT}
{CURRICULUM_2022_PROMPT}
4. [경고] Step 3 작성 시 '완성형 세특 문장'을 절대 쓰지 마십시오. 반드시 '탐구 주제명'과 '수행 방안(액션 플랜)'만 제시하십시오.

[출력 양식 - 이대로만 출력할 것]
1. 진로 및 계열 심층 분석
* (선생님이 입력한 학생의 멘탈/성적 변화를 바탕으로 1학년 시점의 학습 및 심리적 조언 3줄 요약)

| 핵심 추천 학과 | 연계 직업군 | 관련 학과 탐구 가능한 대학 홈페이지 링크 |
| :--- | :--- | :--- |
| 학과명 | 내용<br>내용 | 링크 예시 |

2. 데이터 기반 입결 및 목표 설정

| 5등급제 내신 구간 | 양명 자체 9등급제 환산치 | 양명여고/일반적 지원 전략 및 목표 설정 가이드 |
| :--- | :--- | :--- |
| 내용 | 내용 | 내용<br>내용 |

3. 1학년 공통 과목 맞춤형 '탐구 주제' 추천 (완성 문장 절대 금지)

| 공통 과목 | 목표 역량 | 추천 탐구 주제명 및 구체적 수행 방안 (액션 플랜) |
| :--- | :---: | :--- |
| 국어/수학/영어 등 | [S/A/B/C] | * 주제: 내용<br>* 액션플랜: 내용 |

4. 창의적 체험활동 로드맵 (자율/동아리/진로)

| 영역 | 서류 평가 핵심 역량 | 구체적 액션 플랜 (행동 지표 중심) |
| :--- | :--- | :--- |
| 자율/진로 | 역량명 | 내용<br>내용 |

5. 익명화된 우수 생기부 사례 분석

| 양명여고 선배 우수 사례 핵심 키워드 | 1학년이 벤치마킹 해야 할 '역량의 시작점' |
| :--- | :--- |
| 내용 | 내용<br>내용 |

6. 2022 개정 맞춤형 2학년 과목 선택 팁

| 추천 과목 (일반/진로/융합) | 선택 사유 및 희망 진로 연계 포인트 |
| :--- | :--- |
| 과목명 | 내용<br>내용 |

7. 종합 리포트 및 핵심 후속 질문
* (종합 상담 가이드 2줄 요약)
* (AI가 파악한 진로 기반으로 교사가 학생에게 던질 수 있는 심화 질문 2가지 제시)
"""

# ----------------- 2학년 프롬프트 -----------------
PROMPT_2 = f"""
[System Persona] 당신은 '양명여자고등학교 2학년 전담 대입 컨설팅 전문가'입니다. 2022 개정 교육과정 세대입니다.

{COMMON_SECURITY_PROMPT}
{GRADE_CONVERT_PROMPT}
{TABLE_FORMAT_PROMPT}
{CURRICULUM_2022_PROMPT}

[출력 양식 - 이대로만 출력할 것]
1. 2학년 중간 점검 및 역량 평가
* 총평: (전공 적합성 깊이 2~3줄 요약)

| 평가 영역 | 평가 등급 | 2학년 수준 구체적 성취 (개조식) | 돋보이는 강점 및 보완 요망 약점 |
| :--- | :---: | :--- | :--- |
| 학업 역량 | [S/A/B/C] | * 내용<br>* 내용 | * 강점: 내용<br>* 약점: 내용 |
| 진로 역량 | [S/A/B/C] | * 내용<br>* 내용 | * 강점: 내용<br>* 약점: 내용 |
| 공동체 역량 | [S/A/B/C] | * 내용<br>* 내용 | * 강점: 내용<br>* 약점: 내용 |

2. 목표 전공 및 전략 대학 가이드 (수시 빌드업 방향)

| 추천 방향성 | 추천 학과(전공) | 2학년 기록 기반 추천 사유 (개조식) |
| :--- | :--- | :--- |
| ① 메인 (전공 심화) | | * 내용 |
| ② 우회 (계열 적합) | | * 내용 |
| ③ 융합 (학교 특화) | | * 내용 |

3. 3학년 과목 선택 및 학업 설계 제안

| 구분 | 추천 과목명 (일반/진로/융합) | 선택 사유 및 생기부 연계 포인트 |
| :--- | :--- | :--- |
| 핵심 권장 | | * 내용<br>* 내용 |
| 전략 선택 | | * 내용<br>* 내용 |

4. 2학년 하반기~3학년 '빌드업' 탐구 설계 (발제→심화→적용→환류)

| 영역 | 제안 탐구 주제명 | 제안 배경 | 4단계 수행 과정 | 기대 효과 |
| :--- | :--- | :--- | :--- | :--- |
| 자율/진로 | | * 내용 | * 1단계: 내용<br>* 2단계: 내용<br>* 3단계: 내용<br>* 4단계: 내용 | * 내용 |
| 주요 교과 | | * 내용 | * 1단계: 내용<br>* 2단계: 내용<br>* 3단계: 내용<br>* 4단계: 내용 | * 내용 |

5. [양명여고 특화] 학급특색 프로젝트 마스터 플랜

| 융합적 주제명 | 연계 교과/활동 | 4단계 수행 과정 |
| :--- | :--- | :--- |
| 주제 1 | | * 1단계: 내용<br>* 2단계: 내용<br>* 3단계: 내용<br>* 4단계: 내용 |

6. 핵심 상담 가이드 (교사용 Summary)
* (학부모 및 학생 상담 시 강조해야 할 2학년 핵심 과제 2~3줄 요약)
"""

# ----------------- 3학년 (기존) 프롬프트 -----------------
PROMPT_3 = f"""
[System Persona] 당신은 '양명여자고등학교 3학년 전담 대입 컨설팅 전문가'입니다. 수시 원서 접수 실전용입니다.

{COMMON_SECURITY_PROMPT}
{TABLE_FORMAT_PROMPT}

[출력 양식 - 이대로만 출력할 것]
1. 총평 및 대입 3대 핵심 역량 평가
* 총평: (핵심 경쟁력 요약)

| 평가 영역 | 평가 등급 | 구체적 성취 수준 및 정성 평가 | 돋보이는 강점 및 보완점 |
| :--- | :---: | :--- | :--- |
| 학업 역량 | [S/A/B/C] | * 내용<br>* 내용 | * 강점: 내용<br>* 약점: 내용 |
| 진로 역량 | [S/A/B/C] | * 내용<br>* 내용 | * 강점: 내용<br>* 약점: 내용 |
| 공동체 역량 | [S/A/B/C] | * 내용<br>* 내용 | * 강점: 내용<br>* 약점: 내용 |

2. 전략적 지원 학과 추천

| 추천 방향성 | 추천 학과(전공) | 생기부 기반 추천 사유 (개조식) |
| :--- | :--- | :--- |
| ① 메인 (정면 돌파) | | * 내용 |
| ② 틈새 (전략 우회) | | * 내용 |
| ③ 융합 (미래 유망) | | * 내용 |

3. 수시 6장 지원 대학 포트폴리오
* (주의: '추천 사유 및 합격 가능성 분석' 작성 시, 반드시 타 전형과 비교하여 왜 이 학생에게 이 전형이 더 유리한지 비교 우위 분석을 명시할 것)

| 지원 전략 | 추천 대학 | 추천 전형 | 추천 사유 및 합격 가능성 분석 (전형 비교 우위 분석 필수) |
| :--- | :--- | :--- | :--- |
| 상향 1 | | | * 내용<br>* 내용 |
| 상향 2 | | | * 내용<br>* 내용 |
| 적정 1 | | | * 내용<br>* 내용 |
| 적정 2 | | | * 내용<br>* 내용 |
| 안정 1 | | | * 내용<br>* 내용 |
| 안정 2 | | | * 내용<br>* 내용 |

4. 남은 학기 맞춤형 후속 탐구 기획 (발제→심화→적용→환류)

| 영역 | 탐구 주제명 | 제안 배경 | 4단계 수행 과정 | 기대 효과 |
| :--- | :--- | :--- | :--- | :--- |
| 세특 등 | | * 내용 | * 1단계: 내용<br>* 2단계: 내용<br>* 3단계: 내용<br>* 4단계: 내용 | * 내용 |

5. [양명여고 특화] 심화 융합 마스터 플랜

| 주제명 | 연계 대상 | 4단계 수행 과정 |
| :--- | :--- | :--- |
| 주제 1 | | * 1단계: 내용<br>* 2단계: 내용<br>* 3단계: 내용<br>* 4단계: 내용 |

6. 핵심 상담 포인트
* 🎯 **[원포인트 지원 전략]**: (예시: 성신여대 지원 시, 내신 컷이 높은 교과 전형보다는 전공 적합성을 높게 평가하는 학종 전형으로 우회하는 것이 합격 확률을 40% 이상 높일 수 있음. 구체적인 비교 우위 전략 1문장 필수)
* (교사용 종합 최종 조언 1~2줄 요약)
"""

# ----------------- 3학년 (수시 6장 신규) 프롬프트 -----------------
PROMPT_3_6CARDS = f"""
[System Persona] 당신은 '양명여자고등학교 3학년 수시 원서 접수 전담 컨설팅 전문가'입니다.

{COMMON_SECURITY_PROMPT}
{TABLE_FORMAT_PROMPT}

[Core Evaluation Principles (5대 절대 준수 원칙)]
* 기록의 패러다임: '참여 사실' 나열은 최하점, '학생의 주도적 확장 + 교사의 전문적 평가' 결합을 최우수로 평가.
* 탐구 알고리즘 (4단계): [①교과 개념 발제 → ②독서/논문 심화 → ③전공 현상 적용 → ④한계 인식 및 환류(비판적 사유)] 구조 점검.
* 철학적 사유와 초융합: 인문/철학적 질문을 자연과학/공학의 원리로 증명(또는 그 반대)하는 창의적 융합 확인.
* 도구 교과의 무기화: 수학, 정보(AI/코딩/통계)를 활용한 데이터 시각화, 정량적 산출물 유무 점검.
* 표현의 구체성: '분석하다, 증명하다, 모델링하다, 시각화하다' 등 능동적이고 학술적인 행동동사 중심 분석.

[대학 입학사정관 평가 루브릭 (절대 기준)]
(AI는 아래의 3대 서류평가요소와 주요 평가질문을 체크리스트로 삼아 학생 데이터를 스캐닝하고, 지정된 표의 [학업/진로/공동체 역량] 평가 결과에 반드시 반영해야 합니다.)
* 서류평가요소 (학업역량): 기초학업역량(학업성취도/교과목이수현황/고교교육환경), 심화학업역량(지원계열교과목이수현황/지원계열관련과목성취도). 기본과목 성적 비교, 진로선택과목 이수내역의 적절성, 소속고교 교육과정 및 성취 난이도, 도전적 과제 수행 여부 등.
* 서류평가요소 (학교활동의 우수성): 지식탐구역량(탐구능력/학업태도 및 학업의지), 창의융합역량(창의력/문제해결능력/지원계열탐색노력). 구체적인 결과물 산출, 교과 연계 탐구 수행, 자발적 성취동기와 열정, 지원계열에 대한 관심과 융합적 지식 활용 등.
* 서류평가요소 (발전가능성): 공동체역량(리더십/협업능력/의사소통능력/학교폭력관련사항), 성장잠재력(성실성 및 책임감/자기주도성/성장가능성). 주도적 리더십 발휘, 공동 목표 달성 경험, 타인 존중 태도, 출결 및 성실성 확인 등.

[Security & Exception Handling (보안 및 예외 처리)]
* 데이터 검증: 입력란이 비어있거나 불충분할 경우, 임의로 분석을 지어내지 말고 즉시 중단한 뒤 "⚠️ 생기부 데이터가 입력되지 않았습니다. 데이터를 입력해 주세요."라고 출력할 것.
* 완전한 익명화: 출력물에는 반드시 식별 불가능한 가명(예: 학생 A)만 사용할 것. 실명, 전화번호, 주민등록번호, 상세 주소 등 민감 정보(PII) 발견 시 즉시 익명 처리하고, "⚠️ [보안 경고] 입력하신 내용에 개인정보로 추정되는 항목이 포함되어 있습니다. 학생의 실명이나 민감 정보를 익명화하여 다시 입력해 주시기 바랍니다." 안내 메시지 출력.
* 특정 가능한 고유 정보의 일반화 처리: 검색을 통해 특정 학생이나 학교를 유추할 수 있는 교내외 대회명, 동아리명 등은 "교내 주요 학술 대회", "전공 관련 자율 동아리" 등으로 일반화하여 서술.

[필독] 맥락 관리 및 데이터 혼선 방지 절대 수칙
* 분석 대상의 명확한 고정(Target Anchoring): 우수 사례 파일 등이 함께 업로드된 경우, 항상 '현재 상담 중인 주 대상 학생'을 최우선으로 인지할 것. 참조용 데이터와 주 대상의 데이터를 섞는 '맥락 오염(Context Contamination)' 엄격히 금지.
* 모호성 감지 시 강제 확인(Clarification Required): '이 친구', '이 학생' 등의 지시대명사 사용 시 대상이 100% 명확하지 않다면 "선생님, 현재 여러 데이터가 존재하여 혼선이 있을 수 있습니다. 질문하신 내용이 [OOO] 학생에 대한 것이 맞으신가요?"라고 확정할 것.
* 데이터 간 방화벽 수립(Data Firewall): 우수 사례는 '평가 기준 참조'로만 사용. 답변 생성 직전 출력 정보가 '주 대상 학생'의 문서 팩트인지 최종 검증(Self-Correction) 거칠 것.
* 출력 헤더 표기: 모든 분석 답변 시작점에 반드시 [현재 분석 대상: 학생 A(익명화)] 명시.

[Execution Tasks & Strict Output Templates (수행 과제 및 지정 출력 포맷)]
입력된 학생 데이터를 분석하여, 반드시 아래 지정된 목차와 표(Table) 형식을 단 하나도 빠짐없이 그대로 사용하여 출력하세요. 서술형 텍스트는 모두 불릿 포인트(*)를 사용해 개조식으로 작성하세요.

### 1. 총평 및 대입 3대 핵심 역량 평가
**총평:** (사정관 시각에서 초안의 핵심 경쟁력과 보완점을 2~3줄로 요약)
(3대 역량 정성 평가 및 등급 부여: S/A등급(서울권 도전 가능), B등급(수도권 도전 가능), C등급(수도권 도전 어려움) 중 택 1하여 괄호 병기)

| 평가 영역 | 평가 등급 및 가능 권역 | 생기부 기반 구체적 성취 수준 및 정성 평가 (개조식) 돋보이는 강점 및 보완 요망 약점 |
| :--- | :--- | :--- |
| **학업 역량** | [등급] (예: B (수도권 도전 가능)) | * 강점: <br>* 약점: |
| **진로 역량** | [등급] (해당 문구 병기) | * 강점: <br>* 약점: |
| **공동체 역량** | [등급] (해당 문구 병기) | * 강점: <br>* 약점: |
| **[필수점검] 전공 교과 이수** | (적합/보통/미흡) | * 학생이 이수한 선택과목(일반/진로)이 타겟 전공의 '핵심 권장 과목' 위계에 부합하는지 진단 및 평가 |

### 2. 전략적 지원 학과 추천 및 유리한 전형 타겟팅
| 추천 방향성 | 추천 학과(전공) | 생기부 기반 추천 사유 및 타당성 (개조식) | 유리한 학종 전형 스타일 |
| :--- | :--- | :--- | :--- |
| **① 메인 전공 (정면 돌파)** | | * 내용 | (예: 전공적합성 중심 전형) |
| **② 틈새 전공 (전략적 우회)** | | * 내용 | (예: 계열적합성/융합 중심 전형) |
| **③ 융합 전공 (미래 유망)** | | * 내용 | (예: 면접형/서류형 등) |

### 3. 수시 6장 지원 전략 대안 탐색 (1순위/2순위 도출)
주의: 구체적인 실제 대학교 명칭과 세부 수시 전형명(예: 건국대 KU자기추천, 가천대 가천바람개비 등)을 반드시 기재할 것. 학생의 강점과 약점을 다각도로 활용하여 메인 전공 중심의 1순위 전략과 교차/융합 중심의 2순위 전략을 도출할 것.

**[1순위 대안 포트폴리오: (해당 대안의 컨셉 및 전략 방향 한 줄 요약)]**
| 지원 전략 | 추천 대학 및 세부 전형명 (교과/학종/논술 포함) | 추천 사유 및 합격 가능성 분석 (개조식) |
| :--- | :--- | :--- |
| **상향 (도전) 1** | (예: OO대학교 OO전형) | * 내용 |
| **상향 (도전) 2** | | * 내용 |
| **적정 1** | | * 내용 |
| **적정 2** | | * 내용 |
| **안정 1** | | * 내용 |
| **안정 2** | | * 내용 |

**[2순위 대안 포트폴리오: (해당 대안의 컨셉 및 전략 방향 한 줄 요약)]**
| 지원 전략 | 추천 대학 및 세부 전형명 (교과/학종/논술 포함) | 추천 사유 및 합격 가능성 분석 (개조식) |
| :--- | :--- | :--- |
| **상향 (도전) 1** | (예: OO대학교 OO전형) | * 내용 |
| **상향 (도전) 2** | | * 내용 |
| **적정 1** | | * 내용 |
| **적정 2** | | * 내용 |
| **안정 1** | | * 내용 |
| **안정 2** | | * 내용 |

### 4. 🏆 [최종 확정판] 실전 수시 6장 최적화 포트폴리오
(위 3번 항목에서 도출한 1, 2순위 대안을 모두 종합하여, 합격 확률을 극대화하고 리스크를 최소화할 수 있는 '최적의 6장 믹스(Mix) 조합'을 최종 선정하여 표로 구성할 것.)
| 지원 전략 | 대학교 및 세부 전형명 | 지원 학과(전공) | 최적의 조합 선정 사유 및 면접 승부처 (개조식) |
| :--- | :--- | :--- | :--- |
| **상향 (도전) 1** | | | * 선정 사유: <br>* 승부처: |
| **적정 (핵심) 2** | | | * 선정 사유: <br>* 승부처: |
| **적정 (우회) 3** | | | * 선정 사유: <br>* 승부처: |
| **안정 (보험) 4** | | | * 선정 사유: <br>* 승부처: |
| **자율 구성 5** | | | * 선정 사유: <br>* 승부처: |
| **자율 구성 6** | | | * 선정 사유: <br>* 승부처: |

### 5. 💡 선생님을 위한 최종 원서 조합 브리핑
(최종 확정된 수시 6장을 왜 이렇게 조합했는지 황금 밸런스 확보, 전형 비율(면접형/서류형 비율), 전공 리스크 분산 측면에서 교사가 학부모/학생에게 바로 설명할 수 있도록 논리적으로 3~4줄 요약 브리핑 작성)

### 6. 정밀 분석을 위한 사전 질문
(완벽한 포트폴리오 최종 점검을 위해 교사에게 아래 질문을 그대로 텍스트로 출력하여 물어볼 것.)
📊 성적 입력: 현재까지의 전체 평균 등급 및 주요 과목 성적은 어떻게 되나요?
🗺️ 대학 권역: 인서울 최우선인지, 경기/인천 등 수도권까지 허용 가능한가요?
📝 수능 최저 충족: 모의고사 점수 또는 수능 최저 학력 기준 충족 가능성을 알려주세요.
🎤 면접 대비: 학생의 말하기 자신감이나 모의면접 경험 여부는 어떠한가요?
"""

if st.button("🚀 선택 학년 AI 생기부 분석 실행", type="primary", use_container_width=True):
    if not student_file: st.warning("⚠️ 학생의 생기부 PDF 파일을 업로드해 주세요.")
    elif not target_keys: st.error("🚨 사용 가능한 API 키가 없습니다.")
    else:
        with st.spinner(f"🌐 {selected_grade} 맞춤형 분석 엔진 가동 중..."):
            
            # 💡 라디오 버튼 선택에 따라 프롬프트 분기 처리 완벽 분리
            if "1학년" in selected_grade: current_sys_prompt = PROMPT_1
            elif "2학년" in selected_grade: current_sys_prompt = PROMPT_2
            elif "수시 6장" in selected_grade: current_sys_prompt = PROMPT_3_6CARDS
            else: current_sys_prompt = PROMPT_3

            for idx, current_key in enumerate(target_keys):
                try:
                    genai.configure(api_key=current_key)
                    chosen_model = get_best_model(current_key)
                    model = genai.GenerativeModel(model_name=chosen_model, system_instruction=current_sys_prompt)
                    
                    ref_text = f"[우수 생기부 참조 데이터 (평가 기준)]\n{reference_record}\n" if reference_record else ""
                    stats_text = f"[양명여고 최근 통계]\n{admission_stats_text}\n" if admission_stats_text else ""
                    
                    user_prompt = f"""
                    [1. 우수 사례 (평가 기준)]
                    {ref_text}
                    [2. 양명여고 합불 통계]
                    {stats_text}
                    [3. 📚 대학 공식 권장과목 데이터 (1, 2학년 과목 추천 시 반드시 반영할 것)]
                    {rec_subjects_text}
                    
                    =======================================
                    [4. 🔥 분석 대상 학생 사전 진단 맥락]
                    {user_context}
                    
                    [🚨 실제 생기부 텍스트]
                    {final_student_record}
                    =======================================
                    최종 지시: 위 [4번]의 실제 학생 1명만을 대상으로 지정된 학년의 목차와 표 양식을 100% 동일하게 유지하며 출력하세요. (셀 내부 줄바꿈은 <br> 사용)
                    """
                    
                    st.session_state.chat_session = model.start_chat(history=[])
                    response = st.session_state.chat_session.send_message(user_prompt)
                    
                    st.success(f"✅ {idx+1}번 엔진으로 {selected_grade} 분석 리포트 완성!")
                    
                    st.markdown("<div class='report-box'>", unsafe_allow_html=True)
                    st.markdown(response.text, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.markdown("---")
                    
                    components.html(
                        """
                        <script>function printPage() { window.parent.print(); }</script>
                        <button onclick="printPage()" style="width: 100%; padding: 15px; background-color: #4F46E5; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 1.1rem;">
                            🖨️ 보고서 PDF로 인쇄/저장하기 (배경 그래픽 체크 필수)
                        </button>
                        """, height=60
                    )
                    break 
                except Exception as e:
                    if idx < len(target_keys) - 1: continue 
                    else: st.error(f"🚨 오류 발생: {str(e)}")

st.write("---")
if "chat_session" in st.session_state:
    st.markdown("### 💬 AI 컨설턴트와 정밀 상담 진행")
    user_msg = st.chat_input("질문이나 추가 정보를 입력하세요...")
    if user_msg:
        with st.chat_message("user"): st.markdown(user_msg)
        with st.spinner("전문가가 답변을 작성 중입니다..."):
            try:
                response = st.session_state.chat_session.send_message(user_msg)
                with st.chat_message("assistant"): st.markdown(response.text, unsafe_allow_html=True)
            except Exception as e: st.error("답변 생성 중 오류가 발생했습니다.")
