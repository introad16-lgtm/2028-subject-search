import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import json

# 1. 페이지 설정
st.set_page_config(page_title="2028 양명여고 진학 상담", page_icon="📊", layout="wide")

# 2. 스트림릿 배경 스타일 (선생님 UI와 어울리는 연한 핑크/크림)
st.markdown("""
<style>
    .stApp { background-color: #FFFDF5; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    .block-container { padding: 0 !important; max-width: 100% !important; }
    /* 홈 버튼 스타일 */
    .stButton > button {
        margin: 10px; background-color: white; color: #f57c00;
        border: 2px solid #ffe082; border-radius: 10px; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 3. 홈 버튼
if st.button("🏠 메인 화면으로 돌아가기"):
    st.switch_page("app.py")

# 4. 엑셀 데이터 파싱 함수
@st.cache_data
def get_excel_mapping_json():
    target_filename = "수시NAVI(등급변환표 탑재).xlsx"
    # 파일 경로 후보군 체크
    paths = [target_filename, f"../{target_filename}", f"pages/{target_filename}"]
    file_path = next((p for p in paths if os.path.exists(p)), None)
    
    if not file_path:
        return "{}" # 파일 없을 시 빈 데이터 반환
        
    try:
        # '기타' 시트에서 G열(index 6)과 J열(index 9) 읽기
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
        return "{}"

conversion_json = get_excel_mapping_json()

# 5. HTML 템플릿 (파이썬 문법 충돌을 방지하기 위해 f-string을 쓰지 않음)
html_template = """
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
            font-family: 'Pretendard', sans-serif; background: linear-gradient(135deg, #fffdf5 0%, #fff3e0 100%); 
            color: #4a4a4a; margin: 0; padding: 20px 10px; min-height: 100vh;
        }
        .container { 
            width: 100%; max-width: 950px; margin: 0 auto; background: #ffffff; padding: 30px 20px; 
            border-radius: 20px; box-shadow: 0 10px 30px rgba(255, 165, 0, 0.1); border: 2px solid #ffe082; 
        }
        .header-wrapper { display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 5px; }
        .header-logo { height: 35px; border-radius: 8px; }
        h1 { font-family: 'GmarketSans', sans-serif; background: linear-gradient(to right, #e65100, #e91e63); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 24px; margin: 0; }
        h4 { text-align: center; color: #ff9800; margin: 10px 0 20px; font-size: 15px; }
        .school-badge { text-align: center; background: #fff8e1; color: #d84315; padding: 15px; border-radius: 12px; margin-bottom: 25px; border: 1px solid #ffe082; font-size: 14px; font-weight: 800; }
        .toggle-section { display: flex; gap: 10px; margin-bottom: 25px; }
        .toggle-btn { flex: 1; padding: 12px; font-size: 15px; font-weight: 800; text-align: center; border: 2px solid #ffe082; border-radius: 12px; cursor: pointer; background: #fff; color: #f57c00; }
        .toggle-btn.active-gyogwa { background: linear-gradient(135deg, #ffca28, #ff9800); color: #fff; border-color: transparent; }
        .toggle-btn.active-jonghap { background: linear-gradient(135deg, #f06292, #e91e63); color: #fff; border-color: transparent; }
        .input-section { background: #fffdf5; padding: 20px; border-radius: 15px; border: 2px dashed #ffe082; margin-bottom: 25px; }
        .slider-group { margin-bottom: 20px; display: flex; flex-direction: column; gap: 10px; }
        .slider-group.disabled { opacity: 0.35; }
        .input-controls { display: flex; align-items: center; gap: 15px; }
        input[type=range] { flex: 1; accent-color: #ff9800; }
        .number-input { width: 80px; padding: 8px; text-align: center; border: 2px solid #ffcc80; border-radius: 8px; font-weight: 800; color: #e65100; }
        .result-section { display: flex; flex-direction: column; align-items: center; gap: 15px; margin-bottom: 30px; background: #fff; padding: 20px; border-radius: 15px; border: 1px solid #ffecb3; }
        @media (min-width: 600px) { .result-section { flex-direction: row; gap: 40px; } }
        .grade-value-5 { font-family: 'GmarketSans', sans-serif; font-size: 42px; color: #ff9800; font-weight: bold; }
        .grade-value-9 { font-family: 'GmarketSans', sans-serif; font-size: 42px; color: #e91e63; font-weight: bold; }
        .vs-badge { font-size: 16px; font-weight: 900; color: #fff; padding: 10px; background: linear-gradient(135deg, #ffb300, #f06292); border-radius: 50%; }
        .gauge-container { position: relative; width: 100%; height: 20px; background: linear-gradient(to right, #fff59d, #ffca28, #ff9800, #f06292, #c2185b); border-radius: 10px; margin-bottom: 40px; }
        .gauge-marker { position: absolute; top: -10px; width: 4px; height: 40px; background: #3e2723; border-radius: 2px; transition: left 0.4s; }
        .gauge-marker::after { content: '내 위치'; position: absolute; top: -25px; left: -22px; width: 48px; font-size: 11px; font-weight: bold; color: #fff; background: #3e2723; border-radius: 4px; padding: 2px 0; text-align: center; }
        .gauge-labels { display: flex; justify-content: space-between; font-size: 12px; font-weight: 800; color: #d84315; }
        .card-univ { padding: 25px; border-radius: 15px; text-align: center; background: #fff; border: 2px solid #ffca28; }
        .card-univ.jonghap { border-color: #f06292; }
        .card-value { font-family: 'GmarketSans', sans-serif; font-size: 26px; font-weight: bold; margin: 10px 0; }
    </style>
</head>
<body>
<div class="container">
    <div class="header-wrapper">
        <img src="logo.jpeg" alt="로고" class="header-logo" onerror="this.style.display='none'">
        <h1>2028 대입 교과/종합 상담</h1>
    </div>
    <h4>♥ 양명여고 진로진학부 ♥</h4>
    <div class="school-badge">
        [2026 대입 주요대학 3개년 컷오프] + [수시NAVI 엑셀 변환] 적용
        <span style="display:block; font-size:12px; margin-top:5px;">✨ 평균에서 0.05를 빼서 보정</span>
    </div>
    <div class="toggle-section">
        <div class="toggle-btn active-gyogwa" id="btn-gyogwa" onclick="setMode('gyogwa')">📘 교과 전형</div>
        <div class="toggle-btn" id="btn-jonghap" onclick="setMode('jonghap')">📙 종합 전형</div>
    </div>
    <div class="input-section">
        <div class="slider-group">
            <div style="font-weight:800;">1학년 1학기 (5등급)</div>
            <div class="input-controls">
                <input type="range" id="s1" min="1.0" max="5.0" step="0.001" value="1.528" oninput="sync('s1', 'n1')">
                <input type="number" id="n1" class="number-input" value="1.528" oninput="sync('n1', 's1')">
            </div>
        </div>
        <div class="slider-group disabled" id="g2">
            <label style="font-weight:800;"><input type="checkbox" id="c2" onchange="toggle(2)"> 1학년 2학기</label>
            <div class="input-controls">
                <input type="range" id="s2" min="1.0" max="5.0" step="0.001" value="1.528" oninput="sync('s2', 'n2')">
                <input type="number" id="n2" class="number-input" value="1.528" oninput="sync('n2', 's2')">
            </div>
        </div>
        <div class="slider-group disabled" id="g3">
            <label style="font-weight:800;"><input type="checkbox" id="c3" onchange="toggle(3)"> 2학년 1학기</label>
            <div class="input-controls">
                <input type="range" id="s3" min="1.0" max="5.0" step="0.001" value="1.528" oninput="sync('s3', 'n3')">
                <input type="number" id="n3" class="number-input" value="1.528" oninput="sync('n3', 's3')">
            </div>
        </div>
        <div class="slider-group disabled" id="g4">
            <label style="font-weight:800;"><input type="checkbox" id="c4" onchange="toggle(4)"> 2학년 2학기</label>
            <div class="input-controls">
                <input type="range" id="s4" min="1.0" max="5.0" step="0.001" value="1.528" oninput="sync('s4', 'n4')">
                <input type="number" id="n4" class="number-input" value="1.528" oninput="sync('n4', 's4')">
            </div>
        </div>
    </div>
    <div class="result-section">
        <div style="text-align:center; flex:1;">
            <div style="color:#d84315; font-weight:800;">🆕 현행 (5등급) 평균</div>
            <div class="grade-value-5" id="res5">1.478</div>
        </div>
        <div class="vs-badge">VS</div>
        <div style="text-align:center; flex:1;">
            <div style="color:#d84315; font-weight:800;">⏳ 9등급제 환산</div>
            <div class="grade-value-9" id="res9">2.345</div>
        </div>
    </div>
    <div class="gauge-container"><div class="gauge-marker" id="marker"></div></div>
    <div class="gauge-labels"><span>1.0 극상위</span><span>2.0</span><span>3.0 중위</span><span>4.0</span><span>5.0</span></div>
    <br>
    <div class="card-univ" id="univ-card">
        <div style="font-weight:800; font-size:18px; color:#f57f17;" id="univ-title">🏫 [교과 전형] 예상 라인</div>
        <div class="card-value" id="univ">국숭세단 및 과기대</div>
        <div style="font-size:14px; color:#e65100; font-weight:700;" id="univ-desc">국민대, 숭실대, 세종대, 단국대 등</div>
    </div>
</div>

<script>
    const conversionMap = JSON_DATA_PLACEHOLDER;
    let mode = 'gyogwa';

    function setMode(newMode) {
        mode = newMode;
        const bG = document.getElementById('btn-gyogwa');
        const bJ = document.getElementById('btn-jonghap');
        const uC = document.getElementById('univ-card');
        const uT = document.getElementById('univ-title');
        
        if(mode === 'gyogwa') {
            bG.className = 'toggle-btn active-gyogwa'; bJ.className = 'toggle-btn';
            uC.className = 'card-univ'; uT.innerText = '🏫 [교과 전형] 예상 라인';
            uT.style.color = '#f57f17';
        } else {
            bJ.className = 'toggle-btn active-jonghap'; bG.className = 'toggle-btn';
            uC.className = 'card-univ jonghap'; uT.innerText = '🏫 [종합 전형] 예상 라인';
            uT.style.color = '#d81b60';
        }
        calc();
    }

    function sync(src, dst) {
        let val = parseFloat(document.getElementById(src).value);
        document.getElementById(dst).value = val.toFixed(3);
        calc();
    }

    function toggle(n) {
        const isChecked = document.getElementById('c' + n).checked;
        const group = document.getElementById('g' + n);
        isChecked ? group.classList.remove('disabled') : group.classList.add('disabled');
        calc();
    }

    function map5to9(g5) {
        let key = (Math.round(g5 * 100) / 100).toFixed(2);
        if (conversionMap[key]) return conversionMap[key];
        
        const pts = [[1.0, 1.0], [1.1, 1.35], [1.2, 1.65], [1.31, 1.99], [1.478, 2.345], [1.715, 2.753], [2.004, 3.261], [3.0, 6.0], [5.0, 9.0]];
        if (g5 <= 1.0) return 1.0; if (g5 >= 5.0) return 9.0;
        for (let i = 0; i < pts.length - 1; i++) {
            if (g5 >= pts[i][0] && g5 <= pts[i+1][0]) {
                return pts[i][1] + (g5 - pts[i][0]) / (pts[i+1][0] - pts[i][0]) * (pts[i+1][1] - pts[i][1]);
            }
        }
        return 9.0;
    }

    function calc() {
        let sum = parseFloat(document.getElementById('n1').value);
        let cnt = 1;
        for(let i=2; i<=4; i++) {
            if(document.getElementById('c' + i).checked) {
                sum += parseFloat(document.getElementById('n' + i).value);
                cnt++;
            }
        }
        let avg5 = (sum / cnt) - 0.05;
        avg5 = Math.max(1.0, Math.min(5.0, avg5));
        let avg9 = map5to9(avg5);

        document.getElementById('res5').innerText = avg5.toFixed(3);
        document.getElementById('res9').innerText = avg9.toFixed(3) + " 등급";
        document.getElementById('marker').style.left = ((avg5 - 1.0) / 4.0 * 100) + "%";

        let u = "", d = "";
        if(mode === 'gyogwa') {
            if(avg9 <= 1.4) { u = "SKY / 핵심과기원"; d = "서울대, 연세대, 고려대, 카이스트 등"; }
            else if(avg9 <= 1.7) { u = "서성한 라인"; d = "서강, 성균관, 한양, 포스텍 등"; }
            else if(avg9 <= 1.9) { u = "중경외시이 라인"; d = "중앙, 경희, 외대, 시립, 이화 등"; }
            else if(avg9 <= 2.2) { u = "건동홍숙 / 교대"; d = "건국, 동국, 홍익, 숙명, 교대 등"; }
            else if(avg9 <= 2.6) { u = "국숭세단 / 과기대"; d = "국민, 숭실, 세종, 단국, 과기대 등"; }
            else if(avg9 <= 3.1) { u = "광명상가 / 지거국 상위"; d = "광운, 명지, 상명, 가톨릭, 부산 등"; }
            else if(avg9 <= 3.6) { u = "인가경 / 수도권 주요"; d = "인천, 가천, 경기, 충남, 전남 등"; }
            else if(avg9 <= 4.2) { u = "수도권 중위 / 지거국"; d = "수원, 강남, 안양, 강원, 전북 등"; }
            else { u = "기타 지역 / 전문대"; d = "전국 권역별 일반 전형"; }
        } else {
            if(avg9 <= 1.7) { u = "SKY / 핵심과기원"; d = "서울대, 연세대, 고려대, 카이스트 등"; }
            else if(avg9 <= 2.1) { u = "서성한 라인"; d = "서강, 성균관, 한양, 포스텍 등"; }
            else if(avg9 <= 2.5) { u = "중경외시이 라인"; d = "중앙, 경희, 외대, 시립, 이화 등"; }
            else if(avg9 <= 2.8) { u = "건동홍숙 / 교대"; d = "건국, 동국, 홍익, 숙명, 교대 등"; }
            else if(avg9 <= 3.2) { u = "국숭세단 / 과기대"; d = "국민, 숭실, 세종, 단국, 과기대 등"; }
            else if(avg9 <= 3.6) { u = "광명상가 / 지거국 상위"; d = "광운, 명지, 상명, 가톨릭, 부산 등"; }
            else if(avg9 <= 4.2) { u = "인가경 / 수도권 주요"; d = "인천, 가천, 경기, 충남, 전남 등"; }
            else if(avg9 <= 4.8) { u = "수도권 중위 / 지거국"; d = "수원, 강남, 안양, 강원, 전북 등"; }
            else { u = "기타 지역 / 전문대"; d = "전국 권역별 일반 전형"; }
        }
        document.getElementById('univ').innerText = u;
        document.getElementById('univ-desc').innerText = d;
    }
    window.onload = calc;
</script>
</body>
</html>
"""

# 6. JSON 데이터 안전하게 치환 (파이썬 SyntaxError 방지)
final_html = html_template.replace("JSON_DATA_PLACEHOLDER", conversion_json)

# 7. 컴포넌트 출력
components.html(final_html, height=1100, scrolling=False)
