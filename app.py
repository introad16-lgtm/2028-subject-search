import streamlit as st
from PIL import Image

# 1. 웹 페이지 설정 (기본 유지)
st.set_page_config(
    page_title="나만의 검색기",
    page_icon="🎓",
    layout="centered"
)

# 2. 로고 이미지 넣기
# 💡 'logo.png' 부분을 선생님의 이미지 파일 이름으로 바꿔주세요.
try:
    image = Image.open('logo.png') 
    # use_column_width=True로 설정하면 이미지 크기를 화면 너비에 맞춰 보기 좋게 조절해 줍니다.
    st.image(image, use_column_width=True) 
except FileNotFoundError:
    st.error("⚠️ 로고 이미지 파일을 찾을 수 없습니다. 파일 이름이 'logo.png'인지, app.py와 같은 폴더에 있는지 확인해 주세요.")

# 3. 다른 내용 추가
st.title("🏫 검색기를 만들어보세요!")
# ... 나머지 코드 ...
