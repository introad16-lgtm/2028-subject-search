import streamlit as st
import pandas as pd
import os

# 1. 웹 페이지 기본 설정
st.set_page_config(
    page_title="2028 대학별 권장과목 검색기",
    page_icon="🎓",
    layout="centered"
)

# 2. 헤더 디자인 (깨지지 않는 이모지 🏫 사용)
st.markdown("""
<div style='text-align: center; padding: 20px 0 10px 0;'>
    <h2 style='color: #1E3A8A; font-size: 2.1rem; margin: 0;'>🏫 양명여고 진로진학부</h2>
</div>
<div style='text-align: center; padding-bottom: 20px;'>
    <h1 style='color: #333; font-size: 2.3rem; margin-top: 10px;'>2028학년도 대학별 권장과목 검색기</h1>
    <p style='color: #666; font-size: 0.95rem;'>원하는 대학이나 학과를 입력하고 <b>'검색하기'</b> 버튼을 눌러주세요.</p>
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
        st.markdown("### 🔍 어디를 찾으시나요?")
        col1, col2 = st.columns(2)
        with col1:
            u_keyword = st.text_input("🏫 대학 이름", placeholder="예: 서울대")
        with col2:
            d_keyword = st.text_input("📚 학과/모집단위", placeholder="예: 컴퓨터")
        submit_button = st.form_submit_button("🔍 검색하기", use_container_width=True)

    if submit_button:
        if u_keyword or d_keyword:
            result = df.copy()
            
            # 짧은 코드로 분리하여 잘림 방지
            if u_keyword:
                mask1 = result['대학명'].str.contains(u_keyword, na=False, case=False)
                result = result[mask1]
            if d_keyword:
                mask2 = result['모집단위'].str.contains(d_keyword, na=False, case=False)
                result = result[mask2]
            
            if result.empty:
                st.warning("❌ 검색 결과가 없습니다.")
            else:
                st.success(f"✅ 총 **{len(result)}건**의 결과를 찾았습니다.")
                for _, row in result.iterrows():
                    dept_name = row['모집단위'].strip()
                    with st.expander(f"🏫 [{row['대학명']}] {dept_name}", expanded=True):
                        if row['핵심과목'] and row['핵심과목'] != '-': 
                            st.markdown(f"**📌 핵심과목:** {row['핵심과목']}")
                        if row['권장과목'] and row['권장과목'] != '-': 
                            st.markdown(f"**💡 권장과목:** {row['권장과목']}")
                        
                        # 에러가 났던 부분도 짧게 수정 완료!
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
    <br><br><hr>
    <div style='text-align: center; color: gray; font-size: 0.9rem;'>
        © 2026 양명여자고등학교 진로진학부 | 꿈과 미래를 잇는 통로
    </div>
""", unsafe_allow_html=True)
