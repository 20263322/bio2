import streamlit as st
import time

# 웹페이지 기본 설정
st.set_page_config(page_title="Bio-II ZPD Diagnostic System", page_icon="🧬", layout="centered")

# 세션 상태 초기화 (재진단 이력 저장용)
if 'history' not in st.session_state:
    st.session_state.history = {}  # 단원별 이전 진단 기록 저장
if 'started' not in st.session_state:
    st.session_state.started = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# 타이틀 및 안내 문구
st.title("🧬 [생명과학 II] 맞춤형 ZPD 진단 시스템")
st.markdown("문제를 풀고 제출하면 **정답률과 메타인지 확신도**를 종합 분석하여 맞춤형 학습 비계(Scaffolding)를 처방해 드립니다.")

st.divider()

# 1. 멘티 기본 정보 입력
col1, col2 = st.columns(2)
with col1:
    mentee_name = st.text_input("멘티 이름", value="", placeholder="이름을 입력하세요")
with col2:
    selected_unit = st.selectbox("진단 단원 선택", [
        "1회차: 효소와 반응 속도", 
        "2회차: 세포 호흡과 광합성", 
        "3회차: DNA 복제 기작", 
        "4회차: 유전자 발현 조절 및 집단 유전"
    ], disabled=st.session_state.started)

