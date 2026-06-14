import streamlit as st
import math

# 스마트폰 화면에 맞게 페이지 설정
st.set_page_config(page_title="화학 pH 마스터 v2.3", layout="centered")

st.write("풀고 싶은 문제 유형을 선택하고 숫자를 입력하세요.")

# 메뉴 선택
menu = st.selectbox(
    "문제 유형 선택:",
    [
        "1. H+ 이온 농도로 pH 구하기",
        "2. H+ 이온 농도로 OH- 이온 농도 구하기",
        "3. pH 값을 주고 수소 이온 농도 [H+] 역산하기",
        "4. 같은 성질의 산성/염기성 용액 혼합하기 (N 농도 기반)",
        "5. 강산 또는 강염기 단일 용액의 pH 구하기",
        "6. 두 용액을 섞은 혼합 용액의 pH 구하기 (산+염기 또는 같은 액성 혼합)",
        "7. 중화 적정 실험 데이터로 미지 용액의 농도 및 pH 구하기",
        "8. 약산/약염기 pH 계산기 (전리도 또는 해리상수 Ka/Kb 선택)",
        "9. 농도 단위 교차 환산기 (M, N, ppm, % 무조건 변환)",
        "10. 수산화 이온 농도 [OH-]로 곧바로 pH 구하기"
    ]
)

st.write("---")

# --- 유형 1: H+ 농도로 pH 구하기 ---
if menu == "1. H+ 이온 농도로 pH 구하기":
    st.write("수소 이온 농도를 지수 형태로 입력하세요.")
    col_p1, col_p2 = st.columns(2)
    with col_p1: hp_prefix = st.number_input("농도 앞자리 숫자 (예: 5.8):", value=5.8, step=0.1, key="u1_ph_p")
    with col_p2: hp_exponent = st.number_input("10의 마이너스 지수 (예: -4):", value=-4, step=1, key="u1_ph_e")
    if st.button("정답 확인", type="primary", key="u1_btn"):
        if hp_prefix <= 0: st.write("농도 앞자리는 0보다 커야 합니다.")
        else:
            h_conc_val = hp_prefix * (10 ** hp_exponent)
            st.write(f"입력된 수소 이온 농도: {hp_prefix} * 10^{hp_exponent} mol/L")
            st.write(f"최종 계산 정답: pH = {-math.log10(h_conc_val):.2f}")

# --- 유형 2: H+ 농도로 OH- 농도 구하기 ---
elif menu == "2. H+ 이온 농도로 OH- 이온 농도 구하기":
    st.write("H+ 이온 농도를 지수 형태로 입력하세요.")
    col_h1, col_h2 = st.columns(2)
    with col_h1: h_prefix = st.number_input("농도 앞자리 숫자 (예: 4.0):", value=4.0, step=0.1, key="u2_hp")
    with col_h2: h_exponent = st.number_input("10의 마이너스 지수 (예: -2):", value=-2, step=1, key="u2_he")
    if st.button("정답 확인", type="primary", key="u2_btn"):
        if h_prefix <= 0: st.write("농도 앞자리는 0보다 커야 합니다.")
        else:
            oh_conc = 1e-14 / (h_prefix * (10 ** h_exponent))
            base, exponent_val = f"{oh_conc:.2e}".split('e')
            st.write(f"입력된 수소 이온 농도: {h_prefix} * 10^{h_exponent} mol/L")
            st.write(f"최종 정답: OH- 이온 농도 = {base} * 10^{int(exponent_val)} mole/L")

# --- 유형 3: pH 값을 주고 수소 이온 농도 역산하기 ---
elif menu == "3. pH 값을 주고 수소 이온 농도 [H+] 역산하기":
    st.write("측정된 pH 값을 입력하세요.")
    ph_input = st.number_input("pH 값:", value=4.70, format="%.2f", step=0.01, key="u3_ph")
    use_log_hint = st.checkbox("로그 단서 활용하기", value=True, key="u3_chk")
    log_base_num, log_value = 2.0, 0.30
    if use_log_hint:
        col_l1, col_l2 = st.columns(2)
        with col_l1: log_base_num = st.number_input("로그 진수 (예: 2):", value=2.0, step=0.1, key="u3_l1")
        with col_l2: log_value = st.number_input("로그 값 (예: 0.30):", value=0.30, step=0.01, key="u3_l2")
    if st.button("정답 확인", type="primary", key="u3_btn"):
        h_conc = 10 ** (-ph_input)
        st.write(f"일반 소수점 표기: {h_conc:.7f} mol/L")
        st.write(f"컴퓨터 지수 표기: {h_conc:.2e} mol/L")
        if use_log_hint:
            floor_val = math.ceil(ph_input)
            diff = floor_val - ph_input
            if abs(diff - log_value) < 0.02: st.write(f"시험 보기 정답 형태: {log_base_num} * 10^-{floor_val} mol/L")

