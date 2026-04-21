import streamlit as st
import pandas as pd
import os
import base64
from PIL import Image
import io

# 1. 웹 페이지 설정
st.set_page_config(
    page_title="2028 대학별 권장과목 검색기",
    page_icon="🎓",
    layout="centered"
)

# --- 확장자 상관없이 이미지를 무조건 표준 PNG로 읽어오는 함수 ---
def get_image_html():
    logo_path = None
    for file_name in ['logo.png', 'logo.jpg', 'logo.jpeg', 'logo.PNG', 'logo.JPG']:
        if os.path.exists(file_name):
            logo_path = file_name
            break

    if logo_path:
        try:
            img = Image.open(logo_path)
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            # 🌟 로고 크기도 글자에 맞춰 80px -> 60px로 살짝 줄여 비율을 맞췄습니다.
            return f'<img src="data:image/png;base64,{img_str}" style="height: 60px; margin-right: 15px;">'
        except Exception:
            return ""
    return ""

# 2. 헤더 디자인 (글자 크기 축소 및 밸런스 조절)
img_html = get_image_html()

st.markdown(f"""
<div style='display: flex; align-items: center; justify-content: center; padding: 20px 0 10px 0;'>
{img_html}
<h1 style='color: #1E3A8A; font-size: 1.8rem; margin: 0; white-space: nowrap;'>양명여고 진로진학부</h1>
</div>
<div style='text-align: center; padding-bottom: 20px;'>
<h2 style='color: #333; font-size: 1.3rem; margin-top: 10px;'>2028학년도 대학별 권장과목 검색기</h2>
<p style='color: #666; font-size: 0.95rem;'>원하는 대학이나 학과를 입력하고 <b>'검색하기'</b> 버튼을 눌러주세요.</p>
</div>
""", unsafe_allow_html=True)

# 3. 데이터 로드 함수
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
        df['핵심과목'] = df.iloc
