import streamlit as st
import math

# 스마트폰 화면에 맞게 페이지 설정
st.set_page_config(page_title="화학 pH 마스터", layout="centered")

st.title("📱 pH & 중화적정 만능 계산기")
st.write("올려주신 모든 유형의 기출문제를 완벽하게 풀어낼 수 있는 종합 도우미 앱입니다.")

st.markdown("---")

# 메뉴 선택 (유형 세분화)
menu = st.selectbox(
    "풀고 싶은 문제 유형을 선택하세요:",
    [
        "1. pH 값을 주고 수소 이온 농도 [H+] 역산하기",
        "2. 같은 성질의 산성/염기성 용액 혼합하기 (N 농도 기반)",
        "3. 중화 적정 실험 데이터로 미지 용액의 농도 및 pH 구하기",
        "4. 단일 용액(HCl, NaOH, H2SO4)의 기본 pH 구하기",
        "5. 산성 용액 + 염기성 용액 혼합하기 (중화 반응 후 pH)",
        "6. 약산/약염기 pH 계산기 (전리도 또는 해리상수 Ka/Kb 선택)",
        "7. 용액의 농도 단위환산 (1 → 100 표현법 등)"
    ]
)

st.markdown("---")

# --- 유형 1 (새로 올린 이미지 4번 유형 대응) ---
if menu == "1. pH 값을 주고 수소 이온 농도 [H+] 역산하기":
    st.subheader("🧪 pH 기반 수소 이온 농도 [H⁺] 역산기")
    st.write("예: 미지 용액의 pH가 4.70일 때 [H+] 구하기")
    
    ph_input = st.number_input("측정된 pH 값을 입력하세요:", value=4.70, format="%.2f", step=0.01)
    
    st.markdown("##### 💡 소수점 pH 계산을 위한 로그 단서 (선택 사항)")
    st.write("문제에 'log10(2) = 0.30' 같은 단서가 있다면 아래에 입력해 더 직관적인 지수 형태 표기를 볼 수 있습니다.")
    
    use_log_hint = st.checkbox("로그 단서 활용하기", value=True)
    log_base_num = 2.0
    log_value = 0.30
    if use_log_hint:
        col_l1, col_l2 = st.columns(2)
        with col_l1: log_base_num = st.number_input("로그 진수 (예: log의 '2')", value=2.0, step=0.1)
        with col_l2: log_value = st.number_input("로그 값 (예: '0.30')", value=0.30, step=0.01)

    if st.button("🎉 [H+] 농도 정답 확인", type="primary"):
        # 기본 수학적 계산
        h_conc = 10 ** (-ph_input)
        
        st.markdown("### 📋 계산 결과")
        st.success(f"🔹 **일반 소수점 표기:** {h_conc:.7f} mol/L")
        st.success(f"🔹 **컴퓨터 지수 표기:** {h_conc:.2e} mol/L")
        
        # 로그 힌트 역산 프로세스 보여주기
        if use_log_hint:
            floor_val = math.ceil(ph_input) # 내림 차수를 위해 천장값 구함
            diff = floor_val - ph_input
            if abs(diff - log_value) < 0.02:
                st.info(f"💡 **시험 보기 맞춤형 해설:**\n\n"
                        f"10^(-{ph_input}) = 10^({diff:.2f}) × 10^(-{floor_val}) 이며,\n"
                        f"주어진 log10({log_base_num}) = {log_value} 이므로 10^({diff:.2f})은 {log_base_num}가 됩니다.\n\n"
                        f"따라서 기출문제 정답 형태는 **{log_base_num} × 10^{{-{floor_val}}} mol/L** 입니다!")
            else:
                st.warning("⚠️ 입력하신 로그 값과 pH의 소수점 자리가 수학적으로 일치하지 않아 자동 서식 변환이 생략되었습니다. 위의 기본 표기를 확인해 주세요.")