# --- 유형 4: 같은 성질 혼합 (N농도) ---
elif menu == "4. 같은 성질의 산성/염기성 용액 혼합하기 (N 농도 기반)":
    sol_kind = st.radio("용액 성질 선택:", ["산성 용액끼리 섞음", "염기성 용액끼리 섞음"], key="u4_rad")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.write("1번 용액 입력")
        n1 = st.number_input("1번 노르말 농도 (N):", value=0.10, format="%.4f", step=0.01, key="u4_n1")
        v1 = st.number_input("1번 부피 (mL):", value=50, step=5, key="u4_v1")
    with col_m2:
        st.write("2번 용액 입력")
        n2 = st.number_input("2번 노르말 농도 (N):", value=0.20, format="%.4f", step=0.01, key="u4_n2")
        v2 = st.number_input("2번 부피 (mL):", value=50, step=5, key="u4_v2")
    if st.button("정답 확인", type="primary", key="u4_btn"):
        total_v_l = (v1 + v2) / 1000.0
        final_n = ((n1 * v1 / 1000.0) + (n2 * v2 / 1000.0)) / total_v_l
        st.write(f"혼합 후 최종 노르말 농도: {final_n:.4f} N")
        if sol_kind == "산성 용액끼리 섞음": st.write(f"최종 혼합 용액의 정답 pH = {-math.log10(final_n):.2f}")
        else: st.write(f"최종 혼합 용액의 정답 pH = {14.0 - (-math.log10(final_n)):.2f}")

# --- 유형 5: 강산/강염기 단일 pH ---
elif menu == "5. 강산 또는 강염기 단일 용액의 pH 구하기":
    sol_type = st.radio("용액의 성질:", ["강산성 용액", "강염기성 용액"], key="u5_r1")
    unit_type = st.radio("농도 단위:", ["몰 농도 (M)", "노르말 농도 (N)"], key="u5_r2")
    valence = st.radio("용액의 가수:", ["1가 용액", "2가 용액"], key="u5_r3")
    raw_conc = st.number_input("농도 수치 입력:", value=0.0100, format="%.4f", step=0.001, key="u5_conc")
    if st.button("정답 확인", type="primary", key="u5_btn"):
        final_n = raw_conc
        if unit_type == "몰 농도 (M)" and "2가" in valence:
            final_n = raw_conc * 2
            st.write(f"2가 몰농도 보정 반영: {final_n:.4f} N")
        if "강산성" in sol_type: st.write(f"최종 pH = {-math.log10(final_n):.2f}")
        else:
            poh = -math.log10(final_n)
            st.write(f"최종 pH = {14.0 - poh:.2f} (pOH = {poh:.2f})")

