import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import time

# 1. 페이지 설정
st.set_page_config(page_title="양명여고 학생부 AI 설계기", page_icon="📋", layout="wide")

# 2. 양명여고 전용 화사한 테마 CSS & 🖨️ 인쇄(PDF) 전용 숨김 CSS
st.markdown("""
<style>
    /* 기본 화면 스타일 */
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    
    .home-btn > button {
        background-color: #FFFFFF !important; color: #FF1493 !important;
        border: 2px solid #FFC0CB !important; border-radius: 10px !important;
        font-weight: 800 !important; padding: 5px 20px !important;
        transition: all 0.3s ease !important; box-shadow: 0 2px 5px rgba(255, 105, 180, 0.1) !important;
        margin-bottom: 20px !important;
    }
    .home-btn > button:hover { background-color: #FFF0F5 !important; border-color: #FF1493 !important; transform: translateY(-2px) !important; }

    .styled-card {
        background-color: #FFFFFF; border: 3px solid #FFC0CB; border-radius: 20px;
        padding: 30px; box-shadow: 0 8px 20px rgba(255, 105, 180, 0.1); margin-bottom: 25px;
    }

    div.row-widget.stRadio > div { flex-direction: column; gap: 10px; }
    
    .gemini-btn > button {
        background: linear-gradient(135deg, #FF69B4 0%, #FFA500 100%) !important;
        color: white !important; border: none !important; border-radius: 15px !important;
        font-weight: 900 !important; font-size: 1.4rem !important; padding: 15px 0 !important;
        box-shadow: 0 6px 15px rgba(255, 105, 180, 0.4) !important; transition: all 0.3s ease !important;
        width: 100%;
    }
    .gemini-btn > button:hover {
        transform: translateY(-5px) !important; box-shadow: 0 10px 25px rgba(255, 215, 0, 0.5) !important;
        background: linear-gradient(135deg, #FFA500 0%, #FF1493 100%) !important;
    }

    /* 🖨️ PDF 인쇄 시 쓸데없는 요소 숨기기 (결과만 깔끔하게 출력) */
    @media print {
        header { display: none !important; }
        [data-testid="stSidebar"] { display: none !important; }
        .styled-card { display: none !important; }
        .gemini-btn { display: none !important; }
        .home-btn { display: none !important; }
        .stRadio { display: none !important; }
        h1, p { display: none !important; } /* 상단 타이틀 숨기기 */
        /* 인쇄할 때는 배경을 흰색으로, 글씨는 검은색으로 고정 */
        .stApp { background-color: white !important; }
        .result-box { box-shadow: none !important; border: 1px solid #ccc !important; }
    }
</style>
""", unsafe_allow_html=True)

# 💡 API 키 자동 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = None

with st.sidebar:
    st.markdown("### 🤖 제미나이 AI 연결 상태")
    if api_key:
        st.success("✅ AI 서버에 정상적으로 연결되었습니다!")
    else:
        st.error("🚨 API 키가 설정되지 않았습니다. 관리자의 설정이 필요합니다.")
    st.write("---")
    st.markdown("💖 **양명여자고등학교 진로진학부**")

st.markdown('<div class="home-btn">', unsafe_allow_html=True)
if st.button("🏠 메인 화면으로 돌아가기"):
    st.switch_page("app.py")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding-bottom: 30px;'>
    <h1 style='color: #FF1493; font-weight: 900; font-size: 3.5rem;'>🤖 실시간 학생부 AI 설계기</h1>
    <p style='color: #64748B; font-size: 1.2rem; margin-top: 10px;'>계열과 학과를 선택하면 맞춤 활동을 추천하고, 제미나이 AI가 <b>구체적인 활동 전개 방법</b>을 즉석에서 짜드립니다.</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# [데이터 세팅] 
