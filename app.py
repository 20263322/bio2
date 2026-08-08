import streamlit as st
import time

# 웹페이지 기본 설정
st.set_page_config(page_title="Bio-II ZPD Diagnostic System", page_icon="🧬", layout="centered")

# 타이틀 및 안내 문구
st.title("🧬 [생명과학 II] 맞춤형 ZPD 진단 시스템")
st.markdown("문제를 풀고 제출하면 **정답률, 풀이 시간, 확신도**를 종합 분석하여 맞춤형 학습 비계(Scaffolding)를 처방해 드립니다.")

st.divider()

# 1. 멘티 기본 정보 입력
col1, col2 = st.columns(2)
with col1:
    mentee_name = st.text_input("멘티 이름", value="", placeholder="이름을 입력하세요")
with col2:
    selected_unit = st.selectbox("진단 단원", [
        "1회차: 효소와 반응 속도", 
        "2회차: 세포 호흡과 광합성", 
        "3회차: DNA 복제 기작", 
        "4회차: 유전자 발현 조절 및 집단 유전"
    ])

# 타이머 작동 시작 시점 기록
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

st.subheader("📝 10분 ZPD 진단 문항")

user_answers = {}

# -------------------- 1회차 문항 --------------------
if selected_unit == "1회차: 효소와 반응 속도":
    st.info("💡 [1회차: 효소와 반응 속도] 문항을 읽고 정답을 선택해 주세요.")
    
    user_answers['q1'] = st.radio(
        "Q1. 경쟁적 저해제를 첨가했을 때 효소 반응 속도론적 변화로 옳은 것은?",
        ["Vmax 감소, Km 증가", "Vmax 일정, Km 증가", "Vmax 감소, Km 일정", "Vmax 일정, Km 감소"],
        index=None
    )
    user_answers['q2'] = st.radio(
        "Q2. 비경쟁적 저해제가 결합하는 효소의 결합 부위는 어디인가?",
        ["활성 부위", "타당성(Allosteric) 부위", "기질 결합 부위", "비활성 부위"],
        index=None
    )
    user_answers['q3'] = st.radio(
        "Q3. 효소 작용 시 반응 속도에 영향을 주는 인자 중 옳은 설명은?",
        ["효소는 활성화 에너지를 감소시킨다.", "효소는 반응열(ΔH)을 증가시킨다.", "효소는 반응물 자체의 에너지를 높인다.", "비경쟁적 저해제는 기질 농도를 높이면 완전히 극복된다."],
        index=None
    )

# -------------------- 2회차 문항 --------------------
elif selected_unit == "2회차: 세포 호흡과 광합성":
    st.info("💡 [2회차: 세포 호흡과 광합성] 문항을 읽고 정답을 선택해 주세요.")
    
    user_answers['q1'] = st.radio(
        "Q1. TCA 회로에서 C6(시트르산)이 C5(알파케토글루타르산)로 변할 때 방출되는 물질은?",
        ["CO2 및 NADH", "ATP 및 FADH2", "O2 및 H2O", "피루브산"],
        index=None
    )
    user_answers['q2'] = st.radio(
        "Q2. 세포 호흡 과정 중 가장 많은 ATP가 생성되는 장소와 과정은?",
        ["세포질 - 해당작업", "미토콘드리아 기질 - TCA 회로", "미토콘드리아 내막 - 산화적 인산화", "미토콘드리아 외막 - 피루브산 산화"],
        index=None
    )
    user_answers['q3'] = st.radio(
        "Q3. 포도당 1분자가 해당작업을 거칠 때 알짜 생성물로 옳은 것은?",
        ["2 피루브산, 2 ATP, 2 NADH", "2 피루브산, 4 ATP, 2 FADH2", "1 피루브산, 2 ATP, 1 NADH", "2 아세틸 CoA, 2 CO2, 2 ATP"],
        index=None
    )

# -------------------- 3회차 문항 --------------------
elif selected_unit == "3회차: DNA 복제 기작":
    st.info("💡 [3회차: DNA 복제 기작] 문항을 읽고 정답을 선택해 주세요.")
    
    user_answers['q1'] = st.radio(
        "Q1. DNA 중합 효소가 새로운 가닥을 신장시키는 방향은?",
        ["5' → 3' 방향", "3' → 5' 방향", "양방향 임의 합성", "프라이머의 방향에 따라 가변적"],
        index=None
    )
    user_answers['q2'] = st.radio(
        "Q2. 지연가닥(Lagging strand)에서 불연속적으로 합성되는 짧은 DNA 조각의 명칭은?",
        ["프라이머 절편", "오카자키 절편", "리게이스 절편", "선도 절편"],
        index=None
    )
    user_answers['q3'] = st.radio(
        "Q3. DNA 복제 과정 중 RNA 프라이머를 제거하고 진짜 DNA 뉴클레오타이드로 교체하는 효소는?",
        ["DNA 헬리카아제", "DNA 중합 효소 I", "DNA 중합 효소 III", "DNA 연결 효소(Ligase)"],
        index=None
    )