# --- 유형 2 (새로 올린 이미지 1번 유형 대응) ---
elif menu == "2. 같은 성질의 산성/염기성 용액 혼합하기 (N 농도 기반)":
    st.subheader("🧪 산+산 또는 염기+염기 혼합 계산기")
    st.write("서로 다른 농도를 가진 같은 액성의 두 용액을 섞었을 때의 최종 pH를 구합니다.")
    
    sol_kind = st.radio("섞으려는 용액들의 성질은 무엇인가요?", ["산성 용액끼리 섞음 (HCl + H2SO4 등)", "염기성 용액끼리 섞음"])
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("##### 🔴 1번 용액")
        n1 = st.number_input("1번 노르말 농도 (N)", value=0.10, format="%.4f", step=0.01, key="n1")
        v1 = st.number_input("1번 부피 (mL)", value=50, step=5, key="v1")
    with col_m2:
        st.markdown("##### 🔴 2번 용액")
        n2 = st.number_input("2번 노르말 농도 (N)", value=0.20, format="%.4f", step=0.01, key="n2")
        v2 = st.number_input("2번 부피 (mL)", value=50, step=5, key="v2")
        
    if st.button("🎉 혼합 pH 정답 확인", type="primary"):
        total_v_l = (v1 + v2) / 1000.0
        eq1 = n1 * (v1 / 1000.0)
        eq2 = n2 * (v2 / 1000.0)
        total_eq = eq1 + eq2
        final_n = total_eq / total_v_l
        
        st.markdown("### 📋 혼합 프로세스 분석 결과")
        st.info(f"1번 용액 당량수: {eq1:.4f} eq / 2번 용액 당량수: {eq2:.4f} eq")
        st.info(f"혼합 후 최종 노르말 농도: **{final_n:.4f} N**")
        
        if sol_kind == "산성 용액끼리 섞음 (HCl + H2SO4 등)":
            final_ph = -math.log10(final_n)
            st.success(f"🎉 **최종 혼합 용액의 정답 pH = {final_ph:.2f}**")
        else:
            final_poh = -math.log10(final_n)
            final_ph = 14.0 - final_poh
            st.success(f"🎉 **최종 혼합 용액의 정답 pH = {final_ph:.2f}** (pOH = {final_poh:.2f})")

# --- 유형 3 (새로 올린 이미지 2, 3번 유형 대응) ---
elif menu == "3. 중화 적정 실험 데이터로 미지 용액의 농도 및 pH 구하기":
    st.subheader("🧪 중화 적정 실험 전용 계산기")
    st.write("N1 * V1 = N2 * V2 공식을 기반으로 미지 용액의 농도와 pH를 즉시 도출합니다.")
    
    target_type = st.radio("농도를 알아내려는 미지의 용액 성질은?", ["미지의 강산 (농도 모르는 HCl 등)", "미지의 강염기 (농도 모르는 KOH 등)"])
    
    st.markdown("##### 🧪 1. 실험에 사용한 미지 용액의 부피 조건")
    v_target = st.number_input("미지 용액의 채취량 (mL)", value=100, step=10)
    
    st.markdown("##### 🧪 2. 적정에 소비된 표준 용액(농도를 아는 용액)의 조건")
    n_standard = st.number_input("표준 용액의 노르말 농도 (N)", value=0.1000, format="%.4f", step=0.01)
    v_standard = st.number_input("적정에 실제 들어간 표준 용액의 부피 (mL)", value=10, step=1)
    
    if st.button("🎉 중화 적정 결과 판정", type="primary"):
        # N * V = N' * V' -> N_result 구하기
        n_result = (n_standard * v_standard) / v_target
        
        st.markdown("### 📋 적정 분석 데이터 리포트")
        st.info(f"📊 **산출된 미지 용액의 농도** = ({n_standard} N × {v_standard} mL) ÷ {v_target} mL = **{n_result:.4f} N**")
        
        if target_type == "미지의 강산 (농도 모르는 HCl 등)":
            ph = -math.log10(n_result)
            st.success(f"🎉 **미지 강산 용액의 최종 pH = {ph:.2f}**")
        else:
            poh = -math.log10(n_result)
            ph = 14.0 - poh
            st.success(f"🎉 **미지 강염기 용액의 최종 pH = {ph:.2f}** (pOH = {poh:.2f})")
        st.warning(f"💡 만약 시험 문제 보기가 정수(1, 2, 3...) 형태라면 가장 근접한 정수인 **{round(ph)}**를 정답으로 마킹하세요!")

# --- 유형 4 ---
elif menu == "4. 단일 용액(HCl, NaOH, H2SO4)의 기본 pH 구하기":
    st.subheader("💡 단일 용액 pH 계산기")
    solution_name = st.selectbox("용액을 선택하세요:", ["HCl (1가 산)", "NaOH (1가 염기)", "H2SO4 (2가 산)"])
    unit_type = st.radio("입력할 농도 단위 종류:", ["몰 농도 (M)", "노르말 농도 (N)"])
    raw_conc = st.number_input("농도 수치를 입력하세요:", value=0.01, format="%.4f", step=0.001)
    
    if st.button("정답 확인"):
        final_n = raw_conc
        if unit_type == "몰 농도 (M)" and solution_name == "H2SO4 (2가 산)":
            final_n = raw_conc * 2
        
        if "NaOH" in solution_name:
            poh = -math.log10(final_n)
            ph = 14.0 - poh
        else:
            ph = -math.log10(final_n)
        st.success(f"🎉 정답: pH = **{ph:.2f}**")

