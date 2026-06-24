@st.cache_data
def get_local_admission_stats(file_path, target_univ, target_major):
    if not os.path.exists(file_path):
        return ""
    try:
        df = pd.read_excel(file_path, sheet_name=0)
        filtered_df = df.copy()
        
        # 1단계: 입력한 대학명과 학과명이 둘 다 일치하는 데이터 필터링
        if target_univ:
            filtered_df = filtered_df[filtered_df['대학명'].str.contains(target_univ, na=False)]
        if target_major:
            filtered_df = filtered_df[filtered_df['지원학과(모집단위)'].str.contains(target_major, na=False)]
        
        # 2단계: 만약 해당 대학에 데이터가 없다면, 대학 무관 '같은 학과' 데이터만 다시 검색
        is_fallback = False
        if filtered_df.empty and target_major:
             filtered_df = df[df['지원학과(모집단위)'].str.contains(target_major, na=False)]
             is_fallback = True

        # 3단계: 타 대학을 뒤졌는데도 아예 학과 자체가 없으면 안내문 출력
        if filtered_df.empty:
            return f"❌ 최근 3개년(2022~2025) 양명여고 데이터에 '{target_major}' 관련 지원 기록이 아예 존재하지 않습니다."
        
        # 통계 계산 진행
        stats = filtered_df.groupby(['대학명', '전형명', '최종합불결과'])['전교과_내신평균'].agg(['count', 'mean', 'min', 'max']).reset_index()
        stats.columns = ['대학명', '전형명', '결과', '지원건수', '평균내신', '최고내신(min)', '최저내신(max)']
        
        # 💡 선생님의 의견 반영: 타 대학 데이터일 경우 안내 문구를 명확하게 구분!
        if is_fallback and target_univ:
            stats_str = f"💡 [참고 데이터] 최근 3년간 양명여고 선배들의 '{target_univ} {target_major}' 지원 기록이 없습니다.\n"
            stats_str += f"👉 대신 엑셀 DB에 등록된 **'다른 대학교의 {target_major}'** 관련 지원 통계를 출력합니다.\n\n"
        else:
            stats_str = f"📈 [양명여고 최근 3년 '{target_univ} {target_major}' 관련 지원 통계]\n\n"
            
        for index, row in stats.iterrows():
            stats_str += f"- 대학/전형: {row['대학명']} ({row['전형명']})\n"
            stats_str += f"  결과: {row['결과']} ({row['지원건수']}건)\n"
            stats_str += f"  내신: 평균 {row['평균내신']:.2f} (최고 {row['최고내신(min)']:.2f} ~ 최저 {row['최저내신(max)']:.2f})\n\n"
            
        return stats_str
    except Exception as e:
        return f"엑셀 데이터 분석 중 오류 발생: {e}"
