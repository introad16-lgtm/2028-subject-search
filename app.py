import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components

# ==========================================
# 1. 웹 페이지 기본 설정
# ==========================================
st.set_page_config(
    page_title="양명여고 진로진학 통합 시스템",
    page_icon="💖",
    layout="wide"
)

# --- 🎨 전체 사이드바 및 배경 (핑크 & 옐로우) 테마 ---
st.markdown("""
<style>
    /* 전체 배경색을 아주 연한 베이비 핑크로 설정 */
    .stApp {
        background-color: #FFF5F7;
    }
    
    /* 사이드바 배경색 및 텍스트 색상 수정 */
    [data-testid="stSidebar"] {
        background-color: #FEFFED;
        border-right: 2px solid #FFD700;
    }
    
    /* 라디오 버튼 선택 시 핑크색 강조 */
    div.stRadio > div[role="radiogroup"] > label > div:first-child {
        background-color: #FFF5F7;
    }
    div.stRadio > div[role="radiogroup"] > label[data-checked="true"] > div:first-child > div {
        background-color: #FF1493;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 사이드바(메뉴 버튼) 구성
# ==========================================
st.sidebar.markdown("""
    <div style='text-align: center; padding: 10px 0;'>
        <div style='font-size: 2.5rem; margin-bottom: 5px;'>💖🏫💛</div>
        <h2 style='color: #FF1493; font-size: 1.5rem; margin: 0; font-weight: 900; text-shadow: 1px 1px 0px #FFD70033;'>양명여고<br>진로진학부</h2>
    </div>
""", unsafe_allow_html=True)
st.sidebar.divider()

# 메뉴 선택 라디오 버튼
menu = st.sidebar.radio(
    "👉 원하는 기능을 선택하세요:",
    ("🏠 메인 홈 (안내)", "🎓 2028 대학별 권장과목 검색", "🎯 생기부 핀셋 설계 시스템")
)

st.sidebar.divider()
st.sidebar.markdown("<div style='text-align: center; color: #DB2777; font-size: 0.8em; font-weight: 600;'>© 2026 양명여자고등학교 💖</div>", unsafe_allow_html=True)


# ==========================================
# 3. 메뉴별 화면 출력 로직
# ==========================================

# ------------------------------------------
# [메뉴 1] 메인 홈 화면
# ------------------------------------------
if menu == "🏠 메인 홈 (안내)":
    st.markdown("""
        <div style='text-align: center; padding: 40px 0 20px 0;'>
            <div style='font-size: 4rem; margin-bottom: 10px;'>🏫</div>
            <h1 style='color: #FF1493; font-size: 3rem; margin: 0; font-weight: 900; text-shadow: 2px 2px 0px #FFD70033;'>양명여자고등학교 진로진학 포털</h1>
            <p style='color: #CA8A04; font-size: 1.2rem; margin-top: 15px; font-weight: 600;'>학생들의 성공적인 2028학년도 대입을 위한 통합 지원 시스템입니다.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div style='background-color: #FEFFED; padding: 30px; border-radius: 20px; border: 2px solid #FFD700; height: 100%; box-shadow: 0 10px 30px rgba(255, 105, 180, 0.1);'>
                <h3 style='color: #FF1493; margin-top: 0;'>🎓 대학별 권장과목 검색</h3>
                <p style='color: #475569; font-size: 1.1rem; line-height: 1.6;'>학생이 희망하는 <b>대학과 학과</b>를 검색하여, 입학처에서 요구하는 핵심/권장 과목을 빠르게 조회합니다.</p>
                <p style='color: #CA8A04; font-weight: bold; margin-bottom: 0;'>👈 왼쪽 메뉴에서 선택하세요.</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div style='background-color: #FFF0F5; padding: 30px; border-radius: 20px; border: 2px solid #FF69B4; height: 100%; box-shadow: 0 10px 30px rgba(255, 105, 180, 0.1);'>
                <h3 style='color: #FF1493; margin-top: 0;'>🎯 생기부 핀셋 설계 시스템</h3>
                <p style='color: #475569; font-size: 1.1rem; line-height: 1.6;'>양명여고의 <b>핵심 활동</b>을 바탕으로, 학생의 진로와 성향에 맞춘 초개인화 생기부 포트폴리오를 설계하고 PDF로 출력합니다.</p>
                <p style='color: #DB2777; font-weight: bold; margin-bottom: 0;'>👈 왼쪽 메뉴에서 선택하세요.</p>
            </div>
        """, unsafe_allow_html=True)


# ------------------------------------------
# [메뉴 2] 기존 코드: 권장과목 검색기
# ------------------------------------------
elif menu == "🎓 2028 대학별 권장과목 검색":
    
    # --- 기존 검색기 전용 디자인(CSS) ---
    st.markdown("""
    <style>
        /* 1. 검색 버튼을 화사한 비비드 핑크 그라데이션으로 변경 */
        .stButton > button {
            background: linear-gradient(135deg, #FF69B4 0%, #FF1493 100%);
            color: white;
            border: none;
            border-radius: 20px;
            font-weight: bold;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(255, 20, 147, 0.3);
            transition: all 0.3s ease;
            padding: 10px 20px;
        }
        
        /* 버튼 호버 효과: 노란색 광채 */
        .stButton > button:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 6px 20px rgba(255, 215, 0, 0.5);
            color: white;
            background: linear-gradient(135deg, #FF1493 0%, #FF69B4 100%);
        }

        /* 2. 검색창(Form)을 연한 노란색 카드로 변경 */
        [data-testid="stForm"] {
            background-color: #FEFFED;
            border-radius: 20px;
            border: 2px solid #FFD700;
            box-shadow: 0 10px 30px rgba(255, 105, 180, 0.1);
            padding: 30px;
            margin-bottom: 25px;
        }

        /* 3. 입력칸(텍스트 박스) 디자인: 핑크색 포커스 */
        div[data-baseweb="input"] > div {
            border-radius: 10px;
            background-color: white;
            border: 1px solid #FFC0CB;
        }
        
        div[data-baseweb="input"] > div:focus-within {
            border-color: #FF1493;
            box-shadow: 0 0 0 3px rgba(255, 20, 147, 0.2);
        }

        /* 4. 결과 창(Expander) 디자인 */
        [data-testid="stExpander"] {
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid #FFE4E1;
            margin-bottom: 15px;
        }
        
        [data-testid="stExpander"] summary:hover {
            color: #FF1493;
        }

        div[data-testid="stNotification"] {
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    # 2. 헤더 디자인 (핑크 & 옐로우 테마)
    st.markdown("""
    <div style='text-align: center; padding-bottom: 30px;'>
        <h2 style='color: #333; font-size: 2.1rem; margin-top: 5px; font-weight: 700;'>🎓 2028학년도 대학별 권장과목 검색기</h2>
        <p style='color: #64748B; font-size: 1.05rem; margin-top: 12px;'>원하는 대학이나 학과를 입력하고 <b style='color: #FF1493; background-color: #FFD70033; padding: 2px 5px; border-radius: 5px;'>검색하기</b> 버튼을 눌러주세요.</p>
    </div>
    """, unsafe_allow_html=True)

    # 3. 데이터 불러오기 함수
    @st.cache_data
    def load_data():
        file_path = 'data.csv' if os.path.exists('data.csv') else 'data.xlsx'
        if not os.path.exists(file_path):
            st.error("데이터 파일을 찾을 수 없습니다.")
            return pd.DataFrame()
        
        try:
            if file_path.endswith('.csv'):
                try:
                    df = pd.read_csv(file_path, skiprows=2, encoding='utf-8')
                except:
                    df = pd.read_csv(file_path, skiprows=2, encoding='cp949')
            else:
                df = pd.read_excel(file_path, skiprows=2)
                
            df['대학명'] = df.iloc[:, 2].fillna('').astype(str)
            col3 = df.iloc[:, 3].fillna('').astype(str)
            col4 = df.iloc[:, 4].fillna('').astype(str)
            df['모집단위'] = col3 + " " + col4
            df['핵심과목'] = df.iloc[:, 5].fillna('-').astype(str)
            
            if len(df.columns) > 6:
                df['권장과목'] = df.iloc[:, 6].fillna('-').astype(str)
            else:
                df['권장과목'] = '-'
                
            if len(df.columns) > 7:
                df['비고'] = df.iloc[:, 7].fillna('-').astype(str)
            else:
                df['비고'] = '-'

            df = df.replace('nan', '', regex=True)
            df = df.drop_duplicates(subset=['대학명', '모집단위', '핵심과목', '권장과목'], keep='first')
            return df
        except Exception as e:
            st.error(f"파일 오류: {e}")
            return pd.DataFrame()

    df = load_data()

    # 4. 검색 화면 구성
    if not df.empty:
        with st.form("search_form"):
            st.markdown("<h3 style='color: #FF1493; font-size: 1.3rem; margin-bottom: 18px; font-weight: 700;'>🔍 어디를 찾으시나요?</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                u_keyword = st.text_input("💖 대학 이름", placeholder="예: 서울대, 연세대")
            with col2:
                d_keyword = st.text_input("💛 학과/모집단위", placeholder="예: 컴퓨터, 디자인, 간호")
            
            st.write("") 
            submit_button = st.form_submit_button("💖 검색하기 💛", use_container_width=True)

        if submit_button:
            if u_keyword or d_keyword:
                result = df.copy()
                
                if u_keyword:
                    mask1 = result['대학명'].str.contains(u_keyword, na=False, case=False)
                    result = result[mask1]
                if d_keyword:
                    mask2 = result['모집단위'].str.contains(d_keyword, na=False, case=False)
                    result = result[mask2]
                
                if result.empty:
                    st.warning("❌ 검색 결과가 없습니다. 단어를 조금 더 짧게 입력해 보세요.")
                else:
                    st.success(f"✅ 총 **{len(result)}건**의 결과를 찾았습니다.")
                    for _, row in result.iterrows():
                        dept_name = row['모집단위'].strip()
                        with st.expander(f"🏫 [{row['대학명']}] {dept_name}", expanded=True):
                            if row['핵심과목'] and row['핵심과목'] != '-': 
                                st.markdown(f"**📌 핵심과목:** <span style='color: #FF1493; font-weight: bold;'>{row['핵심과목']}</span>", unsafe_allow_html=True)
                            if row['권장과목'] and row['권장과목'] != '-': 
                                st.markdown(f"**💡 권장과목:** <span style='color: #CA8A04; font-weight: bold;'>{row['권장과목']}</span>", unsafe_allow_html=True)
                            
                            has_note = row['비고']
                            note_valid = row['비고'] != '-'
                            if has_note and note_valid: 
                                st.markdown(f"**📝 비고:** {row['비고']}")
            else:
                st.info("💡 대학이나 학과 중 하나라도 입력해 주세요.")
    else:
        st.info("데이터를 불러오는 중이거나 파일이 없습니다.")

    st.markdown("""
        <br><br><br>
        <div style='text-align: center; color: #DB2777; font-size: 0.9rem; border-top: 2px solid #FFC0CB; padding-top: 20px; background-color: #FFF0F5; padding-bottom: 20px; border-radius: 15px 15px 0 0;'>
            © 2026 양명여자고등학교 진로진학부 💖<br>
            <span style='font-size: 0.8rem; color: #CA8A04; font-weight: 600;'>꿈과 미래를 잇는 상큼한 통로 💛</span>
        </div>
    """, unsafe_allow_html=True)


# ------------------------------------------
# [메뉴 3] 신규: 핑크 & 옐로우 테마 생기부 설계기
# ------------------------------------------
elif menu == "🎯 생기부 핀셋 설계 시스템":
    
    html_source_code = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Pretendard', sans-serif; background-color: transparent; color: #1e293b; word-break: keep-all; }
            .gradient-text { background: linear-gradient(135deg, #FF1493, #FFD700); -webkit-background-clip: text; color: transparent; }
            .card-anim { transition: transform 0.2s ease, box-shadow 0.2s ease; }
            .card-anim:hover { transform: translateY(-4px); box-shadow: 0 10px 15px -3px rgba(255, 20, 147, 0.1), 0 4px 6px -2px rgba(255, 20, 147, 0.05); }
            
            .checkbox-pill input { display: none; }
            .checkbox-pill label { 
                display: inline-flex; align-items: center; justify-content: center;
                padding: 0.5rem 1rem; border: 1px solid #FFC0CB; border-radius: 9999px;
                background-color: white; color: #64748b; font-size: 0.85rem; font-weight: 700;
                cursor: pointer; transition: all 0.2s; user-select: none; margin-bottom: 0.3rem;
            }
            /* 전체 켜기 등 버튼 체크 시 핫핑크 */
            .checkbox-pill input:checked + label { background-color: #FF1493; border-color: #FF1493; color: white; box-shadow: 0 4px 6px -1px rgba(255, 20, 147, 0.3); }
            /* 전공 추천 대기 상태 (노랑/골드) */
            .checkbox-pill input.recommended-item + label { border: 2px solid #FFD700; color: #CA8A04; background-color: #FEFFED; }
            /* 전공 추천 체크 시 (골드) */
            .checkbox-pill input.recommended-item:checked + label { background-color: #CA8A04; border-color: #CA8A04; color: white; box-shadow: 0 4px 6px -1px rgba(202, 138, 4, 0.3); }
            .checkbox-pill label:hover { filter: brightness(0.95); }

            .highlight-border { position: relative; border: 2px solid #CA8A04 !important; box-shadow: 0 10px 15px -3px rgba(202, 138, 4, 0.15) !important; }
            
            .topic-pick { transition: all 0.2s; border: 2px solid transparent; cursor: pointer; }
            .topic-pick:hover { background-color: #FFF0F5; border-color: #FFC0CB; }
            .topic-pick.selected { border-color: #FF1493; background-color: #FFF0F5; box-shadow: 0 4px 6px -1px rgba(255, 20, 147, 0.2); }
            .topic-pick .check-icon { opacity: 0; transform: scale(0.5); transition: all 0.2s; }
            .topic-pick.selected .check-icon { opacity: 1; transform: scale(1); color: #FF1493; }

            /* 주도성 라벨 컬러 (핑크 & 옐로우 & 그레이) */
            .tag-lead { background-color: #FF1493; color: white; } 
            .tag-semi { background-color: #CA8A04; color: white; } 
            .tag-part { background-color: #94A3B8; color: white; } 

            @media print {
                body { background: white; padding: 0; }
                #app-view { display: none !important; } 
                #print-view { display: block !important; } 
                .page-break { page-break-inside: avoid; break-inside: avoid; margin-bottom: 2rem; }
                @page { margin: 15mm; }
            }
        </style>
    </head>
    <body>
        <div id="app-view" class="p-4 md:p-8 max-w-6xl mx-auto block print:hidden">
            <header class="text-center mb-8 mt-2">
                <div class="inline-flex items-center gap-2 px-5 py-2 mb-4 text-sm font-bold text-pink-700 bg-pink-50 border border-pink-200 rounded-full">
                    🎯 다변화 학과 & 핀셋 교과 연계 시스템
                </div>
                <h1 class="text-3xl md:text-4xl font-extrabold mb-3 tracking-tight">생기부 <span class="gradient-text">장바구니 & 자동 설계기</span></h1>
                <p class="text-[16px] text-slate-500 font-medium max-w-2xl mx-auto leading-relaxed">
                    학생 주도성이 높은 활동은 전공 뼈대로 밀고 가며,<br><b>가변적인 특강/실습에만 텍스트 엔진이 개입하여 깊이 있는 교과 연계를 제안</b>합니다.
                </p>
            </header>

            <div class="bg-white p-6 md:p-8 rounded-3xl shadow-sm border border-slate-200 mb-8 relative overflow-hidden">
                <div class="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-pink-500 to-yellow-400"></div>

                <div class="flex flex-col md:flex-row gap-5 mb-6 border-b border-pink-100 pb-6 items-end">
                    <div class="w-full md:w-5/12">
                        <label class="block text-sm font-bold text-slate-700 mb-2">1. 희망 계열</label>
                        <select id="track-filter" onchange="onTrackChange()" class="w-full px-4 py-3.5 rounded-xl border-2 border-slate-200 focus:border-pink-500 outline-none font-bold text-slate-700 cursor-pointer bg-slate-50">
                            <option value="">▶ 관심 계열 선택</option>
                            <option value="인문어문">📚 인문/어문 계열</option>
                            <option value="사회상경">💼 사회/상경 계열</option>
                            <option value="자연과학">🔬 자연과학 계열</option>
                            <option value="공학IT">⚙️ 공학/IT 계열</option>
                            <option value="의약보건">🏥 의약/보건 계열</option>
                            <option value="사범교육">🏫 사범/교육 계열</option>
                        </select>
                    </div>
                    
                    <div class="w-full md:w-5/12">
                        <label class="block text-sm font-bold text-slate-700 mb-2">2. 세부 전공 (맞춤 자동 추천)</label>
                        <select id="major-filter" onchange="onMajorChange()" disabled class="w-full px-4 py-3.5 rounded-xl border-2 border-slate-200 focus:border-yellow-500 outline-none font-bold text-pink-700 cursor-pointer bg-slate-50 disabled:opacity-50">
                            <option value="">계열을 먼저 선택하세요</option>
                        </select>
                    </div>

                    <div class="w-full md:w-2/12">
                        <button onclick="generatePDF()" class="w-full h-[52px] bg-gradient-to-r from-pink-500 to-rose-500 hover:from-rose-500 hover:to-pink-600 text-white font-extrabold rounded-xl shadow-md transition-colors flex items-center justify-center gap-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path></svg>
                            PDF 출력
                        </button>
                    </div>
                </div>

                <div id="dynamic-input-panel" style="display: none;" class="w-full mb-6 p-5 bg-yellow-50 rounded-2xl border border-yellow-200">
                    <h4 class="text-sm font-extrabold text-yellow-700 mb-3 flex items-center gap-2">
                        ✨ 현장 변수 입력 (※ 특강 및 과학관 실습 활동에만 실시간 융합됩니다)
                    </h4>
                    <div class="flex flex-col md:flex-row gap-4">
                        <div class="flex-1">
                            <label class="block text-xs font-bold text-slate-600 mb-1">전문직업인 특강 현장 주제 (예: AI 윤리, 빅데이터)</label>
                            <input type="text" id="custom-expert" placeholder="강연 주제나 직업을 입력하세요" class="w-full px-4 py-2.5 rounded-xl border border-yellow-300 text-sm focus:border-pink-500 focus:ring-1 focus:ring-pink-500 outline-none transition-all bg-white" onkeyup="renderContent()">
                        </div>
                        <div class="flex-1">
                            <label class="block text-xs font-bold text-slate-600 mb-1">과학관 실습 장비/기술 (예: 분광기, 유전자 가위)</label>
                            <input type="text" id="custom-science" placeholder="체험한 장비나 기술을 입력하세요" class="w-full px-4 py-2.5 rounded-xl border border-yellow-300 text-sm focus:border-pink-500 focus:ring-1 focus:ring-pink-500 outline-none transition-all bg-white" onkeyup="renderContent()">
                        </div>
                    </div>
                </div>

                <div id="selection-panel" style="display: none;">
                    <div class="flex justify-between items-center mb-4">
                        <label class="block text-sm font-bold text-slate-700">3. 생기부 반영 활동 선택 (전체 13종)</label>
                        <div class="space-x-1">
                            <button onclick="checkRecommended()" class="text-[12px] font-bold bg-yellow-100 text-yellow-700 border border-yellow-300 px-3 py-1.5 rounded-lg hover:bg-yellow-200 transition-colors">★ 전공 추천만 켜기</button>
                            <button onclick="toggleSet('all')" class="text-[12px] font-bold bg-slate-100 text-slate-600 px-3 py-1.5 rounded-lg hover:bg-slate-200 transition-colors">전체 켜기</button>
                            <button onclick="toggleSet('none')" class="text-[12px] font-bold bg-slate-100 text-slate-600 px-3 py-1.5 rounded-lg hover:bg-slate-200 transition-colors">전체 끄기</button>
                        </div>
                    </div>
                    <div id="all-checkboxes" class="flex flex-wrap gap-2"></div>
                </div>
            </div>

            <div id="content-area">
                <div class="text-center py-24 bg-white rounded-3xl border-2 border-dashed border-pink-200 shadow-sm">
                    <span class="text-5xl mb-4 block">🖱️</span>
                    <h3 class="text-2xl font-extrabold text-pink-700 mb-2">세부 전공을 선택해 주세요.</h3>
                    <p class="text-slate-500 font-medium">전공에 맞춘 추천 활동과 <b>과세특 연계 선택지</b>가 표시됩니다.</p>
                </div>
            </div>
        </div>

        <div id="print-view" class="hidden p-8 max-w-4xl mx-auto">
            <div class="text-center border-b-4 border-pink-500 pb-6 mb-8">
                <h1 class="text-3xl font-extrabold text-slate-900 tracking-tight mb-2">2026학년도 학종 맞춤형 핀셋 설계안</h1>
                <p id="print-major-title" class="text-xl font-bold text-pink-600"></p>
                <div class="mt-4 flex justify-between items-end text-sm font-bold text-slate-600">
                    <span>학번/이름 : ______________________</span>
                    <span>출력일 : <span id="print-date"></span></span>
                </div>
            </div>
            <div id="print-content" class="space-y-8"></div>
        </div>

        <script>
            // == 학과 데이터 및 프로그램 로직은 앞서 수정한 내용과 100% 동일하게 유지합니다. ==
            const majorData = {
                "인문어문": {
                    "국어국문학과": { k1: "언어의 사회성과 담화", k2: "혐오 표현과 매체 언어", k3: "건강한 소통 문화", recs: ["p1", "p10"] },
                    "영어영문학과": { k1: "비교문학과 텍스트 분석", k2: "글로벌 언어 패권 현상", k3: "다문화적 이해와 번역", recs: ["p1", "p12"] },
                    "철학과": { k1: "인식론과 실존주의 윤리", k2: "기술 소외와 알고리즘 윤리", k3: "주체적 사유와 자아 확립", recs: ["p1", "p9"] },
                    "사학과": { k1: "사료 교차 검증과 미시사", k2: "역사 왜곡과 정보 편향", k3: "다원적 시각과 객관적 인식", recs: ["p1", "p12"] }
                },
                "사회상경": {
                    "경영학과": { k1: "ESG 지표와 조직 행동론", k2: "기업의 도덕적 해이 사례", k3: "윤리적 가치 창출과 리더십", recs: ["p1", "p13"] },
                    "경제학과": { k1: "행동경제학과 거시 지표", k2: "자원 배분과 플랫폼 독과점", k3: "합리적 시장 효율성 제고", recs: ["p1", "p2"] },
                    "행정학과": { k1: "공공 거버넌스와 행정망", k2: "지방 소멸과 공공 서비스 공백", k3: "투명하고 효율적인 공공 가치", recs: ["p1", "p13"] },
                    "사회학과": { k1: "구조적 불평등과 계층화", k2: "저출산 고령화와 복지 사각지대", k3: "시민 연대와 포용적 공동체", recs: ["p1", "p13"] },
                    "심리학과": { k1: "인지 편향과 발달 심리", k2: "청소년 우울 및 고립 실태", k3: "정서적 연대와 상담 윤리", recs: ["p1", "p8"] },
                    "미디어커뮤니케이션": { k1: "프레이밍 이론과 의제 설정", k2: "확증 편향의 알고리즘 전파", k3: "저널리즘 윤리와 리터러시", recs: ["p1", "p6"] }
                },
                "자연과학": {
                    "수학과": { k1: "대수학 및 위상수학 증명", k2: "알고리즘 암호학과 데이터 보안", k3: "수리적 논증과 패턴 발견", recs: ["p1", "p2"] },
                    "물리학과": { k1: "양자역학과 전자기학", k2: "기초과학 연구 지원의 사각지대", k3: "우주 원리 탐구와 과학 철학", recs: ["p1", "p15"] },
                    "화학과": { k1: "유기 합성 및 반응 동역학", k2: "유해 화학물질과 환경 규제", k3: "안전한 물질 개발과 연구 윤리", recs: ["p1", "p3"] },
                    "생명과학과": { k1: "분자생물학과 유전자 가위", k2: "기후 위기로 인한 생물 다양성 급감", k3: "생태계 보전과 바이오 윤리", recs: ["p1", "p3"] },
                    "지구환경/천문우주": { k1: "지질/대기 순환 및 천체 물리", k2: "기후 재난과 우주 쓰레기 문제", k3: "지속가능한 지구/우주 생태계", recs: ["p15", "p1"] }
                },
                "공학IT": {
                    "컴퓨터공학과": { k1: "자료구조와 알고리즘", k2: "디지털 소외 계층의 정보 격차", k3: "모두를 위한 오픈소스 혁신", recs: ["p1", "p13"] },
                    "인공지능(AI)학과": { k1: "딥러닝과 자연어처리(NLP)", k2: "AI 환각 및 데이터 편향성", k3: "설명 가능한 AI(XAI)와 윤리", recs: ["p1", "p12"] },
                    "기계/항공우주공학": { k1: "열역학 및 전산유체역학(CFD)", k2: "에너지 효율 및 우주 쓰레기", k3: "친환경 모빌리티 설계", recs: ["p1", "p15"] },
                    "전기전자공학과": { k1: "전자기 유도와 반도체 소자", k2: "재생 에너지 전환과 전력망", k3: "에너지 효율 극대화", recs: ["p1", "p3"] },
                    "화학/신소재공학": { k1: "고분자 화합물과 나노 물질", k2: "희토류 무기화와 재활용 한계", k3: "미래 지향적 친환경 신소재", recs: ["p1", "p3"] }
                },
                "의약보건": {
                    "의예/치의예과": { k1: "해부생리학 및 병리기전", k2: "초고령화 및 취약계층 보건", k3: "보편적 의료 질 향상", recs: ["p1", "p13"] },
                    "약학과": { k1: "약동학(ADME) 및 수용체 결합", k2: "항생제 내성 및 의약품 오남용", k3: "안전한 신약 개발과 보건 증진", recs: ["p1", "p12"] },
                    "간호학과": { k1: "근거 기반 간호(EBP) 역량", k2: "신종 감염병 및 인력 번아웃", k3: "환자 중심의 전인적 간호", recs: ["p1", "p9"] }
                },
                "사범교육": {
                    "교육/특수교육과": { k1: "교육과정 설계와 UDL 원리", k2: "입시 위주 교육과 심리적 소외", k3: "다양성을 포용하는 통합 교육", recs: ["p1", "p13"] },
                    "국어/영어교육과": { k1: "언어 습득론 및 매체 언어학", k2: "문해력 저하 및 맹목적 학습", k3: "글로벌 상호이해와 비판적 사고", recs: ["p1", "p10"] },
                    "수학교육과": { k1: "수학적 모델링과 인지 발달", k2: "기계적 문제풀이와 수포자 양산", k3: "논리적 추론과 문제해결 기법", recs: ["p1", "p2"] }
                }
            };

            const allPrograms = [
                { id: "p1", title: "드림업 프로젝트", type: "개인/팀 소논문", leadLabel: "학생 100% 주도", leadClass: "tag-lead",
                  desc: "주제 선정부터 데이터 수집, 가설 검증, 최종 집필까지 학생이 주도하는 최고 난도 연구 활동입니다.",
                  getGroups: (m, c) => [
                      { groupTitle: "📌 [학술·실험 연계]", items: [
                         `<b>[변인 통제 설계]</b> <b>${m.k1}</b> 관련 핵심 가설을 세우고, 직접 통제된 실험 환경에서 데이터를 수집하여 논문 집필`,
                         `<b>[데이터 시뮬레이션]</b> 고교 실험실의 한계를 극복하기 위해 <b>${m.k1}</b> 현상을 파이썬 소프트웨어로 모델링하여 정량적 도출`,
                         `<b>[문헌 메타분석]</b> <b>${m.k1}</b>에 대한 최신 영문 KCI/SCI급 논문 10여 편을 교차 대조하여 기존 이론의 맹점을 고찰`
                      ]},
                      { groupTitle: "📌 [사회·제도 연계]", items: [
                         `<b>[실태 데이터 분석]</b> <b>${m.k2}</b> 문제의 심각성을 증명하기 위해 자체 설문지를 개발하고 표본 데이터를 통계적으로 교차 분석`,
                         `<b>[비교 정책 논증]</b> <b>${m.k2}</b> 해결을 위해 선진국의 법제도 사례를 비교하고 한국형 정책 가이드라인을 제시하는 논문 작성`,
                         `<b>[집단 딜레마 연구]</b> <b>${m.k2}</b>를 둘러싼 이해관계자들의 갈등 구조를 게임이론 관점에서 분석하고 논리적 합의점 도출`
                      ]},
                      { groupTitle: "📌 [실천·공동체 연계]", items: [
                         `<b>[액션 리서치]</b> <b>${m.k3}</b> 가치 실현을 위한 캠페인을 직접 기획/실행하고, 전후 행동 변화를 측정하여 행동 연구 논문 집필`,
                         `<b>[연구 리더십 발휘]</b> 8개월간 팀을 이끌며, <b>${m.k3}</b> 시각을 바탕으로 팀원 간의 학술적 이견을 데이터 기반으로 조율`,
                         `<b>[연구 윤리 고찰]</b> 논문 집필 과정에서 AI와 외부 오픈 데이터를 활용하며 발생한 팩트체크 이슈를 스스로 비판적 수용`
                      ]}
                  ]
                },
                { id: "p13", title: "학생주도 프로젝트 봉사활동", type: "자율 장기기획", leadLabel: "학생 100% 주도", leadClass: "tag-lead",
                  desc: "학기 단위로 스스로 목표를 세우고 전공 특기를 살려 기획/실행하는 완벽한 주도형 활동입니다.",
                  getGroups: (m, c) => [
                      { groupTitle: "📌 [데이터 기반 기획]", items: [
                         `<b>${m.k1}</b> 지식을 바탕으로 봉사 활동 전후의 인식 개선 효과를 통계적 검정(t-test 등)을 통해 증명하는 결과 보고서 제출`,
                         `단순 노동형 봉사를 지양하고, 수혜자의 잠재적 니즈(Needs)를 파악하기 위한 사전 설문 문항을 직접 설계 및 분석`,
                         `목표 달성률 지표(KPI)를 명확히 세우고 학기 말에 활동의 실효성을 객관적으로 평가하는 체계적 포트폴리오 작성`
                      ]},
                      { groupTitle: "📌 [사회 문제 해결]", items: [
                         `지역 사회에 방치된 <b>${m.k2}</b> 문제를 포착하여 일회성이 아닌 학기 단위의 장기 개선 프로젝트 주도`,
                         `단순 물질적 지원이 아니라 소외 계층이 스스로 자립할 수 있는 교육적/기술적 시스템 구축 방안 모색`,
                         `지자체 산하 기관이나 교내 타 동아리와 연계하여 봉사 활동의 융합적 시너지와 사회적 파급력 확장`
                      ]},
                      { groupTitle: "📌 [전공 맞춤 나눔]", items: [
                         `자신의 전공 학업 능력을 살려 <b>${m.k3}</b> 가치를 전파하는 '교학상장(敎學相長)' 형태의 맞춤형 재능 기부 실시`,
                         `정보/학력 취약 계층 대상을 위해 전공 지식을 알기 쉽게 풀어쓴 시각 가이드북이나 멘토링 매뉴얼 직접 제작`,
                         `시혜적인 태도에서 벗어나 수혜자의 입장에 깊이 공감하며 진정성 있는 시민 의식을 체화하는 과정 기록`
                      ]}
                  ]
                },
                { id: "p11", title: "IB 벽화 공모전", type: "자율 융합디자인", leadLabel: "학생 100% 주도", leadClass: "tag-lead",
                  desc: "학교 공간을 캔버스 삼아 자신의 전공 가치와 IB 이념을 시각적으로 주도하여 설계합니다.",
                  getGroups: (m, c) => [
                      { groupTitle: "📌 [설계·기술 연계]", items: [
                         `<b>${m.k1}</b> 개념을 직관적인 인포그래픽으로 시각화하여 지정된 벡터 그래픽 규격을 준수해 도안 제출`,
                         `벽화 설치 시 사용될 페인트 등 재료의 물성, 반사율 및 내구성을 화학/물리적 관점에서 조사한 보고서 작성`,
                         `학교 건물의 채광 시간과 학생들의 시각적 동선을 계산하여 최적의 색채 심리학 원리를 적용한 공간 설계`
                      ]},
                      { groupTitle: "📌 [공간·사회 연계]", items: [
                         `<b>${m.k2}</b> 등 현대 사회의 삭막함을 극복하고 교내 구성원의 정서적 유대감을 높이는 소통 중심의 대안 공간 기획`,
                         `학교를 단순한 건물이 아닌 커뮤니티 허브로 규정하고, 로컬 브랜딩 관점에서 벽화의 사회적 기능 제안`,
                         `벽화 공모 과정 자체를 학생들이 능동적으로 참여하는 '공간 주권(Space Sovereignty)' 확립 과정으로 의미 부여`
                      ]},
                      { groupTitle: "📌 [예술·가치 연계]", items: [
                         `추상적인 IB 교육 철학을 <b>${m.k3}</b> 가치와 접목하여 학우들에게 심미적 영감과 휴식을 주는 스케치안 기획`,
                         `신체적 불편함이나 인지적 차이가 있는 학우들도 동등하게 즐길 수 있는 배리어프리(무장애) 유니버설 디자인 적용`,
                         `일상의 예술 작품이 학생들의 학업 스트레스를 완화하는 정서적 치유(Art Therapy) 기능을 함을 역설하는 설명서 제출`
                      ]}
                  ]
                },
                { id: "p12", title: "독서탐구", type: "자율 자필기록", leadLabel: "학생 100% 주도", leadClass: "tag-lead",
                  desc: "학교가 지정한 책이 아닌, 자신의 관심 분야 도서를 스스로 찾아 심화 탐구하는 주도적 독서입니다.",
                  getGroups: (m, c) => [
                      { groupTitle: "📌 [현상 파고들기]", items: [
                         `독서 중 발생한 <b>${m.k1}</b> 관련 학문적 의문점을 풀기 위해 K-MOOC 등 대학 온라인 강의를 스스로 찾아 듣고 기록`,
                         `국내 번역서의 한계를 느끼고, 저자의 주장을 비판적으로 검증하기 위해 관련된 영문 학술지를 직접 찾아 교차 대조`,
                         `단일 도서 독서에 그치지 않고, 동일 저자의 다른 저서들이나 반대 학파의 책을 계보학적으로 엮어 읽는 집요함 증명`
                      ]},
                      { groupTitle: "📌 [현실 적용 비판]", items: [
                         `도서에 제시된 이상적인 이론이 실제 한국 사회의 <b>${m.k2}</b> 문제를 철저히 간과하고 있음을 데이터로 지적`,
                         `책에서 극찬한 해외의 성공 사례를 국내 실정에 맞게 적용하기 위해 필요한 법적/제도적 보완점 고찰`,
                         `미디어에 의해 왜곡되거나 단편적으로 소비되는 대중 지식을 전공 도서를 통해 논리적으로 바로잡는 심층 비평 작성`
                      ]},
                      { groupTitle: "📌 [성찰 및 내면화]", items: [
                         `독서를 통해 자신이 알던 지식의 한계를 뼈저리게 인정하고, <b>${m.k3}</b> 가치를 내면화하는 지적 겸손함을 기록`,
                         `책 속의 역사적 딜레마나 뼈아픈 실패 사례를 자신의 진로 가치관에 투영하여, '어떤 전문가가 될 것인가'를 서술`,
                         `피상적인 활자 읽기를 넘어, 독서 후 깨달은 바를 일상생활이나 학급 내 작은 실천으로 끈기 있게 적용한 사례`
                      ]}
                  ]
                },
                { id: "p10", title: "이음 책모임", type: "자율 비경쟁토의", leadLabel: "선택적 주도", leadClass: "tag-semi",
                  desc: "공통 주제가 주어지지만, '어떤 책'을 고르고 '어떤 관점'으로 토의를 이끌지는 학생의 선택입니다.",
                  getGroups: (m, c) => [
                      { groupTitle: "📌 [지식 큐레이션]", items: [
                         `조원들이 읽은 각기 다른 책의 파편화된 정보를 <b>${m.k1}</b> 기준으로 체계적으로 분류하여 '주제별 도서 목록 카드' 완성`,
                         `서로 다른 저자의 학술적 주장을 <b>${m.k1}</b> 관점에서 비교 분석하는 모둠 내 벤다이어그램 발표 주도`,
                         `독서 중 발견한 전공 심화 개념을 마인드맵으로 구조화하여 지식이 부족한 조원들에게 설명하고 지식 공유`
                      ]},
                      { groupTitle: "📌 [정보 팩트체크]", items: [
                         `책의 내용이 현실의 <b>${m.k2}</b> 현상과 어떻게 연결되는지 신뢰할 수 있는 학술 논문 출처를 직접 찾아 결합함`,
                         `도서에 인용된 통계 지표나 주장의 원문을 직접 추적하여 과장된 부분을 팩트체크하는 탁월한 정보 활용 역량 발휘`,
                         `주제와 관련된 최신 뉴스 기사를 스크랩하여, 출판 시점과 현재 시점의 갭(Gap)을 메우고 내용의 시대적 한계 보완`
                      ]},
                      { groupTitle: "📌 [소통 및 중재]", items: [
                         `비경쟁 토의 중 <b>${m.k3}</b> 관점을 발휘해 조원들의 상충하는 이견을 부드럽게 요약하고 합의점을 이끌어냄`,
                         `나와 반대되는 주장을 담은 책을 일부러 찾아 읽고, 확증 편향을 깨기 위해 수용적 태도로 비판적 독서 소감문 작성`,
                         `토론의 결론을 '누가 맞고 틀린가'의 논쟁이 아닌, 사회를 위한 '새로운 융합적 대안 도출'이라는 발전적 방향으로 유도`
                      ]}
                  ]
                },
                { id: "p6", title: "스마트폰 이별주간", type: "자율 교내캠페인", leadLabel: "선택적 주도", leadClass: "tag-semi",
                  desc: "학교 행사에 참여하되, '메시지와 진행 방식'을 자치적으로 주도하여 전공과 연결할 수 있습니다.",
                  getGroups: (m, c) => [
                      { groupTitle: "📌 [현상 심층 분석]", items: [
                         `단순 캠페인 참여를 넘어, 기기 과의존을 <b>${m.k1}</b> 관점(알고리즘 중독, 뇌 도파민 보상 회로 등)에서 과학적으로 분석하는 자료 배포`,
                         `학생들의 숏폼 시청 시간과 실제 학업 집중도 간의 상관관계를 통계적으로 교차 분석하는 자체 조사 기획`,
                         `자극적인 미디어 콘텐츠가 청소년의 비판적 사고 발달에 미치는 부정적 영향을 다룬 문헌 리뷰 전시 부스 운영`
                      ]},
                      { groupTitle: "📌 [구조적 대안 제안]", items: [
                         `디지털 과의존이 개인의 의지 문제가 아니라 <b>${m.k2}</b> 문제와 연결되는 플랫폼 기업의 구조적 메커니즘임을 알리는 활동 주도`,
                         `교사의 일방적인 압수 방식 교칙을 비판하고, 학생 자치 법정을 통해 자율적 통제를 유도하는 선진적 교칙 개정안 제안`,
                         `단발성 캠페인에 그치지 않고, 학급 내 미디어 리터러시 및 정보 윤리 교육을 정규 창체 시간에 편성하자는 기획안 발표`
                      ]},
                      { groupTitle: "📌 [소통 행동 촉구]", items: [
                         `<b>${m.k3}</b> 가치를 전면에 내세워 '스마트폰을 끄면 보이는 것들'이라는 긍정적이고 포지티브한 방식의 챌린지 주도`,
                         `디지털 디톡스 기간 동안 오프라인에서 학우들과 눈을 맞추고 대화해야만 해결할 수 있는 게릴라 대면 미션 기획`,
                         `SNS 상의 사이버 폭력 및 익명성 폐해를 극복하기 위해, 오프라인 교내 '칭찬 릴레이 선플 달기' 운동을 자발적으로 전개`
                      ]}
                  ]
                },
                { id: "p9", title: "환경인문독서토론", type: "자율 찬반토론", leadLabel: "선택적 주도", leadClass: "tag-semi",
                  desc: "환경이라는 고정 주제 안에서, 발제와 토론의 '관점(프레임)'을 전공에 맞게 틀어내는 전략이 필요합니다.",
                  getGroups: (m, c) => [
                      { groupTitle: "📌 [학술 프레임 제안]", items: [
                         `환경 도서의 핵심 내용을 단순 수용하지 않고 <b>${m.k1}</b>의 렌즈로 재해석하여, 저자의 논리적 비약이나 한계점을 예리하게 발제`,
                         `기후 위기 예측 모델을 다룬 과학적 데이터의 신뢰성을 통계적으로 교차 검증하여 토론의 학술적 수준을 끌어올림`,
                         `인류세(Anthropocene) 담론을 인간 중심주의에서 벗어나 전공 학문의 생태적 시각으로 재정의하는 심층 에세이 발표`
                      ]},
                      { groupTitle: "📌 [정책 실효성 논증]", items: [
                         `환경 파괴가 유발하는 <b>${m.k2}</b> 문제에 초점을 맞춰, 감정적 호소가 아닌 객관적 데이터 기반의 찬반 토론 주도`,
                         `탄소세 도입 및 글로벌 기업의 그린워싱(Greenwashing) 규제 방안에 대해 경제적/정책적 실효성을 따져 묻는 대안 제안`,
                         `국제 환경 협약이 선진국 중심이며 개발도상국에 미치는 경제적/사회적 불평등 구조를 내포하고 있음을 날카롭게 비판`
                      ]},
                      { groupTitle: "📌 [가치 융합 중재]", items: [
                         `환경 문제를 단순한 과학 기술로만 풀지 않고 <b>${m.k3}</b>이라는 인문학적/윤리적 가치와 결합하여 새로운 패러다임 주장`,
                         `생태 중심주의 철학과 인류의 기술 발전 사이의 극단적 대립을 완화하고, 현실적이고 지속가능한 타협점을 찾는 중재 역할 수행`,
                         `지금 당장의 비용 편익을 넘어, 지속 가능한 미래를 위한 세대 간 정의(Intergenerational Justice)를 전공 개념과 엮어 역설`
                      ]}
                  ]
                },
                { id: "p8", title: "이달의 IB 학습자 상 추천", type: "자율 공동체", leadLabel: "선택적 주도", leadClass: "tag-semi",
                  desc: "추천 양식은 정해져 있으나, '어떤 대상을, 어떤 잣대로' 관찰하여 의미를 부여할지는 학생의 몫입니다.",
                  getGroups: (m, c) => [
                      { groupTitle: "📌 [분석적 관찰]", items: [
                         `학우의 행동을 "착하다"고 단순히 칭찬하지 않고, <b>${m.k1}</b>의 학문적/전문적 잣대로 정밀 분석하여 학술적 근거가 담긴 추천사 작성`,
                         `학업 과정에서 '탐구자(Inquirers)' 역량을 발휘한 학우의 행동 패턴을 교육학/심리학적 관찰 일지 형태로 기록`,
                         `단일 학생의 우수성을 넘어, 교우 관계망 내에서 그 긍정적 영향력이 전파되는 과정을 네트워크 기법으로 구조화하여 분석`
                      ]},
                      { groupTitle: "📌 [리더십 발휘]", items: [
                         `수동적 참여를 넘어, 학급 회의를 열어 <b>${m.k2}</b> 문제를 막기 위해 학습자상 추천 제도를 학급 자치 캠페인으로 확장`,
                         `학급 내 학습자상 추천 참여율을 높이기 위해 행동경제학적 넛지(Nudge) 요소를 활용한 참신한 리워드 시스템 직접 기획`,
                         `소외되거나 돋보이지 않는 조용한 학생들도 골고루 조명받을 수 있도록, 추천의 사각지대 모니터링 체계를 구축하고 주도함`
                      ]},
                      { groupTitle: "📌 [공동체 연대]", items: [
                         `수행평가 등 예민한 갈등 상황에서 <b>${m.k3}</b> 역량으로 이견을 조율하고 팀을 위기에서 구한 학우의 숨은 헌신을 발굴하여 추천`,
                         `'타인을 배려하는 사람(Caring)'의 가치를 우리 반만의 특색 있는 규칙으로 승화시켜 학급 문화로 정착시키는 구심점 역할`,
                         `성적 경쟁 구도에서 벗어나 상호 존중과 협력을 이끄는 성숙하고 포용적인 학급 분위기 조성을 주도함`
                      ]}
                  ]
                },

                // === C. 수동 참여형 (커스텀 동적 키워드 반영 + 과세특/현장 분석 딥 다이브) ===
                { id: "p4", title: "전문직업인 초청 특강", type: "진로 심층Q&A", leadLabel: "의미 부여 집중", leadClass: "tag-part",
                  desc: "[수동 참여형] 강사의 일방적 강연입니다. 상단에 입력한 [강연 주제]를 교과 이론과 대조하여 날카롭게 해부해야 합니다.",
                  getGroups: (m, c) => {
                      const expertTopic = c.expert ? `<span style='color:#FF1493;'>[${c.expert}]</span>` : "해당 분야";
                      return [
                      { groupTitle: `💡 [현장-이론 교차 분석]`, items: [
                         `<b>[교과서의 맹점 지적]</b> 강연자가 언급한 ${expertTopic} 실무 현장의 어려움을 특정 교과서 내의 이상적 이론과 대조하여 분석하는 심층 보고서`,
                         `<b>[데이터 활용 탐색]</b> ${expertTopic} 현장에서 빅데이터나 최신 기술 역량이 어떻게 교과서적 한계를 극복하는지 강연자에게 예리하게 질의`,
                         `<b>[미래 로드맵 재설계]</b> 단순 강연 청취를 넘어, ${expertTopic} 직군이 AI 자동화로 직면할 위기를 <b>${m.k1}</b> 전공 관점에서 돌파할 청사진 제시`
                      ]},
                      { groupTitle: `💡 [정책적 구조 비판]`, items: [
                         `<b>[사회·도덕 과세특 연계]</b> 전문가가 현장에서 겪는 ${expertTopic}의 뼈아픈 구조적 딜레마를 통합사회 교과의 불평등 개념으로 재해석하여 과세특 제출`,
                         `<b>[제도적 맹점 파고들기]</b> ${expertTopic} 문제 해결을 위해 업계에서 요구하는 정책 지원 방향을 묻고, 기존 법안의 사각지대를 논증하는 분석문`,
                         `<b>[국어·영어 과세특 연계]</b> ${expertTopic} 직군의 열악한 환경이나 시스템적 한계를 다룬 비문학 지문/영문 기사를 찾아 교과 발표로 융합 어필`
                      ]},
                      { groupTitle: `💡 [후속 심화 탐구]`, items: [
                         `<b>[관련 논문 자율 탐독]</b> 특강 후 강연자가 지나가듯 언급한 ${expertTopic} 윤리적 쟁점에 꽂혀, 관련된 대학 논문을 스스로 찾아 읽고 서평 제출`,
                         `<b>[자율 동아리 기획]</b> 직업적 가치관인 <b>${m.k3}</b>을 실천하기 위해, 교내에서 ${expertTopic} 관련 문제를 토론하는 자율 스터디 모임을 주도적으로 조직`,
                         `<b>[능동적 진로 개척]</b> 강연 내용을 바탕으로 실제 ${expertTopic} 업계 전문가나 기관에 추가 이메일 인터뷰를 시도하며 집요한 진로 탐색 의지 증명`
                      ]}
                  ]}
                },
                { id: "p3", title: "과천 과학관 실습 프로그램", type: "진로 현장체험", leadLabel: "의미 부여 집중", leadClass: "tag-part",
                  desc: "[수동 참여형] 정해진 기기를 조작합니다. 상단에 입력한 [실습 기기] 측정값의 오차를 교과 개념으로 수학적/과학적으로 증명해야 합니다.",
                  getGroups: (m, c) => {
                      const scienceTopic = c.science ? `<span style='color:#FF1493;'>[${c.science}]</span>` : "실습 장비";
                      return [
                      { groupTitle: `💡 [데이터 오차 증명]`, items: [
                         `<b>[물·화·생·지 과세특 연계]</b> ${scienceTopic} 조작 중 측정한 데이터를 과학 교과의 이상적 수치와 정확히 매칭하고, 오차 발생 원인을 물리학/화학적으로 증명`,
                         `<b>[수학·정보 과세특 연계]</b> ${scienceTopic} 실습 중 발생한 노이즈 데이터를 통계적 방법(표준편차 등)으로 계산하고 코딩으로 보정하는 과세특 탐구`,
                         `<b>[기술 트렌드 비판]</b> 과학관의 ${scienceTopic} 구형 장비와 실제 현대 연구실의 첨단 디지털 장비의 성능 격차를 비교하며 향후 <b>${m.k1}</b> 기술 발전 방향 예측`
                      ]},
                      { groupTitle: `💡 [사회적 파급력 고찰]`, items: [
                         `<b>[통합사회·환경 과세특 연계]</b> ${scienceTopic} 기술이 실제 상용화될 때 발생할 수 있는 <b>${m.k2}</b> 문제를 환경/사회 과목의 수행평가 주제로 선정하여 융합`,
                         `<b>[접근성 한계 지적]</b> ${scienceTopic} 관련 첨단 기술의 특허 현황을 조사하고, 소외 계층의 접근을 막는 독점적 규제 장벽의 문제점 고찰`,
                         `<b>[전시 기획 평가]</b> 단순 견학을 넘어, ${scienceTopic} 전시물의 구성 방식이나 UI가 일반 대중의 과학적 이해도를 얼마나 직관적으로 높이는지 전공 맞춤형 리뷰`
                      ]},
                      { groupTitle: `💡 [후속 심화 탐구]`, items: [
                         `<b>[K-MOOC 연계 수강]</b> ${scienceTopic} 실험 과정에서 교과서 수준을 넘어선 <b>${m.k3}</b> 관련 의문점을 해소하기 위해 대학 교양 강의를 찾아 수강`,
                         `<b>[생활과윤리 과세특 연계]</b> ${scienceTopic} 기술 도입이 유발하는 생명/공학 윤리적 쟁점을 사회 윤리 과세특 토론 주제로 융합하여 철학적 에세이 제출`,
                         `<b>[교내 모의 실험 기획]</b> 과천과학관에서 다룬 ${scienceTopic} 이슈를 교내 과학 동아리로 가져와 제한된 환경에서 변형된 모의 실험을 다시 설계해보는 집요함`
                      ]}
                  ]}
                },
                { id: "p15", title: "이공계 진로캠프(천체 관측)", type: "진로 야간관측", leadLabel: "의미 부여 집중", leadClass: "tag-part",
                  desc: "[수동 참여형] 지정된 야간 관측입니다. 별을 본 감상을 넘어 물리/지구과학 교과의 광학적, 천체역학적 원리로 해석해 내야 합니다.",
                  getGroups: (m, c) => [
                      { groupTitle: "📌 [관측 데이터 수리 모델링]", items: [
                         `<b>[물리·수학 과세특 연계]</b> 천체 망원경의 광학적 배율 및 집광력 원리를 물리 교과서의 파동/광학 단원과 연계하여 수학적으로 모델링한 심층 보고서 제출`,
                         `<b>[지구과학 과세특 연계]</b> 관측한 천체의 위상 변화나 스펙트럼 데이터를 기반으로 대기 굴절에 의한 오차를 계산해내는 지구과학 심화 탐구 일지`,
                         `<b>[정보·알고리즘 연계]</b> 관측 보조용 스마트폰 천문 앱의 구동 원리(자이로센서, AR 매핑 등)를 파악하고 <b>${m.k1}</b> 기술을 접목하여 기존 UI를 개선하는 기획안`
                      ]},
                      { groupTitle: "📌 [공해/산업 거시적 비판]", items: [
                         `<b>[통합사회·환경 과세특 연계]</b> 도심 야간 관측의 치명적 한계인 '빛 공해(Light Pollution)' 현상을 <b>${m.k2}</b> 문제와 연결하여 지자체 조도 규제 정책을 비판하는 수행평가`,
                         `<b>[경제·지리 과세특 연계]</b> 천문학의 발전이 현대 민간 우주 산업(New Space) 생태계와 우주 쓰레기 독점 문제에 미치는 파급력을 다룬 정책/경제 보고서`,
                         `<b>[과학 대중화 기획]</b> 천체 관측의 즐거움을 일반 대중과 나누기 위해, <b>${m.k2}</b> 정보 소외 계층을 타겟으로 한 교내 과학 나눔 멘토링 캠프 세부 기획안 작성`
                      ]},
                      { groupTitle: "📌 [인문학적 후속 확장]", items: [
                         `<b>[철학·국어 과세특 연계]</b> 밤하늘의 별자리를 보며 단순한 호기심을 넘어, 우주 속 인간 존재의 의미와 <b>${m.k3}</b> 가치를 융합적으로 성찰하는 문학적 에세이`,
                         `<b>[미술·창체 연계]</b> 스마트폰으로 직접 촬영한 달과 행성의 천체 사진을 <b>${m.k3}</b> 관점에서 미학적으로 보정하고 분석하여 교내 작은 미니 사진전 주도`,
                         `<b>[생태 보전 독서 연계]</b> 광활한 우주 속 창백한 푸른 점(지구)의 가치를 깨닫고, <b>${m.k3}</b> 실현을 다룬 칼세이건 류의 전문 과학 도서를 찾아 읽는 후속 자율 독서`
                      ]}
                  ]
                },
                { id: "p2", title: "금융 리터러시 아카데미", type: "진로 모둠", leadLabel: "의미 부여 집중", leadClass: "tag-part",
                  desc: "[수동 참여형] 정해진 교안으로 진행되는 특강입니다. 5인의 전담 교사 코칭을 집요하게 활용하여 수학/경제 데이터로 엮어냅니다.",
                  getGroups: (m, c) => [
                      { groupTitle: "📌 [비용-편익 데이터 증명]", items: [
                         `<b>[교사 코칭 집중 활용]</b> 코칭 시간을 전략적으로 활용해 <b>${m.k1}</b> 관련 산업의 잠재적 경제 가치를 장기적 비용-편익(Cost-Benefit) 관점에서 정량적으로 수치화한 보고서`,
                         `<b>[확률과통계 과세특 연계]</b> 수학 시간에 배운 모델링을 활용하여, 특강에 나온 복리/이자율 개념을 <b>${m.k1}</b> 시장 성장성 데이터와 결합해 분석한 산출물 제출`,
                         `<b>[기업 재무 분석]</b> 단순 금융 상식을 넘어, 실제 <b>${m.k1}</b> 관련 기업들의 재무제표 데이터를 바탕으로 투자 타당성과 재무 건전성을 정밀하게 교차 분석`
                      ]},
                      { groupTitle: "📌 [자본 배분 구조 비판]", items: [
                         `<b>[통합사회·경제 과세특 연계]</b> 사회/경제 교과에서 배운 '자본주의 한계' 개념을 바탕으로, 금융 지식이 부족해 <b>${m.k2}</b> 현상을 겪는 취약 계층을 위한 금융 정책 제안서`,
                         `<b>[역사·지리 과세특 연계]</b> 금융 자본의 불균형이 초래하는 <b>${m.k2}</b> 문제를 역사적/지리적 관점의 지역 양극화 개념과 융합하여 구조적으로 비판하는 수행평가 발표`,
                         `<b>[정책 실효성 토론]</b> 강연 내용을 바탕으로 <b>${m.k2}</b> 극복을 위한 정부 보조금 및 조세 정책의 한계를 금융 관점에서 날카롭게 지적하는 교사와의 심층 토론`
                      ]},
                      { groupTitle: "📌 [ESG/소셜 모의 창업]", items: [
                         `<b>[가상 기업 IR 기획]</b> <b>${m.k3}</b> 지향점을 담은 소셜 벤처(사회적 기업)를 설립했다고 가정하고, 크라우드 펀딩을 받기 위한 투자 설명서(IR 피칭덱) 자체 제작 및 발표`,
                         `<b>[후속 자율 독서]</b> <b>${m.k3}</b> 실현을 위해 금융이 어떤 공익적 역할을 해야 하는지 '착한 자본주의' 및 ESG 관련 전문 도서를 도서관에서 찾아 후속 독서 탐구`,
                         `<b>[자율 캠페인 실천]</b> 특강에서 배운 보이스피싱 등 금융 범죄 의식을 바탕으로, 교내 학생들을 대상으로 한 '청소년 금융 사기 예방 캠페인'을 자발적으로 조직`
                      ]}
                  ]
                },

                // --- 3학년 전용 프로그램 (뒤로 배치) ---
                { id: "p5", title: "창의융합 주제탐구 프로젝트", type: "3학년 전용 / 개인세특", leadLabel: "학생 100% 주도", leadClass: "tag-lead",
                  desc: "[3학년] 2개 이상의 교과 성취기준을 융합하여 20장 이내의 최종 보고서를 스스로 기획·작성합니다.",
                  getGroups: (m, c) => [
                      { groupTitle: "📌 [이론·수리 융합]", items: [
                         `수학/과학 성취기준을 융합해 <b>${m.k1}</b>에 대한 고도의 논리적 증명이 담긴 소논문급 융합 보고서 완성`,
                         `단순 문헌 조사를 넘어, 수집한 실험 데이터나 공공 통계 자료를 다변량 분석 기법을 통해 수학적으로 정밀 모델링함`,
                         `교과서의 기본 개념을 전공 수준의 심화 이론으로 확장하여 이질적인 두 과목 간의 연결 고리를 논리적으로 증명하는 압도적 학업 역량`
                      ]},
                      { groupTitle: "📌 [사회·데이터 융합]", items: [
                         `사회/경제 교과 성취기준과 융합하여 <b>${m.k2}</b> 현상의 인과관계를 통계적으로 명확히 밝혀내는 실증적 융합 탐구`,
                         `과거의 역사적 실패 사례와 현대의 사회 구조적 문제를 횡단/종단적으로 비교 분석하여 거시적인 시사점 도출`,
                         `실제 정부의 공공 데이터 포털(API) 원시 자료를 직접 가공 및 인포그래픽으로 시각화하여 독창적인 인사이트 제시`
                      ]},
                      { groupTitle: "📌 [실천·대안 융합]", items: [
                         `<b>${m.k3}</b> 가치를 중심에 두고, 현실의 법이나 제도에 즉시 적용 가능한 정책적 대안 및 입법안 설계`,
                         `인문/윤리 교과와 융합하여 무분별한 첨단 기술 발전이 나아가야 할 바람직하고 윤리적인 미래상에 대한 철학적 에세이 융합`,
                         `다양한 과목의 지식을 단순히 파편적으로 엮는 데 그치지 않고, 하나의 탄탄한 문제 해결 스토리보드로 완결성 있게 구성`
                      ]}
                  ]
                },
                { id: "p7", title: "아침 책 한 장 & 학급 특색", type: "3학년 전용 / 자율", leadLabel: "의미 부여 집중", leadClass: "tag-part",
                  desc: "[3학년] 정해진 아침 독서 시간입니다. 수능 대비를 넘어 특정 교과 '과세특'으로 의미를 연계하여 극대화해야 합니다.",
                  getGroups: (m, c) => [
                      { groupTitle: "📌 [수능 독해 ↔ 과세특 연계]", items: [
                         `<b>[독서·심화국어 과세특]</b> 수능 대비용 최고난도 과학/기술/경제 비문학 지문을 읽고, 이를 <b>${m.k1}</b> 전공 심화 개념과 연결하여 국어 교과 과세특 발표로 연계`,
                         `<b>[진로선택과목 과세특]</b> 아침 독서 중 발견한 지식의 빈틈을 3학년 심화 선택 과목(사회문제탐구, 융합과학 등)의 수행평가 주제로 끌고 와 독서-교과 유기적 융합`,
                         `어려운 문장 구조를 논리적으로 도식화하고 단락별 핵심 개념을 스스로 요약하는 아침 루틴을 형성하여, 입학 후 전공 원서를 읽어낼 탄탄한 독해력 증명`
                      ]},
                      { groupTitle: "📌 [사회 현상 ↔ 윤리/사회 과세특]", items: [
                         `<b>[윤리·사회 과세특]</b> 책에서 비판한 <b>${m.k2}</b> 문제를 교과서의 윤리/사회 이론을 바탕으로 재비판하며 논리적 사고력을 입증하는 과세특 보고서 제출`,
                         `신문 칼럼이나 시사/경제 잡지를 정기 구독하며 복잡한 현대 사회 현상을 보는 날카로운 안목을 기르고, 이를 바탕으로 심화 융합 보고서 작성`,
                         `단순한 전공 지식 암기를 넘어, 사회 구조적 모순에 대해 자신만의 비판적이고 논리적인 견해를 뚜렷하게 서술하는 에세이`
                      ]},
                      { groupTitle: "📌 [수험 생활 ↔ 후속 멘탈 관리]", items: [
                         `<b>[후속 탐구]</b> <b>${m.k3}</b> 가치관을 기르기 위해 읽은 책의 저자 강연이나 다큐멘터리를 공강 시간에 추가로 찾아보며 지식의 폭을 자율적으로 확장`,
                         `아침 독서로 촉발된 지적 호기심을 바탕으로 도서관에서 관련 주제의 상위 호환 도서들을 연쇄적으로 빌려 읽으며 치열한 고3 수험생활의 멘탈을 주도적으로 관리`,
                         `명문대 진학이라는 단기 목표를 넘어 '어떤 어른, 어떤 전문가가 될 것인가'를 고민하며, <b>${m.k3}</b> 실천을 위한 자신의 일상 루틴 개선 계획 수립`
                      ]}
                  ]
                }
            ];

            // ----------------------------------------------------
            // 3. UI 로직
            // ----------------------------------------------------
            window.onTrackChange = function() {
                const track = document.getElementById('track-filter').value;
                const majorSelect = document.getElementById('major-filter');
                const selectionPanel = document.getElementById('selection-panel');
                const dynamicPanel = document.getElementById('dynamic-input-panel');
                
                majorSelect.innerHTML = '<option value="">▶ 세부 전공 선택</option>';
                
                if (track && majorData[track]) {
                    majorSelect.disabled = false;
                    selectionPanel.style.display = 'block';
                    dynamicPanel.style.display = 'block';
                    Object.keys(majorData[track]).forEach(major => {
                        const opt = document.createElement('option');
                        opt.value = major;
                        opt.textContent = major;
                        majorSelect.appendChild(opt);
                    });
                    
                    initCheckboxes();
                    document.getElementById('content-area').innerHTML = `
                        <div class="text-center py-24 bg-white rounded-3xl border-2 border-dashed border-slate-300 shadow-sm no-print">
                            <span class="text-5xl mb-4 block">🖱️</span>
                            <h3 class="text-2xl font-extrabold text-slate-700 mb-2">세부 전공을 선택해 주세요.</h3>
                        </div>`;
                } else {
                    majorSelect.disabled = true;
                    selectionPanel.style.display = 'none';
                    dynamicPanel.style.display = 'none';
                }
            }

            window.onMajorChange = function() {
                const track = document.getElementById('track-filter').value;
                const major = document.getElementById('major-filter').value;
                if(!major) return;

                const mData = majorData[track][major];
                
                const inputs = document.querySelectorAll('.checkbox-pill input');
                inputs.forEach(input => {
                    input.checked = false;
                    input.classList.remove('recommended-item');
                    const label = input.nextElementSibling;
                    label.innerHTML = label.innerHTML.replace('<span class="text-green-600 mr-1">★</span> ', '');
                });

                mData.recs.forEach(recId => {
                    const chk = document.getElementById(`chk_${recId}`);
                    if(chk) {
                        chk.checked = true;
                        chk.classList.add('recommended-item');
                        chk.nextElementSibling.innerHTML = `<span class="text-green-600 mr-1">★</span> ` + chk.nextElementSibling.innerHTML;
                    }
                });

                renderContent();
            }

            window.checkRecommended = function() {
                const track = document.getElementById('track-filter').value;
                const major = document.getElementById('major-filter').value;
                if(!major) return;
                const mData = majorData[track][major];
                
                const inputs = document.querySelectorAll('.checkbox-pill input');
                inputs.forEach(input => {
                    input.checked = mData.recs.includes(input.value);
                });
                renderContent();
            }

            window.toggleSet = function(type) {
                const inputs = document.querySelectorAll('.checkbox-pill input');
                inputs.forEach(input => {
                    if (type === 'all') input.checked = true;
                    else if (type === 'none') input.checked = false;
                });
                renderContent();
            }

            function initCheckboxes() {
                const container = document.getElementById('all-checkboxes');
                container.innerHTML = '';
                allPrograms.forEach(p => {
                    const isSeniorProgram = p.id === "p5" || p.id === "p7";
                    const labelColor = isSeniorProgram ? "text-blue-600 font-extrabold" : "text-slate-600";
                    
                    container.insertAdjacentHTML('beforeend', `
                        <div class="checkbox-pill w-full sm:w-auto">
                            <input type="checkbox" id="chk_${p.id}" value="${p.id}" onchange="renderContent()">
                            <label for="chk_${p.id}" class="w-full sm:w-auto text-left shadow-sm ${labelColor}">${p.title} <span class="text-[10px] font-normal text-slate-400 ml-1">(${p.type})</span></label>
                        </div>
                    `);
                });
            }

            window.toggleTopic = function(element) {
                element.classList.toggle('selected');
            }

            window.renderContent = function() {
                const track = document.getElementById('track-filter').value;
                const major = document.getElementById('major-filter').value;
                const contentArea = document.getElementById('content-area');
                
                if (!major) return;

                const checkedInputs = document.querySelectorAll('.checkbox-pill input:checked');
                const checkedIds = Array.from(checkedInputs).map(el => el.value);

                if (checkedIds.length === 0) {
                    contentArea.innerHTML = `
                    <div class="text-center py-24 bg-white rounded-3xl border-2 border-dashed border-slate-300 shadow-sm no-print">
                        <span class="text-5xl mb-4 block opacity-60">👀</span>
                        <h3 class="text-xl font-bold text-slate-600 mb-2">선택된 활동이 없습니다.</h3>
                        <p class="text-slate-500 text-base">위 패널에서 화면에 표시할 활동을 켜주세요.</p>
                    </div>`;
                    return;
                }

                const mData = majorData[track][major];
                
                const customData = {
                    expert: document.getElementById('custom-expert').value.trim(),
                    science: document.getElementById('custom-science').value.trim()
                };
                
                let html = `
                    <div class="mb-5 flex flex-col md:flex-row justify-between items-center gap-4 bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
                        <div class="flex items-center gap-3">
                            <span class="text-blue-600 text-xl font-extrabold bg-blue-50 px-4 py-1.5 rounded-xl border border-blue-100">${major}</span>
                            <span class="text-slate-500 font-medium text-sm">과세특 연계 솔루션</span>
                        </div>
                        <div class="text-sm font-bold text-blue-600 flex items-center gap-2 bg-blue-50 px-4 py-2 rounded-full border border-blue-100">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122"></path></svg>
                            가장 마음에 드는 구체적인 내용을 직접 클릭(Pick) 하세요!
                        </div>
                    </div>
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">`;

                const checkedPrograms = allPrograms.filter(p => checkedIds.includes(p.id));
                
                checkedPrograms.forEach(p => {
                    const groups = p.getGroups(mData, customData);
                    const isRecommended = mData.recs.includes(p.id);
                    const isSeniorProgram = p.id === "p5" || p.id === "p7";
                    
                    let cardBorder = 'border border-slate-200 shadow-sm';
                    if(isRecommended) cardBorder = 'highlight-border';
                    if(isSeniorProgram && !isRecommended) cardBorder = 'border-2 border-blue-300 shadow-sm';
                    
                    html += `
                        <div class="bg-white rounded-3xl p-6 md:p-8 flex flex-col relative card-anim ${cardBorder}">
                            ${isRecommended ? `<div class="absolute top-0 right-0 bg-green-500 text-white text-[11.5px] font-extrabold px-4 py-1.5 rounded-bl-xl shadow-sm tracking-wide">★ 최우선 추천 (주도성 높음)</div>` : ''}
                            ${isSeniorProgram && !isRecommended ? `<div class="absolute top-0 right-0 bg-blue-500 text-white text-[11px] font-bold px-4 py-1.5 rounded-bl-xl shadow-sm">🎓 3학년 전용 심화</div>` : ''}
                            
                            <div class="flex items-center gap-2 mb-3 mt-1">
                                <span class="text-[11px] font-bold ${p.leadClass} px-2.5 py-1 rounded-md tracking-wide">${p.leadLabel}</span>
                                <span class="text-[11px] font-bold text-slate-500 bg-slate-100 px-2.5 py-1 rounded-md">${p.type}</span>
                            </div>
                            <h3 class="text-[21px] font-extrabold text-slate-800 mb-2 tracking-tight">${p.title}</h3>
                            <p class="text-[13px] text-slate-500 mb-6 font-medium leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-100">${p.desc}</p>
                            
                            <div class="space-y-5">`;
                    
                    groups.forEach(group => {
                        const isCustom = group.groupTitle.includes("💡");
                        const titleClass = isCustom ? "text-green-600 bg-green-50 px-2 py-1 rounded-lg inline-block border border-green-200" : "text-blue-700";
                        
                        html += `
                            <div>
                                <h4 class="text-[14px] font-bold ${titleClass} mb-2.5">${group.groupTitle}</h4>
                                <div class="space-y-2">`;
                        
                        group.items.forEach(item => {
                            html += `
                                    <div class="topic-pick p-3.5 rounded-xl bg-white flex items-start gap-3 group" 
                                         onclick="toggleTopic(this)" 
                                         data-program="${p.title}" 
                                         data-type="${group.groupTitle}" 
                                         data-content='${item.replace(/'/g, "&#39;").replace(/<[^>]*>?/gm, '')}'>
                                        <div class="check-icon mt-0.5 shrink-0">
                                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                                        </div>
                                        <div class="text-[13.5px] text-slate-700 leading-relaxed font-medium pt-0.5 group-hover:text-slate-900">${item}</div>
                                    </div>`;
                        });
                        
                        html += `</div></div>`;
                    });
                    
                    html += `</div></div>`;
                });
                html += `</div>`;
                contentArea.innerHTML = html;
            }

            window.generatePDF = function() {
                const major = document.getElementById('major-filter').value;
                if(!major) {
                    alert("세부 전공을 먼저 선택해 주세요.");
                    return;
                }

                const selectedTopics = document.querySelectorAll('.topic-pick.selected');
                if(selectedTopics.length === 0) {
                    alert("장바구니가 비어있습니다. 화면에서 마음에 드는 상세 주제안을 1개 이상 클릭(Pick)하여 파란색으로 만든 후 다시 눌러주세요!");
                    return;
                }

                const today = new Date();
                document.getElementById('print-date').innerText = `${today.getFullYear()}.${today.getMonth()+1}.${today.getDate()}`;
                document.getElementById('print-major-title').innerText = `[희망 전공: ${major}]`;

                const groupedData = {};
                selectedTopics.forEach(el => {
                    const program = el.getAttribute('data-program');
                    let type = el.getAttribute('data-type');
                    type = type.replace("💡 ", "").replace("📌 ", "");
                    const content = el.getAttribute('data-content');

                    if(!groupedData[program]) groupedData[program] = {};
                    if(!groupedData[program][type]) groupedData[program][type] = [];
                    groupedData[program][type].push(content);
                });

                const printContainer = document.getElementById('print-content');
                let printHtml = '';

                for (const [program, types] of Object.entries(groupedData)) {
                    printHtml += `
                        <div class="page-break bg-slate-50 p-6 rounded-2xl border border-slate-200">
                            <h2 class="text-2xl font-extrabold text-slate-800 mb-4 pb-2 border-b-2 border-slate-300 flex items-center gap-2">
                                <span class="text-blue-600">■</span> ${program}
                            </h2>
                            <div class="space-y-5 pl-2">`;
                    
                    for (const [type, contents] of Object.entries(types)) {
                        printHtml += `
                                <div>
                                    <h3 class="text-[16px] font-bold text-slate-700 mb-2">${type}</h3>
                                    <ul class="list-none space-y-3">`;
                        contents.forEach(content => {
                            printHtml += `
                                        <li class="flex items-start gap-2 text-[15px] text-slate-800 leading-relaxed font-medium">
                                            <span class="text-blue-500 mt-1">✔</span> <span>${content}</span>
                                        </li>`;
                        });
                        printHtml += `</ul></div>`;
                    }
                    printHtml += `</div></div>`;
                }

                printContainer.innerHTML = printHtml;
                window.print();
            }
        </script>
    """

    components.html(html_source_code, height=1200, scrolling=True)
