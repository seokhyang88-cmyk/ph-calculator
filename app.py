import streamlit as st
import math

# 스마트폰 화면에 맞게 페이지 설정
st.set_page_config(page_title="pH 마스터", layout="centered")

st.title("📱 pH/pH 혼합 문제 해결사")
st.write("지수 형태(x 10^-n)를 보기 쉽게 변환해 주는 업그레이드 버전입니다.")

st.markdown("---")

# 메뉴 선택 (유형별로 나누기)
menu = st.selectbox(
    "풀고 싶은 문제 유형을 선택하세요:",
    [
        "1. 수소 이온 농도로 수산화 이온 농도 구하기",
        "2. 소수점이 포함된 수소 이온 농도로 pH 구하기",
        "3. 단일 용액(NaOH, H2SO4 등)의 pH 구하기",
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
        
        # 과학적 표기법(e-13)을 지수식 형태로 예쁘게 쪼개는 로직 적용
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

# --- 유형 3 ---
elif menu == "3. 단일 용액(NaOH, H2SO4 등)의 pH 구하기":
    st.subheader("💡 유형 3 계산기")
    st.write("예: 0.002N NaOH 또는 0.005M H2SO4의 pH는?")
    
    solution_type = st.radio("용액의 성질을 고르세요:", ["산성 용액 (H2SO4, HCl 등)", "염기성 용액 (NaOH, KOH 등)"])
    conc = st.number_input("농도 입력 (M 또는 N)", value=0.002, format="%.4f")
    
    st.caption("ℹ️ 이 계산기는 간편하게 수소/수산화 이온으로 바로 바뀌는 노르말 농도(N) 혹은 1가 이온 기준으로 계산합니다.")

    if st.button("정답 확인"):
        if solution_type == "산성 용액 (H2SO4, HCl 등)":
            ph = -math.log10(conc)
        else:
            poh = -math.log10(conc)
            ph = 14 - poh
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