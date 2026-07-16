import streamlit as st
import pandas as pd
import os

# 1. 페이지 설정
st.set_page_config(page_title="2028 내신 정밀 산출 및 변환기", page_icon="📊", layout="wide")

# 2. 디자인 및 여백 최적화 CSS
st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    .block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; max-width: 1000px !important; }
    
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
    
    /* 🎁 입력 폼 디자인 */
    [data-testid="stForm"] {
        background-color: #FFFFFF !important; 
        border: 3px solid #FFC0CB !important; 
        border-radius: 20px !important; 
        padding: 30px !important;
        box-shadow: 0 8px 20px rgba(255, 105, 180, 0.15) !important; 
    }
    
    /* 🚀 변환 버튼 디자인 */
    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #FF69B4 0%, #FFA500 100%) !important; 
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        padding: 10px 0 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 15px rgba(255, 105, 180, 0.3) !important;
        width: 100%;
    }
    [data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 20px rgba(255, 215, 0, 0.4) !important;
    }
    
    /* 결과 박스 디자인 */
    .result-box {
        background-color: white;
        border: 3px solid #2563EB;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.15);
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 3. 홈 버튼
st.markdown('<div class="home-btn">', unsafe_allow_html=True)
if st.button("🏠 메인 화면으로 돌아가기"):
    st.switch_page("app.py")
st.markdown('</div>', unsafe_allow_html=True)

# 4. 헤더
st.markdown("""
<div style='text-align: center; padding-bottom: 30px;'>
    <h1 style='color: #FF1493; font-weight: 900; font-size: 3rem;'>📊 2028 수시NAVI 등급 변환기</h1>
    <p style='color: #64748B; font-size: 1.2rem; margin-top: 10px;'>선생님께서 업로드하신 <b>'수시NAVI(등급변환표)'</b> 데이터를 바탕으로 정밀 변환합니다.</p>
</div>
""", unsafe_allow_html=True)

# 5. 엑셀 데이터 파싱 함수 (캐싱 적용으로 속도 최적화)
@st.cache_data
def load_conversion_data():
    target_filename = "수시NAVI(등급변환표 탑재).xlsx"
    possible_paths = [target_filename, f"../{target_filename}"]
    file_path = None
    for path in possible_paths:
        if os.path.exists(path):
            file_path = path
            break
            
    if not file_path:
        return None
        
    try:
        # 선생님 엑셀의 '기타' 시트에 있는 매핑 로직을 읽어옵니다.
        # (5등급 값은 G열(index 6), 9등급 전과목 변환값은 J열(index 9)에 위치)
        df = pd.read_excel(file_path, sheet_name='기타', header=None, engine='openpyxl')
        mapping = {}
        for i in range(len(df)):
            try:
                g5 = float(df.iloc[i, 6])
                g9 = float(df.iloc[i, 9])
                mapping[round(g5, 2)] = g9
            except:
                continue
        return mapping
    except Exception as e:
        return None

conversion_map = load_conversion_data()

# 6. 메인 입력 폼
with st.form("grade_form"):
    st.markdown("<h3 style='color: #334155;'>📝 5등급제 내신 입력</h3>", unsafe_allow_html=True)
    g5_input = st.number_input("학생의 현재 5등급제 내신을 입력하세요 (예: 1.50)", min_value=1.0, max_value=5.0, value=1.50, step=0.01)
    
    st.write("")
    submit_button = st.form_submit_button("✨ 9등급제 보정 산출하기")

# 7. 변환 실행 로직
if submit_button:
    if conversion_map is None:
        st.error("🚨 '수시NAVI(등급변환표 탑재).xlsx' 파일을 찾을 수 없습니다. 파일이 정확한 위치에 있는지 확인해 주세요.")
    else:
        g5_rounded = round(g5_input, 2)
        
        # 딕셔너리 매핑 룩업 (동일 값이 없으면 가장 가까운 상위 값 매핑)
        if g5_rounded in conversion_map:
            g9_result = conversion_map[g5_rounded]
        else:
            closest_keys = sorted(conversion_map.keys())
            g9_result = None
            for k in closest_keys:
                if k >= g5_rounded:
                    g9_result = conversion_map[k]
                    break
            if g9_result is None:
                g9_result = conversion_map[closest_keys[-1]]

        # 변환 결과 시각화 UI
        st.markdown(f"""
        <div class='result-box'>
            <h3 style='color: #64748B; font-weight: 700; margin-bottom: 20px;'>🔍 수시NAVI 알고리즘 분석 결과</h3>
            <div style='display: flex; justify-content: center; align-items: center; gap: 30px;'>
                <div style='background-color: #F8FAFC; padding: 20px; border-radius: 15px; width: 40%;'>
                    <p style='color: #94A3B8; font-size: 1.1rem; margin: 0;'>입력된 5등급제</p>
                    <h2 style='color: #FF1493; margin: 5px 0; font-size: 2.5rem; font-weight: 900;'>{g5_input:.2f}</h2>
                </div>
                <h1 style='color: #CBD5E1; font-size: 3rem;'>▶</h1>
                <div style='background-color: #EFF6FF; padding: 20px; border-radius: 15px; width: 40%;'>
                    <p style='color: #3B82F6; font-size: 1.1rem; margin: 0; font-weight: bold;'>9등급제 보정 컷</p>
                    <h2 style='color: #1D4ED8; margin: 5px 0; font-size: 2.8rem; font-weight: 900;'>{g9_result:.2f}</h2>
                </div>
            </div>
            <p style='color: #475569; margin-top: 25px; font-size: 1.05rem;'>
                💡 위 점수는 <b>일반고 기준 5등급간 석차 누적비</b>를 정밀 분석하여<br>대학 입학사정관들이 바라보는 <b>'실질적 9등급제 환산 점수'</b>입니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # [세션 상태 저장] - 이 변수가 나중에 수시 6장 분석기 등 다른 탭으로 넘어갈 수 있습니다!
        st.session_state['converted_9_grade'] = g9_result
