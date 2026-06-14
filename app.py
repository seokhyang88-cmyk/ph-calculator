import streamlit as st
import math

# 스마트폰 화면에 맞게 최적화 설정
st.set_page_config(page_title="화학 계산기", layout="centered")

st.title("🧮 화학 전용 모바일 계산기")
st.write("일반 숫자 패드 형식으로 간편하게 누르며 계산할 수 있습니다.")

st.markdown("---")

# 1. 계산기 디스플레이 (상단 입력창 상태 관리)
if "calc_input" not in st.session_state:
    st.session_state.calc_input = ""

# 상단 대형 디스플레이 박스
display_text = st.text_input("Display", value=st.session_state.calc_input, disabled=True, label_visibility="collapsed")

# 버튼 입력을 처리하는 헬퍼 함수
def press(key):
    if key == "C":
        st.session_state.calc_input = ""
    elif key == "◀":
        st.session_state.calc_input = st.session_state.calc_input[:-1]
    elif key == "×10^":
        st.session_state.calc_input += "*10**("
    else:
        st.session_state.calc_input += str(key)

st.markdown("### 🔢 키패드")

# 2. 바둑판 형태의 계산기 버튼 배치 (st.columns 활용)
# 1행: 지수, 로그, 지우기 기능 버튼들
row1 = st.columns(4)
with row1[0]:
    if st.button("C", use_container_width=True): press("C")
with row1[1]:
    if st.button("◀", use_container_width=True): press("◀")
with row1[2]:
    if st.button("log10", use_container_width=True): press("math.log10(")
with row1[3]:
    if st.button("×10^n", use_container_width=True): press("×10^")

# 2행: 숫자 7, 8, 9 및 괄호
row2 = st.columns(4)
with row2[0]:
    if st.button("7", use_container_width=True): press(7)
with row2[1]:
    if st.button("8", use_container_width=True): press(8)
with row2[2]:
    if st.button("9", use_container_width=True): press(9)
with row2[3]:
    if st.button(")", use_container_width=True): press(")")

# 3행: 숫자 4, 5, 6 및 사칙연산
row3 = st.columns(4)
with row3[0]:
    if st.button("4", use_container_width=True): press(4)
with row3[1]:
    if st.button("5", use_container_width=True): press(5)
with row3[2]:
    if st.button("6", use_container_width=True): press(6)
with row3[3]:
    if st.button("/", use_container_width=True): press("/")

# 4행: 숫자 1, 2, 3 및 사칙연산 곱하기
row4 = st.columns(4)
with row4[0]:
    if st.button("1", use_container_width=True): press(1)
with row4[1]:
    if st.button("2", use_container_width=True): press(2)
with row4[2]:
    if st.button("3", use_container_width=True): press(3)
with row4[3]:
    if st.button("*", use_container_width=True): press("*")

# 5행: 마이너스 부호, 숫자 0, 소수점, 빼기 연산
row5 = st.columns(4)
with row5[0]:
    if st.button("- (부호)", use_container_width=True): press("-")
with row5[1]:
    if st.button("0", use_container_width=True): press(0)
with row5[2]:
    if st.button(".", use_container_width=True): press(".")
with row5[3]:
    if st.button("- (빼기)", use_container_width=True): press("-")

st.markdown("---")

# 3. 화학 퀵 계산 단축키 (원클릭 정답 도우미)
st.markdown("### 🧪 화학 문제 원클릭 해결 매크로")
st.write("디스플레이에 숫자를 입력한 상태에서 아래 버튼을 누르면 바로 산출됩니다.")

col_macro1, col_macro2 = st.columns(2)

with col_macro1:
    if st.button("수소이온농도 ➡️ pH 변환", use_container_width=True, type="primary"):
        try:
            raw_expression = st.session_state.calc_input
            if raw_expression.count("(") > raw_expression.count(")"):
                raw_expression += ")" * (raw_expression.count("(") - raw_expression.count(")"))
            
            conc = eval(raw_expression)
            ph = -math.log10(conc)
            st.session_state.calc_input = f"{ph:.2f}"
            st.rerun()
        except:
            st.error("입력된 농도 수식이 올바르지 않습니다.")

with col_macro2:
    if st.button("수산이온농도 ➡️ pH 변환", use_container_width=True, type="primary"):
        try:
            raw_expression = st.session_state.calc_input
            if raw_expression.count("(") > raw_expression.count(")"):
                raw_expression += ")" * (raw_expression.count("(") - raw_expression.count(")"))
                
            conc = eval(raw_expression)
            poh = -math.log10(conc)
            ph = 14 - poh
            st.session_state.calc_input = f"{ph:.2f}"
            st.rerun()
        except:
            st.error("입력된 농도 수식이 올바르지 않습니다.")

# 사용법 안내 가이드라인
st.info("💡 사용 팁:\n"
        "1. '4.0'을 누르고 '×10^n' 버튼을 누른 뒤 '-2)'를 완성하면 '4.0 * 10의 -2승' 수식이 완성됩니다.\n"
        "2. 그 상태에서 아래 파란색 '수산이온농도 ➡️ pH 변환' 버튼을 누르면 14에서 뺀 최종 pH 정답이 대형 화면에 바로 표기됩니다!")