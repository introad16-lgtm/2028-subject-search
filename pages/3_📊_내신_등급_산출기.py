import streamlit as st
import pandas as pd
import os

# 1. 페이지 설정
st.set_page_config(page_title="2028 내신 정밀 산출 및 변환기", page_icon="📊", layout="wide")

# 2. 선생님의 디자인을 스트림릿 네이티브로 완벽 이식하는 CSS
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    @import url('https://webfontworld.github.io/gmarket/GmarketSans.css');
    
    /* 전체 테마 및 폰트 적용 */
    .stApp { 
        background: linear-gradient(135deg, #fffdf5 0%, #fff3e0 100%); 
        font-family: 'Pretendard', sans-serif;
    } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    
    /* 🏠 메인 홈 버튼 디자인 */
    .home-btn > button {
        background-color: #FFFFFF !important; color: #f57c00 !important;
        border: 2px solid #ffe082 !important; border-radius: 10px !important;
        font-weight: 800 !important; padding: 5px 20px !important;
        box-shadow: 0 2px 5px rgba(255, 165, 0, 0.1) !important;
    }
    
    /* 메인 컨테이너 스타일 */
    .main-container { 
        width: 100%; max-width: 950px; margin: 0 auto; 
        background: #ffffff; padding: 30px 40px; 
        border-radius: 20px; box-shadow: 0 10px 30px rgba(255, 165, 0, 0.1); 
        border: 2px solid #ffe082; 
    }

    /* 헤더 스타일 */
    h1.main-title { 
        font-family: 'GmarketSans', sans-serif; 
        background: linear-gradient(to right, #e65100, #e91e63); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 32px; font-weight: bold; margin: 0; text-align: center;
    }
    h4.sub-title { text-align: center; color: #ff9800; margin-top: 10px; margin-bottom: 20px; font-size: 16px; font-weight: 700; }

    /* 배지 스타일 */
    .school-badge { 
        text-align: center; background-color: #fff8e1; color: #d84315; 
        font-weight: 800; padding: 15px; border-radius: 12px; margin-bottom: 25px; 
        font-size: 15px; border: 1px solid #ffe082; 
    }
    .alert-badge { display: block; margin-top: 8px; font-size: 13px; } 

    /* 스트림릿 입력창 커스텀 (노란색/주황색 톤업) */
    div[data-baseweb="input"] { border: 2px solid #ffcc80 !important; border-radius: 8px !important; }
    div[data-baseweb="input"]:focus-within { border-color: #ff9800 !important; box-shadow: 0 0 0 1px #ff9800 !important; }
    
    /* 📱 결과 점수 섹션 */
    .result-section { 
        display: flex; flex-direction: row; justify-content: center; align-items: center; gap: 40px; 
        margin: 30px 0; background: #fff; padding: 30px 20px; border-radius: 15px; border: 1px solid #ffecb3; 
    }
    .grade-item { text-align: center; width: 100%; }
    .grade-title { font-size: 16px; color: #d84315; font-weight: 800; margin-bottom: 5px; }
    .grade-value-5 { font-family: 'GmarketSans', sans-serif; font-size: 48px; font-weight: bold; color: #ff9800; }
    .grade-value-9 { font-family: 'GmarketSans', sans-serif; font-size: 48px; font-weight: bold; color: #e91e63; }
    .vs-badge { font-size: 18px; font-weight: 900; color: #fff; padding: 15px; background: linear-gradient(135deg, #ffb300, #f06292); border-radius: 50%; }

    /* 컬러 게이지 바 */
    .gauge-wrapper { padding: 0 10px; margin-bottom: 40px; }
    .gauge-container { position: relative; width: 100%; height: 20px; background: linear-gradient(to right, #fff59d, #ffca28, #ff9800, #f06292, #c2185b); border-radius: 10px; }
    .gauge-marker { position: absolute; top: -10px; width: 4px; height: 40px; background: #3e2723; border-radius: 2px; transition: left 0.4s; }
    .gauge-marker::after { content: '내 위치'; position: absolute; top: -25px; left: -22px; width: 48px; text-align: center; font-size: 11px; font-weight: bold; color: #fff; background: #3e2723; padding: 2px 0; border-radius: 4px; }
    .gauge-labels { display: flex; justify-content: space-between; margin-top: 10px; font-size: 13px; color: #d84315; font-weight: 800; }

    /* 대학교 결과 카드 */
    .card-univ { padding: 30px 20px; border-radius: 15px; text-align: center; background: #fff; }
    .card-univ.gyogwa { border: 2px solid #ffca28; background: linear-gradient(to bottom, #fff, #fffdf5); }
    .card-univ.jonghap { border: 2px solid #f06292; background: linear-gradient(to bottom, #fff, #fff0f3); }
    .card-univ .card-title { font-size: 18px; font-weight: 800; margin-bottom: 15px; }
    .card-univ.gyogwa .card-title { color: #f57f17; }
    .card-univ.jonghap .card-title { color: #d81b60; }
    .card-univ .card-value { font-family: 'GmarketSans', sans-serif; font-size: 28px; font-weight: bold; margin-bottom: 10px; color: #3e2723;}
    .card-univ .card-desc { font-size: 15px; color: #e65100; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# 3. 홈 버튼
st.markdown('<div class="home-btn">', unsafe_allow_html=True)
if st.button("🏠 메인 화면으로 돌아가기"):
    st.switch_page("app.py")
st.markdown('</div>', unsafe_allow_html=True)

# 4. 헤더 렌더링
st.markdown("""
<div class="main-container">
    <div style="display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 10px; margin-bottom: 5px;">
        <h1 class="main-title">2028 대입 교과/종합 상담</h1>
    </div>
    <h4 class="sub-title">♥ 양명여고 진로진학부 ♥</h4>
    <div class="school-badge">
        [2026 대입 주요대학 3개년 컷오프] 적용
        <span class="alert-badge">✨ 평균에서 0.05를 빼서 보정</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("") # 여백

# 5. 엑셀 데이터 파싱 함수 (캐싱 적용)
@st.cache_data
def load_conversion_data():
    target_filename = "수시NAVI(등급변환표 탑재).xlsx"
    possible_paths = [target_filename, f"../{target_filename}"]
    file_path = None
    for path in possible_paths:
        if os.path.exists(path): file_path = path; break
    if not file_path: return None
    try:
        df = pd.read_excel(file_path, sheet_name='기타', header=None, engine='openpyxl')
        mapping = {}
        for i in range(len(df)):
            try:
                g5 = float(df.iloc[i, 6])
                g9 = float(df.iloc[i, 9])
                mapping[round(g5, 2)] = g9
            except: continue
        return mapping
    except: return None

conversion_map = load_conversion_data()

# 6. 전형 선택 (라디오 버튼을 선생님 UI처럼 배치)
st.markdown("<h4 style='color: #d84315; font-weight: bold;'>📌 전형 및 성적 입력</h4>", unsafe_allow_html=True)
mode = st.radio("전형 선택", ["📘 교과 전형", "📙 종합 전형"], horizontal=True, label_visibility="collapsed")

# 7. 성적 입력 폼 (체크박스와 숫자 입력 연동)
col1, col2 = st.columns(2)
with col1:
    st.markdown("**1학년 1학기 (필수)**")
    v1 = st.number_input("1학년 1학기 내신", min_value=1.0, max_value=5.0, value=1.528, step=0.01, label_visibility="collapsed")
    c3 = st.checkbox("2학년 1학기 포함")
    v3 = st.number_input("2학년 1학기 내신", min_value=1.0, max_value=5.0, value=1.528, step=0.01, disabled=not c3, label_visibility="collapsed")
with col2:
    c2 = st.checkbox("1학년 2학기 포함")
    v2 = st.number_input("1학년 2학기 내신", min_value=1.0, max_value=5.0, value=1.528, step=0.01, disabled=not c2, label_visibility="collapsed")
    c4 = st.checkbox("2학년 2학기 포함")
    v4 = st.number_input("2학년 2학기 내신", min_value=1.0, max_value=5.0, value=1.528, step=0.01, disabled=not c4, label_visibility="collapsed")

# 8. 계산 로직 (선생님 HTML 공식 + 엑셀 맵핑 융합)
vals = [v1]
if c2: vals.append(v2)
if c3: vals.append(v3)
if c4: vals.append(v4)

# 선생님 공식: 평균에서 0.05 빼기
avg5_raw = sum(vals) / len(vals) - 0.050
avg5 = max(1.0, min(5.0, avg5_raw))

# 엑셀 기반 9등급 변환
g5_rounded = round(avg5, 2)
avg9 = 9.0

if conversion_map:
    if g5_rounded in conversion_map:
        avg9 = conversion_map[g5_rounded]
    else:
        closest_keys = sorted(conversion_map.keys())
        for k in closest_keys:
            if k >= g5_rounded:
                avg9 = conversion_map[k]
                break
        if avg9 == 9.0 and closest_keys: avg9 = conversion_map[closest_keys[-1]]
else:
    # 엑셀 파일 없을 경우 대비 선생님 오리지널 스크립트 백업 공식
    points = [[1.0, 1.0], [1.1, 1.35], [1.2, 1.65], [1.31, 1.99], [1.478, 2.345], [1.715, 2.753], [2.004, 3.261], [3.0, 6.0], [5.0, 9.0]]
    for i in range(len(points) - 1):
        if points[i][0] <= avg5 <= points[i+1][0]:
            avg9 = points[i][1] + (avg5 - points[i][0]) / (points[i+1][0] - points[i][0]) * (points[i+1][1] - points[i][1])
            break

# 9. 대학 라인 판별 로직 (선생님 HTML 원본 100% 일치)
is_gyogwa = "교과" in mode
if is_gyogwa:
    if avg9 <= 1.4: u, desc = "SKY / 핵심과기원", "서울대, 연세대, 고려대, 카이스트 등"
    elif avg9 <= 1.7: u, desc = "서성한 라인", "서강, 성균관, 한양, 포스텍 등"
    elif avg9 <= 1.9: u, desc = "중경외시이 라인", "중앙, 경희, 외대, 시립, 이화 등"
    elif avg9 <= 2.2: u, desc = "건동홍숙 / 교대", "건국, 동국, 홍익, 숙명, 교대 등"
    elif avg9 <= 2.6: u, desc = "국숭세단 / 과기대", "국민, 숭실, 세종, 단국, 과기대 등"
    elif avg9 <= 3.1: u, desc = "광명상가 / 지거국 상위", "광운, 명지, 상명, 가톨릭, 부산 등"
    elif avg9 <= 3.6: u, desc = "인가경 / 수도권 주요", "인천, 가천, 경기, 충남, 전남 등"
    elif avg9 <= 4.2: u, desc = "수도권 중위 / 지거국", "수원, 강남, 안양, 강원, 전북 등"
    else: u, desc = "기타 지역 / 전문대", "전국 권역별 일반 전형"
else: # 종합전형
    if avg9 <= 1.7: u, desc = "SKY / 핵심과기원", "서울대, 연세대, 고려대, 카이스트 등"
    elif avg9 <= 2.1: u, desc = "서성한 라인", "서강, 성균관, 한양, 포스텍 등"
    elif avg9 <= 2.5: u, desc = "중경외시이 라인", "중앙, 경희, 외대, 시립, 이화 등"
    elif avg9 <= 2.8: u, desc = "건동홍숙 / 교대", "건국, 동국, 홍익, 숙명, 교대 등"
    elif avg9 <= 3.2: u, desc = "국숭세단 / 과기대", "국민, 숭실, 세종, 단국, 과기대 등"
    elif avg9 <= 3.6: u, desc = "광명상가 / 지거국 상위", "광운, 명지, 상명, 가톨릭, 부산 등"
    elif avg9 <= 4.2: u, desc = "인가경 / 수도권 주요", "인천, 가천, 경기, 충남, 전남 등"
    elif avg9 <= 4.8: u, desc = "수도권 중위 / 지거국", "수원, 강남, 안양, 강원, 전북 등"
    else: u, desc = "기타 지역 / 전문대", "전국 권역별 일반 전형"

# [세션 상태 저장] - 데이터 통신의 핵심!
st.session_state['converted_9_grade'] = avg9

# 10. 선생님 디자인 기반 결과 화면 렌더링
left_percent = ((avg5 - 1.0) / 4.0) * 100

st.markdown(f"""
<div class="main-container" style="margin-top: 20px;">
    <div class="result-section">
        <div class="grade-item">
            <div class="grade-title">🆕 현행 (5등급) 평균</div>
            <div class="grade-value-5">{avg5:.3f}</div>
        </div>
        <div class="vs-badge">VS</div>
        <div class="grade-item">
            <div class="grade-title">⏳ 9등급제 환산</div>
            <div class="grade-value-9">{avg9:.3f}</div>
        </div>
    </div>

    <div class="gauge-wrapper">
        <div class="gauge-container">
            <div class="gauge-marker" style="left: {left_percent}%;"></div>
        </div>
        <div class="gauge-labels">
            <span>1.0 극상위</span><span>2.0</span><span>3.0 중위</span><span>4.0</span><span>5.0</span>
        </div>
    </div>

    <div class="card-univ {'gyogwa' if is_gyogwa else 'jonghap'}">
        <div class="card-title">🏫 [{'교과' if is_gyogwa else '종합'} 전형] 예상 라인</div>
        <div class="card-value">{u}</div>
        <div class="card-desc">{desc}</div>
    </div>
</div>
""", unsafe_allow_html=True)