# -------------------- 40개 문항 데이터베이스 --------------------
question_db = {
    "1회차: 효소와 반응 속도": [
        {"q": "Q1. 경쟁적 저해제를 첨가했을 때 효소 반응 속도론적 변화로 옳은 것은?", "opts": ["Vmax 감소, Km 증가", "Vmax 일정, Km 증가", "Vmax 감소, Km 일정", "Vmax 일정, Km 감소"], "ans": "Vmax 일정, Km 증가"},
        {"q": "Q2. 비경쟁적 저해제가 결합하는 효소의 결합 부위는 어디인가?", "opts": ["활성 부위", "타당성(Allosteric) 부위", "기질 결합 부위", "비활성 부위"], "ans": "타당성(Allosteric) 부위"},
        {"q": "Q3. 효소 작용 시 반응 속도 및 에너지 변화에 대한 설명으로 옳은 것은?", "opts": ["효소는 활성화 에너지를 감소시킨다.", "효소는 반응열(ΔH)을 증가시킨다.", "효소는 반응물 자체의 에너지를 높인다.", "비경쟁적 저해제는 기질 농도를 높이면 완전히 극복된다."], "ans": "효소는 활성화 에너지를 감소시킨다."},
        {"q": "Q4. 기질 농도가 충분히 높을 때 효소 반응 속도가 더 이상 증가하지 않고 일정해지는 원인은?", "opts": ["기질의 변성", "모든 효소의 활성 부위가 기질로 포화됨", "저해제의 강한 결합", "반응열의 소진"], "ans": "모든 효소의 활성 부위가 기질로 포화됨"},
        {"q": "Q5. 최적 온도를 초과했을 때 효소의 반응 속도가 급격히 감소하는 주된 이유는?", "opts": ["기질의 농도 감소", "효소 단백질의 3차원 입체 구조 변성", "활성화 에너지의 증가", "생성물의 기질 재변환"], "ans": "효소 단백질의 3차원 입체 구조 변성"},
        {"q": "Q6. 미카엘리스 상수(Km)에 대한 설명으로 옳은 것은?", "opts": ["반응 속도가 Vmax일 때의 기질 농도이다.", "반응 속도가 1/2 Vmax일 때의 기질 농도이다.", "Km 값이 클수록 효소와 기질의 친화도가 높다.", "효소의 농도에 비례하여 증가한다."], "ans": "반응 속도가 1/2 Vmax일 때의 기질 농도이다."},
        {"q": "Q7. 효소의 주효소와 조효소가 결합하여 완전한 활성을 가질 때의 상태를 무엇이라 하는가?", "opts": ["아포효소", "전효소(Holoenzyme)", "조효소", "비활성 효소"], "ans": "전효소(Holoenzyme)"},
        {"q": "Q8. 음성 피드백 조절(Feedback Inhibition)에서 최종 산물이 주로 결합하는 부위는?", "opts": ["첫 번째 효소의 활성 부위", "첫 번째 효소의 타당성(Allosteric) 부위", "마지막 효소의 기질 부위", "수용체 부위"], "ans": "첫 번째 효소의 타당성(Allosteric) 부위"},
        {"q": "Q9. 비경쟁적 저해제를 추가했을 때 Km값과 Vmax값의 변화로 옳은 것은?", "opts": ["Km 일정, Vmax 감소", "Km 증가, Vmax 일정", "Km 감소, Vmax 감소", "Km 증가, Vmax 증가"], "ans": "Km 일정, Vmax 감소"},
        {"q": "Q10. 효소-기질 복합체(ES)가 형성되는 핵심 원리는 무엇인가?", "opts": ["기질의 무작위 분해", "효소 활성 부위와 기질의 입체 구조적 상열성(기질 특이성)", "공유 결합에 의한 영구 결합", "온도 상승에 의한 강제 결합"], "ans": "효소 활성 부위와 기질의 입체 구조적 상열성(기질 특이성)"}
    ],
    "2회차: 세포 호흡과 광합성": [
        {"q": "Q1. TCA 회로에서 C6(시트르산)이 C5(알파케토글루타르산)로 변할 때 방출되는 물질은?", "opts": ["CO2 및 NADH", "ATP 및 FADH2", "O2 및 H2O", "피루브산"], "ans": "CO2 및 NADH"},
        {"q": "Q2. 세포 호흡 과정 중 가장 많은 ATP가 생성되는 장소와 과정은?", "opts": ["세포질 - 해당작업", "미토콘드리아 기질 - TCA 회로", "미토콘드리아 내막 - 산화적 인산화", "미토콘드리아 외막 - 피루브산 산화"], "ans": "미토콘드리아 내막 - 산화적 인산화"},
        {"q": "Q3. 포도당 1분자가 해당작업을 거칠 때 알짜 생성물로 옳은 것은?", "opts": ["2 피루브산, 2 ATP, 2 NADH", "2 피루브산, 4 ATP, 2 FADH2", "1 피루브산, 2 ATP, 1 NADH", "2 아세틸 CoA, 2 CO2, 2 ATP"], "ans": "2 피루브산, 2 ATP, 2 NADH"},
        {"q": "Q4. 산화적 인산화 과정에서 ATP 합성 효소를 구동시키는 직접적인 원동력은?", "opts": ["전자전달계의 직접적인 ATP 분해", "미토콘드리아 막간 공간과 기질 사이의 수소 이온(H+) 농도 기배", "산소 분자의 산화력", "피루브산의 탈카복실화"], "ans": "미토콘드리아 막간 공간과 기질 사이의 수소 이온(H+) 농도 기배"},
        {"q": "Q5. 산소가 없을 때 해당작업이 지속되기 위해 반드시 재산화되어야 하는 물질은?", "opts": ["FADH2", "NADH", "ATP", "피루브산"], "ans": "NADH"},
        {"q": "Q6. 광합성의 명반응이 일어나는 장소와 암반응(캘빈 회로)이 일어나는 장소가 바르게 짝지어진 것은?", "opts": ["스트로마 - 틸라코이드 내막", "틸라코이드 내막 - 스트로마", "외막 - 내막", "그라나 - 크리스티"], "ans": "틸라코이드 내막 - 스트로마"},
        {"q": "Q7. 광합성 명반응의 최종 산물로 캘빈 회로에 공급되는 물질 2가지는?", "opts": ["ATP, NADPH", "CO2, H2O", "포도당, O2", "ADP, NADP+"], "ans": "ATP, NADPH"},
        {"q": "Q8. 캘빈 회로에서 CO2를 최초로 받아들이는 5탄소 화합물은?", "opts": ["3-PG", "G3P", "RuBP", "옥살아세트산"], "ans": "RuBP"},
        {"q": "Q9. 광합성 과정 중 물(H2O)의 광분해로 인해 방출되는 기체는?", "opts": ["CO2", "O2", "N2", "H2"], "ans": "O2"},
        {"q": "Q10. 세포 호흡의 호흡률(RQ = 방출된 CO2량 / 소비된 O2량)이 1.0인 호흡 기질은?", "opts": ["탄수화물", "지방", "단백질", "유기산"], "ans": "탄수화물"}
    ],
    "3회차: DNA 복제 기작": [
        {"q": "Q1. DNA 중합 효소가 새로운 가닥을 신장시키는 방향은?", "opts": ["5' → 3' 방향", "3' → 5' 방향", "양방향 임의 합성", "프라이머의 방향에 따라 가변적"], "ans": "5' → 3' 방향"},
        {"q": "Q2. 지연가닥(Lagging strand)에서 불연속적으로 합성되는 짧은 DNA 조각의 명칭은?", "opts": ["프라이머 절편", "오카자키 절편", "리게이스 절편", "선도 절편"], "ans": "오카자키 절편"},
        {"q": "Q3. DNA 복제 과정 중 RNA 프라이머를 제거하고 진짜 DNA 뉴클레오타이드로 교체하는 효소는?", "opts": ["DNA 헬리카아제", "DNA 중합 효소 I", "DNA 중합 효소 III", "DNA 연결 효소(Ligase)"], "ans": "DNA 중합 효소 I"},
        {"q": "Q4. DNA 이중 가닥의 수소 결합을 풀어서 복제 팽대(Replication fork)를 형성하는 효소는?", "opts": ["DNA 헬리카아제", "프라이메이스", "DNA 연결 효소", "토포이소머레이스"], "ans": "DNA 헬리카아제"},
        {"q": "Q5. DNA 중합 효소가 합성을 시작하기 위해 반드시 필요한 3'-OH기를 제공해 주는 물질은?", "opts": ["RNA 프라이머", "DNA 프로모터", "오카자키 절편", "신호 단백질"], "ans": "RNA 프라이머"},
        {"q": "Q6. 끊어진 DNA 가닥의 3'-OH와 5'-인산기 사이에 인산디에스테르 결합을 형성하여 연결해 주는 효소는?", "opts": ["DNA 연결 효소(Ligase)", "DNA 헬리카아제", "RNA 중합 효소", "제한 효소"], "ans": "DNA 연결 효소(Ligase)"},
        {"q": "Q7. 메셀슨과 스타일의 실험을 통해 증명된 DNA 복제 방식은?", "opts": ["보존적 복제", "반보존적 복제", "분산적 복제", "랜덤 복제"], "ans": "반보존적 복제"},
        {"q": "Q8. DNA 복제 시 이중 가닥이 풀릴 때 발생하는 과도한 꼬임(장력)을 해제해 주는 효소는?", "opts": ["토포이소머레이스(선회효소)", "DNA 중합 효소 II", "프라이메이스", "엑소뉴클레아제"], "ans": "토포이소머레이스(선회효소)"},
        {"q": "Q9. 진핵생물의 선형 염색체 말단이 복제 과정을 거치며 짧아지는 것을 방지하는 특수 구조는?", "opts": ["테로메어(Telomere)", "센트로메어", "뉴클레오솜", "플라스미드"], "ans": "테로메어(Telomere)"},
        {"q": "Q10. DNA 중합 효소가 잘못 삽입된 뉴클레오타이드를 즉시 확인하고 제거하는 교정 기능(Proofreading)의 방향은?", "opts": ["3' → 5' 엑소뉴클레아제 활성", "5' → 3' 엑소뉴클레아제 활성", "3' → 5' 엔도뉴클레아제 활성", "양방향 동시 활성"], "ans": "3' → 5' 엑소뉴클레아제 활성"}
    ],
    "4회차: 유전자 발현 조절 및 집단 유전": [
        {"q": "Q1. 대장균의 젖당 오페론에서 젖당이 존재하는 경우 일어나는 현상은?", "opts": ["억제 단백질이 작동 부위에 강하게 결합한다.", "젖당(알로젖당)이 억제 단백질과 결합하여 작동 부위에서 떼어낸다.", "RNA 중합 효소가 프로모터에 결합하지 못한다.", "전사가 완전히 중단된다."], "ans": "젖당(알로젖당)이 억제 단백질과 결합하여 작동 부위에서 떼어낸다."},
        {"q": "Q2. 하디-바인베르크 평형 집단에서 열성 표현형(aa) 개체의 빈도가 0.16일 때, 열성 대립유전자(a)의 빈도 q는?", "opts": ["0.16", "0.32", "0.4", "0.6"], "ans": "0.4"},
        {"q": "Q3. 위 집단(q=0.4, p=0.6)에서 이형접합자(Aa) 개체의 빈도 2pq는?", "opts": ["0.24", "0.36", "0.48", "0.52"], "ans": "0.48"},
        {"q": "Q4. 젖당 오페론에서 RNA 중합 효소가 직접 결합하여 전사를 시작하는 부위는?", "opts": ["프로모터(Promoter)", "작동 부위(Operator)", "조절 유전자", "구조 유전자"], "ans": "프로모터(Promoter)"},
        {"q": "Q5. 대장균에서 포도당은 없고 젖당만 있을 때 젖당 오페론 전사가 최대화되는 이유는?", "opts": ["cAMP 농도가 높아져 CAP-cAMP 복합체가 프로모터에 결합하기 때문", "cAMP 농도가 낮아져 억제 단백질이 파괴되기 때문", "포도당이 억제 단백질을 활성화하기 때문", "RNA 중합 효소가 불활성화되기 때문"], "ans": "cAMP 농도가 높아져 CAP-cAMP 복합체가 프로모터에 결합하기 때문"},
        {"q": "Q6. 하디-바인베르크 평형이 유지되기 위한 멘델 집단의 조건으로 옳지 않은 것은?", "opts": ["집단의 크기가 충분히 커야 한다.", "무작위 교배가 이루어져야 한다.", "자연선택과 돌연변이가 활발히 일어나야 한다.", "개체의 이입과 이출이 없어야 한다."], "ans": "자연선택과 돌연변이가 활발히 일어나야 한다."},
        {"q": "Q7. 소규모 집단에서 우연한 사건으로 인해 대립유전자 빈도가 예측 없이 급격히 변하는 현상을 무엇이라 하는가?", "opts": ["유전적 부드리(Genetic drift)", "자연선택", "유전자 흐름", "지리적 격리"], "ans": "유전적 부드리(Genetic drift)"},
        {"q": "Q8. 진핵생물에서 DNA 염기서열 변화 없이 DNA 메틸화나 히스톤 아세틸화 등을 통해 유전자 발현이 조절되는 학문 분야는?", "opts": ["후전유전학(Epigenetics)", "집단유전학", "멘델유전학", "전사유전학"], "ans": "후전유전학(Epigenetics)"},
        {"q": "Q9. 진핵생물의 전사 조절 과정에서 프로모터 외에 전사 효율을 촉진하는 멀리 떨어진 조절 부위는?", "opts": ["원거리 조절 부위(Enhancer/인핸서)", "작동 부위(Operator)", "인트론", "종결자"], "ans": "원거리 조절 부위(Enhancer/인핸서)"},
        {"q": "Q10. 하디-바인베르크 집단에서 우성 표현형(AA + Aa)의 빈도가 0.91일 때, 열성 대립유전자(a)의 빈도 q는?", "opts": ["0.09", "0.3", "0.7", "0.81"], "ans": "0.3"}
    ]
}

