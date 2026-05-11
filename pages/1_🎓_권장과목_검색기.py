import streamlit as st
import pandas as pd
import os

# 1. 페이지 설정
st.set_page_config(page_title="2028 권장과목 검색", page_icon="🎓", layout="wide")

# 2. ✨검색창 맞춤형 화사한 핑크 & 옐로우 CSS 마법✨
st.markdown("""
<style>
    /* 전체 배경 옅은 핑크 */
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 

    /* 🎁 검색 폼(박스) 전체 디자인 */
    [data-testid="stForm"] {
        background-color: #FFFFFF !important; /* 하얀색 배경 */
        border: 3px solid #FFC0CB !important; /* 연한 핑크색 테두리 */
        border-radius: 20px !important; /* 둥근 모서리 */
        padding: 30px !important;
        box-shadow: 0 8px 20px rgba(255, 105, 180, 0.15) !important; /* 예쁜 그림자 */
    }

    /* ✏️ 입력창(텍스트 박스) 디자인 */
    div[data-baseweb="input"] > div {
        background-color: #FAFAFA !important;
        border: 2px solid #FFD700 !important; /* 💛 상큼한 골드색 테두리 */
        border-radius: 12px !important;
        transition: all 0.3s ease;
    }
    
    /* 입력창 클릭했을 때 (포커스) 효과 */
    div[data-baseweb="input"] > div:focus-within {
        border-color: #FF1493 !important; /* 💖 핫핑크로 변함 */
        box-shadow: 0 0 0 3px rgba(255, 20, 147, 0.2) !important;
    }

    /* 입력창 위 제목(라벨) 글씨 진하게 */
    label p {
        font-weight: 800 !important;
        color: #475569 !important;
        font-size: 1.05rem !important;
    }

    /* 🚀 검색하기 버튼 디자인 */
    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #FF69B4 0%, #FFA500 100%) !important; /* 핑크->오렌지 그라데이션 */
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
    
    /* 버튼 마우스 올렸을 때 효과 */
    [data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 20px rgba(255, 215, 0, 0.4) !important;
        background: linear-gradient(135deg, #FFA500 0%, #FF1493 100%) !important;
    }
    
    /* 버튼 안의 글씨 색상 고정 */
    [data-testid="stFormSubmitButton"] button p {
        color: white !important;
        font-size: 1.2rem !important;
        margin: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

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
    possible_paths = [
        target_filename,                
        f"../{target_filename}",        
        target_filename.lower(),        
        f"../{target_filename.lower()}" 
    ]
    
    file_path = None
    for path in possible_paths:
        if os.path.exists(path):
            file_path = path
            break
            
    if not file_path:
        st.error(f"🚨 '{target_filename}' 파일을 찾을 수 없습니다. 깃허브에 파일이 있는지 확인해주세요.")
        return pd.DataFrame()
        
    try:
        df = pd.read_excel(file_path, skiprows=2, engine='openpyxl')
        df['대학명'] = df.iloc[:, 2].fillna('').astype(str)
        df['모집단위'] = df.iloc[:, 3].fillna('').astype(str) + " " + df.iloc[:, 4].fillna('').astype(str)
        df['핵심과목'] = df.iloc[:, 5].fillna('-').astype(str)
        df['권장과목'] = df.iloc[:, 6].fillna('-').astype(str) if len(df.columns) > 6 else '-'
        df['비고'] = df.iloc[:, 7].fillna('-').astype(str) if len(df.columns) > 7 else '-'
        return df.replace('nan', '', regex=True).drop_duplicates(subset=['대학명', '모집단위', '핵심과목', '권장과목'])
    except Exception as e:
        st.error(f"데이터를 읽는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

df = load_data()

# 5. 예쁜 검색 폼 화면
if not df.empty:
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        with col1: 
            # 💡 양명대 예시 삭제!
            u_keyword = st.text_input("💖 대학 이름", placeholder="예: 서울대, 연세대")
        with col2: 
            d_keyword = st.text_input("💛 학과 / 모집단위", placeholder="예: 컴퓨터, 간호, 디자인")
        
        st.write("") # 간격 살짝 띄우기
        
        # 💡 버튼을 가운데로 예쁘게 정렬하는 마법 (양옆에 빈 공간 넣기)
        empty1, btn_col, empty2 = st.columns([1, 2, 1])
        with btn_col:
            submit_button = st.form_submit_button("🔍 권장과목 검색하기 ✨", use_container_width=True)

    # 검색 결과 로직
    if submit_button:
        result = df.copy()
        if u_keyword: result = result[result['대학명'].str.contains(u_keyword, na=False, case=False)]
        if d_keyword: result = result[result['모집단위'].str.contains(d_keyword, na=False, case=False)]
        
        if result.empty: 
            st.warning("❌ 검색 조건에 맞는 결과가 없습니다.")
        else:
            st.success(f"✅ 총 **{len(result)}건**의 결과를 찾았습니다.")
            for _, row in result.iterrows():
                # 결과 박스 (Expander)
                with st.expander(f"🏫 [{row['대학명']}] {row['모집단위'].strip()}", expanded=True):
                    if row['핵심과목'] != '-': st.markdown(f"**📌 핵심과목:** <span style='color: #FF1493; font-weight: bold;'>{row['핵심과목']}</span>", unsafe_allow_html=True)
                    if row['권장과목'] != '-': st.markdown(f"**💡 권장과목:** <span style='color: #CA8A04; font-weight: bold;'>{row['권장과목']}</span>", unsafe_allow_html=True)
                    if row['비고'] != '-': st.markdown(f"**📝 비고:** {row['비고']}")
