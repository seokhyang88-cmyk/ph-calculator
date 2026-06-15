import streamlit as st
import math

# 스마트폰 화면 비율에 맞게 페이지 설정
st.set_page_config(page_title="공학용 pH 마스터 v3.0", layout="centered")

# --- 🎨 공학용 계산기 스타일 CSS 입히기 ---
st.markdown("""
    <style>
    /* 전체 배경을 어두운 계산기 프레임 느낌으로 설정 */
    .stApp {
        background-color: #1e2022;
    }
    /* 민트색 모니터 액정 화면 스타일 정의 */
    .lcd-screen {
        background-color: #e2ebd9;
        color: #1a251c;
        font-family: 'Courier New', monospace;
        padding: 15px;
        border-radius: 8px;
        border: 4px solid #2d3238;
        box-shadow: inset 0px 4px 10px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        min-height: 180px;
    }
    /* 가이드라인과 텍스트 크기를 차분하게 고정 */
    .lcd-text {
        font-size: 15px;
        line-height: 1.5;
        margin: 2px 0;
    }
    </style>
""", unsafe_allowed_html=True)

# 버튼 입력을 실시간으로 기억하기 위한 세션 스테이트(메모리) 초기화
if "calc_menu" not in st.session_state: st.session_state.calc_menu = "1"
if "p_val" not in st.session_state: st.session_state.p_val = "5.8"
if "e_val" not in st.session_state: st.session_state.e_val = "-4"
if "ph_result" not in st.session_state: st.session_state.ph_result = ""

# --- 📱 1. 위쪽 민트색 모니터 액정 화면 (LCD) ---
# 이 영역 안에 선택창, 안내문구, 계산 결과가 모두 들어갑니다.
screen_placeholder = st.container()

with screen_placeholder:
    # HTML 주입을 통해 이미지와 똑같은 감성의 민트색 액정 상자를 만듭니다.
    lcd_content = f"""
    <div class="lcd-screen">
        <div class="lcd-text"><b>[MODE {st.session_state.calc_menu}] 단일 용액 pH 산출 모드</b></div>
        <div class="lcd-text">· 입력된 H+ 농도: {st.session_state.p_val} × 10^{st.session_state.e_val} mol/L</div>
        <div class="lcd-text">· 대표 가이드: HCl(강산), CH3COOH(약산), NaOH(강염기)</div>
        <hr style="border: 0.5px solid #1a251c; margin: 10px 0;">
        <div class="lcd-text" style="font-size: 18px; font-weight: bold; color: #0d381e;">
            {st.session_state.ph_result if st.session_state.ph_result else "INPUT VALUE & PRESS [=]"}
        </div>
    </div>
    """
    st.markdown(lcd_content, unsafe_allowed_html=True)

st.write("---")

# --- ⌨️ 2. 아래쪽 검은색 물리 버튼 패드 ---
st.write("계산기 키패드 조작창")

# [상단 제어기 라인] 유형(모드) 선택 및 값 세팅 조절창을 패드 내부에 조화롭게 배치
menu_select = st.selectbox(
    "MODE (문제 유형 변경):",
    [
        "1. H+ 이온 농도로 pH 구하기",
        "2. H+ 이온 농도로 OH- 이온 농도 구하기",
        "3. 강산 또는 강염기 단일 용액의 pH 구하기",
        "4. 약산/약염기 pH 계산기 (전리도 기반)"
    ],
    key="mode_box"
)
st.session_state.calc_menu = menu_select.split(".")[0]

# 이미지 속 계산기의 상단 특수키 구역처럼 수치 조절 필드를 배치
col_input1, col_input2 = st.columns(2)
with col_input1:
    in_p = st.text_input("농도 앞자리 (숫자 패드 대용):", value=st.session_state.p_val, key="in_p_key")
    st.session_state.p_val = in_p
with col_input2:
    in_e = st.text_input("10의 마이너스 지수 (Exp 대용):", value=st.session_state.e_val, key="in_e_key")
    st.session_state.e_val = in_e

st.write("")

# [하단 연산 패드 라인] 기능 실행을 위한 핵심 물리 버튼 배치
col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    if st.button("AC (초기화)", use_container_width=True):
        st.session_state.p_val = "1.0"
        st.session_state.e_val = "-7"
        st.session_state.ph_result = "SYSTEM RESET 완료"
        st.rerun()

with col_btn2:
    # 이미지 속 Log, Exp 역할을 하는 단서 확인용 인터럽트 버튼
    if st.button("Log (단서 확인)", use_container_width=True):
        try:
            val_p = float(st.session_state.p_val)
            st.session_state.ph_result = f"LOG DATA: log10({val_p}) = {math.log10(val_p):.4f}"
        except:
            st.session_state.ph_result = "수치 입력 오류"
        st.rerun()

with col_btn3:
    # 이미지 속 가장 중요한 우측 하단의 [ = ] 버튼 역할
    if st.button(" ＝ (결과 출력)", type="primary", use_container_width=True):
        try:
            p = float(st.session_state.p_val)
            e = float(st.session_state.e_val)
            
            if p <= 0:
                st.session_state.ph_result = "ERROR: 앞자리는 0보다 커야 합니다."
            else:
                h_conc = p * (10 ** e)
                
                # 선택된 모드에 따라 민트색 모니터창에 띄울 결과를 다르게 연산
                if st.session_state.calc_menu == "1":
                    final_ph = -math.log10(h_conc)
                    st.session_state.ph_result = f"OUTPUT ──> pH = {final_ph:.2f}"
                elif st.session_state.calc_menu == "2":
                    oh_conc = 1e-14 / h_conc
                    base, exp_v = f"{oh_conc:.2e}".split('e')
                    st.session_state.ph_result = f"OUTPUT ──> [OH-] = {base} × 10^{int(exp_v)}"
                elif st.session_state.calc_menu == "3":
                    final_ph = -math.log10(h_conc)
                    st.session_state.ph_result = f"강산 OUTPUT ──> pH = {final_ph:.2f}"
                elif st.session_state.calc_menu == "4":
                    # 간소화된 약산 연산 결과 예시 표출
                    final_ph = -math.log10(h_conc * 0.01)
                    st.session_state.ph_result = f"약산(1%전리) ──> pH = {final_ph:.2f}"
        except:
            st.session_state.ph_result = "ERROR: 입력 값을 다시 확인하세요."
        st.rerun()