# -------------------- 진단 시작 / 진행 제어 --------------------
if not st.session_state.started:
    st.info("💡 준비가 완료되면 아래 **[⏱️ 진단 시작]** 버튼을 눌러주세요. 클릭 시 타이머가 가동됩니다.")
    if st.button("⏱️ 진단 시작 (10문항)", use_container_width=True):
        if not mentee_name.strip():
            st.error("멘티 이름을 먼저 입력해 주세요!")
        else:
            st.session_state.started = True
            st.session_state.start_time = time.time()
            st.rerun()

else:
    # 타이머 표시
    st.success(f"⏱️ **진단 진행 중입니다.** ({mentee_name} 멘티님, 차분하게 문제를 풀고 확신도를 체크해 주세요.)")
    
    questions = question_db[selected_unit]
    
    with st.form(key="diagnostic_form"):
        user_answers = {}
        user_confidences = {}
        
        for idx, q_data in enumerate(questions):
            st.markdown(f"#### **{q_data['q']}**")
            
            # 문제 답변
            user_answers[f"q_{idx}"] = st.radio(
                f"정답 선택 (Q{idx+1})",
                q_data["opts"],
                index=None,
                key=f"ans_{selected_unit}_{idx}"
            )
            
            # 문항별 개별 확신도 평가
            user_confidences[f"c_{idx}"] = st.slider(
                f"💡 Q{idx+1} 확신도 (1점: 찍음 ~ 5점: 확신함)",
                min_value=1, max_value=5, value=3,
                key=f"conf_{selected_unit}_{idx}"
            )
            st.write("") # 간격 조정
        
        submit_btn = st.form_submit_button("🚀 진단 결과 제출 및 처방전 보기", use_container_width=True)

    # -------------------- 제출 처리 및 분석 --------------------
    if submit_btn:
        if any(ans is None for ans in user_answers.values()):
            st.warning("⚠️ 아직 풀지 않은 문항이 있습니다! 모든 문항의 정답을 선택해 주세요.")
        else:
            # 1. 계산
            elapsed_time = round(time.time() - st.session_state.start_time, 1)
            correct_count = sum(1 for idx, q_data in enumerate(questions) if user_answers[f"q_{idx}"] == q_data["ans"])
            total_questions = len(questions)
            score = round((correct_count / total_questions) * 100)
            avg_confidence = round(sum(user_confidences.values()) / total_questions, 2)
            
            # 2. 리포트 출력
            st.divider()
            st.balloons()
            st.header(f"📊 {mentee_name} 멘티의 ZPD 진단 리포트")
            
            # 이전 진단 이력 비교 (Delta 계산)
            prev_data = st.session_state.history.get(selected_unit)
            
            col_a, col_b, col_c = st.columns(3)
            
            if prev_data:
                score_delta = score - prev_data['score']
                conf_delta = round(avg_confidence - prev_data['avg_confidence'], 2)
                time_delta = round(elapsed_time - prev_data['elapsed_time'], 1)
                
                col_a.metric("정답률 (주 지표)", f"{score}점 ({correct_count}/10문항)", delta=f"{score_delta:+d}점 (이전 대비)")
                col_b.metric("평균 확신도 (주 지표)", f"{avg_confidence}점 / 5.0점", delta=f"{conf_delta:+.2f}점 (이전 대비)")
                col_c.metric("소요 시간 (보조 지표)", f"{elapsed_time}초", delta=f"{time_delta:+.1f}초 (이전 대비)", delta_color="inverse")
                st.caption(f"🔄 **재진단 비교 완료:** 이전 진단 기록과 비교된 변화량이 표시됩니다.")
            else:
                col_a.metric("정답률 (주 지표)", f"{score}점 ({correct_count}/10문항)")
                col_b.metric("평균 확신도 (주 지표)", f"{avg_confidence}점 / 5.0점")
                col_c.metric("소요 시간 (보조 지표)", f"{elapsed_time}초")
                st.caption("ℹ️ 첫 번째 진단 결과입니다. 다시 진단하시면 변화량이 자동으로 측정됩니다.")

            # 3. 주 지표(정답률 + 확신도) 중심 인지 상태 및 ZPD 진단
            st.subheader("💡 인지 상태 분석 및 맞춤형 학습 비계(Scaffolding) 처방")
            
            # 시간 보조 지표 체크 (10문항 기준 10분 = 600초 초과 시 병목 판단)
            is_time_bottleneck = elapsed_time > 600
            
            # [진단 로직: 정답률 + 확신도 주 지표]
            if score < 60 or (score < 70 and avg_confidence <= 2.5):
                st.error("🔴 **Red Level (개념 재구조화 및 기초 비계 필요)**")
                st.write("**[인지 분석]** 핵심 개념 스키마 형성이 미흡하며, 정답률과 확신도 모두 낮아 개념 이해에 어려움을 겪는 상태입니다.")
                st.markdown("""
                **[추천 비계 전략]**
                * 시각적 이중코딩 맵을 활용한 핵심 탄소 골격 및 메커니즘 도식화 재학습
                * 3단계 이하 핵심 청크화(Chunking) 빈칸 카드 활용
                * 일상적 비유(Analogy) 기반 1:1 개념 재설명 진행
                """)
                
            elif (60 <= score < 80) or (score >= 80 and avg_confidence <= 3.5) or is_time_bottleneck:
                st.warning("🟡 **Yellow Level (절차화 및 단계적 비계 설정 필요) [ZPD 핵심 적정 구간]**")
                
                reason = []
                if score < 80: reason.append("응용 문제 적용 숙달 필요")
                if avg_confidence <= 3.5: reason.append("아는 것 같은 착각(친숙함 오류) 존재")
                if is_time_bottleneck: reason.append("풀이 시간 과다로 인한 인지적 병목 발생")
                
                st.write(f"**[인지 분석]** 개념은 알고 있으나, 문제 적용 시 인지적 병목이 존재합니다. ({', '.join(reason)})")
                st.markdown("""
                **[추천 비계 전략]**
                * 단계별 힌트 카드 제공 후 점진적으로 거두어내는 **'비계 제거(Fading)'** 적용
                * 하디-바인베르크 3단계 계산 및 4-Condition Matrix 분석 알고리즘 적용
                * 확신도가 낮았던 문항 위주의 백지 복기 및 원인 분석 멘토링
                """)
                
            else:
                st.success("🟢 **Green Level (완달성 및 파인만 역발상 추론 구간)**")
                st.write("**[인지 분석]** 정답률과 메타인지 확신도가 모두 높으며, 개념이 장기 기억에 체계적으로 구조화된 상태입니다.")
                st.markdown("""
                **[추천 비계 전략]**
                * **파인만 기법 기반 역발상 설명법(Reverse Teaching):** 멘티가 멘토에게 메커니즘을 쉬운 용어로 역설명
                * '특정 효소 결손 시 기작 변화' 등 변형 조건(What-If) 질문을 통한 고난도 추론 확장
                """)

            # 4. 이력 업데이트 및 재진단 버튼
            st.session_state.history[selected_unit] = {
                'score': score,
                'avg_confidence': avg_confidence,
                'elapsed_time': elapsed_time
            }
            
            st.divider()
            if st.button("🔄 다른 단원 선택 또는 재진단하기", use_container_width=True):
                st.session_state.started = False
                st.rerun()
            
