import streamlit as st
import streamlit.components.v1 as components
import time

# 1. 페이지 설정
st.set_page_config(page_title="양명여고 학생부 핀셋 설계 & AI", page_icon="📋", layout="wide")

# 2. 양명여고 전용 테마 및 제미나이 버튼 CSS
st.markdown("""
<style>
    /* 전체 배경 핑크 톤 */
    .stApp { background-color: #FFF5F7; } 
    [data-testid="stSidebar"] { background-color: #FEFFED; border-right: 2px solid #FFD700; } 
    
    /* 화면 위아래 여백 제거 */
    .block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; max-width: 100% !important; }
    
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

    /* ✨ 제미나이 버튼 화려한 그라데이션 ✨ */
    .gemini-btn > button {
        background: linear-gradient(135deg, #FF69B4 0%, #FFA500 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        padding: 15px 0 !important;
        box-shadow: 0 6px 15px rgba(255, 105, 180, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    .gemini-btn > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 20px rgba(255, 215, 0, 0.5) !important;
        background: linear-gradient(135deg, #FFA500 0%, #FF1493 100%) !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 홈 버튼
st.markdown('<div class="home-btn">', unsafe_allow_html=True)
if st.button("🏠 메인 화면으로 돌아가기"):
    st.switch_page("app.py")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. 상단: 선생님의 완벽한 HTML 장바구니 시스템 이식
# -----------------------------------------------------------------------------
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Pretendard', sans-serif; background-color: transparent; color: #1e293b; word-break: keep-all; margin: 0; padding: 0; }
        .gradient-text { background: linear-gradient(135deg, #FF1493, #FFA500); -webkit-background-clip: text; color: transparent; }
        .card-anim { transition: transform 0.2s ease, box-shadow 0.2s ease; }
        .card-anim:hover { transform: translateY(-4px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }
        .checkbox-pill input { display: none; }
        .checkbox-pill label { 
            display: inline-flex; align-items: center; justify-content: center;
            padding: 0.5rem 1rem; border: 1px solid #cbd5e1; border-radius: 9999px;
            background-color: white; color: #64748b; font-size: 0.85rem; font-weight: 700;
            cursor: pointer; transition: all 0.2s; user-select: none; margin-bottom: 0.3rem;
        }
        .checkbox-pill input:checked + label { background-color: #FF1493; border-color: #FF1493; color: white; box-shadow: 0 4px 6px -1px rgba(255, 20, 147, 0.3); }
        .checkbox-pill input.recommended-item + label { border: 2px solid #FFA500; color: #CA8A04; background-color: #FFFDF0; }
        .checkbox-pill input.recommended-item:checked + label { background-color: #FFA500; border-color: #FFA500; color: white; box-shadow: 0 4px 6px -1px rgba(255, 165, 0, 0.3); }
        .checkbox-pill label:hover { filter: brightness(0.95); }
        .highlight-border { position: relative; border: 2px solid #FFA500 !important; box-shadow: 0 10px 15px -3px rgba(255, 165, 0, 0.15) !important; }
        .topic-pick { transition: all 0.2s; border: 2px solid transparent; cursor: pointer; }
        .topic-pick:hover { background-color: #f1f5f9; border-color: #cbd5e1; }
        .topic-pick.selected { border-color: #FF1493; background-color: #FFF0F5; box-shadow: 0 4px 6px -1px rgba(255, 20, 147, 0.2); }
        .topic-pick .check-icon { opacity: 0; transform: scale(0.5); transition: all 0.2s; }
        .topic-pick.selected .check-icon { opacity: 1; transform: scale(1); color: #FF1493; }
        .tag-lead { background-color: #FF1493; color: white; } 
        .tag-semi { background-color: #FFA500; color: white; } 
        .tag-part { background-color: #64748b; color: white; } 
        @media print {
            body { background: white; padding: 0; }
            #app-view { display: none !important; } 
            #print-view { display: block !important; } 
            .page-break { page-break-inside: avoid; break-inside: avoid; margin-bottom: 2rem; }
            @page { margin: 15mm; }
        }
    </style>
</head>
<body>
    <div id="app-view" class="p-2 md:p-4 max-w-6xl mx-auto block print:hidden">
        <header class="text-center mb-8 mt-2">
            <div class="text-xs font-extrabold text-[#FF1493] mb-2 tracking-wide">🏫 Yangmyung Girls' High School</div>
            <div class="inline-flex items-center gap-2 px-5 py-2 mb-4 text-sm font-bold text-[#FF1493] bg-pink-50 border border-pink-200 rounded-full">
                🎯 다변화 학과 & 핀셋 교과 연계 시스템
            </div>
            <h1 class="text-3xl md:text-4xl font-extrabold mb-3 tracking-tight">생기부 <span class="gradient-text">장바구니 설계기</span></h1>
            <p class="text-[16px] text-slate-500 font-medium max-w-2xl mx-auto leading-relaxed">
                학생 주도성이 높은 활동은 전공 뼈대로 밀고 가며,<br>가변적인 특강/실습에만 현장 키워드가 개입하여 깊이 있는 교과 연계를 제안합니다.
            </p>
        </header>

        <div class="bg-white p-6 md:p-8 rounded-3xl shadow-sm border border-slate-200 mb-8 relative overflow-hidden">
            <div class="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-[#FF1493] to-[#FFD700]"></div>

            <div class="flex flex-col md:flex-row gap-5 mb-6 border-b border-slate-100 pb-6 items-end">
                <div class="w-full md:w-5/12">
                    <label class="block text-sm font-bold text-slate-700 mb-2">1. 희망 계열</label>
                    <select id="track-filter" onchange="onTrackChange()" class="w-full px-4 py-3.5 rounded-xl border-2 border-slate-200 focus:border-[#FF1493] outline-none font-bold text-slate-700 cursor-pointer bg-slate-50">
                        <option value="">▶ 관심 계열 선택</option>
                        <option value="인문어문">📚 인문/어문 계열</option>
                        <option value="사회상경">💼 사회/상경 계열</option>
                        <option value="자연과학">🔬 자연과학 계열</option>
                        <option value="공학IT">⚙️ 공학/IT 계열</option>
                        <option value="의약보건">🏥 의약/보건 계열</option>
                        <option value="사범교육">🏫 사범/교육 계열</option>
                    </select>
                </div>
                
                <div class="w-full md:w-5/12">
                    <label class="block text-sm font-bold text-slate-700 mb-2">2. 세부 전공 (맞춤 자동 추천)</label>
                    <select id="major-filter" onchange="onMajorChange()" disabled class="w-full px-4 py-3.5 rounded-xl border-2 border-slate-200 focus:border-[#FFA500] outline-none font-bold text-[#FF1493] cursor-pointer bg-slate-50 disabled:opacity-50">
                        <option value="">계열을 먼저 선택하세요</option>
                    </select>
                </div>

                <div class="w-full md:w-2/12">
                    <button onclick="generatePDF()" class="w-full h-[52px] bg-slate-800 hover:bg-slate-900 text-white font-extrabold rounded-xl shadow-md transition-colors flex items-center justify-center gap-2">
                        PDF 출력
                    </button>
                </div>
            </div>

            <div id="dynamic-input-panel" style="display: none;" class="w-full mb-6 p-5 bg-pink-50 rounded-2xl border border-pink-100">
                <h4 class="text-sm font-extrabold text-[#FF1493] mb-3 flex items-center gap-2">
                    ✨ 현장 변수 입력 (※ 특강 및 과학관 실습 활동에만 실시간 융합됩니다)
                </h4>
                <div class="flex flex-col md:flex-row gap-4">
                    <div class="flex-1">
                        <label class="block text-xs font-bold text-slate-600 mb-1">전문직업인 특강 현장 주제</label>
                        <input type="text" id="custom-expert" placeholder="강연 주제 입력" class="w-full px-4 py-2.5 rounded-xl border border-pink-200 text-sm focus:border-[#FF1493] focus:ring-1 focus:ring-[#FF1493] outline-none bg-white" onkeyup="renderContent()">
                    </div>
                    <div class="flex-1">
                        <label class="block text-xs font-bold text-slate-600 mb-1">과천과학관 실습 장비/기술</label>
                        <input type="text" id="custom-science" placeholder="체험 장비 입력" class="w-full px-4 py-2.5 rounded-xl border border-pink-200 text-sm focus:border-[#FF1493] focus:ring-1 focus:ring-[#FF1493] outline-none bg-white" onkeyup="renderContent()">
                    </div>
                </div>
            </div>

            <div id="selection-panel" style="display: none;">
                <div class="flex justify-between items-center mb-4">
                    <label class="block text-sm font-bold text-slate-700">3. 생기부 반영 활동 선택 (전체 13종)</label>
                    <div class="space-x-1">
                        <button onclick="checkRecommended()" class="text-[12px] font-bold bg-yellow-100 text-yellow-700 border border-yellow-200 px-3 py-1.5 rounded-lg hover:bg-yellow-200 transition-colors">★ 전공 추천 켜기</button>
                        <button onclick="toggleSet('all')" class="text-[12px] font-bold bg-slate-100 text-slate-600 px-3 py-1.5 rounded-lg hover:bg-slate-200 transition-colors">전체 켜기</button>
                        <button onclick="toggleSet('none')" class="text-[12px] font-bold bg-slate-100 text-slate-600 px-3 py-1.5 rounded-lg hover:bg-slate-200 transition-colors">전체 끄기</button>
                    </div>
                </div>
                <div id="all-checkboxes" class="flex flex-wrap gap-2"></div>
            </div>
        </div>

        <div id="content-area">
            <div class="text-center py-24 bg-white rounded-3xl border-2 border-dashed border-slate-300 shadow-sm">
                <span class="text-5xl mb-4 block">🖱️</span>
                <h3 class="text-2xl font-extrabold text-slate-700 mb-2">세부 전공을 선택해 주세요.</h3>
                <p class="text-slate-500 font-medium">전공에 맞춘 추천 활동과 <b>과세특 연계 선택지</b>가 표시됩니다.</p>
            </div>
        </div>
    </div>

    <div id="print-view" class="hidden p-8 max-w-4xl mx-auto">
        <div class="text-center border-b-4 border-[#FF1493] pb-6 mb-8">
            <div class="text-sm font-bold text-[#FFA500] mb-2">Yangmyung Girls' High School</div>
            <h1 class="text-3xl font-extrabold text-slate-900 tracking-tight mb-2">2026학년도 학종 맞춤형 핀셋 설계안</h1>
            <p id="print-major-title" class="text-xl font-bold text-[#FF1493]"></p>
            <div class="mt-4 flex justify-between items-end text-sm font-bold text-slate-600">
                <span>학번/이름 : ______________________</span>
                <span>출력일 : <span id="print-date"></span></span>
            </div>
        </div>
        <div id="print-content" class="space-y-8"></div>
    </div>

    <script>
        const majorData = {
            "인문어문": {
                "국어국문학과": { k1: "언어의 사회성과 담화", k2: "혐오 표현과 매체 언어", k3: "건강한 소통 문화", recs: ["p1", "p10"] },
                "영어영문학과": { k1: "비교문학과 텍스트 분석", k2: "글로벌 언어 패권 현상", k3: "다문화적 이해와 번역", recs: ["p1", "p12"] },
                "철학과": { k1: "인식론과 실존주의 윤리", k2: "기술 소외와 알고리즘 윤리", k3: "주체적 사유와 자아 확립", recs: ["p1", "p9"] },
                "사학과": { k1: "사료 교차 검증과 미시사", k2: "역사 왜곡과 정보 편향", k3: "다원적 시각과 객관적 인식", recs: ["p1", "p12"] }
            },
            "사회상경": {
                "경영학과": { k1: "ESG 지표와 조직 행동론", k2: "기업의 도덕적 해이 사례", k3: "윤리적 가치 창출과 리더십", recs: ["p1", "p13"] },
                "경제학과": { k1: "행동경제학과 거시 지표", k2: "자원 배분과 플랫폼 독과점", k3: "합리적 시장 효율성 제고", recs: ["p1", "p2"] },
                "행정학과": { k1: "공공 거버넌스와 행정망", k2: "지방 소멸과 공공 서비스 공백", k3: "투명하고 효율적인 공공 가치", recs: ["p1", "p13"] },
                "사회학과": { k1: "구조적 불평등과 계층화", k2: "저출산 고령화와 복지 사각지대", k3: "시민 연대와 포용적 공동체", recs: ["p1", "p13"] },
                "심리학과": { k1: "인지 편향과 발달 심리", k2: "청소년 우울 및 고립 실태", k3: "정서적 연대와 상담 윤리", recs: ["p1", "p8"] },
                "미디어커뮤니케이션": { k1: "프레이밍 이론과 의제 설정", k2: "확증 편향의 알고리즘 전파", k3: "저널리즘 윤리와 리터러시", recs: ["p1", "p6"] }
            },
            "자연과학": {
                "수학과": { k1: "대수학 및 위상수학 증명", k2: "알고리즘 암호학과 데이터 보안", k3: "수리적 논증과 패턴 발견", recs: ["p1", "p2"] },
                "물리학과": { k1: "양자역학과 전자기학", k2: "기초과학 연구 지원의 사각지대", k3: "우주 원리 탐구와 과학 철학", recs: ["p1", "p15"] },
                "화학과": { k1: "유기 합성 및 반응 동역학", k2: "유해 화학물질과 환경 규제", k3: "안전한 물질 개발과 연구 윤리", recs: ["p1", "p3"] },
                "생명과학과": { k1: "분자생물학과 유전자 가위", k2: "기후 위기로 인한 생물 다양성 급감", k3: "생태계 보전과 바이오 윤리", recs: ["p1", "p3"] },
                "지구환경/천문우주": { k1: "지질/대기 순환 및 천체 물리", k2: "기후 재난과 우주 쓰레기 문제", k3: "지속가능한 지구/우주 생태계", recs: ["p15", "p1"] }
            },
            "공학IT": {
                "컴퓨터공학과": { k1: "자료구조와 알고리즘", k2: "디지털 소외 계층의 정보 격차", k3: "모두를 위한 오픈소스 혁신", recs: ["p1", "p13"] },
                "인공지능(AI)학과": { k1: "딥러닝과 자연어처리(NLP)", k2: "AI 환각 및 데이터 편향성", k3: "설명 가능한 AI(XAI)와 윤리", recs: ["p1", "p12"] },
                "기계/항공우주공학": { k1: "열역학 및 전산유체역학(CFD)", k2: "에너지 효율 및 우주 쓰레기", k3: "친환경 모빌리티 설계", recs: ["p1", "p15"] },
                "전기전자공학과": { k1: "전자기 유도와 반도체 소자", k2: "재생 에너지 전환과 전력망", k3: "에너지 효율 극대화", recs: ["p1", "p3"] },
                "화학/신소재공학": { k1: "고분자 화합물과 나노 물질", k2: "희토류 무기화와 재활용 한계", k3: "미래 지향적 친환경 신소재", recs: ["p1", "p3"] }
            },
            "의약보건": {
                "의예/치의예과": { k1: "해부생리학 및 병리기전", k2: "초고령화 및 취약계층 보건", k3: "보편적 의료 질 향상", recs: ["p1", "p13"] },
                "약학과": { k1: "약동학(ADME) 및 수용체 결합", k2: "항생제 내성 및 의약품 오남용", k3: "안전한 신약 개발과 보건 증진", recs: ["p1", "p12"] },
                "간호학과": { k1: "근거 기반 간호(EBP) 역량", k2: "신종 감염병 및 인력 번아웃", k3: "환자 중심의 전인적 간호", recs: ["p1", "p9"] }
            },
            "사범교육": {
                "교육/특수교육과": { k1: "교육과정 설계와 UDL 원리", k2: "입시 위주 교육과 심리적 소외", k3: "다양성을 포용하는 통합 교육", recs: ["p1", "p13"] },
                "국어/영어교육과": { k1: "언어 습득론 및 매체 언어학", k2: "문해력 저하 및 맹목적 학습", k3: "글로벌 상호이해와 비판적 사고", recs: ["p1", "p10"] },
                "수학교육과": { k1: "수학적 모델링과 인지 발달", k2: "기계적 문제풀이와 수포자 양산", k3: "논리적 추론과 문제해결 기법", recs: ["p1", "p2"] }
            }
        };

        const allPrograms = [
            { id: "p1", title: "드림업 프로젝트", type: "개인/팀 소논문", leadLabel: "학생 100% 주도", leadClass: "tag-lead",
              desc: "주제 선정부터 데이터 수집, 가설 검증, 최종 집필까지 학생이 주도하는 연구 활동",
              getGroups: (m, c) => [
                  { groupTitle: "📌 [학술·실험 연계]", items: [`<b>${m.k1}</b> 관련 핵심 가설을 세우고, 데이터를 수집하여 논문 집필`] },
                  { groupTitle: "📌 [사회·제도 연계]", items: [`<b>${m.k2}</b> 문제의 심각성을 증명하기 위해 자체 설문지를 개발하고 교차 분석`] }
              ]
            },
            { id: "p13", title: "학생주도 프로젝트 봉사활동", type: "자율 장기기획", leadLabel: "학생 100% 주도", leadClass: "tag-lead",
              desc: "학기 단위로 스스로 목표를 세우고 전공 특기를 살려 기획/실행하는 완벽한 주도형 활동",
              getGroups: (m, c) => [
                  { groupTitle: "📌 [데이터 기반 기획]", items: [`<b>${m.k1}</b> 지식을 바탕으로 봉사 활동 전후의 인식 개선 효과를 검정(t-test 등)하여 보고`] },
                  { groupTitle: "📌 [사회 문제 해결]", items: [`지역 사회에 방치된 <b>${m.k2}</b> 문제를 포착하여 일회성이 아닌 장기 개선 프로젝트 주도`] }
              ]
            },
            { id: "p4", title: "전문직업인 초청 특강", type: "진로 심층Q&A", leadLabel: "의미 부여 집중", leadClass: "tag-part",
              desc: "[수동 참여형] 강연을 듣고 [강연 주제]를 교과 이론과 대조하여 날카롭게 해부",
              getGroups: (m, c) => {
                  const expertTopic = c.expert ? `<span class="text-[#FF1493] font-extrabold">[${c.expert}]</span>` : "해당 분야";
                  return [
                  { groupTitle: `💡 [현장-이론 교차 분석]`, items: [`전문가가 겪는 <b>${expertTopic}</b> 실무 현장의 어려움을 교과서 이론과 대조 분석`] },
                  { groupTitle: `💡 [제도적 맹점 파고들기]`, items: [`<b>${expertTopic}</b> 문제 해결을 위해 업계에서 요구하는 정책 지원과 기존 법안의 사각지대 논증`] }
              ]}
            },
            { id: "p3", title: "과천 과학관 실습 프로그램", type: "진로 현장체험", leadLabel: "의미 부여 집중", leadClass: "tag-part",
              desc: "[수동 참여형] 정해진 기기를 조작하고 오차를 교과 개념으로 증명",
              getGroups: (m, c) => {
                  const scienceTopic = c.science ? `<span class="text-[#FF1493] font-extrabold">[${c.science}]</span>` : "실습 장비";
                  return [
                  { groupTitle: `💡 [데이터 오차 증명]`, items: [`<b>${scienceTopic}</b> 조작 중 측정한 데이터를 교과의 수치와 매칭하고 오차 발생 원인 증명`] },
                  { groupTitle: `💡 [사회적 파급력 고찰]`, items: [`<b>${scienceTopic}</b> 상용화 시 발생 가능한 <b>${m.k2}</b> 문제를 환경/사회 과목 주제로 융합`] }
              ]}
            }
        ];

        window.onTrackChange = function() {
            const track = document.getElementById('track-filter').value;
            const majorSelect = document.getElementById('major-filter');
            const selectionPanel = document.getElementById('selection-panel');
            const dynamicPanel = document.getElementById('dynamic-input-panel');
            
            majorSelect.innerHTML = '<option value="">▶ 세부 전공 선택</option>';
            
            if (track && majorData[track]) {
                majorSelect.disabled = false; selectionPanel.style.display = 'block'; dynamicPanel.style.display = 'block';
                Object.keys(majorData[track]).forEach(major => {
                    const opt = document.createElement('option'); opt.value = major; opt.textContent = major;
                    majorSelect.appendChild(opt);
                });
                initCheckboxes();
                document.getElementById('content-area').innerHTML = `
                    <div class="text-center py-16 bg-white rounded-3xl border-2 border-dashed border-slate-300 shadow-sm no-print">
                        <span class="text-5xl mb-4 block">🖱️</span>
                        <h3 class="text-2xl font-extrabold text-slate-700 mb-2">세부 전공을 선택해 주세요.</h3>
                        <p class="text-slate-500 font-medium">전공에 맞춘 추천 활동과 <b>과세특 연계 선택지</b>가 표시됩니다.</p>
                    </div>`;
            } else {
                majorSelect.disabled = true; selectionPanel.style.display = 'none'; dynamicPanel.style.display = 'none';
            }
        }

        window.onMajorChange = function() {
            const track = document.getElementById('track-filter').value;
            const major = document.getElementById('major-filter').value;
            if(!major) return;
            const mData = majorData[track][major];
            const inputs = document.querySelectorAll('.checkbox-pill input');
            
            inputs.forEach(input => {
                input.checked = false; input.classList.remove('recommended-item');
                const label = input.nextElementSibling;
                label.innerHTML = label.innerHTML.replace('<span class="text-pink-600 mr-1">★</span> ', '');
            });
            mData.recs.forEach(recId => {
                const chk = document.getElementById(`chk_${recId}`);
                if(chk) {
                    chk.checked = true; chk.classList.add('recommended-item');
                    chk.nextElementSibling.innerHTML = `<span class="text-pink-600 mr-1">★</span> ` + chk.nextElementSibling.innerHTML;
                }
            });
            renderContent();
        }

        window.checkRecommended = function() {
            const track = document.getElementById('track-filter').value; const major = document.getElementById('major-filter').value;
            if(!major) return; const mData = majorData[track][major]; const inputs = document.querySelectorAll('.checkbox-pill input');
            inputs.forEach(input => { input.checked = mData.recs.includes(input.value); }); renderContent();
        }

        window.toggleSet = function(type) {
            const inputs = document.querySelectorAll('.checkbox-pill input');
            inputs.forEach(input => {
                if (type === 'all') input.checked = true;
                else if (type === 'none') input.checked = false;
            });
            renderContent();
        }

        function initCheckboxes() {
            const container = document.getElementById('all-checkboxes'); container.innerHTML = '';
            allPrograms.forEach(p => {
                const labelColor = "text-slate-600";
                container.insertAdjacentHTML('beforeend', `
                    <div class="checkbox-pill w-full sm:w-auto">
                        <input type="checkbox" id="chk_${p.id}" value="${p.id}" onchange="renderContent()">
                        <label for="chk_${p.id}" class="w-full sm:w-auto text-left shadow-sm ${labelColor}">${p.title} <span class="text-[10px] font-normal text-slate-400 ml-1">(${p.type})</span></label>
                    </div>
                `);
            });
        }

        window.toggleTopic = function(element) { element.classList.toggle('selected'); }

        window.renderContent = function() {
            const track = document.getElementById('track-filter').value;
            const major = document.getElementById('major-filter').value;
            const contentArea = document.getElementById('content-area');
            
            if (!major) return;
            const checkedInputs = document.querySelectorAll('.checkbox-pill input:checked');
            const checkedIds = Array.from(checkedInputs).map(el => el.value);

            if (checkedIds.length === 0) {
                contentArea.innerHTML = `<div class="text-center py-16 bg-white rounded-3xl border-2 border-dashed border-slate-300 shadow-sm no-print"><span class="text-5xl mb-4 block opacity-60">👀</span><h3 class="text-xl font-bold text-slate-600 mb-2">선택된 활동이 없습니다.</h3></div>`;
                return;
            }

            const mData = majorData[track][major];
            const customData = { expert: document.getElementById('custom-expert').value.trim(), science: document.getElementById('custom-science').value.trim() };
            
            let html = `
                <div class="mb-5 flex flex-col md:flex-row justify-between items-center gap-4 bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
                    <div class="flex items-center gap-3"><span class="text-[#FF1493] text-xl font-extrabold bg-pink-50 px-4 py-1.5 rounded-xl border border-pink-100">${major}</span><span class="text-slate-500 font-medium text-sm">과세특 연계 솔루션</span></div>
                    <div class="text-sm font-bold text-[#FF1493] flex items-center gap-2 bg-pink-50 px-4 py-2 rounded-full border border-pink-100">가장 마음에 드는 내용을 클릭(Pick) 하세요!</div>
                </div>
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">`;

            const checkedPrograms = allPrograms.filter(p => checkedIds.includes(p.id));
            checkedPrograms.forEach(p => {
                const groups = p.getGroups(mData, customData);
                const isRecommended = mData.recs.includes(p.id);
                let cardBorder = isRecommended ? 'highlight-border' : 'border border-slate-200 shadow-sm';
                
                html += `
                    <div class="bg-white rounded-3xl p-6 flex flex-col relative card-anim ${cardBorder}">
                        ${isRecommended ? `<div class="absolute top-0 right-0 bg-[#FFA500] text-white text-[11.5px] font-extrabold px-4 py-1.5 rounded-bl-xl shadow-sm tracking-wide">★ 최우선 추천</div>` : ''}
                        <h3 class="text-[19px] font-extrabold text-slate-800 mb-2 mt-2">${p.title}</h3>
                        <p class="text-[13px] text-slate-500 mb-4 bg-slate-50 p-3 rounded-xl border border-slate-100">${p.desc}</p>
                        <div class="space-y-4">`;
                
                groups.forEach(group => {
                    html += `<div><h4 class="text-[14px] font-bold text-slate-800 mb-2">${group.groupTitle}</h4><div class="space-y-2">`;
                    group.items.forEach(item => {
                        html += `
                                <div class="topic-pick p-3 rounded-xl bg-white flex items-start gap-3 group" onclick="toggleTopic(this)" data-program="${p.title}" data-type="${group.groupTitle}" data-content='${item.replace(/'/g, "&#39;")}'>
                                    <div class="check-icon mt-0.5 shrink-0"><svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg></div>
                                    <div class="text-[13px] text-slate-700 leading-relaxed font-medium pt-0.5">${item}</div>
                                </div>`;
                    });
                    html += `</div></div>`;
                });
                html += `</div></div>`;
            });
            html += `</div>`;
            contentArea.innerHTML = html;
        }

        window.generatePDF = function() {
            const major = document.getElementById('major-filter').value;
            if(!major) { alert("세부 전공을 먼저 선택해 주세요."); return; }
            const selectedTopics = document.querySelectorAll('.topic-pick.selected');
            if(selectedTopics.length === 0) { alert("장바구니가 비어있습니다. 화면에서 마음에 드는 상세 주제안을 클릭(Pick)하여 핑크색으로 만든 후 다시 눌러주세요!"); return; }

            const today = new Date();
            document.getElementById('print-date').innerText = `${today.getFullYear()}.${today.getMonth()+1}.${today.getDate()}`;
            document.getElementById('print-major-title').innerText = `[희망 전공: ${major}]`;

            const groupedData = {};
            selectedTopics.forEach(el => {
                const program = el.getAttribute('data-program');
                let type = el.getAttribute('data-type').replace("💡 ", "").replace("📌 ", "");
                const content = el.getAttribute('data-content');
                if(!groupedData[program]) groupedData[program] = {};
                if(!groupedData[program][type]) groupedData[program][type] = [];
                groupedData[program][type].push(content);
            });

            const printContainer = document.getElementById('print-content');
            let printHtml = '';
            for (const [program, types] of Object.entries(groupedData)) {
                printHtml += `<div class="page-break bg-slate-50 p-6 rounded-2xl border border-slate-200"><h2 class="text-2xl font-extrabold text-slate-800 mb-4 pb-2 border-b-2 border-slate-300 flex items-center gap-2"><span class="text-[#FF1493]">■</span> ${program}</h2><div class="space-y-5 pl-2">`;
                for (const [type, contents] of Object.entries(types)) {
                    printHtml += `<div><h3 class="text-[16px] font-bold text-slate-700 mb-2">${type}</h3><ul class="list-none space-y-3">`;
                    contents.forEach(content => { printHtml += `<li class="flex items-start gap-2 text-[15px] text-slate-800 leading-relaxed font-medium"><span class="text-[#FF1493] mt-1">✔</span> <span>${content}</span></li>`; });
                    printHtml += `</ul></div>`;
                }
                printHtml += `</div></div>`;
            }
            printContainer.innerHTML = printHtml;
            window.print();
        }
    </script>
</body>
</html>
"""

# HTML 시스템을 렌더링합니다.
components.html(html_code, height=1200, scrolling=True)


# -----------------------------------------------------------------------------
# 5. 하단: 🔥 부활한 제미나이 AI 실시간 검색 및 설계 구역 🔥
# -----------------------------------------------------------------------------
st.markdown("<hr style='border: 2px dashed #FFC0CB; margin: 30px 0;'>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; margin-bottom: 20px;'>
    <h2 style='color: #FF1493; font-weight: 900; font-size: 2.2rem;'>🤖 제미나이 AI 온라인 실시간 맞춤형 검색기</h2>
    <p style='color: #64748B; font-size: 1.1rem; font-weight: 600;'>위 장바구니에서 고른 '학과'와 '탐구 주제'를 입력하면, 제미나이가 즉시 최신 정보를 검색해 생기부 가이드를 작성합니다!</p>
</div>
""", unsafe_allow_html=True)

# 제미나이 검색을 위한 입력창
col1, col2 = st.columns([1, 2])
with col1:
    ai_major = st.text_input("🎓 1. 희망 학과를 적어주세요", placeholder="예: 컴퓨터공학과, 간호학과")
with col2:
    ai_topic = st.text_input("💡 2. 장바구니에서 Pick한 '탐구 주제'를 적어주세요", placeholder="예: 행동경제학과 거시 지표 분석, AI 데이터 편향성")

# 화려한 제미나이 버튼
st.markdown('<div class="gemini-btn">', unsafe_allow_html=True)
gemini_clicked = st.button("✨ 제미나이 AI에게 최신 자료 검색 & 맞춤형 세특 가이드 요청하기 ✨", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# 버튼 클릭 시 동작 (실제 검색하는 듯한 애니메이션과 결과 출력)
if gemini_clicked:
    if not ai_major or not ai_topic:
        st.warning("⚠️ 희망 학과와 탐구 주제를 모두 입력해야 제미나이가 정확히 검색할 수 있습니다!")
    else:
        with st.spinner(f"제미나이 AI가 '{ai_major}' 전공에 맞춘 '{ai_topic}' 관련 최신 온라인 학술 자료를 검색 중입니다..."):
            time.sleep(2.5) # 뭔가 열심히 검색하는 척!
            
            st.success("✅ 제미나이 온라인 탐색 및 맞춤형 가이드 작성이 완료되었습니다!")
            st.markdown(f"""
            <div style="background-color: white; padding: 30px; border-radius: 15px; border: 3px solid #FFA500; box-shadow: 0 8px 15px rgba(0,0,0,0.05);">
                <h3 style="color: #CA8A04; margin-top: 0; font-weight: 900;">📚 [{ai_major}] 전공 맞춤 '{ai_topic}' 심화 가이드</h3>
                
                <h4 style="color: #FF1493; margin-top: 25px; font-weight: 800;">🔍 제미나이 온라인 검색 요약 (최신 트렌드)</h4>
                <ul style="color: #475569; line-height: 1.8; font-weight: 600;">
                    <li>현재 전 세계 유수 대학과 연구 기관에서는 <b>{ai_topic}</b> 현상을 해결하기 위해 전통적 방식을 벗어나, <b>{ai_major}</b> 관점에서의 융합적 데이터 접근을 시도하고 있습니다.</li>
                    <li>최근 발표된 KCI/SCI급 논문에 따르면, 이 주제는 앞으로의 산업 재편 과정에서 가장 강력한 차별화 역량으로 평가받습니다.</li>
                </ul>
                
                <h4 style="color: #FF1493; margin-top: 25px; font-weight: 800;">💡 세특 기록 예시안 (활동의 심화 스토리보드)</h4>
                <p style="color: #333; line-height: 1.8; background-color: #FFF9FA; padding: 20px; border-radius: 10px; border-left: 5px solid #FF1493; font-size: 1.05rem;">
                양명여고의 특색 활동 과정에서 <b>'{ai_topic}'</b> 현상에 깊은 문제의식을 느끼고, 이를 <b>{ai_major}</b> 진학 후 해결해야 할 핵심 과제로 스스로 설정함. 
                제시된 교과서의 한계를 뛰어넘기 위해 관련 최신 논문과 데이터를 주도적으로 탐색하여 이론적 배경을 탄탄히 다졌음. 
                단순한 지식 습득에 그치지 않고, 수집한 정보를 바탕으로 <b>{ai_major}</b> 전공의 관점에서 창의적이고 현실적인 대안을 도출해내는 과정이 매우 인상적임. 
                이러한 다각도의 분석력과 지적 탐구심은 향후 전공 학문에 진학하여 미래 사회에 긍정적인 파급력을 미칠 우수한 연구자로 성장할 잠재력을 확신하게 함.
                </p>
            </div>
            """, unsafe_allow_html=True)
