import streamlit as st
import pandas as pd
import os

# 1. 웹 페이지 기본 설정
st.set_page_config(
    page_title="2028 대학별 권장과목 검색기",
    page_icon="🎓",
    layout="centered"
)

# --- 🎨 디자인 업그레이드 (CSS 마법) ---
st.markdown("""
<style>
    /* 1. 검색 버튼을 입체적이고 예쁜 파란색 그라데이션으로 변경 */
    .stButton > button {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1.1rem;
        box-shadow: 0 4px 10px rgba(30, 58, 138, 0.3);
        transition: all 0.3s ease;
    }
    
    /* 버튼에 마우스를 올렸을 때 살짝 떠오르는 효과 */
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(30, 58, 138, 0.4);
        color: white;
    }

    /* 2. 검색창(Form) 배경을 둥글고 부드러운 카드 형태로 변경 */
    [data-testid="stForm"] {
        border-radius: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        padding: 30px;
        margin-bottom: 20px;
    }

    /* 3. 입력칸(텍스트 박스) 디자인 다듬기 */
    div[data-baseweb="input"] > div {
        border-radius: 8px;
        background-color: #F8FAFC;
    }

    /* 4. 결과 창(Expander)을 예쁜 카드처럼 분리 */
    [data-testid="stExpander"] {
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #F1F5F9;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 2. 헤더 디자인 (여백과 비율을 더 보기 좋게 다듬음)
st.markdown("""
<div style='text-align: center; padding: 30px 0 15px 0;'>
    <div style='font-size: 3rem; margin-bottom: 10px;'>🏫</div>
    <h1 style='color: #1E3A8A; font-size: 2.2rem; margin: 0; font-weight: 800;'>양명여고 진로진학부</h1>
</div>
<div style='text-align: center; padding-bottom: 30px;'>
    <h2 style='color: #333; font-size: 1.3rem; margin-top: 5px; font-weight: 600;'>2028학년도 대학별 권장과목 검색기</h2>
    <p style='color: #64748B; font-size: 1rem; margin-top: 10px;'>원하는 대학이나 학과를 입력하고 <b style='color: #1E3A8A;'>검색하기</b> 버튼을 눌러주세요.</p>
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
        st.markdown("<h3 style='color: #1E293B; font-size: 1.2rem; margin-bottom: 15px;'>🔍 어디를 찾으시나요?</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            u_keyword = st.text_input("🏫 대학 이름", placeholder="예: 서울대, 고려대")
        with col2:
            d_keyword = st.text_input("📚 학과/모집단위", placeholder="예: 컴퓨터, 경영, 의예")
        
        st.write("") # 버튼 위아래 여백 조금 추가
        submit_button = st.form_submit_button("🔍 검색하기", use_container_width=True)

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
                            st.markdown(f"**📌 핵심과목:** <span style='color: #D97706; font-weight: bold;'>{row['핵심과목']}</span>", unsafe_allow_html=True)
                        if row['권장과목'] and row['권장과목'] != '-': 
                            st.markdown(f"**💡 권장과목:** <span style='color: #059669; font-weight: bold;'>{row['권장과목']}</span>", unsafe_allow_html=True)
                        
                        has_note = row['비고']
                        note_valid = row['비고'] != '-'
                        if has_note and note_valid: 
                            st.markdown(f"**📝 비고:** {row['비고']}")
        else:
            st.info("💡 대학이나 학과 중 하나라도 입력해 주세요.")
else:
    st.info("데이터를 불러오는 중이거나 파일이 없습니다.")

# 5. 하단 푸터
st.markdown("""
    <br><br><br>
    <div style='text-align: center; color: #94A3B8; font-size: 0.85rem; border-top: 1px solid #E2E8F0; padding-top: 20px;'>
        © 2026 양명여자고등학교 진로진학부<br>
        <span style='font-size: 0.75rem;'>꿈과 미래를 잇는 통로</span>
    </div>
""", unsafe_allow_html=True)
