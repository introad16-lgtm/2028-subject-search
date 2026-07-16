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

# 5. 선생님의 HTML 원본 소스에 엑셀 데이터 매핑 로직 주입
html_code = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>2028 양명여고 진학 상담 프로그램</title>
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        @import url('https://webfontworld.github.io/gmarket/GmarketSans.css');
        
        * {{ box-sizing: border-box; }} 
        
        body {{ 
            font-family: 'Pretendard', 'Malgun Gothic', '맑은 고딕', sans-serif; 
            background: linear-gradient(135deg, #fffdf5 0%, #fff3e0 100%); 
            color: #4a4a4a; margin: 0; padding: 10px;
            min-height: 100vh; line-height: 1.6;
        }}

        .container {{ 
            width: 100%; max-width: 950px; margin: 0 auto; 
            background: #ffffff; padding: 30px 20px; 
            border-radius: 20px; box-shadow: 0 10px 30px rgba(255, 165, 0, 0.1); 
            border: 2px solid #ffe082; 
        }}

        .header-wrapper {{ display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 10px; margin-bottom: 5px; flex-wrap: wrap; }}
        .header-logo {{ height: 35px; width: auto; border-radius: 8px; }}
        
        h1 {{ 
            font-family: 'GmarketSans', sans-serif; 
            background: linear-gradient(to right, #e65100, #e91e63); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-size: 24px; font-weight: bold; margin: 0; text-align: center;
        }}
        
        h4 {{ text-align: center; color: #ff9800; margin-top: 10px; margin-bottom: 20px; font-size: 15px; font-weight: 700; }}

        .school-badge {{ 
            text-align: center; background-color: #fff8e1; color: #d84315; 
            font-weight: 800; padding: 15px; border-radius: 12px; margin-bottom: 25px; 
            font-size: 14px; border: 1px solid #ffe082; 
        }}
        .alert-badge {{ display: block; margin-top: 8px; font-size: 12px; }} 
        
        .toggle-section {{ display: flex; flex-direction: row; justify-content: center; margin-bottom: 25px; gap: 10px; }}
        .toggle-btn {{ 
            flex: 1; padding: 12px 10px; font-size: 15px; font-weight: 800; 
            text-align: center; border: 2px solid #ffe082; border-radius: 12px; cursor: pointer; 
            background: #fff; color: #f57c00; word-break: keep-all;
        }}
        .toggle-btn.active-gyogwa {{ background: linear-gradient(135deg, #ffca28, #ff9800); color: #fff; border-color: transparent; }}
        .toggle-btn.active-jonghap {{ background: linear-gradient(135deg, #f06292, #e91e63); color: #fff; border-color: transparent; }}
        
        .input-section {{ background: #fffdf5; padding: 20px; border-radius: 15px; border: 2px dashed #ffe082; margin-bottom: 25px; }}
        .slider-group {{ margin-bottom: 20px; display: flex; flex-direction: column; gap: 10px; transition: opacity 0.3s; }}
        .slider-group.disabled {{ opacity: 0.35; }}
        
        .slider-label {{ font-weight: 800; color: #5d4037; font-size: 15px; display: flex; align-items: center; gap: 8px; }}
        .input-controls {{ display: flex; flex-direction: row; align-items: center; gap: 15px; width: 100%; }}
        .slider-input {{ flex: 1; }}
        
        input[type=range] {{ width: 100%; accent-color: #ff9800; }} 
        input[type=checkbox] {{ width: 20px; height: 20px; accent-color: #ff9800; }}
        
        .number-input {{ 
            width: 80px; padding: 8px; font-size: 15px; text-align: center; 
            border: 2px solid #ffcc80; border-radius: 8px; font-weight: 800; color: #e65100; 
        }}

        .result-section {{ 
            display: flex; flex-direction: column; align-items: center; gap: 15px; 
            margin-bottom: 30px; background: #fff; padding: 20px; border-radius: 15px; border: 1px solid #ffecb3; 
        }}
        @media (min-width: 600px) {{ .result-section {{ flex-direction: row; gap: 40px; }} }} 
        
        .grade-item {{ text-align: center; width: 100%; }}
        .grade-title {{ font-size: 15px; color: #d84315; font-weight: 800; margin-bottom: 5px; }}
        
        .grade-value-5 {{ font-family: 'GmarketSans', sans-serif; font-size: 42px; font-weight: bold; color: #ff9800; }}
        .grade-value-9 {{ font-family: 'GmarketSans', sans-serif; font-size: 42px; font-weight: bold; color: #e91e63; }}
        .vs-badge {{ font-size: 16px; font-weight: 900; color: #fff; padding: 10px; background: linear-gradient(135deg, #ffb300, #f06292); border-radius: 50%; }}

        .gauge-wrapper {{ padding: 0 10px; margin-bottom: 40px; }}
        .gauge-container {{ position: relative; width: 100%; height: 20px; background: linear-gradient(to right, #fff59d, #ffca28, #ff9800, #f06292, #c2185b); border-radius: 10px; }}
        .gauge-marker {{ position: absolute; top: -10px; width: 4px; height: 40px; background: #3e2723; border-radius: 2px; transition: left 0.4s; }}
        .gauge-marker::after {{ content: '내 위치'; position: absolute; top: -25px; left: -22px; width: 48px; text-align: center; font-size: 11px; font-weight: bold; color: #fff; background: #3e2723; padding: 2px 0; border-radius: 4px; }}
        .gauge-labels {{ display: flex; justify-content: space-between; margin-top: 10px; font-size: 12px; color: #d84315; font-weight: 800; }}
        @media (max-width: 400px) {{ .gauge-labels span:nth-child(2), .gauge-labels span:nth-child(4) {{ display: none; }} }} 

        .card-univ {{ padding: 25px 15px; border-radius: 15px; text-align: center; background: #fff; }}
        .card-univ.gyogwa {{ border: 2px solid #ffca28; background: linear-gradient(to bottom, #fff, #fffdf5); }}
        .card-univ.jonghap {{ border: 2px solid #f06292; background: linear-gradient(to bottom, #fff, #fff0f3); }}
        
        .card-univ .card-title {{ font-size: 18px; font-weight: 800; margin-bottom: 15px; }}
        .card-univ.gyogwa .card-title {{ color: #f57f17; }}
        .card-univ.jonghap .card-title {{ color: #d81b60; }}
        
        .card-univ .card-value {{ font-family: 'GmarketSans', sans-serif; font-size: 26px; font-weight: bold; line-height: 1.3; margin-bottom: 10px; color: #3e2723; word-break: keep-all;}}
        .card-univ .card-desc {{ font-size: 14px; color: #e65100; font-weight: 700; word-break: keep-all; line-height: 1.4; }}
    </style>
</head>
<body>

<div class="container">
    <div class="header-wrapper">
        <img src="logo.jpeg" alt="양명여고 로고" class="header-logo" onerror="this.style.display='none'">
        <h1>2028 대입 교과/종합 상담</h1>
    </div>
    <h4>♥ 양명여고 진로진학부 ♥</h4>

    <div class="school-badge">
        [수시NAVI 등급변환 실시간 연동 완료]
        <span class="alert-badge">✨ 5등급제 평균 누적비 기준 9등급 변환 엑셀 데이터 적용</span>
    </div>
    
    <div class="toggle-section">
        <div class="toggle-btn active-gyogwa" id="btn-gyogwa" onclick="setMode('gyogwa')">📘 교과 전형</div>
        <div class="toggle-btn" id="btn-jonghap" onclick="setMode('jonghap')">📙 종합 전형</div>
    </div>

    <div class="input-section">
        <div class="slider-group">
            <div class="slider-label">1학년 1학기 (5등급)</div>
            <div class="input-controls">
                <div class="slider-input"><input type="range" id="s1" min="1.0" max="5.0" step="0.001" value="1.528" oninput="sync('s1', 'n1')"></div>
                <input type="number" id="n1" class="number-input" min="1.0" max="5.0" step="0.001" value="1.528" oninput="sync('n1', 's1')">
            </div>
        </div>
        <div class="slider-group disabled" id="g2">
            <label class="slider-label" for="c2"><input type="checkbox" id="c2" onchange="toggle(2)"> 1학년 2학기</label>
            <div class="input-controls">
                <div class="slider-input"><input type="range" id="s2" min="1.0" max="5.0" step="0.001" value="1.528" oninput="sync('s2', 'n2')"></div>
                <input type="number" id="n2" class="number-input" min="1.0" max="5.0" step="0.001" value="1.528" oninput="sync('n2', 's2')">
            </div>
        </div>
        <hr style="border:0; border-top:2px dashed #ffe082; margin: 20px 0;">
        <div class="slider-group disabled" id="g3">
            <label class="slider-label" for="c3"><input type="checkbox" id="c3" onchange="toggle(3)"> 2학년 1학기</label>
            <div class="input-controls">
                <div class="slider-input"><input type="range" id="s3" min="1.0" max="5.0" step="0.001" value="1.528" oninput="sync('s3', 'n3')"></div>
                <input type="number" id="n3" class="number-input" min="1.0" max="5.0" step="0.001" value="1.528" oninput="sync('n3', 's3')">
            </div>
        </div>
        <div class="slider-group disabled" id="g4">
            <label class="slider-label" for="c4"><input type="checkbox" id="c4" onchange="toggle(4)"> 2학년 2학기</label>
            <div class="input-controls">
                <div class="slider-input"><input type="range" id="s4" min="1.0" max="5.0" step="0.001" value="1.528" oninput="sync('s4', 'n4')"></div>
                <input type="number" id="n4" class="number-input" min="1.0" max="5.0" step="0.001" value="1.528" oninput="sync('n4', 's4')">
            </div>
        </div>
    </div>

    <div class="result-section">
        <div class="grade-item">
            <div class="grade-title">🆕 현행 (5등급) 평균</div>
            <div class="grade-value-5" id="res5">1.478</div>
        </div>
        <div class="vs-badge">VS</div>
        <div class="grade-item">
            <div class="grade-title">⏳ 9등급제 환산 (수시NAVI)</div>
            <div class="grade-value-9" id="res9">2.345</div>
        </div>
    </div>

    <div class="gauge-wrapper">
        <div class="gauge-container"><div class="gauge-marker" id="marker"></div></div>
        <div class="gauge-labels"><span>1.0 극상위</span><span>2.0</span><span>3.0 중위</span><span>4.0</span><span>5.0</span></div>
    </div>

    <div class="card-univ gyogwa" id="univ-card">
        <div class="card-title" id="univ-title">🏫 [교과 전형] 예상 라인</div>
        <div class="card-value" id="univ">국숭세단 및 과기대</div>
        <div class="card-desc" id="univ-desc">국민대, 숭실대, 세종대, 단국대, 서울과기대 등</div>
    </div>
</div>

<script>
    // 💡 파이썬에서 주입된 수시나비 엑셀 데이터 0.01 단위 변환 테이블
    const conversionMap = {conversion_json};

    let mode = 'gyogwa';
    function setMode(newMode) {
        mode = newMode;
        if(mode === 'gyogwa') {
            document.getElementById('btn-gyogwa').className = 'toggle-btn active-gyogwa';
            document.getElementById('btn-jonghap').className = 'toggle-btn';
            document.getElementById('univ-card').className = 'card-univ gyogwa';
            document.getElementById('univ-title').innerText = '🏫 [교과 전형] 예상 라인';
        } else {
            document.getElementById('btn-jonghap').className = 'toggle-btn active-jonghap';
            document.getElementById('btn-gyogwa').className = 'toggle-btn';
            document.getElementById('univ-card').className = 'card-univ jonghap';
            document.getElementById('univ-title').innerText = '🏫 [종합 전형] 예상 라인';
        }
        calc();
    }
    function sync(src, dst) {{ 
        let val = parseFloat(document.getElementById(src).value);
        if(isNaN(val)) return; 
        document.getElementById(dst).value = val.toFixed(3); 
        calc(); 
    }}
    function toggle(n) {{ 
        const isChecked = document.getElementById('c' + n).checked;
        const group = document.getElementById('g' + n);
        isChecked ? group.classList.remove('disabled') : group.classList.add('disabled');
        calc(); 
    }}
    
    // 💡 수시나비 엑셀 데이터를 우선 조회하고, 없을 경우 선형 보간법으로 처리하는 하이브리드 알고리즘
    function map5to9(g5) {{
        let key = (Math.round(g5 * 100) / 100).toFixed(2);
        if (conversionMap && conversionMap[key]) {{
            return conversionMap[key];
        }}
        
        // 백업용 선형보간 공식
        const points = [[1.0, 1.0], [1.1, 1.35], [1.2, 1.65], [1.31, 1.99], [1.478, 2.345], [1.715, 2.753], [2.004, 3.261], [3.0, 6.0], [5.0, 9.0]];
        if (g5 <= 1.0) return 1.0; if (g5 >= 5.0) return 9.0;
        for (let i = 0; i < points.length - 1; i++) {{
            if (g5 >= points[i][0] && g5 <= points[i+1][0]) {{
                return points[i][1] + (g5 - points[i][0]) / (points[i+1][0] - points[i][0]) * (points[i+1][1] - points[i][1]);
            }
        }} return 9.0;
    }}
    
    function calc() {{
        let v1 = parseFloat(document.getElementById('n1').value);
        let v2 = parseFloat(document.getElementById('n2').value);
        if(isNaN(v1)) v1 = 1.0; if(isNaN(v2)) v2 = 1.0;
        let sum = v1; let count = 1;
        if(document.getElementById('c2').checked) {{ let v = parseFloat(document.getElementById('n2').value); if(!isNaN(v)) {{ sum += v; count++; }} }}
        if(document.getElementById('c3').checked) {{ let v = parseFloat(document.getElementById('n3').value); if(!isNaN(v)) {{ sum += v; count++; }} }}
        if(document.getElementById('c4').checked) {{ let v = parseFloat(document.getElementById('n4').value); if(!isNaN(v)) {{ sum += v; count++; }} }}
        
        let avg5 = (sum / count) - 0.050;
        if(avg5 < 1.0) avg5 = 1.0; if(avg5 > 5.0) avg5 = 5.0;
        let avg9 = map5to9(avg5);

        document.getElementById('res5').innerText = avg5.toFixed(3);
        document.getElementById('res9').innerText = avg9.toFixed(3) + " 등급";
        document.getElementById('marker').style.left = ((avg5 - 1.0) / 4.0 * 100) + "%";

        let u = "", desc = "";
        if (mode === 'gyogwa') {{
            if(avg9 <= 1.4) {{ u = "SKY / 핵심과기원"; desc = "서울대, 연세대, 고려대, 카이스트 등"; }}
            else if(avg9 <= 1.7) {{ u = "서성한 라인"; desc = "서강, 성균관, 한양, 포스텍 등"; }}
            else if(avg9 <= 1.9) {{ u = "중경외시이 라인"; desc = "중앙, 경희, 외대, 시립, 이화 등"; }}
            else if(avg9 <= 2.2) {{ u = "건동홍숙 / 교대"; desc = "건국, 동국, 홍익, 숙명, 교대 등"; }}
            else if(avg9 <= 2.6) {{ u = "국숭세단 / 과기대"; desc = "국민, 숭실, 세종, 단국, 과기대 등"; }}
            else if(avg9 <= 3.1) {{ u = "광명상가 / 지거국 상위"; desc = "광운, 명지, 상명, 가톨릭, 부산 등"; }}
            else if(avg9 <= 3.6) {{ u = "인가경 / 수도권 주요"; desc = "인천, 가천, 경기, 충남, 전남 등"; }}
            else if(avg9 <= 4.2) {{ u = "수도권 중위 / 지거국"; desc = "수원, 강남, 안양, 강원, 전북 등"; }}
            else {{ u = "기타 지역 / 전문대"; desc = "전국 권역별 일반 전형"; }}
        }} else {{
            if(avg9 <= 1.7) {{ u = "SKY / 핵심과기원"; desc = "서울대, 연세대, 고려대, 카이스트 등"; }}
            else if(avg9 <= 2.1) {{ u = "서성한 라인"; desc = "서강, 성균관, 한양, 포스텍 등"; }}
            else if(avg9 <= 2.5) {{ u = "중경외시이 라인"; desc = "중앙, 경희, 외대, 시립, 이화 등"; }}
            else if(avg9 <= 2.8) {{ u = "건동홍숙 / 교대"; desc = "건국, 동국, 홍익, 숙명, 교대 등"; }}
            else if(avg9 <= 3.2) {{ u = "국숭세단 / 과기대"; desc = "국민, 숭실, 세종, 단국, 과기대 등"; }}
            else if(avg9 <= 3.6) {{ u = "광명상가 / 지거국 상위"; desc = "광운, 명지, 상명, 가톨릭, 부산 등"; }}
            else if(avg9 <= 4.2) {{ u = "인가경 / 수도권 주요"; desc = "인천, 가천, 경기, 충남, 전남 등"; }}
            else if(avg9 <= 4.8) {{ u = "수도권 중위 / 지거국"; desc = "수원, 강남, 안양, 강원, 전북 등"; }}
            else {{ u = "기타 지역 / 전문대"; desc = "전국 권역별 일반 전형"; }}
        }}
        document.getElementById('univ').innerText = u;
        document.getElementById('univ-desc').innerText = desc;
    }}
    window.onload = calc;
</script>
</body>
</html>
"""

# 6. 완성된 네이티브 액자식 웹 렌더링 (높이 유연화 및 이질감 제로)
components.html(html_code, height=1100, scrolling=False)
