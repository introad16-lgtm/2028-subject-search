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
            특히 해당 학과와 관련된 실제 도서나 논문, 참고할 만한 웹사이트 링크를 반드시 포함해 주세요.
            
            아래 마크다운 양식에 맞춰 작성하세요:
            ### 💡 1. [{target_name}] 맞춤형 탐구 주제 제안 (2가지)
            ### 📚 2. 탐구를 위한 구체적인 활동 전개 팁 (자료 조사 방법, 결과물 형태 등)
            ### 🎓 3. 생기부 과세특/창체 기록 예시안 (4~5줄)
            ### 📖 4. 심화 탐구를 위한 추천 참고 문헌 (추천 도서 2권 및 RISS/KCI 논문 검색 키워드)
            ### 🔗 5. [{target_name}] 전공 탐색 추천 웹사이트 (주요 대학 학과 홈페이지, 관련 국책 연구소, 학회 링크 등)
            """
        else:
            prompt = f"""
            당신은 대한민국 최고 수준의 고등학교 진로진학 전문 교사입니다.
            - 학생 진로/학과: {target_name}
            - 선택한 학교 활동: {selected_act} (비주도형/강의 청취형 활동)
            - 수강한 강의/특강 제목: {custom_title}
            
            요청: 이 학생이 '{custom_title}'라는 수동적인 강의/특강을 들은 후, '{target_name}' 전공과 연계하여 
            '어떤 심화 후속 활동'을 스스로 진행하면 생기부에 주도성을 어필할 수 있을지 가이드라인을 제시해 주세요.
            특히 해당 학과와 관련된 실제 도서나 논문, 참고할 만한 웹사이트 링크를 반드시 포함해 주세요.
            
            아래 마크다운 양식에 맞춰 작성하세요:
            ### 🔍 1. 강의 내용과 [{target_name}]의 연결 고리
            ### 🏃‍♂️ 2. 주도성 어필을 위한 후속 심화 활동 가이드 (추가 독서, 소논문 등)
            ### 🎓 3. 생기부 과세특/창체 기록 예시안 (4~5줄)
            ### 📖 4. 심화 탐구를 위한 추천 참고 문헌 (강의 내용과 전공을 엮을 수 있는 도서 2권 및 논문 키워드)
            ### 🔗 5. [{target_name}] 전공 탐색 추천 웹사이트 (주요 대학 학과 홈페이지, 관련 국책 연구소, 학회 등)
            """
            
        try:
            with st.spinner(f"🌐 제미나이 AI가 '{target_name}' 진로에 맞춰 실시간으로 가이드와 참고 문헌을 검색 중입니다..."):
                genai.configure(api_key=api_key)
                
                # 가용 모델 자동 탐색 로직
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
                    
                    st.success(f"✅ 제미나이 AI가 맞춤형 문헌 검색 및 설계를 완료했습니다! (모델: {chosen_model})")
                    
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
                    
                    # 🖨️ PDF 출력 버튼 추가
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
                    </div>
                    """, height=100)

        except Exception as e:
            st.error(f"🚨 제미나이 통신 중 오류가 발생했습니다. (에러 내용: {e})")
