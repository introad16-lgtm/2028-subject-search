import streamlit as st
import google.generativeai as genai
import time

# 1. 페이지 설정
st.set_page_config(page_title="양명여고 학생부 AI 설계기", page_icon="📋", layout="wide")

# 2. 양명여고 전용 화사한 테마 CSS
st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    
    /* 🏠 메인 홈 버튼 디자인 */
    .home-btn > button {
        background-color: #FFFFFF !important; color: #FF1493 !important;
        border: 2px solid #FFC0CB !important; border-radius: 10px !important;
        font-weight: 800 !important; padding: 5px 20px !important;
        transition: all 0.3s ease !important; box-shadow: 0 2px 5px rgba(255, 105, 180, 0.1) !important;
        margin-bottom: 20px !important;
    }
    .home-btn > button:hover {
        background-color: #FFF0F5 !important; border-color: #FF1493 !important; transform: translateY(-2px) !important;
    }

    /* 카드형 컨테이너 디자인 */
    .styled-card {
        background-color: #FFFFFF; border: 3px solid #FFC0CB; border-radius: 20px;
        padding: 30px; box-shadow: 0 8px 20px rgba(255, 105, 180, 0.1); margin-bottom: 25px;
    }

    /* ✨ 화려한 제미나이 버튼 ✨ */
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
</style>
""", unsafe_allow_html=True)

# 3. 사이드바 (API 키 입력 및 설정)
with st.sidebar:
    st.markdown("### 🔑 제미나이 AI 설정")
    st.info("이 프로그램은 실시간으로 AI를 구동합니다. 구글 Gemini API 키를 입력해 주세요.")
    api_key = st.text_input("Gemini API Key 입력", type="password")
    st.write("---")
    st.markdown("💖 **양명여자고등학교 진로진학부**")

# 홈 버튼
st.markdown('<div class="home-btn">', unsafe_allow_html=True)
if st.button("🏠 메인 화면으로 돌아가기"):
    st.switch_page("app.py")
st.markdown('</div>', unsafe_allow_html=True)

# 4. 상단 헤더
st.markdown("""
<div style='text-align: center; padding-bottom: 30px;'>
    <h1 style='color: #FF1493; font-weight: 900; font-size: 3.5rem;'>🤖 실시간 학생부 AI 설계기</h1>
    <p style='color: #64748B; font-size: 1.2rem; margin-top: 10px;'>제미나이 AI가 학생의 진로와 학교 활동을 결합하여, <b>세상에 하나뿐인 나만의 활동 전략</b>을 즉석에서 짜드립니다.</p>
</div>
""", unsafe_allow_html=True)

# 5. 학생 선택 폼 (카드 디자인 적용)
st.markdown("<div class='styled-card'>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #FF1493; margin-bottom: 20px;'>📝 STEP 1. 나의 진로 및 활동 선택</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    target_major = st.text_input("🎓 희망 학과 (구체적으로 적어주세요)", placeholder="예: 미디어커뮤니케이션학과, 간호학과")
with col2:
    target_activity = st.selectbox(
        "📋 참여 예정인 학교 활동 (택 1)",
        [
            "드림업 프로젝트 (학생 주도 소논문/탐구)",
            "학생주도 프로젝트 봉사활동",
            "독서탐구 (자율 심화 독서)",
            "이음 책모임 (비경쟁 토론)",
            "환경인문독서토론",
            "전문직업인 초청 특강",
            "과천 과학관 실습 프로그램",
            "이공계 진로캠프 (야간 천체 관측 등)",
            "금융 리터러시 아카데미",
            "창의융합 주제탐구 프로젝트",
            "스마트폰 이별주간 캠페인",
            "이달의 IB 학습자 상 추천"
        ]
    )

st.write("")
extra_keyword = st.text_input("💡 세부 관심사 / 현장 변수 입력 (선택사항)", placeholder="예: 특강에서 들은 'AI 윤리', 과학관에서 본 '분광기', 읽고 있는 책 이름 등")
st.markdown("</div>", unsafe_allow_html=True)

# 6. 제미나이 실행 버튼
st.markdown("<h3 style='color: #CA8A04; text-align: center; margin-bottom: 20px;'>🚀 STEP 2. AI에게 분석 요청하기</h3>", unsafe_allow_html=True)

st.markdown('<div class="gemini-btn">', unsafe_allow_html=True)
gemini_btn = st.button("✨ 제미나이 AI 실시간 활동 가이드 생성 ✨", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# 7. 제미나이 AI 구동 및 결과 출력
if gemini_btn:
    if not api_key:
        st.error("🚨 화면 왼쪽 사이드바에 Gemini API Key를 먼저 입력해 주세요!")
    elif not target_major:
        st.warning("⚠️ 희망 학과를 입력해야 맞춤형 가이드를 생성할 수 있습니다.")
    else:
        # 프롬프트 생성 (선생님의 의도에 맞게 AI에게 지시)
        prompt = f"""
        당신은 대한민국 최고 수준의 고등학교 진로진학 전문 교사입니다.
        지금 학생이 학생부(생기부) 활동을 준비하고 있습니다.
        
        - 학생의 희망 학과: {target_major}
        - 학생이 참여할 학교 활동: {target_activity}
        - 학생의 세부 관심사 및 힌트: {extra_keyword if extra_keyword else '특별한 키워드 없음, 학과 전공적합성에 맞춰서 자유롭게 제안'}
        
        이 학생이 '{target_activity}' 활동을 할 때, 수동적으로 참여하지 않고 '{target_major}' 전공에 맞춰 
        주도적이고 깊이 있는 탐구를 할 수 있도록 구체적인 [활동 가이드라인]을 작성해주세요. 
        인터넷 검색 엔진처럼 최신 학술 트렌드나 전공 이슈를 융합하여 아주 구체적으로 제안해야 합니다.
        
        아래 양식에 맞춰서 마크다운으로 예쁘게 출력해주세요:
        
        ### 🔍 1. 최근 [희망 학과] 분야의 최신 트렌드/이슈 요약 (간단히)
        ### 💡 2. 이 활동에서 탐구하면 좋을 핵심 주제 (3가지 추천)
        ### 📝 3. 구체적인 활동 전개 팁 (어떤 자료를 찾고, 어떤 결과물을 만들면 좋을지)
        ### 🎓 4. 활동 완료 후 과세특(세부능력 및 특기사항) 기록 예시안 (4~5줄)
        """
        
        try:
            with st.spinner(f"🌐 제미나이 AI가 '{target_major}' 전공 최신 데이터를 검색하여 맞춤형 활동을 설계하고 있습니다..."):
                genai.configure(api_key=api_key)
                # 모델 설정 (최신 모델인 1.5 플래시 사용)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # API 호출
                response = model.generate_content(prompt)
                
                st.success("✅ 제미나이 AI의 실시간 맞춤형 설계가 완료되었습니다!")
                
                # 결과 출력 박스
                st.markdown(f"""
                <div style="background-color: #FFFFFF; border: 3px solid #FFA500; border-radius: 20px; padding: 40px; box-shadow: 0 10px 25px rgba(0,0,0,0.08);">
                    <h2 style="color: #CA8A04; margin-top: 0; text-align: center; border-bottom: 2px dashed #FFD700; padding-bottom: 20px; margin-bottom: 30px;">
                        🎯 {target_major} 맞춤형 활동 솔루션
                    </h2>
                    <div style="font-size: 1.1rem; line-height: 1.8; color: #333;">
                        {response.text}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"🚨 제미나이 통신 중 오류가 발생했습니다. API 키가 정확한지 확인해 주세요. (에러 내용: {e})")