# -------------------------------------------------------------
career_data = {
    "인문계열": ["계열 전반 (특정 학과 미정)", "국어국문학과", "영어영문학과", "사학과", "철학과", "심리학과", "중어중문학과", "일어일문학과", "불어불문학과", "노어노문학과", "언어학과", "문헌정보학과", "문화인류학과"],
    "사회계열": ["계열 전반 (특정 학과 미정)", "경영학과", "경제학과", "정치외교학과", "사회복지학과", "미디어커뮤니케이션학과", "행정학과", "국제통상학과", "회계학과", "관광경영학과", "사회학과", "도시행정학과"],
    "교육계열": ["계열 전반 (특정 학과 미정)", "초등교육과", "국어교육과", "수학교육과", "영어교육과", "유아교육과", "특수교육과", "교육학과", "역사교육과", "지리교육과", "윤리교육과", "체육교육과"],
    "공학계열": ["계열 전반 (특정 학과 미정)", "컴퓨터공학과", "인공지능(AI)학과", "기계공학과", "전기전자공학과", "화학공학과", "건축학과", "신소재공학과", "산업공학과", "생명공학과", "소프트웨어공학과", "정보통신공학과", "항공우주공학과"],
    "자연계열": ["계열 전반 (특정 학과 미정)", "수학과", "물리학과", "화학과", "생명과학과", "환경과학과", "통계학과", "지구환경과학과", "천문우주학과", "해양학과"],
    "의약계열": ["계열 전반 (특정 학과 미정)", "의예과", "치의예과", "한의예과", "약학과", "간호학과", "수의예과", "보건행정학과", "물리치료학과", "임상병리학과", "방사선학과", "치위생학과"],
    "예체능계열": ["계열 전반 (특정 학과 미정)", "디자인학과", "회화과", "음악학과", "체육학과", "연극영화과", "무용과", "애니메이션학과", "실용음악과", "패션디자인학과", "시각디자인학과"]
}

activities_db = {
    "드림업 프로젝트": "주도형", "학생주도 프로젝트 봉사활동": "주도형", "독서탐구": "주도형",
    "이음 책모임": "주도형", "환경인문독서토론": "주도형", "창의융합 주제탐구 프로젝트": "주도형",
    "스마트폰 이별주간 캠페인": "주도형", "이달의 IB 학습자 상 추천": "주도형",
    "전문직업인 초청 특강": "비주도형", "과천 과학관 실습 프로그램": "비주도형",
    "이공계 진로캠프 (야간 천체 관측)": "비주도형", "금융 리터러시 아카데미": "비주도형"
}

# 💡 3학년 전용인 "창의융합 주제탐구 프로젝트"를 추천 목록에서 제거!
recommended_activities = {
    "인문계열": ["드림업 프로젝트", "독서탐구", "이음 책모임", "전문직업인 초청 특강"],
    "사회계열": ["학생주도 프로젝트 봉사활동", "환경인문독서토론", "전문직업인 초청 특강", "금융 리터러시 아카데미"],
    "교육계열": ["학생주도 프로젝트 봉사활동", "이음 책모임", "스마트폰 이별주간 캠페인", "전문직업인 초청 특강"],
    "공학계열": ["과천 과학관 실습 프로그램", "전문직업인 초청 특강", "드림업 프로젝트", "독서탐구"],
    "자연계열": ["이공계 진로캠프 (야간 천체 관측)", "과천 과학관 실습 프로그램", "환경인문독서토론", "독서탐구"],
    "의약계열": ["학생주도 프로젝트 봉사활동", "독서탐구", "전문직업인 초청 특강", "과천 과학관 실습 프로그램"],
    "예체능계열": ["드림업 프로젝트", "스마트폰 이별주간 캠페인", "이달의 IB 학습자 상 추천", "전문직업인 초청 특강"]
}

