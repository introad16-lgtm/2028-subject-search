import streamlit as st
import pandas as pd
import os

# 1. 웹 페이지 설정
st.set_page_config(
    page_title="2028 대학별 권장과목 검색기",
    page_icon="🎓",
    layout="centered"
)

# 2. 헤더 디자인 (양명여고 진로진학부 강력 강조)
st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='color: #1E3A8A; font-size: 3.5rem; margin-bottom: 5px;'>🏫 양명여고 진로진학부</h1>
        <h2 style='color: #333; font-size: 1.8rem;'>2028학년도 대학별 권장과목 검색기</h2>
        <p style='color: #666; font-size: 1.1rem;'>원하는 대학이나 학과를 입력하고 <b>'검색하기'</b> 버튼을 눌러주세요.</p>
    </div>
""", unsafe_allow_html=True)

# 3. 데이터 로드 함수 (중복 제거 완벽 반영)
@st.cache_data
def load_data():
    # 파일 확인
    file_path = 'data.csv' if os.path.exists('data.csv') else 'data.xlsx'
    if not os.path.exists(file_path):
        st.error("데이터 파일(data.csv 또는 data.xlsx)을 찾을 수 없습니다.")
        return pd.DataFrame()
    
    try:
        if file_path.endswith('.csv'):
            try:
                df = pd.read_csv(file_path, skiprows=2, encoding='utf-8')
            except:
                df = pd.read_csv(file_path, skiprows=2, encoding='cp949')
        else:
            df = pd.read_excel(file_path, skiprows=2)
            
        # 열 이름 정리
        if 'Unnamed: 4' in df.columns: df = df.drop(columns=['Unnamed: 4'])
        df.rename(columns={'모집단위\n(계열, 단과대, 학과)': '모집단위', '반영과목': '핵심과목', 'Unnamed: 6': '권장과목'}, inplace=True)
        
        # 완전 중복 데이터 제거 (똑같은 내용이 여러 번 나오는 문제 해결)
        df = df.drop_duplicates(subset=['대학명', '모집단위', '핵심과목', '권장과목'], keep='first')
        
        return df.drop(0).reset_index(drop=True).fillna('')
    except Exception as e:
        st.error(f"파일을 읽는 중 오류 발생: {e}")
        return pd.DataFrame()

df = load_data()

# 4. 검색 창 및 버튼 디자인 (st.form 사용)
# 폼을 사용하면 검색어를 다 치고 버튼을 누를 때만 화면이 업데이트됩니다.
with st.form("search_form"):
    st.markdown("### 🔍 어디를 찾으시나요?")
    col1, col2 = st.columns(2)
    
    with col1:
        u_keyword = st.text_input("🏫 대학 이름", placeholder="예: 서울대, 가톨릭대")
    with col2:
        d_keyword = st.text_input("📚 학과/모집단위", placeholder="예: 컴퓨터, 의예, 경영")
    
    # 검색 버튼 (가로 폭 가득 채우기)
    submit_button = st.form_submit_button("🔍 검색하기", use_container_width=True)

# 5. 검색 로직 실행
if submit_button:
    if u_keyword or d_keyword:
        # 검색 시작
        result = df.copy()
        
        if u_keyword:
            result = result[result['대학명'].str.contains(u_keyword, na=False, case=False)]
            
        if d_keyword:
            result = result[result['모집단위'].str.contains(d_keyword, na=False, case=False)]
            
        if result.empty:
            st.warning("❌ 검색 결과가 없습니다. 검색어를 조금 더 짧게 입력해 보세요.")
        else:
            st.success(f"✅ 총 **{len(result)}건**의 검색 결과를 찾았습니다.")
            for _, row in result.iterrows():
                with st.expander(f"🏫 [{row['대학명']}] {row['모집단위']}", expanded=True):
                    if row['핵심과목']: st.markdown(f"**📌 핵심과목:** {row['핵심과목']}")
                    if row['권장과목']: st.markdown(f"**💡 권장과목:** {row['권장과목']}")
                    if row['비고'] and row['비고'] != '-': st.markdown(f"**📝 비고:** {row['비고']}")
    else:
        st.info("💡 대학 이름이나 학과명 중 하나라도 입력해 주세요!")
else:
    # 초기 안내문
    st.info("찾으시는 대학이나 학과를 입력하고 검색 버튼을 눌러주세요.")

# 6. 하단 푸터
st.markdown("""
    <br><br><hr>
    <div style='text-align: center; color: gray; font-size: 0.9rem;'>
        © 2026 양명여자고등학교 진로진학부 | 학생들의 빛나는 미래를 응원합니다.
    </div>
""", unsafe_allow_html=True)
