import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import streamlit.components.v1 as components

# ==========================================
# 1. 웹 페이지 기본 설정 및 API 연결
# ==========================================
st.set_page_config(
    page_title="양명여고 진로진학 통합 시스템",
    page_icon="💖",
    layout="wide"
)

# Secrets 금고에서 Gemini API 키 꺼내기
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    api_status = True
except Exception as e:
    api_status = False

# ==========================================
# 2. 핑크 & 옐로우 전체 테마 CSS
# ==========================================
st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; }
    [data-testid="stSidebar"] {
        background-color: #FEFFED;
        border-right: 2px solid #FFD700;
    }
    div.stRadio > div[role="radiogroup"] > label > div:first-child { background-color: #FFF5F7; }
    div.stRadio > div[role="radiogroup"] > label[data-checked="true"] > div:first-child > div { background-color: #FF1493; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 사이드바 (메뉴 구성)
# ==========================================
st.sidebar.markdown("""
    <div style='text-align: center; padding: 10px 0;'>
        <div style='font-size: 2.5rem; margin-bottom: 5px;'>💖🏫💛</div>
        <h2 style='color: #FF1493; font-size: 1.5rem; margin: 0; font-weight: 900; text-shadow: 1px 1px 0px #FFD70033;'>양명여고<br>진로진학부</h2>
    </div>
""", unsafe_allow_html=True)
st.sidebar.divider()

menu = st.sidebar.radio(
    "👉 원하는 기능을 선택하세요:",
    ("🎓 2028 대학별 권장과목 검색", "🎯 AI 생기부 핀셋 설계 시스템")
)

st.sidebar.divider()
st.sidebar.markdown("<div style='text-align: center; color: #DB2777; font-size: 0.8em; font-weight: 600;'>© 2026 양명여자고등학교 💖</div>", unsafe_allow_html=True)


# ==========================================
# 4. [메뉴 1] 권장과목 검색기 (선생님 원본 코드)
# ==========================================
if menu == "🎓 2028 대학별 권장과목 검색":
    
    st.markdown("""
    <style>
        .stButton > button {
            background: linear-gradient(135deg, #FF69B4 0%, #FF1493 100%);
            color: white; border: none; border-radius: 20px; font-weight: bold; font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(255, 20, 147, 0.3); transition: all 0.3s ease; padding: 10px 20px;
        }
        .stButton > button:hover {
            transform: translateY(-3px) scale(1.02); box-shadow: 0 6px 20px rgba(255, 215, 0, 0.5);
            color: white; background: linear-gradient(135deg, #FF1493 0%, #FF69B4 100%);
        }
        [data-testid="stForm"] {
            background-color: #FEFFED; border-radius: 20px; border: 2px solid #FFD700;
            box-shadow: 0 10px 30px rgba(255, 105, 180, 0.1); padding: 30px; margin-bottom: 25px;
        }
        div[data-baseweb="input"] > div { border-radius: 10px; background-color: white; border: 1px solid #FFC0CB; }
        div[data-baseweb="input"] > div:focus-within { border-color: #FF1493; box-shadow: 0 0 0 3px rgba(255, 20, 147, 0.2); }
        [data-testid="stExpander"] { background-color: white; border-radius: 12px; border: 1px solid #FFE4E1; margin-bottom: 15px; }
        [data-testid="stExpander"] summary:hover { color: #FF1493; }
    </style>
    <div style='text-align: center; padding-bottom: 30px;'>
        <h2 style='color: #333; font-size: 2.1rem; margin-top: 5px; font-weight: 700;'>🎓 2028학년도 대학별 권장과목 검색기</h2>
        <p style='color: #64748B; font-size: 1.05rem; margin-top: 12px;'>원하는 대학이나 학과를 입력하고 <b style='color: #FF1493; background-color: #FFD70033; padding: 2px 5px; border-radius: 5px;'>검색하기</b> 버튼을 눌러주세요.</p>
    </div>
    """, unsafe_allow_html=True)

    @st.cache_data
    def load_data():
        file_path = 'data.csv' if os.path.exists('data.csv') else 'data.xlsx'
        if not os.path.exists(file_path): return pd.DataFrame()
        try:
            if file_path.endswith('.csv'):
                try: df = pd.read_csv(file_path, skiprows=2, encoding='utf-8')
                except: df = pd.read_csv(file_path, skiprows=2, encoding='cp949')
            else: df = pd.read_excel(file_path, skiprows=2)
            df['대학명'] = df.iloc[:, 2].fillna('').astype(str)
            df['모집단위'] = df.iloc[:, 3].fillna('').astype(str) + " " + df.iloc[:, 4].fillna('').astype(str)
            df['핵심과목'] = df.iloc[:, 5].fillna('-').astype(str)
            df['권장과목'] = df.iloc[:, 6].fillna('-').astype(str) if len(df.columns) > 6 else '-'
            df['비고'] = df.iloc[:, 7].fillna('-').astype(str) if len(df.columns) > 7 else '-'
            return df.replace('nan', '', regex=True).drop_duplicates(subset=['대학명', '모집단위', '핵심과목', '권장과목'])
        except: return pd.DataFrame()

    df = load_data()

    if not df.empty:
        with st.form("search_form"):
            st.markdown("<h3 style='color: #FF1493; font-size: 1.3rem; margin-bottom: 18px; font-weight: 700;'>🔍 어디를 찾으시나요?</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1: u_keyword = st.text_input("💖 대학 이름", placeholder="예: 서울대, 연세대")
            with col2: d_keyword = st.text_input("💛 학과/모집단위", placeholder="예: 컴퓨터, 디자인, 간호")
            submit_button = st.form_submit_button("💖 검색하기 💛", use_container_width=True)

        if submit_button:
            if u_keyword or d_keyword:
                result = df.copy()
                if u_keyword: result = result[result['대학명'].str.contains(u_keyword, na=False, case=False)]
                if d_keyword: result = result[result['모집단위'].str.contains(d_keyword, na=False, case=False)]
                if result.empty: st.warning("❌ 검색 결과가 없습니다.")
                else:
                    st.success(f"✅ 총 **{len(result)}건**의 결과를 찾았습니다.")
                    for _, row in result.iterrows():
                        with st.expander(f"🏫 [{row['대학명']}] {row['모집단위'].strip()}", expanded=True):
                            if row['핵심과목'] != '-': st.markdown(f"**📌 핵심과목:** <span style='color: #FF1493; font-weight: bold;'>{row['핵심과목']}</span>", unsafe_allow_html=True)
                            if row['권장과목'] != '-': st.markdown(f"**💡 권장과목:** <span style='color: #CA8A04; font-weight: bold;'>{row['권장과목']}</span>", unsafe_allow_html=True)
                            if row['비고'] != '-': st.markdown(f"**📝 비고:** {row['비고']}")
            else: st.info("💡 대학이나 학과 중 하나라도 입력해 주세요.")
    else: st.info("데이터를 불러오는 중입니다. data.csv 파일을 확인해주세요.")

# ==========================================
# 5. [메뉴 2] AI 생기부 핀셋 설계기 (제미나이 연동)
# ==========================================
elif menu == "🎯 AI 생기부 핀셋 설계 시스템":
    st.markdown("""
    <div style='text-align: center; padding-bottom: 20px;'>
        <h2 style='color: #FF1493; font-size: 2.3rem; margin-top: 0; font-weight: 800;'>🎯 AI 생기부 핀셋 설계 시스템</h2>
        <p style='color: #64748B; font-size: 1.1rem;'>입력하신 현장 주제를 <b>제미나이 AI</b>가 실시간으로 분석하여 전공 맞춤형 세특을 창작합니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # UI 입력창
    col1, col2 = st.columns(2)
    with col1:
        major_sel = st.selectbox("📚 1. 학생의 희망 전공 선택", ["국어국문학과", "영어영문학과", "경영학과", "경제학과", "미디어커뮤니케이션", "수학과", "화학과", "생명과학과", "컴퓨터공학과", "인공지능(AI)학과", "기계/항공우주공학", "의예/치의예과", "간호학과", "교육/특수교육과"])
    with col2:
        expert_inp = st.text_input("🎙️ 2. 전문직업인 특강 현장 주제", placeholder="예: 인공지능 윤리, 범죄 프로파일링")
        science_inp = st.text_input("🔬 3. 과천과학관 실습 기기/기술", placeholder="예: 적외선 분광기, 유전자 가위")

    st.markdown("""
    <style>
        .ai-button > button {
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            color: #b00020; border: none; border-radius: 20px; font-weight: 900; font-size: 1.2rem;
            box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4); padding: 15px 20px;
        }
        .ai-button > button:hover { background: linear-gradient(135deg, #FFA500 0%, #FFD700 100%); color: #b00020; transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="ai-button">', unsafe_allow_html=True)
    ai_run = st.button("✨ 제미나이 AI 실시간 창작 및 설계기 열기 ✨", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if ai_run:
        if not api_status:
            st.error("🚨 API 키가 연결되지 않았습니다. 관리자 대시보드 Secrets 설정을 다시 확인해주세요.")
        elif not expert_inp and not science_inp:
            st.warning("💡 특강 주제나 과학관 실습 기기 중 최소 1개는 입력해야 AI가 창작할 수 있습니다!")
        else:
            exp_topic = expert_inp if expert_inp else "해당 전공 진로 특강"
            sci_topic = science_inp if science_inp else "첨단 과학 기술 실습"
            
            with st.spinner("✨ 구글 제미나이 AI가 현장 주제를 분석하고 있습니다... (약 5~10초 소요)"):
                prompt = f"""
                너는 양명여고 진로진학 전문 컨설턴트야.
                학생의 희망 전공: {major_sel}
                
                1. 전문직업인 특강 주제: [{exp_topic}]
                이 특강을 들은 학생이 전공({major_sel})과 연결하여 교과세특이나 후속 탐구로 쓸 수 있는 매우 구체적이고 학술적인 심화 탐구 활동 3가지를 각각 1줄(50자 이내)로 짧게 적어줘.
                
                2. 과천과학관 실습 기기: [{sci_topic}]
                이 실습을 한 학생이 전공({major_sel})과 연결하여 데이터 오차 증명 또는 사회적 파급력에 관해 쓸 수 있는 과세특 탐구 활동 3가지를 각각 1줄(50자 이내)로 짧게 적어줘.
                
                규칙: 반드시 구분자 '|'로만 6개의 문장을 구분해서 답변해. 인사말이나 다른 말은 절대 금지.
                형식: 특강문장1|특강문장2|특강문장3|실습문장1|실습문장2|실습문장3
                """
                
                try:
                    response = model.generate_content(prompt)
                    res_text = response.text.strip().split('|')
                    
                    # AI가 응답을 제대로 못했을 경우를 대비한 기본값
                    if len(res_text) < 6:
                        res_text = [f"AI 생성 지연: {exp_topic} 탐구 1", "탐구 2", "탐구 3", f"AI 생성 지연: {sci_topic} 실습 1", "실습 2", "실습 3"]
                    
                    # HTML 템플릿에 AI 창작 문장 삽입 (핑크/옐로우 테마 적용)
                    html_template = """
                    <!DOCTYPE html>
                    <html lang="ko">
                    <head>
                        <meta charset="UTF-8">
                        <script src="https://cdn.tailwindcss.com"></script>
                        <style>
                            body { font-family: sans-serif; background: transparent; }
                            .topic-pick { transition: all 0.2s; border: 2px solid #FFE4E1; cursor: pointer; padding: 12px; border-radius: 12px; margin-bottom: 8px; background: white; }
                            .topic-pick:hover { background-color: #FFF0F5; border-color: #FFC0CB; }
                            .topic-pick.selected { border-color: #FF1493; background-color: #FFF0F5; box-shadow: 0 4px 6px -1px rgba(255, 20, 147, 0.2); }
                            .check-icon { opacity: 0; color: #FF1493; }
                            .topic-pick.selected .check-icon { opacity: 1; }
                            
                            .btn-print { background: linear-gradient(135deg, #FF69B4, #FF1493); color: white; padding: 12px 24px; border-radius: 12px; font-weight: bold; width: 100%; text-align: center; cursor: pointer; display: block; margin-top: 20px;}
                            @media print { body { padding: 0; } #app-view { display: none !important; } #print-view { display: block !important; } }
                        </style>
                    </head>
                    <body>
                        <div id="app-view">
                            <div class="bg-yellow-50 p-5 rounded-2xl border-2 border-yellow-300 mb-6">
                                <h3 class="text-lg font-bold text-pink-600 mb-2">✨ 제미나이 AI 맞춤 창작 완료!</h3>
                                <p class="text-sm text-slate-600 font-bold mb-1">희망 전공: SELECT_MAJOR</p>
                                <p class="text-sm text-slate-600 font-bold mb-1">입력한 특강: EXPERT_TOPIC</p>
                                <p class="text-sm text-slate-600 font-bold">입력한 실습: SCIENCE_TOPIC</p>
                            </div>
                            
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div class="bg-white p-6 rounded-2xl border border-pink-200 shadow-sm relative">
                                    <div class="absolute top-0 right-0 bg-pink-500 text-white text-xs font-bold px-3 py-1 rounded-bl-lg">AI 창작</div>
                                    <h4 class="text-lg font-extrabold text-slate-800 mb-4">🎙️ 전문직업인 초청 특강 연계</h4>
                                    
                                    <div class="topic-pick group" onclick="this.classList.toggle('selected')" data-prog="특강 연계" data-txt="AI_EXP_1">
                                        <div class="flex gap-2"><span class="check-icon">✔</span><span class="text-sm">AI_EXP_1</span></div>
                                    </div>
                                    <div class="topic-pick group" onclick="this.classList.toggle('selected')" data-prog="특강 연계" data-txt="AI_EXP_2">
                                        <div class="flex gap-2"><span class="check-icon">✔</span><span class="text-sm">AI_EXP_2</span></div>
                                    </div>
                                    <div class="topic-pick group" onclick="this.classList.toggle('selected')" data-prog="특강 연계" data-txt="AI_EXP_3">
                                        <div class="flex gap-2"><span class="check-icon">✔</span><span class="text-sm">AI_EXP_3</span></div>
                                    </div>
                                </div>

                                <div class="bg-white p-6 rounded-2xl border border-yellow-300 shadow-sm relative">
                                    <div class="absolute top-0 right-0 bg-yellow-500 text-white text-xs font-bold px-3 py-1 rounded-bl-lg">AI 창작</div>
                                    <h4 class="text-lg font-extrabold text-slate-800 mb-4">🔬 과천과학관 실습 연계</h4>
                                    
                                    <div class="topic-pick group" onclick="this.classList.toggle('selected')" data-prog="실습 연계" data-txt="AI_SCI_1">
                                        <div class="flex gap-2"><span class="check-icon">✔</span><span class="text-sm">AI_SCI_1</span></div>
                                    </div>
                                    <div class="topic-pick group" onclick="this.classList.toggle('selected')" data-prog="실습 연계" data-txt="AI_SCI_2">
                                        <div class="flex gap-2"><span class="check-icon">✔</span><span class="text-sm">AI_SCI_2</span></div>
                                    </div>
                                    <div class="topic-pick group" onclick="this.classList.toggle('selected')" data-prog="실습 연계" data-txt="AI_SCI_3">
                                        <div class="flex gap-2"><span class="check-icon">✔</span><span class="text-sm">AI_SCI_3</span></div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="btn-print" onclick="generatePDF()">마음에 드는 문장 클릭(Pick) 후 PDF 출력하기 🖨️</div>
                        </div>

                        <div id="print-view" class="hidden p-8">
                            <h2 style="color:#FF1493; border-bottom: 2px solid #FFD700; padding-bottom:10px;">2026학년도 AI 맞춤형 생기부 설계안</h2>
                            <p style="font-weight:bold; color:gray;">희망 전공: SELECT_MAJOR</p>
                            <div id="print-content" style="margin-top:20px;"></div>
                        </div>

                        <script>
                            function generatePDF() {
                                const picks = document.querySelectorAll('.topic-pick.selected');
                                if(picks.length === 0) { alert("항목을 먼저 클릭(Pick) 해주세요!"); return; }
                                
                                let html = '';
                                picks.forEach(p => {
                                    html += `<div style="margin-bottom:15px;">
                                        <h4 style="color:#CA8A04; margin-bottom:5px;">■ ${p.getAttribute('data-prog')}</h4>
                                        <p style="background:#FFF5F7; padding:10px; border-radius:8px;">✔ ${p.getAttribute('data-txt')}</p>
                                    </div>`;
                                });
                                document.getElementById('print-content').innerHTML = html;
                                window.print();
                            }
                        </script>
                    </body>
                    </html>
                    """
                    
                    # 문자열 교체로 데이터 바인딩
                    final_html = html_template.replace("SELECT_MAJOR", major_sel).replace("EXPERT_TOPIC", exp_topic).replace("SCIENCE_TOPIC", sci_topic)
                    final_html = final_html.replace("AI_EXP_1", res_text[0]).replace("AI_EXP_2", res_text[1]).replace("AI_EXP_3", res_text[2])
                    final_html = final_html.replace("AI_SCI_1", res_text[3]).replace("AI_SCI_2", res_text[4]).replace("AI_SCI_3", res_text[5])
                    
                    st.success("✅ 창작 완료! 아래에서 카드를 확인하세요.")
                    components.html(final_html, height=800, scrolling=True)

                except Exception as e:
                    st.error(f"AI 창작 중 오류가 발생했습니다: {e}")
