import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="2028학년도 대학별 권장과목 검색기", page_icon="🎓", layout="centered")

st.title("🎓 2028 대학별 권장과목 검색")
st.markdown("컴퓨터와 스마트폰 어디서든 편리하게 검색하세요!")

# 파일 자동 불러오기 함수
@st.cache_data
def load_data():
    # 폴더에 있는 data.csv 또는 data.xlsx를 자동으로 찾습니다.
    if os.path.exists('data.csv'):
        try:
            df = pd.read_csv('data.csv', skiprows=2, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv('data.csv', skiprows=2, encoding='cp949')
    elif os.path.exists('data.xlsx'):
        df = pd.read_excel('data.xlsx', skiprows=2)
    else:
        st.error("데이터 파일을 찾을 수 없습니다. 서버에 data.csv 또는 data.xlsx 파일이 있는지 확인해주세요.")
        return pd.DataFrame()
        
    if 'Unnamed: 4' in df.columns:
        df = df.drop(columns=['Unnamed: 4'])
    df.rename(columns={'모집단위\n(계열, 단과대, 학과)': '모집단위', '반영과목': '핵심과목', 'Unnamed: 6': '권장과목'}, inplace=True)
    
    return df.drop(0).reset_index(drop=True).fillna('')

# 앱 메인 로직
df = load_data()

if not df.empty:
    st.divider()
    st.subheader("🔍 검색 조건")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        search_type = st.radio("검색 기준", ["대학 이름", "학과(모집단위)"], horizontal=False)
    with col2:
        keyword = st.text_input("검색어를 입력하세요", placeholder="예: 가톨릭대, 컴퓨터, 생명")
        
    st.divider()
    
    if keyword:
        result = df[df['대학명'].str.contains(keyword, na=False)] if search_type == "대학 이름" else df[df['모집단위'].str.contains(keyword, na=False)]
            
        if result.empty:
            st.warning("❌ 검색 결과가 없습니다.")
        else:
            st.info(f"✅ 총 **{len(result)}건**의 검색 결과를 찾았습니다.")
            for index, row in result.iterrows():
                with st.container():
                    st.markdown(f"#### 🏫 [{row['대학명']}] {row['모집단위']}")
                    if row['핵심과목']: st.markdown(f"**📌 핵심과목:** {row['핵심과목']}")
                    if row['권장과목']: st.markdown(f"**💡 권장과목:** {row['권장과목']}")
                    if row['비고'] and row['비고'] != '-': st.markdown(f"**📝 비고:** {row['비고']}")
                    st.markdown("---")
