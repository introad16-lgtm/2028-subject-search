import streamlit as st
import pandas as pd
import os

# 1. 페이지 설정
st.set_page_config(page_title="2028 권장과목 검색", page_icon="🎓", layout="wide")

# 2. ✨검색창 디자인 고도화 (테두리 겹침 해결 버전)✨
st.markdown("""
<style>
    /* 전체 배경 옅은 핑크 */
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 

    /* 🏠 메인 홈 버튼 디자인 */
    .home-btn > button {
        background-color: #FFFFFF !important;
        color: #FF1493 !important;
        border: 2px solid #FFC0CB !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        padding: 5px 20px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 5px rgba(255, 105, 180, 0.1) !important;
        margin-bottom: 10px !important;
    }
    .home-btn > button:hover {
        background-color: #FFF0F5 !important;
        border-color: #FF1493 !important;
        transform: translateY(-2px) !important;
    }

    /* 🎁 검색 폼(박스) 전체 디자인 */
    [data-testid="stForm"] {
        background-color: #FFFFFF !important; 
        border: 3px solid #FFC0CB !important; 
        border-radius: 20px !important; 
        padding: 30px !important;
        box-shadow: 0 8px 20px rgba(255, 105, 180, 0.15) !important; 
    }

    /* ✏️ 입력창(텍스트 박스) 디자인 - 겹침 현상 해결 */
    div[data-baseweb="input"] {
        border: 2px solid #FFD700 !important; /* 기본 골드 테두리 */
        border-radius: 12px !important;
        background-color: #FAFAFA !important;
    }
    
    /* 실제 입력 영역의 기본 테두리 제거 (겹침 방지) */
    div[data-baseweb="input"] > div {
        border: none !important;
        background-color: transparent !important;
    }
    
    /* 입력창 클릭했을 때 (포커스) 효과 - 겹치지 않고 색상만 변경 */
    div[data-baseweb="input"]:focus-within {
        border-color: #FF1493 !important; /* 💖 핫핑크로 변함 */
        box-shadow: 0 0 0 3px rgba(255, 20, 147, 0.2) !important;
    }

    label p {
        font-weight: 800 !important;
        color: #475569 !important;
        font-size: 1.05rem !important;
    }

    /* 🚀 검색하기 버튼 디자인 */
    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #FF69B4 0%, #FFA500 100%) !important; 
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        padding: 10px 0 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 15px rgba(255, 105, 180, 0.3) !important;
        width: 100%;
    }
    [data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 20px rgba(255, 215, 0, 0.4) !important;
        background: linear-gradient(135deg, #FFA500 0%, #FF1493 100%) !important;
    }
</style>
""", unsafe_allow_html=True)

# 홈 버튼
st.markdown('<div class="home-btn">', unsafe_allow_html=True)
if st.button("🏠 메인 화면으로 돌아가기"):
    st.switch_page("app.py")
st.markdown('</div>', unsafe_allow_html=True)

# 3. 상단 헤더
st.markdown("""
<div style='text-align: center; padding-bottom: 30px;'>
    <h1 style='color: #FF1493; font-weight: 900; font-size: 3rem;'>🎓 2028 대학별 권장과목 검색</h1>
    <p style='color: #64748B; font-size: 1.2rem; margin-top: 10px;'>원하시는 대학이나 학과를 입력하고 <b style="color:#FF1493;">검색 버튼</b>을 눌러주세요.</p>
</div>
""", unsafe_allow_html=True)

# 4. 데이터 불러오기 함수
@st.cache_data
def load_data():
    target_filename = "data.xlsx"
    possible_paths = [target_filename, f"../{target_filename}", target_filename.lower(), f"../{target_filename.lower()}"]
    file_path = None
    for path in possible_paths:
        if os.path.exists(path):
            file_path = path
            break
    if not file_path:
        st.error(f"🚨 '{target_filename}' 파일을 찾을 수 없습니다.")
        return pd.DataFrame()
    try:
        df = pd.read_excel(file_path, skiprows=2, engine='openpyxl')
        df['대학명'] = df.iloc[:, 2].fillna('').astype(str)
        df['모집단위'] = df.iloc[:, 3].fillna('').astype(str) + " " + df.iloc[:, 4].fillna('').astype(str)
        df['핵심과목'] = df.iloc[:, 5].fillna('-').astype(str)
        df['권장과목'] = df.iloc[:, 6].fillna('-').astype(str) if len(df.columns) > 6 else '-'
        df['비고'] = df.iloc[:, 7].fillna('-').astype(str) if len(df.columns) > 7 else '-'
        return df.replace('nan', '', regex=True).drop_duplicates(subset=['대학명', '모집단위', '핵심과목', '권장과목'])
    except:
        return pd.DataFrame()

df = load_data()

# 5. 검색 폼 화면
if not df.empty:
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        with col1: 
            # 💡 연세대를 고려대로 변경 완료!
            u_keyword = st.text_input("💖 대학 이름", placeholder="예: 서울대, 고려대")
        with col2: 
            d_keyword = st.text_input("💛 학과 / 모집단위", placeholder="예: 컴퓨터, 간호, 디자인")
        
        st.write("") 
        empty1, btn_col, empty2 = st.columns([1, 2, 1])
        with btn_col:
            submit_button = st.form_submit_button("🔍 권장과목 검색하기 ✨", use_container_width=True)

    if submit_button:
        result = df.copy()
        if u_keyword: result = result[result['대학명'].str.contains(u_keyword, na=False, case=False)]
        if d_keyword: result = result[result['모집단위'].str.contains(d_keyword, na=False, case=False)]
        if result.empty: 
            st.warning("❌ 검색 조건에 맞는 결과가 없습니다.")
        else:
            st.success(f"✅ 총 **{len(result)}건**의 결과를 찾았습니다.")
            for _, row in result.iterrows():
                with st.expander(f"🏫 [{row['대학명']}] {row['모집단위'].strip()}", expanded=True):
                    if row['핵심과목'] != '-': st.markdown(f"**📌 핵심과목:** <span style='color: #FF1493; font-weight: bold;'>{row['핵심과목']}</span>", unsafe_allow_html=True)
                    if row['권장과목'] != '-': st.markdown(f"**💡 권장과목:** <span style='color: #CA8A04; font-weight: bold;'>{row['권장과목']}</span>", unsafe_allow_html=True)
                    if row['비고'] != '-': st.markdown(f"**📝 비고:** {row['비고']}")
