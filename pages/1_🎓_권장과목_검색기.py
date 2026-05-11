import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="2028 권장과목 검색", page_icon="🎓", layout="wide")

st.markdown("<style>.stApp { background-color: #FFF5F7; }</style>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding-bottom: 30px;'>
    <h1 style='color: #FF1493; font-weight: 900;'>🎓 2028 대학별 권장과목 검색</h1>
    <p style='color: #64748B;'>원하는 대학이나 학과를 입력하고 검색 버튼을 눌러주세요.</p>
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
        col1, col2 = st.columns(2)
        with col1: u_keyword = st.text_input("💖 대학 이름", placeholder="예: 서울대")
        with col2: d_keyword = st.text_input("💛 학과/모집단위", placeholder="예: 컴퓨터")
        submit_button = st.form_submit_button("💖 검색하기 💛", use_container_width=True)

    if submit_button:
        result = df.copy()
        if u_keyword: result = result[result['대학명'].str.contains(u_keyword, na=False, case=False)]
        if d_keyword: result = result[result['모집단위'].str.contains(d_keyword, na=False, case=False)]
        
        if result.empty: st.warning("❌ 검색 결과가 없습니다.")
        else:
            st.success(f"✅ 총 **{len(result)}건**의 결과를 찾았습니다.")
            for _, row in result.iterrows():
                with st.expander(f"🏫 [{row['대학명']}] {row['모집단위'].strip()}", expanded=True):
                    st.markdown(f"**📌 핵심과목:** <span style='color: #FF1493; font-weight: bold;'>{row['핵심과목']}</span>", unsafe_allow_html=True)
                    st.markdown(f"**💡 권장과목:** <span style='color: #CA8A04; font-weight: bold;'>{row['권장과목']}</span>", unsafe_allow_html=True)
                    if row['비고'] != '-': st.markdown(f"**📝 비고:** {row['비고']}")
else:
    st.error("데이터 파일을 찾을 수 없습니다.")
