import streamlit as st

# 페이지 설정
st.set_page_config(page_title="케미컬 에덴", page_icon="🧬", layout="wide")

st.title("🧬 케미컬 에덴: 미니 생태계 시뮬레이터")
st.write("화학 반응을 통해 에너지를 생산하고, 가장 거대한 생태계를 만들어 보세요!")

# 1. 초기 자원 설정 (Session State)
resources = {
    'light': 100,      # 빛 에너지 (턴마다 자동 충전됨)
    'h2o': 50,         # 물
    'co2': 50,         # 이산화탄소
    'o2': 10,          # 산소
    'glucose': 0,      # 포도당 (C6H12O6)
    'atp': 0,          # 생체 에너지
    'biomass': 0       # 생물량 (점수)
}

for key, value in resources.items():
    if key not in st.session_state:
        st.session_state[key] = value

# 메시지 출력용 상태
if 'message' not in st.session_state:
    st.session_state.message = "게임을 시작합니다. 광합성을 통해 포도당을 합성하세요!"

# 2. 화학 반응 함수 정의
def photosynthesis():
    """광합성: 물 6 + 이산화탄소 6 + 빛 -> 포도당 1 + 산소 6"""
    if st.session_state.h2o >= 6 and st.session_state.co2 >= 6 and st.session_state.light >= 10:
        st.session_state.h2o -= 6
        st.session_state.co2 -= 6
        st.session_state.light -= 10
        st.session_state.glucose += 1
        st.session_state.o2 += 6
        st.session_state.message = "🌿 광합성 성공! 포도당과 산소가 생성되었습니다."
    else:
        st.session_state.message = "⚠️ 자원이 부족하여 광합성을 할 수 없습니다 (물 6, CO2 6, 빛 10 필요)."

def cellular_respiration():
    """세포 호흡: 포도당 1 + 산소 6 -> 물 6 + 이산화탄소 6 + 38 ATP"""
    if st.session_state.glucose >= 1 and st.session_state.o2 >= 6:
        st.session_state.glucose -= 1
        st.session_state.o2 -= 6
        st.session_state.h2o += 6
        st.session_state.co2 += 6
        st.session_state.atp += 38
        st.session_state.message = "⚡ 세포 호흡 성공! 막대한 ATP 에너지를 얻었습니다."
    else:
        st.session_state.message = "⚠️ 자원이 부족하여 세포 호흡을 할 수 없습니다 (포도당 1, O2 6 필요)."

def create_life():
    """생명체 창조 (Biomass 증가): 50 ATP 소모"""
    if st.session_state.atp >= 50:
        st.session_state.atp -= 50
        st.session_state.biomass += 1
        # 생명체가 늘어나면 호흡을 위해 약간의 자원이 소모됨
        st.session_state.co2 += 10 
        st.session_state.message = f"🧬 생태계 확장 완료! 현재 Biomass: {st.session_state.biomass}"
    else:
        st.session_state.message = "⚠️ ATP가 부족합니다. 세포 호흡을 더 진행하세요 (50 ATP 필요)."

def end_turn():
    """턴 종료: 빛 에너지 회복 및 자연적인 물 공급"""
    st.session_state.light = min(100, st.session_state.light + 30)
    st.session_state.h2o += 10
    st.session_state.message = "☀️ 날이 밝았습니다. 빛 에너지와 물이 일부 보충되었습니다."

# 3. UI 구성 - 대시보드
st.subheader("📊 현재 행성 자원 상태")
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

col1.metric("☀️ 빛 에너지", st.session_state.light)
col2.metric("💧 물 (H₂O)", st.session_state.h2o)
col3.metric("☁️ 이산화탄소 (CO₂)", st.session_state.co2)
col4.metric("💨 산소 (O₂)", st.session_state.o2)
col5.metric("🍬 포도당", st.session_state.glucose)
col6.metric("⚡ ATP", st.session_state.atp)
col7.metric("🌍 Biomass", st.session_state.biomass)

st.markdown("---")

# 4. 상태 메시지 창
st.info(st.session_state.message)

# 5. 행동 제어판 (Action Panel)
st.subheader("🔬 생화학 반응 제어판")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("**1단계: 유기물 합성**")
    st.latex(r"6CO_2 + 6H_2O \rightarrow C_6H_{12}O_6 + 6O_2")
    if st.button("🌿 광합성 실행"):
        photosynthesis()
        st.rerun()

with c2:
    st.markdown("**2단계: 에너지 생산**")
    st.latex(r"C_6H_{12}O_6 + 6O_2 \rightarrow 6CO_2 + 6H_2O + 38ATP")
    if st.button("⚡ 세포 호흡 실행"):
        cellular_respiration()
        st.rerun()

with c3:
    st.markdown("**3단계: 생태계 확장**")
    st.write("소모: **50 ATP**")
    if st.button("🧬 새로운 세포 분열"):
        create_life()
        st.rerun()

with c4:
    st.markdown("**기타 액션**")
    st.write("빛 에너지 및 물 회복")
    if st.button("⏳ 턴 넘기기"):
        end_turn()
        st.rerun()