# --- 유형 6: 두 용액 교차 혼합 (산+염기 등) ---
elif menu == "6. 두 용액을 섞은 혼합 용액의 pH 구하기 (산+염기 또는 같은 액성 혼합)":
    mix_type = st.radio("혼합 종류 선택:", ["산성 용액 + 염기성 용액 (중화 반응)", "같은 성질의 용액끼리 믹스"], key="u6_type")
    if "중화 반응" in mix_type:
        acid_n = st.number_input("산성 노르말 농도 (N):", value=0.1, step=0.01, key="u6_an")
        acid_v = st.number_input("산성 부피 (mL):", value=50, step=1, key="u6_av")
        base_n = st.number_input("염기성 노르말 농도 (N):", value=0.2, step=0.01, key="u6_bn")
        base_v = st.number_input("염기성 부피 (mL):", value=50, step=1, key="u6_bv")
        if st.button("정답 확인", key="u6_btn_a", type="primary"):
            total_volume_l = (acid_v + base_v) / 1000
            acid_eq, base_eq = acid_n * acid_v / 1000, base_n * base_v / 1000
            if acid_eq > base_eq: ph = -math.log10((acid_eq - base_eq) / total_volume_l)
            elif base_eq > acid_eq: ph = 14 - (-math.log10((base_eq - acid_eq) / total_volume_l))
            else: ph = 7.0
            st.write(f"최종 혼합 용액의 정답: pH = {ph:.2f}")
    else:
        sol_kind = st.radio("용액 성질:", ["산성 용액끼리 섞음", "염기성 용액끼리 섞음"], key="u6_kind_b")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            n1 = st.number_input("1번 노르말 농도 (N):", value=0.0010, format="%.4f", step=0.001, key="u6_n1_b")
            v1 = st.number_input("1번 부피 (mL):", value=100, step=10, key="u6_v1_b")
        with col_m2:
            n2 = st.number_input("2번 노르말 농도 (N):", value=0.0001, format="%.4f", step=0.001, key="u6_n2_b")
            v2 = st.number_input("2번 부피 (mL):", value=100, step=10, key="u6_v2_b")
        if st.button("정답 확인", key="u6_btn_b", type="primary"):
            total_v_l = (v1 + v2) / 1000.0
            final_n = ((n1 * v1 / 1000.0) + (n2 * v2 / 1000.0)) / total_v_l
            if sol_kind == "산성 용액끼리 섞음": st.write(f"최종 혼합 용액의 정답: pH = {-math.log10(final_n):.2f}")
            else: st.write(f"최종 혼합 용액의 정답: pH = {14.0 - (-math.log10(final_n)):.2f}")

# --- 유형 7: 중화 적정 실험 전용 ---
elif menu == "7. 중화 적정 실험 데이터로 미지 용액의 농도 및 pH 구하기":
    target_type = st.radio("미지 용액 종류:", ["미지의 강산 용액", "미지의 강염기 용액"], key="u7_target")
    v_target = st.number_input("미지 용액 채취량 (mL):", value=100, step=10, key="u7_vt")
    n_standard = st.number_input("표준 용액 노르말 농도 (N):", value=0.1000, format="%.4f", step=0.01, key="u7_ns")
    v_standard = st.number_input("소비된 표준 용액 부피 (mL):", value=10, step=1, key="u7_vs")
    if st.button("정답 확인", type="primary", key="u7_btn"):
        n_result = (n_standard * v_standard) / v_target
        st.write(f"산출된 미지 용액 농도 = {n_result:.4f} N")
        ph = -math.log10(n_result) if "강산" in target_type else 14.0 - (-math.log10(n_result))
        st.write(f"미지 용액의 최종 pH = {ph:.2f}")

# --- 유형 8: 약산/약염기 ---
elif menu == "8. 약산/약염기 pH 계산기 (전리도 또는 해리상수 Ka/Kb 선택)":
    acid_base_type = st.radio("용액 성질:", ["약산성 용액", "약염기성 용액"], key="u8_ab")
    given_type = st.radio("주어진 조건 종류:", ["해리 상수 (Ka 또는 Kb)", "전리도"], key="u8_given")
    molarity = st.number_input("용액의 몰 농도 (M):", value=0.100, format="%.4f", step=0.001, key="u8_m")
    if given_type == "해리 상수 (Ka 또는 Kb)":
        col_k1, col_k2 = st.columns(2)
        with col_k1: k_prefix = st.number_input("상수 앞 숫자:", value=1.8, step=0.1, key="u8_kp")
        with col_k2: k_exponent = st.number_input("10의 지수:", value=-5, step=1, key="u8_ke")
        if st.button("정답 확인", key="u8_btn_k", type="primary"):
            ion_conc = math.sqrt(molarity * (k_prefix * (10 ** k_exponent)))
            ph = -math.log10(ion_conc) if "약산성" in acid_base_type else 14.0 - (-math.log10(ion_conc))
            st.write(f"최종 정답 pH = {ph:.2f}")
    else:
        ionization_input = st.number_input("전리도 입력:", value=1.0, format="%.5f", step=0.1, key="u8_ion")
        input_type = st.radio("단위 선택:", ["퍼센트 단위 (%)", "소수점 단위 (0~1)"], key="u8_itype")
        if st.button("정답 확인", key="u8_btn_a", type="primary"):
            alpha = ionization_input / 100.0 if "퍼센트" in input_type else ionization_input
            ion_conc = molarity * alpha
            ph = -math.log10(ion_conc) if "약산성" in acid_base_type else 14.0 - (-math.log10(ion_conc))
            st.write(f"최종 정답 pH = {ph:.2f}")

