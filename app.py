import streamlit as st
import math

# 스마트폰 화면에 맞게 페이지 설정
st.set_page_config(page_title="pH 마스터", layout="centered")

st.title("📱 pH/pH 혼합 문제 해결사")
st.write("지수 변환 및 N/M 농도 선택 기능이 모두 포함된 최종 버전입니다.")

st.markdown("---")

# 메뉴 선택
menu = st.selectbox(
    "풀고 싶은 문제 유형을 선택하세요:",
    [
        "1. 수소 이온 농도로 수산화 이온 농도 구하기",
        "2. 소수점이 포함된 수소 이온 농도로 pH 구하기",
        "3. 단일 용액(NaOH, H2SO4 등)의 pH 구하기 (N/M 선택 가능)",
        "4. 두 용액을 섞은 혼합 용액의 pH 구하기 (퀴즈 유형)"
    ]
)

st.markdown("---")

# --- 유형 1 ---
if menu == "1. 수소 이온 농도로 수산화 이온 농도 구하기":
    st.subheader("💡 유형 1 계산기")
    st.write("예: H+ 농도가 4.0 x 10^-2 일 때 OH- 농도는?")
    
    col1, col2 = st.columns(2)
    with col1:
        prefix = st.number_input("앞의 숫자 (예: 4.0)", value=4.0, step=0.1)
    with col2:
        exponent = st.number_input("10의 지수 (예: -2)", value=-2, step=1)
        
    if st.button("정답 확인"):
        h_conc = prefix * (10 ** exponent)
        oh_conc = 1e-14 / h_conc
        
        if oh_conc == 0:
            st.success("정답: OH- 이온 농도 = **0 mole/L**")
        else:
            oh_str = f"{oh_conc:.2e}"
            base, exponent_val = oh_str.split('e')
            exponent_val = int(exponent_val) 
            st.success(f"🎉 정답: OH- 이온 농도 = **{base} × 10^{{{exponent_val}}} mole/L**")

# --- 유형 2 ---
elif menu == "2. 소수점이 포함된 수소 이온 농도로 pH 구하기":
    st.subheader("💡 유형 2 계산기")
    st.write("예: H+ 농도가 5.8 x 10^-4 일 때 pH는?")
    
    col1, col2 = st.columns(2)
    with col1:
        prefix = st.number_input("앞의 숫자 (예: 5.8)", value=5.8, step=0.1)
    with col2:
        exponent = st.number_input("10의 지수 (예: -4)", value=-4, step=1)
        
    if st.button("정답 확인"):
        h_conc = prefix * (10 ** exponent)
        ph = -math.log10(h_conc)
        st.success(f"🎉 정답: pH = **{ph:.2f}**")

# --- 유형 3 (수정된 부분!) ---
elif menu == "3. 단일 용액(NaOH, H2SO4 등)의 pH 구하기 (N/M 선택 가능)":
    st.subheader("💡 유형 3 계산기")
    st.write("예: 0.002N NaOH 또는 0.005M H2SO4의 pH는?")
    
    # 1. 용액 종류 선택
    solution_name = st.selectbox("어떤 용액인가요?", ["NaOH (1가 염기)", "HCl (1가 산)", "H2SO4 (2가 산)", "기타 용액"])
    
    # 2. 농도 단위 선택 (M vs N)
    unit_type = st.radio("농도 단위를 선택하세요:", ["몰 농도 (M)", "노르말 농도 (N)"])
    
    # 3. 숫자 입력
    raw_conc = st.number_input("농도 숫자를 입력하세요:", value=0.002, format="%.4f", step=0.001)
    
    if st.button("정답 확인"):
        # 노르말 농도(N)로 통일해서 계산하기 위한 변수
        final_n = raw_conc
        
        # 만약 사용자가 '몰 농도(M)'를 골랐고, 2가 산인 H2SO4라면 수소이온이 2배 나오므로 N농도는 2배가 됨
        if unit_type == "몰 농도 (M)" and solution_name == "H2SO4 (2가 산)":
            final_n = raw_conc * 2
            st.info("ℹ️ H2SO4는 2가 산이므로 M 농도에 2를 곱해 N 농도로 자동 변환하여 계산합니다.")
            
        # 액성 판단 (산성인가 염기성인가)
        if "NaOH" in solution_name:
            # 염기성 용액 계산
            poh = -math.log10(final_n)
            ph = 14 - poh
        elif "HCl" in solution_name or "H2SO4" in solution_name:
            # 산성 용액 계산
            ph = -math.log10(final_n)
        else:
            # 기타 용액일 경우 임의로 선택하게 유도
            st.warning("기타 용액은 단위를 노르말 농도(N) 기준으로 계산기 내부에서 처리합니다.")
            ph = -math.log10(final_n)
            
        st.success(f"🎉 정답: pH = **{ph:.2f}**")

# --- 유형 4 ---
elif menu == "4. 두 용액을 섞은 혼합 용액의 pH 구하기 (퀴즈 유형)":
    st.subheader("🧪 13주차 2차시 퀴즈 전용 계산기")
    st.write("산성 용액과 염기성 용액을 섞었을 때의 pH를 구합니다.")
    
    st.markdown("### 🔴 산성 용액 입력 (예: H2SO4 또는 HCl)")
    acid_n = st.number_input("산성 노르말 농도 (N)", value=0.1, step=0.01)
    acid_v = st.number_input("산성 부피 (ml)", value=50, step=1)
    
    st.markdown("### 🔵 염기성 용액 입력 (예: NaOH)")
    base_n = st.number_input("염기성 노르말 농도 (N)", value=0.2, step=0.01)
    base_v = st.number_input("염기성 부피 (ml)", value=50, step=1)
    
    if st.button("혼합 용액 정답 확인"):
        total_volume_l = (acid_v + base_v) / 1000
        acid_eq = acid_n * (acid_v / 1000)
        base_eq = base_n * (base_v / 1000)
        
        if acid_eq > base_eq:
            remain_h = (acid_eq - base_eq) / total_volume_l
            ph = -math.log10(remain_h)
            st.warning(f"산이 더 많아서 '산성'입니다.")
        elif base_eq > acid_eq:
            remain_oh = (base_eq - acid_eq) / total_volume_l
            poh = -math.log10(remain_oh)
            ph = 14 - poh
            st.info(f"염기가 더 많아서 '염기성'입니다.")
        else:
            ph = 7.0
            st.success("완전 중화되었습니다!")
            
        st.success(f"🎉 최종 혼합 용액의 정답: pH = **{ph:.2f}**")