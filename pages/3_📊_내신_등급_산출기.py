import streamlit as st
import streamlit.components.v1 as components
import os

# 1. 페이지 설정
st.set_page_config(page_title="2028 내신 등급 산출기", page_icon="📊", layout="wide")

# 2. 홈 버튼 및 여백 제거 CSS (스트림릿 레이아웃 최적화)
st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    
    /* 화면 위아래 쓸데없는 여백 싹 제거 */
    .block-container { padding-top: 1rem !important; padding-bottom: 0 !important; max-width: 100% !important; }
    
    /* 🏠 메인 홈 버튼 디자인 */
    .home-btn > button {
        background-color: #FFFFFF !important;
        color: #FF1493 !important;
        border: 2px solid #FFC0CB !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        padding: 5px 20px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 5px rgba(255, 105, 180, 0.1) !important;
        margin-bottom: 10px !important;
    }
    .home-btn > button:hover {
        background-color: #FFF0F5 !important;
        border-color: #FF1493 !important;
        transform: translateY(-2px) !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 홈 버튼
st.markdown('<div class="home-btn">', unsafe_allow_html=True)
if st.button("🏠 메인 화면으로 돌아가기"):
    st.switch_page("app.py")
st.markdown('</div>', unsafe_allow_html=True)

# 4. 선생님의 HTML 원본 파일을 직접 읽어와서 네이티브로 띄웁니다!
target_filename = "양명 등급.html"

# 여러 경로에서 파일을 찾도록 안전장치 마련
possible_paths = [
    target_filename, 
    f"../{target_filename}", 
    f"pages/{target_filename}"
]

file_path = None
for path in possible_paths:
    if os.path.exists(path):
        file_path = path
        break

if file_path:
    # 파일을 읽어서 화면에 렌더링
    with open(file_path, "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # 높이를 넉넉하게 주어 스크롤바가 생기지 않도록 설정 (단위 px)
    components.html(html_code, height=1800, scrolling=True)
else:
    # 파일을 못 찾았을 때 안내 메시지
    st.error(f"🚨 '{target_filename}' 파일을 찾을 수 없습니다.")
    st.info("💡 선생님, 깃허브의 가장 바깥쪽 폴더(app.py가 있는 곳)에 '양명 등급.html' 파일이 정확한 이름으로 업로드되어 있는지 확인해 주세요!")