# --- 유형 9: 농도 단위 교차 환산기 ---
elif menu == "9. 농도 단위 교차 환산기 (M, N, ppm, % 무조건 변환)":
    # 사용자의 요청에 따라 대표 원소 및 물질들의 분자량 가이드를 텍스트로 추가했습니다.
    st.write("📋 자주 나오는 대표 물질 분자량 가이드")
    st.write("수산화나트륨 (NaOH) = 40.0 | 염산 (HCl) = 36.5")
    st.write("황산 (H2SO4) = 98.0 | 수산화칼륨 (KOH) = 56.0")
    st.write("질산 (HNO3) = 63.0 | 초산 (CH3COOH) = 60.0")
    st.write("---")
    
    col_i1, col_i2 = st.columns(2)
    with col_i1: mw = st.number_input("물질의 분자량 입력:", value=40.0, step=1.0, key="u9_mw")
    with col_i2: val = st.number_input("물질의 가수 입력 (1 또는 2):", value=1, step=1, key="u9_val")
    
    input_mode = st.radio(
        "알고 있는 농도 종류:",
        ["약전 표기법 (1 → 100 방식)", "W/V % 농도 직접 입력", "몰 농도 (M) 직접 입력", "노르말 농도 (N) 직접 입력", "ppm 농도 직접 입력"],
        key="u9_mode"
    )
    wv_percent = 0.0
    if "약전 표기법" in input_mode:
        col_solute, col_solvol = st.columns(2)
        with col_solute: g_val = st.number_input("녹인 양 (g):", value=1.0, step=0.1, key="u9_g")
        with col_solvol: ml_val = st.number_input("전체 부피 (mL):", value=100.0, step=10.0, key="u9_ml")
        if ml_val > 0: wv_percent = (g_val / ml_val) * 100.0
    elif "%" in input_mode: wv_percent = st.number_input("W/V % 값:", value=1.0, format="%.2f", step=0.1, key="u9_wv")
    elif "(M)" in input_mode:
        m_val = st.number_input("몰 농도 (M) 값:", value=0.25, format="%.4f", step=0.01, key="u9_m")
        wv_percent = (m_val * mw) / 10.0
    elif "(N)" in input_mode:
        n_val = st.number_input("노르말 농도 (N) 값:", value=0.25, format="%.4f", step=0.01, key="u9_n")
        if val > 0: wv_percent = ((n_val / val) * mw) / 10.0
    elif "ppm" in input_mode:
        ppm_val = st.number_input("ppm 값:", value=10000.0, format="%.1f", step=100.0, key="u9_ppm")
        wv_percent = ppm_val / 10000.0
        
    if st.button("일괄 변환하기", type="primary", key="u9_btn"):
        calc_ppm = wv_percent * 10000.0
        calc_m = (wv_percent * 10.0) / mw
        calc_n = calc_m * val
        st.write(f"기준 W/V % 농도 = {wv_percent:.2f} %")
        st.write(f"몰 농도 (M): {calc_m:.4f} M")
        st.write(f"노르말 농도 (N): {calc_n:.4f} N")
        st.write(f"ppm 농도: {calc_ppm:,.0f} ppm")
        st.write(f"W/V % 농도: {wv_percent:.2f} %")

# --- 유형 10: OH-로 곧바로 pH 구하기 ---
elif menu == "10. 수산화 이온 농도 [OH-]로 곧바로 pH 구하기":
    col_oh1, col_oh2 = st.columns(2)
    with col_oh1: oh_p = st.number_input("농도 앞자리 숫자 (예: 1.0):", value=1.0, step=0.1, key="u10_oh_p")
    with col_oh2: oh_e = st.number_input("10의 마이너스 지수 (예: -3):", value=-3, step=1, key="u10_oh_e")
    if st.button("정답 확인", type="primary", key="u10_btn"):
        poh = -math.log10(oh_p * (10 ** oh_e))
        st.write(f"최종 계산 정답: pH = {14.0 - poh:.2f}")