# STEP 1
st.markdown("<div class='styled-card'>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #FF1493; margin-bottom: 20px; border-bottom: 2px solid #FFC0CB; padding-bottom: 10px;'>📝 STEP 1. 계열 및 학과 선택</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1: selected_track = st.selectbox("🌟 희망 계열", list(career_data.keys()))
with col2: selected_major = st.selectbox("🎓 세부 학과 (미정일 경우 '계열 전반' 선택)", career_data[selected_track])

target_name = selected_major if selected_major != "계열 전반 (특정 학과 미정)" else f"{selected_track} 전반"

st.markdown(f"<h3 style='color: #FF1493; margin-top: 30px; margin-bottom: 20px; border-bottom: 2px solid #FFC0CB; padding-bottom: 10px;'>🎯 STEP 2. 활동 선택 (추천 및 기타 활동)</h3>", unsafe_allow_html=True)
st.info(f"💡 **[{target_name}]** 진로에 맞춰 활동을 선택하세요. 추천 활동 외에 '다른 활동'을 골라도 AI가 맞춤형으로 가이드해 줍니다!")

recs = recommended_activities[selected_track]
all_activities = list(activities_db.keys())

display_options = []
for act in recs: display_options.append(f"🌟 [전공 추천] {act}")
for act in all_activities:
    if act not in recs:
        # 3학년 전용 안내 문구 살짝 추가
        if act == "창의융합 주제탐구 프로젝트":
            display_options.append(f"▶ [다른 활동] {act} (🎓3학년 전용)")
        else:
            display_options.append(f"▶ [다른 활동] {act}")

selected_act_display = st.radio("활동 목록", display_options, label_visibility="collapsed")

if selected_act_display.startswith("🌟 [전공 추천] "):
    selected_act = selected_act_display.replace("🌟 [전공 추천] ", "")
else:
    selected_act = selected_act_display.replace("▶ [다른 활동] ", "").replace(" (🎓3학년 전용)", "")

act_type = activities_db.get(selected_act, "주도형")
st.markdown("</div>", unsafe_allow_html=True)

# STEP 3
st.markdown("<div class='styled-card'>", unsafe_allow_html=True)
st.markdown(f"<h3 style='color: #FF1493; margin-bottom: 20px; border-bottom: 2px solid #FFC0CB; padding-bottom: 10px;'>🔍 STEP 3. 세부 정보 입력 ({act_type})</h3>", unsafe_allow_html=True)

custom_title = ""
if act_type == "비주도형":
    st.warning("이 활동은 강연 청취나 정해진 실습을 수행하는 **[비주도형/강의형]** 활동입니다. 수동적인 참여에 그치지 않도록, 제미나이가 **'강연 후 어떻게 심화 후속 활동을 해야 하는지'** 알려드립니다.")
    custom_title = st.text_input("✏️ 수강한 강의/특강/실습의 구체적인 제목을 적어주세요 (필수)", placeholder="예: 빅데이터와 AI 윤리 특강, 과천과학관 DNA 추출 실습")
else:
    st.success("이 활동은 스스로 주제를 정해 탐구하는 **[학생 주도형]** 활동입니다. 제미나이가 **'어떻게 기획하고 실행해야 하는지'** 구체적인 전개 가이드를 제공합니다.")
    custom_title = st.text_input("💡 (선택) 특별히 다루고 싶은 관심 주제나 읽고 있는 책이 있다면 적어주세요.", placeholder="예: 행동경제학, 플랫폼 독과점 문제 (없으면 비워두셔도 됩니다)")
st.markdown("</div>", unsafe_allow_html=True)

# STEP 4
st.markdown("<h3 style='color: #CA8A04; text-align: center; margin-bottom: 20px;'>🚀 STEP 4. AI에게 분석 요청하기</h3>", unsafe_allow_html=True)
st.markdown('<div class="gemini-btn">', unsafe_allow_html=True)
gemini_btn = st.button("✨ 제미나이 AI 실시간 활동 가이드 생성 ✨", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
st.write("---")

if gemini_btn:
    if not api_key:
        st.error("🚨 제미나이 API 키가 시스템에 설정되어 있지 않습니다. 선생님께 문의하세요!")
    elif act_type == "비주도형" and not custom_title:
        st.warning("⚠️ 비주도형 활동의 경우, 후속 활동을 기획하기 위해 반드시 '강의 제목'을 입력해 주셔야 합니다.")
    else:
        if act_type == "주도형":
            prompt = f"""
            당신은 대한민국 최고 수준의 고등학교 진로진학 전문 교사입니다.
            - 학생 진로/학과: {target_name}
            - 선택한 학교 활동: {selected_act} (학생 주도형 활동)
            - 학생의 세부 관심사: {custom_title if custom_title else f'{target_name} 특성에 맞춰 자유롭게 제안'}
            
            요청: 이 학생이 '{target_name}' 진로/진학을 위해 이 주도형 활동을 '어떻게 기획하고 실행하면 좋을지' 가이드라인을 제시해 주세요.
            단순히 주제만 던져주지 말고, 어떤 책/논문을 찾아보고, 어떤 방식으로 탐구 결과물을 낼지 구체적인 '행동 가이드'를 작성해야 합니다.
            
            아래 마크다운 양식에 맞춰 작성하세요:
            ### 💡 1. [{target_name}] 맞춤형 탐구 주제 제안 (2가지)
            ### 📚 2. 탐구를 위한 구체적인 활동 전개 팁 (자료 조사 방법, 결과물 형태 등)
            ### 🎓 3. 생기부 과세특/창체 기록 예시안 (4~5줄)
            """
        else:
            prompt = f"""
            당신은 대한민국 최고 수준의 고등학교 진로진학 전문 교사입니다.
            - 학생 진로/학과: {target_name}
            - 선택한 학교 활동: {selected_act} (비주도형/강의 청취형 활동)
            - 수강한 강의/특강 제목: {custom_title}
            
            요청: 이 학생이 '{custom_title}'라는 수동적인 강의/특강을 들은 후, '{target_name}' 전공과 연계하여 
            '어떤 심화 후속 활동'을 스스로 진행하면 생기부에 주도성을 어필할 수 있을지 가이드라인을 제시해 주세요.
            
            아래 마크다운 양식에 맞춰 작성하세요:
            ### 🔍 1. 강의 내용과 [{target_name}]의 연결 고리
            ### 🏃‍♂️ 2. 주도성 어필을 위한 후속 심화 활동 가이드 (추가 독서, 소논문 등)
            ### 🎓 3. 생기부 과세특/창체 기록 예시안 (4~5줄)
            """
            
        try:
            with st.spinner(f"🌐 제미나이 AI가 '{target_name}' 진로에 맞춰 실시간으로 가이드를 생성 중입니다..."):
                genai.configure(api_key=api_key)
                
                available_models = [m.name.replace("models/", "") for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                if not available_models:
                    st.error("🚨 사용할 수 있는 제미나이 모델이 조회되지 않습니다. 구글 AI Studio 설정을 확인해주세요.")
                else:
                    chosen_model = available_models[0]
                    for target in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro", "gemini-pro"]:
                        if target in available_models:
                            chosen_model = target
                            break
                            
                    model = genai.GenerativeModel(chosen_model)
                    response = model.generate_content(prompt)
                    
                    st.success(f"✅ 제미나이 AI가 맞춤형 설계를 완료했습니다! (모델: {chosen_model})")
                    
                    # 💡 출력 결과 박스 (인쇄 시 이 부분만 깔끔하게 나옵니다)
                    st.markdown(f"""
                    <div class="result-box" style="background-color: #FFFFFF; border: 3px solid #FFA500; border-radius: 20px; padding: 40px; box-shadow: 0 10px 25px rgba(0,0,0,0.08);">
                        <h2 style="color: #CA8A04; margin-top: 0; text-align: center; border-bottom: 2px dashed #FFD700; padding-bottom: 20px; margin-bottom: 30px;">
                            🎯 {target_name} 맞춤형 활동 솔루션
                        </h2>
                        <div style="font-size: 1.1rem; line-height: 1.8; color: #333;">
                            {response.text}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 🖨️ PDF 출력 버튼 추가 (JS 활용)
                    st.write("")
                    components.html("""
                    <script>
                        function printResult() {
                            try {
                                window.parent.print();
                            } catch (e) {
                                window.print();
                            }
                        }
                    </script>
                    <div style="text-align: center; margin-top: 20px;">
                        <button onclick="printResult()" style="background: linear-gradient(135deg, #10B981, #059669); color: white; border: none; padding: 12px 30px; border-radius: 12px; font-weight: 900; font-size: 1.1rem; cursor: pointer; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3); transition: all 0.2s;">
                            🖨️ 결과 화면 PDF로 출력하기 (인쇄)
                        </button>
                        <p style="color: #64748B; font-size: 0.9rem; margin-top: 10px;">
                            (버튼이 작동하지 않으면 키보드에서 <b>Ctrl + P</b> 또는 <b>Cmd + P</b>를 누르세요. 결과 화면만 깔끔하게 출력됩니다!)
                        </p>
                    </div>
                    """, height=120)

        except Exception as e:
            st.error(f"🚨 제미나이 통신 중 오류가 발생했습니다. (에러 내용: {e})")
