import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import json

# 1. 페이지 설정
st.set_page_config(page_title="2028 내신 등급 산출기", page_icon="📊", layout="wide")

# 2. 스트림릿 레이아웃 최적화 CSS (화면 여백 최소화)
st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    .block-container { padding-top: 0rem !important; padding-bottom: 0 !important; max-width: 100% !important; }
</style>
""", unsafe_allow_html=True)

# 3. 홈 버튼
if st.button("🏠 메인 화면으로 돌아가기"):
    st.switch_page("app.py")

# 4. 엑셀 데이터 파싱 및 자바스크립트 주입용 데이터 변환
@st.cache_data
def get_excel_mapping_json():
    target_filename = "수시NAVI(등급변환표 탑재).xlsx"
    possible_paths = [target_filename, f"../{target_filename}", f"pages/{target_filename}"]
    file_path = None
    for path in possible_paths:
        if os.path.exists(path):
            file_path = path
            break
            
    if not file_path:
        return None
        
    try:
        # '기타' 시트에서 G열(5등급 구분, index 6)과 J열(전과목 변환등급, index 9) 추출
        df = pd.read_excel(file_path, sheet_name='기타', header=None, engine='openpyxl')
        mapping = {}
        for i in range(len(df)):
            try:
                g5 = float(df.iloc[i, 6])
                g9 = float(df.iloc[i, 9])
                mapping[f"{g5:.2f}"] = round(g9, 3)
            except:
                continue
        return json.dumps(mapping)
    except:
        return None

conversion_json = get_excel_mapping_json()

if conversion_json is None:
    st.error("🚨 '수시NAVI(등급변환표 탑재).xlsx' 파일을 찾을 수 없습니다.")
    st.info("💡 깃허브 메인 폴더에 엑셀 파일이 올바른 이름으로 업로드되어 있는지 꼭 확인해 주세요!")
    st.stop()

# 5. 선생님의 HTML 원본 소스 구조 보존 및 데이터 연동 (f-string 에러 원천 차단 구조)
raw_html_template = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>2028 양명여고 진학 상담 프로그램</title>
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        @import url('https://webfontworld.github.io/gmarket/GmarketSans.css');
        
        * { box-sizing: border-box; } 
        
        body { 
            font-family: 'Pretendard', 'Malgun Gothic', '맑은 고딕', sans-serif; 
            background: linear-gradient(135deg, #fffdf5 0%, #fff3e0 100%); 
            color: #4a4a4a; margin: 0; padding: 10px;
            min-height: 100vh; line-height: 1.6;
        }

        .container { 
            width: 100%; max-width: 950px; margin: 0 auto; 
            background: #ffffff; padding: 30px 20px; 
            border-radius: 20px; box-shadow: 0 10px 30px rgba(255, 165, 0, 0.1); 
            border: 2px solid #ffe082; 
        }

        .header-wrapper { display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 10px; margin-bottom: 5px; flex-wrap: wrap; }
        .header-logo { height: 35px; width: auto; border-radius: 8px; }
        
        h1 { 
            font-family: 'GmarketSans', sans-serif; 
            background: linear-gradient(to right, #e65100, #e91e63); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-size: 24px; font-weight: bold; margin: 0; text-align: center;
        }
        
        h4 { text-align: center; color: #ff9800; margin-top: 10px; margin-bottom: 20px; font-size: 15px; font-weight: 700; }

        .school-badge { 
            text-align: center; background-color: #fff8e1; color: #d84315; 
            font-weight: 800; padding: 15px; border-radius: 12px; margin-bottom: 25px; 
            font-size: 14px; border: 1px solid #ffe082; 
        }
        .alert-badge { display: block; margin-top: 8px; font-size: 12px; }
