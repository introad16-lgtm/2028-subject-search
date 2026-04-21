import streamlit as st
import pandas as pd
import os
from PIL import Image

# 1. 웹 페이지 설정
st.set_page_config(
    page_title="2028 대학별 권장과목 검색기",
    page_icon="🎓",
    layout="centered"
)

# 2. 로고 이미지와 헤더 출력 (🏫 이모지 대신 선생님의 로고 사용)
# 로고 파일이 서버에 있는지 확인하고 불러옵니다.
col1, col2, col3 = st.columns([1, 2, 1]) # 로고를 중앙에 배치하기 위해 화면을 3칸으로 나눔

with col2: # 가운데 칸에 이미지 배치
    # logo.jpg 또는 logo.png 파일을 찾습니다.
    logo_path = 'logo.jpg' if os.path.exists('logo.jpg') else 'logo.png'
    
    if os.path.exists(logo_path):
        # 이미지가 있으면 띄워줍니다 (가로 폭에 맞게 자동 조절)
        st.image(logo_path, use_column_width=True)
    else:
        # 이미지가 없을 경우를 대비한 예비 텍스트
        st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>양명여고 진로진학부</h1>", unsafe_allow_html=True)

# 그 아래 제목 텍스트 (이제 🏫 이모지는 없습니다)
st.markdown("""
    <div style='text-align: center; padding: 10px;'>
        <h2 style='color: #333; font-size: 1.8rem;'>2028학년도 대학별 권장과목 검색기</h2>
        <p style='color: #666; font-size: 1.1rem;'>원하는 대학이나 학과를 입력하고 <b>'검색하기'</b> 버튼을 눌러주세요.</p>
    </div>
""", unsafe_allow_html=True)

# 3. 데이터 로드 함수 (이전과 동일)
@st.cache_data
def load_data():
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
            
        df['대학명'] = df.iloc[:, 2].fillna('').astype(str)
        col3 = df.iloc[:, 3].fillna('').astype(str)
        col4 = df.iloc[:, 4].fillna('').astype(str)
        df['모집단위'] = col3 + " " + col4
        df['핵심과목'] = df.iloc[:, 5].fillna('-').astype(str)
        
        if len(df.columns) > 6: df['권장과목'] = df.iloc[:, 6].fillna('-').astype(str)
        else: df['권장과목'] = '-'
            
        if len(df.columns) > 7: df['비고'] = df.iloc[:, 7].fillna('-').astype(str)
        else: df['비고'] = '-'

        df = df.replace('nan', '', regex=True)
        df = df.drop_duplicates(subset=['대학명', '모집단위', '핵심과목', '권장과목'], keep='first')
        
        return df
    except Exception as e:
        st.error(f"파일을 읽는 중 오류 발생: {e}")
        return pd.DataFrame()

df = load_data()

# 4. 검색 창 및 버튼 디자인
with st.form("search_form"):
    st.markdown("### 🔍 어디를 찾으시나요?")
    col1, col2 = st.columns(2)
    
    with col1:
        u_keyword = st.text_input("🏫 대학 이름", placeholder="예: 서울대, 동국대")
    with col2:
        d_keyword = st.text_input("📚 학과/모집단위", placeholder="예: 컴퓨터, 반도체, 경영")
    
    submit_button = st.form_submit_button("🔍 검색하기", use_container_width=True)

# 5. 검색 로직 실행
if submit_button:
    if u_keyword or d_keyword:
        result = df.copy()
        
        if u_keyword:
            result = result[result['대학명'].str.contains(u_keyword, na=False, case=False)]
            
        if d_keyword:
            result = result[result['모집단위'].str.contains(d_keyword, na=False, case=False)]
            
        if result.empty:
            st.warning("❌ 검색 결과가 없습니다. 단어를 조금 더 짧게 입력해 보세요. (예: '컴퓨터공학' 대신 '컴퓨터')")
        else:
            st.success(f"✅ 총 **{len(result)}건**의 검색 결과를 찾았습니다.")
            for _, row in result.iterrows():
                dept_name = row['모집단위'].strip()
                with st.expander(f"🏫 [{row['대학명']}] {dept_name}", expanded=True):
                    if row['핵심과목'] and row['핵심과목'] != '-': st.markdown(f"**📌 핵심과목:** {row['핵심과목']}")
                    if row['권장과목'] and row['권장과목'] != '-': st.markdown(f"**💡 권장과목:** {row['권장과목']}")
                    if row['비고'] and row['비고'] != '-': st.markdown(f"**📝 비고:** {row['비고']}")
    else:
        st.info("💡 대학 이름이나 학과명 중 하나라도 입력해 주세요!")
else:
    st.info("찾으시는 대학이나 학과를 입력하고 검색 버튼을 눌러주세요.")

# 6. 하단 푸터
st.markdown("""
    <br><br><hr>
    <div style='text-align: center; color: gray; font-size: 0.9rem;'>
        © 2026 양명여자고등학교 진로진학부 | 학생들의 빛나는 미래를 응원합니다.
    </div>
""", unsafe_allow_html=True)
