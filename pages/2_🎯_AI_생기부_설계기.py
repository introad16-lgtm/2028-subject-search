import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.set_page_config(page_title="AI 생기부 설계기", page_icon="🎯", layout="wide")

# 핑크 & 옐로우 배경 테마
st.markdown("<style>.stApp { background-color: #FFF5F7; }</style>", unsafe_allow_html=True)

# 1. API 키 금고에서 꺼내기
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    api_ready = True
except Exception as e:
    api_ready = False

# 2. 상단 헤더
st.markdown("""
<div style='text-align: center; padding-bottom: 20px;'>
    <h1 style='color: #FF1493; font-weight: 800;'>🎯 AI 생기부 핀셋 설계 시스템</h1>
    <p style='color: #64748B;'>제미나이 AI가 현장 주제를 분석하여 전공 맞춤형 세특을 실시간으로 창작합니다.</p>
</div>
""", unsafe_allow_html=True)

# 3. 입력 창 구성
col1, col2 = st.columns(2)
with col1:
    st.markdown("<h4 style='color: #FF1493;'>📚 1. 희망 전공 선택</h4>", unsafe_allow_html=True)
    major_sel = st.selectbox("전공을 선택하세요", 
        ["국어국문학과", "영어영문학과", "경영학과", "경제학과", "미디어커뮤니케이션", "수학과", "화학과", "생명과학과", "컴퓨터공학과", "인공지능(AI)학과", "기계/항공우주공학", "의예/치의예과", "간호학과", "교육/특수교육과"], 
        label_visibility="collapsed")
with col2:
    st.markdown("<h4 style='color: #CA8A04;'>💡 2. 현장 활동 주제 입력</h4>", unsafe_allow_html=True)
    expert_inp = st.text_input("🎙️ 전문직업인 특강 주제", placeholder="예: 인공지능 윤리, 범죄 프로파일링")
    science_inp = st.text_input("🔬 과천과학관 실습 기기", placeholder="예: 적외선 분광기, 유전자 가위")

st.write("") # 간격 띄우기

# 4. AI 실행 버튼
st.markdown("""
<style>
    .ai-btn > button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #b00020; border: none; border-radius: 20px; font-weight: 900; font-size: 1.2rem; box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4); padding: 15px 20px;
    }
    .ai-btn > button:hover { background: linear-gradient(135deg, #FFA500 0%, #FFD700 100%); transform: scale(1.02); }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="ai-btn">', unsafe_allow_html=True)
run_ai = st.button("✨ 제미나이 AI 실시간 창작 시작 ✨", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# 5. AI 창작 로직
if run_ai:
    if not api_ready:
        st.error("🚨 관리자 대시보드의 Secrets(기미)에 API 키가 제대로 저장되지 않았습니다!")
    elif not expert_inp and not science_inp:
        st.warning("💡 특강 주제나 과학관 실습 기기 중 최소 1개는 입력해야 AI가 글을 쓸 수 있습니다.")
    else:
        exp_topic = expert_inp if expert_inp else "진로 탐색 특강"
        sci_topic = science_inp if science_inp else "첨단 과학 기술 실습"
        
        with st.spinner("✨ 구글 제미나이 AI가 현장 주제를 분석하여 글을 짓고 있습니다... (약 5~7초)"):
            prompt = f"""
            너는 양명여고 진로진학 전문 컨설턴트야.
            학생의 희망 전공: {major_sel}
            
            1. 전문직업인 특강 주제: [{exp_topic}]
            이 특강을 들은 학생이 전공과 연결하여 교과세특이나 후속 탐구로 쓸 수 있는 매우 구체적이고 학술적인 심화 탐구 활동 3가지를 각각 1줄(50자 이내)로 짧게 적어줘.
            
            2. 과천과학관 실습 기기: [{sci_topic}]
            이 실습을 한 학생이 전공과 연결하여 데이터 오차 증명 또는 사회적 파급력에 관해 쓸 수 있는 과세특 탐구 활동 3가지를 각각 1줄(50자 이내)로 짧게 적어줘.
            
            규칙: 반드시 구분자 '|'로만 6개의 문장을 구분해서 답변해. 다른 설명은 절대 금지.
            형식: 특강문장1|특강문장2|특강문장3|실습문장1|실습문장2|실습문장3
            """
            
            try:
                response = model.generate_content(prompt)
                res_text = response.text.strip().split('|')
                if len(res_text) < 6:
                    res_text = ["AI 생성 오류 (다시 시도해주세요)"] * 6
                
                # HTML 결과창 출력
                html_result = f"""
                <div style="font-family: sans-serif; padding: 20px; background: white; border-radius: 15px; border: 2px solid #FFC0CB;">
                    <h3 style="color: #FF1493; margin-top: 0;">✅ AI 창작 완료! ({major_sel})</h3>
                    <div style="margin-bottom: 20px;">
                        <h4 style="color: #CA8A04;">🎙️ 특강: [{exp_topic}] 연계 세특</h4>
                        <ul style="line-height: 1.6; color: #333;">
                            <li>✔ {res_text[0]}</li>
                            <li>✔ {res_text[1]}</li>
                            <li>✔ {res_text[2]}</li>
                        </ul>
                    </div>
                    <div>
                        <h4 style="color: #CA8A04;">🔬 실습: [{sci_topic}] 연계 세특</h4>
                        <ul style="line-height: 1.6; color: #333;">
                            <li>✔ {res_text[3]}</li>
                            <li>✔ {res_text[4]}</li>
                            <li>✔ {res_text[5]}</li>
                        </ul>
                    </div>
                </div>
                """
                st.write("")
                st.markdown(html_result, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