# -------------------- 4회차 문항 --------------------
elif selected_unit == "4회차: 유전자 발현 조절 및 집단 유전":
    st.info("💡 [4회차: 유전자 발현 조절 및 집단 유전] 문항을 읽고 정답을 선택해 주세요.")
    
    user_answers['q1'] = st.radio(
        "Q1. 대장균의 젖당 오페론에서 젖당이 존재하는 경우 일어나는 현상은?",
        ["억제 단백질이 작동 부위에 강하게 결합한다.", "젖당이 억제 단백질과 결합하여 작동 부위에서 떼어낸다.", "RNA 중합 효소가 프로모터에 결합하지 못한다.", "전사가 완전히 중단된다."],
        index=None
    )
    user_answers['q2'] = st.radio(
        "Q2. 하디-바인베르크 평형 집단에서 열성 표현형(aa) 개체의 빈도가 0.16일 때, 열성 대립유전자(a)의 빈도 q는?",
        ["0.16", "0.32", "0.4", "0.6"],
        index=None
    )
    user_answers['q3'] = st.radio(
        "Q3. 위 집단(q=0.4, p=0.6)에서 이형접합자(Aa) 개체의 빈도 2pq는?",
        ["0.24", "0.36", "0.48", "0.52"],
        index=None
    )

# 2. 메타인지 확신도 평가
st.divider()
st.write("💡 **메타인지 자가 진단**")
confidence = st.slider("방금 푼 문항들의 정답에 대해 스스로 얼마나 확신합니까?", 1, 5, 3, help="1점: 거의 찍음 ~ 5점: 확실하게 알고 풂")

# 3. 제출 및 진단 처리
if st.button("🚀 진단 결과 제출 및 처방전 보기", use_container_width=True):
    if not mentee_name:
        st.error("멘티 이름을 입력해 주세요!")
    elif any(ans is None for ans in user_answers.values()):
        st.warning("모든 문항의 답을 선택해 주세요!")
    else:
        # 풀이 소요 시간 계산
        elapsed_time = round(time.time() - st.session_state.start_time, 1)
        
        # 정답지 정의
        correct_answers = {
            "1회차: 효소와 반응 속도": {
                'q1': "Vmax 일정, Km 증가",
                'q2': "타당성(Allosteric) 부위",
                'q3': "효소는 활성화 에너지를 감소시킨다."
            },
            "2회차: 세포 호흡과 광합성": {
                'q1': "CO2 및 NADH",
                'q2': "미토콘드리아 내막 - 산화적 인산화",
                'q3': "2 피루브산, 2 ATP, 2 NADH"
            },
            "3회차: DNA 복제 기작": {
                'q1': "5' → 3' 방향",
                'q2': "오카자키 절편",
                'q3': "DNA 중합 효소 I"
            },
            "4회차: 유전자 발현 조절 및 집단 유전": {
                'q1': "젖당이 억제 단백질과 결합하여 작동 부위에서 떼어낸다.",
                'q2': "0.4",
                'q3': "0.48"
            }
        }
        
        unit_corrects = correct_answers[selected_unit]
        correct_count = sum(1 for q_key, answer in unit_corrects.items() if user_answers.get(q_key) == answer)
        total_questions = len(unit_corrects)
        score = round((correct_count / total_questions) * 100)

        # 진단 리포트 출력
        st.divider()
        st.balloons()
        st.header(f"📊 {mentee_name} 멘티의 ZPD 진단 리포트")
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("정답률", f"{score}점 ({correct_count}/{total_questions}문항)")
        col_b.metric("소요 시간", f"{elapsed_time}초")
        col_c.metric("메타인지 확신도", f"{confidence}점 / 5점")

        # 인지 수준 분석 및 비계 처방 알고리즘
        st.subheader("💡 인지 상태 분석 및 맞춤형 학습 비계(Scaffolding) 처방")
        
        if score < 60:
            st.error("🔴 **Red Level (개념 구조화 및 인지부하 최적화 필요)**")
            st.write("**[인지 분석]** 개념 용어 및 메커니즘 흐름 파악이 부족하여 텍스트 과부하를 겪고 있는 상태입니다.")
            st.markdown("""
            **[추천 비계 전략]**
            * 3D 활성 부위 모형 및 일상적 비유(Analogy)를 활용한 개념 직관화
            * 핵심 탄소 골격 중심의 **'시각적 이중코딩 맵'** 빈칸 학습지 제공
            * 3단계 이하의 핵심 개념 청크화(Chunking) 카드 활용
            """)
            
        elif score >= 60 and (elapsed_time > 180 or confidence <= 3):
            st.warning("🟡 **Yellow Level (절차화 및 단계적 비계 설정 필요) [ZPD 핵심 구간]**")
            st.write("**[인지 분석]** 개념은 알고 있으나 문제 적용 및 조건 변형 해석 과정에서 인지적 병목이 발생하고 있습니다.")
            st.markdown("""
            **[추천 비계 전략]**
            * 4-Condition Matrix 및 하디-바인베르크 3단계 풀이 알고리즘 가이드 제공
            * 단계별 힌트 카드를 제공한 뒤 점진적으로 거두어내는 **'비계 제거(Fading)'** 적용
            * 메커니즘 타일 카드를 활용한 프로세스 순서 맞추기 실습
            """)
            
        else:
            st.success("🟢 **Green Level (메타인지 확장 및 역발상 추론 구간)**")
            st.write("**[인지 분석]** 개념 이해와 적용 능력이 매우 우수하며, 고난도 응용 추론 단계로 확장이 가능합니다.")
            st.markdown("""
            **[추천 비계 전략]**
            * 파인만 기법 기반 **'역발상 설명법(Reverse Teaching)'** 적용 (멘티가 멘토에게 직접 설명)
            * '돌연변이 발생 시 기작 변화'와 같은 변형 조건(What-If) 질문을 통한 추론 능력 강화
            """)
            
        # 재진단을 위한 타이머 리셋
        del st.session_state['start_time']
