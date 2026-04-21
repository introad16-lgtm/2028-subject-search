import streamlit as st
import pandas as pd
import os
import base64
from PIL import Image
import io

# 1. 웹 페이지 기본 설정
st.set_page_config(
    page_title="2028 대학별 권장과목 검색기",
    page_icon="🎓",
    layout="centered"
)

# --- 로고 이미지를 안전하게 불러오는 함수 ---
def get_image_html():
    # 파일 이름 후보들을 순서대로 찾습니다.
    logo_path = None
    files = ['logo.png', 'logo.jpg', 'logo.jpeg', 'logo.PNG', 'logo.JPG']
    for file_name in files:
        if os.path.exists(file_name):
            logo_path = file_name
            break

    if logo_path:
        try:
            img = Image.open(logo_path)
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            # 로고 크기를 적절하게 조절했습니다.
            return f'<img src="data:image/png;base64,{img_str}" style="height: 60px; margin-right: 15px;">'
        except Exception:
            return ""
    return ""

# 2. 헤더 디자인 (글자 크기를 줄이고 로고와 나란히 배치)
img_html = get_image_html()

st.markdown(f"""
<div style='display: flex; align-items: center; justify-content: center; padding: 20px 0 10px 0;'>
{img_html}
<h1 style='color: #1E3A8A; font-size: 1.6rem; margin: 0; white-space: nowrap;'>양명여고 진로진학부</h1>
</div>
<div style='text-align: center; padding-bottom: 20px;'>
<h2 style='color: #333; font-size: 1.2rem; margin-top: 10px;'>2028학년도 대학별 권장과목 검색기</h2>
<p style='color: #666; font-size: 0.9rem;'>원하는 대학이나 학과를 입력하고 <b>'검색하기'</b> 버튼을 눌러주세요.</p>
</div>
""", unsafe_allow_html=True)

# 3. 데이터 불러오기 함수
@st.cache_data
def load_data():
    file_path = 'data.csv' if os.path.exists('data.csv') else 'data.xlsx'
    if not os.path.exists(file_path):
        st.error("데이터 파일을 찾을 수 없습니다. GitHub에 data.csv 또는 data.xlsx를 올려주세요.")
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
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

df = load_data()

# 4. 검색 화면 구성
if not df.empty:
    with st.form("search_form"):
        st.markdown("### 🔍 검색 조건을 입력하세요")
        col1, col2 = st.columns(2)
        with col1:
            u_keyword = st.text_input("🏫 대학 이름", placeholder="예: 서울대")
        with col2:
            d_keyword = st.text_input("📚 학과/모집단위", placeholder="예: 컴퓨터")
        submit_button = st.form_submit_button("🔍 검색하기", use_container_width=True)

    if submit_button:
        if u_keyword or d_keyword:
            result = df.copy()
            if u_keyword:
                result = result[result['대학명'].str.contains(u_keyword, na=False, case=False)]
            if d_keyword:
                result = result[result['모집단위'].str.contains(d_keyword, na=False, case=False)]
            
            if result.empty:
                st.warning("❌ 검색 결과가 없습니다.")
            else:
                st.success(f"✅ 총 **{len(result)}건**의 결과를 찾았습니다.")
                for _, row in result.iterrows():
                    with st.expander(f"🏫 [{row['대학명']}] {row['모집단위'].strip()}", expanded=True):
                        st.markdown(f"**📌 핵심과목:** {row['핵심과목']}")
                        st.markdown(f"**💡 권장과목:** {row['권장과목']}")
                        if row['비고'] and row['비고'] != '-':
                            st.markdown(f"**📝 비고:** {row['비고']}")
        else:
            st.info("💡 대학이나 학과 중 하나라도 입력해 주세요.")
else:
    st.info("검색을 시작하려면 정보를 입력해 주세요.")

st.markdown("""
    <br><br><hr>
    <div style='text-align: center; color: gray; font-size: 0.8rem;'>
        © 2026 양명여자고등학교 진로진학부 | 꿈과 미래를 잇는 통로
    </div>
""", unsafe_allow_html=True)