# --- 유형 5 ---
elif menu == "5. 산성 용액 + 염기성 용액 혼합하기 (중화 반응 후 pH)":
    st.subheader("🧪 산성 + 염기성 혼합(중화) 계산기")
    acid_n = st.number_input("산성 노르말 농도 (N)", value=0.1, step=0.01, key="t5_an")
    acid_v = st.number_input("산성 부피 (mL)", value=50, step=1, key="t5_av")
    base_n = st.number_input("염기성 노르말 농도 (N)", value=0.2, step=0.01, key="t5_bn")
    base_v = st.number_input("염기성 부피 (mL)", value=50, step=1, key="t5_bv")
    
    if st.button("중화 반응 결과 확인"):
        total_volume_l = (acid_v + base_v) / 1000
        acid_eq = acid_n * (acid_v / 1000)
        base_eq = base_n * (base_v / 1000)
        
        if acid_eq > base_eq:
            ph = -math.log10((acid_eq - base_eq) / total_volume_l)
            st.warning("산의 양이 더 많아 혼합 후 성질은 '산성'입니다.")
        elif base_eq > acid_eq:
            ph = 14 - (-math.log10((base_eq - acid_eq) / total_volume_l))
            st.info("염기의 양이 더 많아 혼합 후 성질은 '염기성'입니다.")
        else:
            ph = 7.0
            st.success("산과 염기의 양이 똑같아 완전 중화(중성)되었습니다!")
        st.success(f"🎉 최종 혼합 용액의 정답: pH = **{ph:.2f}**")

# --- 유형 6 ---
elif menu == "6. 🧪 약산/약염기 pH 계산기 (전리도 또는 해리상수 Ka/Kb 선택)":
    st.subheader("🧪 약산/약염기 전리도 및 해리상수 계산기")
    acid_base_type = st.radio("용액 성질 선택:", ["약산성 용액 (CH3COOH 등)", "약염기성 용액 (NH4OH 등)"])
    given_type = st.radio("주어진 조건 종류:", ["해리 상수 (Ka 또는 Kb)", "전리도 (alpha, 해리도)"])
    molarity = st.number_input("용액의 몰 농도 (M)", value=0.100, format="%.4f", step=0.001, key="t6_m")
    
    if given_type == "해리 상수 (Ka 또는 Kb)":
        col_k1, col_k2 = st.columns(2)
        with col_k1: k_prefix = st.number_input("상수 앞 숫자", value=1.8, step=0.1)
        with col_k2: k_exponent = st.number_input("10의 지수", value=-5, step=1)
        if st.button("🎉 계산 결과 보기", key="b6_k"):
            k_value = k_prefix * (10 ** k_exponent)
            ion_conc = math.sqrt(molarity * k_value)
            if acid_base_type == "약산성 용액 (CH3COOH 등)":
                ph = -math.log10(ion_conc)
                st.success(f"🎉 **정답 pH = {ph:.2f}**")
            else:
                poh = -math.log10(ion_conc)
                ph = 14.0 - poh
                st.success(f"🎉 **정답 pH = {ph:.2f}** (pOH = {poh:.2f})")
    else:
        ionization_input = st.number_input("전리도 수치 입력:", value=1.0, format="%.5f", step=0.1)
        input_type = st.radio("전리도 단위 선택:", ["퍼센트 단위 (%)", "소수점 단위 (0~1 사이의 값)"])
        if st.button("🎉 계산 결과 보기", key="b6_a"):
            alpha = ionization_input / 100.0 if input_type == "퍼센트 단위 (%)" else ionization_input
            ion_conc = molarity * alpha
            if acid_base_type == "약산성 용액 (CH3COOH 등)":
                ph = -math.log10(ion_conc)
                st.success(f"🎉 **정답 pH = {ph:.2f}**")
            else:
                poh = -math.log10(ion_conc)
                ph = 14.0 - poh
                st.success(f"🎉 **정답 pH = {ph:.2f}**")

# --- 유형 7 ---
elif menu == "7. 용액의 농도 단위환산 (1 → 100 표현법 등)":
    st.subheader("📊 용액 농도 단위환산기")
    col_a, col_b = st.columns(2)
    with col_a: solute_g = st.number_input("용질의 질량 (g)", value=1.0, step=0.1)
    with col_b: solution_ml = st.number_input("전체 용액 부피 (mL)", value=100.0, step=10.0)
    molecular_weight = st.number_input("용질의 분자량 입력:", value=40.0, step=1.0)
    
    if st.button("🔄 변환 결과 일괄 보기", type="primary"):
        wv_percent = (solute_g / solution_ml) * 100
        g_per_liter = (solute_g / solution_ml) * 1000
        mol_per_liter = g_per_liter / molecular_weight
        mg_per_liter = g_per_liter * 1000
        st.markdown("### 📋 변환 결과 리스트")
        st.success(f"1️⃣ **몰농도 (mol/ℓ):** {mol_per_liter:.4f} mol/L")
        st.success(f"2️⃣ **ppm 농도 (mg/ℓ):** {mg_per_liter:,.0f} ppm")
        st.success(f"3️⃣ **W/V % 농도:** {wv_percent:.2f} W/V %")