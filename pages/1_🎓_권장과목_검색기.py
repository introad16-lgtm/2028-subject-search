import streamlit as st
import pandas as pd
import os

# 1. 페이지 설정 및 배경
st.set_page_config(page_title="2028 권장과목 검색", page_icon="🎓", layout="wide")

st.markdown("<style>.stApp { background-color: #FFF5F7; }</style>", unsafe_allow_html=True)

# 2. 헤더 디자인
st.markdown("""
<div style='text-align: center; padding-bottom: 30px;'>
    <h1 style='color: #FF1493; font-weight: 900;'>🎓 2028 대학별 권장과목 검색</h1>
    <p style='color: #64748B;'>원하는 대학이나 학과를 입력하고 검색 버튼을 눌러주세요.</p>
</div>
""", unsafe_allow_html=True)

# 3. 똑똑한 데이터 로더 (data.xlsx 전용)
@st.cache_data
def load_data():
    # 찾을 파일 후보군 (상위 폴더 포함)
    target_filename = "data.xlsx"
    possible_paths = [
        target_filename,                # 현재 폴더 (pages/)
        f"../{target_filename}",        # 상위 폴더 (루트)
        target_filename.lower(),        # 소문자 버전
        f"../{target_filename.lower()}" # 상위 폴더 소문자 버전
    ]
    
    file_path = None
    for path in possible_paths:
        if os.path.exists(path):
            file_path = path
            break
            
    if not file_path:
        st.error(f"🚨 '{target_filename}' 파일을 찾을 수 없습니다!")
        # 깃허브에 실제 어떤 파일이 있는지 확인해주는 안내 (선생님 확인용)
        current_files = os.listdir('.')
        parent_files = os.listdir('..') if os.path.exists('..') else []
        st.info(f"📁 현재 위치 파일: {', '.join(current_files)}")
        st.info(f"📁 상위 폴더 파일: {', '.join(parent_files)}")
        return pd.DataFrame()
        
    try:
        # 엑셀 파일 읽기 (skiprows=2는 선생님의 데이터 양식에 맞춘 설정입니다)
        df = pd.read_excel(file_path, skiprows=2, engine='openpyxl')
        
        # 열 이름 정리 (기존 로직 유지)
        df['대학명'] = df.iloc[:, 2].fillna('').astype(str)
        df['모집단위'] = df.iloc[:, 3].fillna('').astype(str) + " " + df.iloc[:, 4].fillna('').astype(str)
        df['핵심과목'] = df.iloc[:, 5].fillna('-').astype(str)
        df['권장과목'] = df.iloc[:, 6].fillna('-').astype(str) if len(df.columns) > 6 else '-'
        df['비고'] = df.iloc[:, 7].fillna('-').astype(str) if len(df.columns) > 7 else '-'
        
        return df.replace('nan', '', regex=True).drop_duplicates(subset=['대학명', '모집단위', '핵심과목', '권장과목'])
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

df = load_data()

# 4. 검색 화면 구성
if not df.empty:
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        with col1: u_keyword = st.text_input("💖 대학 이름", placeholder="예: 서울대")
        with col2: d_keyword = st.text_input("💛 학과/모집단위", placeholder="예: 컴퓨터")
        
        st.write("") 
        
        # 버튼 디자인 (핑크 테마)
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
        </style>
        """, unsafe_allow_html=True)
        
        submit_button = st.form_submit_button("💖 검색하기 💛", use_container_width=True)

    if submit_button:
        result = df.copy()
        if u_keyword: result = result[result['대학명'].str.contains(u_keyword, na=False, case=False)]
        if d_keyword: result = result[result['모집단위'].str.contains(d_keyword, na=False, case=False)]
        
        if result.empty: 
            st.warning("❌ 검색 결과가 없습니다.")
        else:
            st.success(f"✅ 총 **{len(result)}건**의 결과를 찾았습니다.")
            for _, row in result.iterrows():
                with st.expander(f"🏫 [{row['대학명']}] {row['모집단위'].strip()}", expanded=True):
                    if row['핵심과목'] != '-': st.markdown(f"**📌 핵심과목:** <span style='color: #FF1493; font-weight: bold;'>{row['핵심과목']}</span>", unsafe_allow_html=True)
                    if row['권장과목'] != '-': st.markdown(f"**💡 권장과목:** <span style='color: #CA8A04; font-weight: bold;'>{row['권장과목']}</span>", unsafe_allow_html=True)
                    if row['비고'] != '-': st.markdown(f"**📝 비고:** {row['비고']}")
