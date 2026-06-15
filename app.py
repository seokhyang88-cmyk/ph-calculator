import streamlit as st
import math

# 스마트폰 화면 비율에 맞게 페이지 설정
st.set_page_config(page_title="공학용 pH 마스터 v5.5", layout="centered")

# 📸 1. 최상단 공학용 계산기 자판 이미지 배치 구역
# (추후 깃허브나 ImgBB에 올리신 본인의 계산기 이미지 주소로 이 링크만 교체하시면 됩니다!)
st.image(
    "https://github.com/seokhyang88-cmyk/ph-calculator/blob/main/pHcal2.jpg?raw=true", 
    caption="Scientific Calculator Active Skin",
    use_container_width=True
)

st.write("---")

# 세션 스테이트(메모리) 초기화
if "ph_result" not in st.session_state: st.session_state.ph_result = ""

# ⚙️ 2. 계산기 내부 조작 및 입력 구역 (1번부터 10번까지 전 메뉴 부활)
menu_select = st.selectbox(
    "계산기 MODE 변경 (유형 선택):",
    [
        "1. H+ 이온 농도로 pH 구하기",
        "2. H+ 이온 농도로 OH- 이온 농도 구하기",
        "3. pH 값을 주고 수소 이온 농도 [H+] 역산하기",
        "4. 같은 성질의 산성/염기성 용액 혼합하기 (N 농도 기반)",
        "5. 강산 또는 강염기 단일 용액의 pH 구하기",
        "6. 두 용액을 섞은 혼합 용액의 pH 구하기 (교차/동일 혼합)",
        "7. 중화 적정 실험 데이터로 미지 용액의 농도 및 pH 구하기",
        "8. 약산/약염기 pH 계산기 (전리도 또는 해리상수 선택)",
        "9. 농도 단위 교차 환산기 (M, N, ppm, % 무조건 변환)",
        "10. 수산화 이온 농도 [OH-]로 곧바로 pH 구하기"
    ],
    key="mode_box"
)
current_mode = menu_select.split(".")[0]

st.write("▼ 현재 모드 입력창 세팅")

# 각 메뉴별 입력창 세팅
if current_mode == "1":
    col1, col2 = st.columns(2)
    with col1: hp_prefix = st.number_input("농도 앞자리 숫자 (예: 5.8):", value=5.8, step=0.1, key="m1_p")
    with col2: hp_exponent = st.number_input("10의 마이너스 지수 (예: -4):", value=-4, step=1, key="m1_e")

elif current_mode == "2":
    col1, col2 = st.columns(2)
    with col1: h_prefix = st.number_input("농도 앞자리 숫자 (예: 4.0):", value=4.0, step=0.1, key="m2_p")
    with col2: h_exponent = st.number_input("10의 마이너스 지수 (예: -2):", value=-2, step=1, key="m2_e")

elif current_mode == "3":
    ph_input = st.number_input("pH 값 입력:", value=4.70, format="%.2f", step=0.01, key="m3_ph")
    use_log_hint = st.checkbox("로그 단서 활용하기", value=True, key="m3_chk")
    col1, col2 = st.columns(2)
    with col1: log_base_num = st.number_input("로그 진수 (예: 2):", value=2.0, step=0.1, key="m3_l1")
    with col2: log_value = st.number_input("로그 값 (예: 0.30):", value=0.30, step=0.01, key="m3_l2")

elif current_mode == "4":
    sol_kind = st.radio("용액 성질 선택:", ["산성 용액끼리 섞음", "염기성 용액끼리 섞음"], key="m4_rad")
    col1, col2 = st.columns(2)
    with col1:
        n1 = st.number_input("1번 노르말 농도 (N):", value=0.10, format="%.4f", step=0.01, key="m4_n1")
        v1 = st.number_input("1번 부피 (mL):", value=50, step=5, key="m4_v1")
    with col2:
        n2 = st.number_input("2번 노르말 농도 (N):", value=0.20, format="%.4f", step=0.01, key="m4_n2")
        v2 = st.number_input("2번 부피 (mL):", value=50, step=5, key="m4_v2")

elif current_mode == "5":
    sol_type = st.radio("용액의 성질:", ["강산성 용액", "강염기성 용액"], key="m5_r1")
    unit_type = st.radio("농도 단위:", ["몰 농도 (M)", "노르말 농도 (N)"], key="m5_r2")
    valence = st.radio("용액의 가수:", ["1가 용액", "2가 용액"], key="m5_r3")
    raw_conc = st.number_input("농도 수치 입력:", value=0.0100, format="%.4f", step=0.001, key="m5_conc")

elif current_mode == "6":
    mix_type = st.radio("혼합 종류 선택:", ["산성 용액 + 염기성 용액 (중화 반응)", "같은 성질의 용액끼리 믹스"], key="m6_type")
    if "중화 반응" in mix_type:
        acid_n = st.number_input("산성 노르말 농도 (N):", value=0.1, step=0.01, key="m6_an")
        acid_v = st.number_input("산성 부피 (mL):", value=50, step=1, key="m6_av")
        base_n = st.number_input("염기성 노르말 농도 (N):", value=0.2, step=0.01, key="m6_bn")
        base_v = st.number_input("염기성 부피 (mL):", value=50, step=1, key="m6_bv")
    else:
        sol_kind_6 = st.radio("용액 성질:", ["산성 용액끼리 섞음", "염기성 용액끼리 섞음"], key="m6_kind_b")
        col1, col2 = st.columns(2)
        with col1:
            n1_6 = st.number_input("1번 노르말 농도 (N):", value=0.0010, format="%.4f", step=0.001, key="m6_n1")
            v1_6 = st.number_input("1번 부피 (mL):", value=100, step=10, key="m6_v1")
        with col2:
            n2_6 = st.number_input("2번 노르말 농도 (N):", value=0.0001, format="%.4f", step=0.001, key="m6_n2")
            v2_6 = st.number_input("2번 부피 (mL):", value=100, step=10, key="m6_v2")

elif current_mode == "7":
    target_type = st.radio("미지 용액 종류:", ["미지의 강산 용액", "미지의 강염기 용액"], key="m7_target")
    v_target = st.number_input("미지 용액 채취량 (mL):", value=100, step=10, key="m7_vt")
    n_standard = st.number_input("표준 용액 노르말 농도 (N):", value=0.1000, format="%.4f", step=0.01, key="m7_ns")
    v_standard = st.number_input("소비된 표준 용액 부피 (mL):", value=10, step=1, key="m7_vs")

elif current_mode == "8":
    acid_base_type = st.radio("용액 성질:", ["약산성 용액", "약염기성 용액"], key="m8_ab")
    given_type = st.radio("주어진 조건 종류:", ["해리 상수 (Ka 또는 Kb)", "전리도"], key="m8_given")
    molarity = st.number_input("용액의 몰 농도 (M):", value=0.010, format="%.4f", step=0.001, key="m8_m")
    if given_type == "해리 상수 (Ka 또는 Kb)":
        col1, col2 = st.columns(2)
        with col1: k_prefix = st.number_input("상수 앞 숫자:", value=1.8, step=0.1, key="m8_kp")
        with col2: k_exponent = st.number_input("10의 지수:", value=-5, step=1, key="m8_ke")
    else:
        ionization_input = st.number_input("전리도 입력:", value=1.0, format="%.5f", step=0.1, key="m8_ion")
        input_type = st.radio("단위 선택:", ["퍼센트 단위 (%)", "소수점 단위 (0~1)"], key="m8_itype")

elif current_mode == "9":
    st.write("분자량 가이드: NaOH=40 | HCl=36.5 | H2SO4=98 | CH3COOH=60")
    col1, col2 = st.columns(2)
    with col1: mw = st.number_input("물질의 분자량 입력:", value=40.0, step=1.0, key="m9_mw")
    with col2: val = st.number_input("물질의 가수 입력 (1 또는 2):", value=1, step=1, key="m9_val")
    input_mode = st.radio(
        "알고 있는 농도 종류:",
        ["W/V % 농도 직접 입력", "몰 농도 (M) 직접 입력", "노르말 농도 (N) 직접 입력", "ppm 농도 직접 입력"],
        key="m9_mode"
    )
    if "%" in input_mode: wv_percent = st.number_input("W/V % 값:", value=1.0, format="%.2f", step=0.1, key="m9_wv")
    elif "(M)" in input_mode:
        m_val = st.number_input("몰 농도 (M) 값:", value=0.25, format="%.4f", step=0.01, key="m9_m")
        wv_percent = (m_val * mw) / 10.0
    elif "(N)" in input_mode:
        n_val = st.number_input("노르말 농도 (N) 값:", value=0.25, format="%.4f", step=0.01, key="m9_n")
        wv_percent = ((n_val / val) * mw) / 10.0 if val > 0 else 0.0
    elif "ppm" in input_mode:
        ppm_val = st.number_input("ppm 값:", value=10000.0, format="%.1f", step=100.0, key="m9_ppm")
        wv_percent = ppm_val / 10000.0

elif current_mode == "10":
    col1, col2 = st.columns(2)
    with col1: oh_p = st.number_input("농도 앞자리 숫자 (예: 1.0):", value=1.0, step=0.1, key="m10_oh_p")
    with col2: oh_e = st.number_input("10의 마이너스 지수 (예: -3):", value=-3, step=1, key="m10_oh_e")

st.write("")

# 🕹️ 3. 결과 출력용 정순 컴포넌트 실행 버튼
if st.button(" ＝ [ RUN CALCULATOR ] ", type="primary", use_container_width=True, key="btn_equal"):
    try:
        if current_mode == "1":
            h_conc_val = hp_prefix * (10 ** hp_exponent)
            st.session_state.ph_result = f"pH = {-math.log10(h_conc_val):.2f}"
            
        elif current_mode == "2":
            oh_conc = 1e-14 / (h_prefix * (10 ** h_exponent))
            base, exponent_val = f"{oh_conc:.2e}".split('e')
            st.session_state.ph_result = f"[OH-] = {base} × 10^{int(exponent_val)} mol/L"
            
        elif current_mode == "3":
            h_conc = 10 ** (-ph_input)
            res = f"[H+] = {h_conc:.2e} mol/L"
            if use_log_hint:
                floor_val = math.ceil(ph_input)
                diff = floor_val - ph_input
                if abs(diff - log_value) < 0.02:
                    res += f"\n(보기 형태: {log_base_num} × 10^-{floor_val} mol/L)"
            st.session_state.ph_result = res
            
        elif current_mode == "4":
            total_v_l = (v1 + v2) / 1000.0
            final_n = ((n1 * v1 / 1000.0) + (n2 * v2 / 1000.0)) / total_v_l
            ans_ph = -math.log10(final_n) if "산성" in sol_kind else 14.0 - (-math.log10(final_n))
            st.session_state.ph_result = f"최종 농도: {final_n:.4f} N\n최종 pH = {ans_ph:.2f}"
            
        elif current_mode == "5":
            final_n = raw_conc * 2 if (unit_type == "몰 농도 (M)" and "2가" in valence) else raw_conc
            ans_ph = -math.log10(final_n) if "강산성" in sol_type else 14.0 - (-math.log10(final_n))
            st.session_state.ph_result = f"pH = {ans_ph:.2f}"
            
        elif current_mode == "6":
            if "중화 반응" in mix_type:
                total_v_l = (acid_v + base_v) / 1000.0
                acid_eq, base_eq = acid_n * acid_v / 1000.0, base_n * base_v / 1000.0
                if acid_eq > base_eq: ans_ph = -math.log10((acid_eq - base_eq) / total_v_l)
                elif base_eq > acid_eq: ans_ph = 14.0 - (-math.log10((base_eq - acid_eq) / total_v_l))
                else: ans_ph = 7.0
            else:
                total_v_l = (v1_6 + v2_6) / 1000.0
                final_n = ((n1_6 * v1_6 / 1000.0) + (n2_6 * v2_6 / 1000.0)) / total_v_l
                ans_ph = -math.log10(final_n) if "산성" in sol_kind_6 else 14.0 - (-math.log10(final_n))
            st.session_state.ph_result = f"혼합 pH = {ans_ph:.2f}"
            
        elif current_mode == "7":
            n_result = (n_standard * v_standard) / v_target
            ans_ph = -math.log10(n_result) if "강산" in target_type else 14.0 - (-math.log10(n_result))
            st.session_state.ph_result = f"미지 농도: {n_result:.4f} N\n최종 pH = {ans_ph:.2f}"
            
        elif current_mode == "8":
            if given_type == "해리 상수 (Ka 또는 Kb)":
                ion_conc = math.sqrt(molarity * (k_prefix * (10 ** k_exponent)))
            else:
                alpha = ionization_input / 100.0 if "퍼센트" in input_type else ionization_input
                ion_conc = molarity * alpha
            ans_ph = -math.log10(ion_conc) if "약산성" in acid_base_type else 14.0 - (-math.log10(ion_conc))
            st.session_state.ph_result = f"pH = {ans_ph:.2f}"
            
        elif current_mode == "9":
            calc_ppm = wv_percent * 10000.0
            calc_m = (wv_percent * 10.0) / mw
            calc_n = calc_m * val
            st.session_state.ph_result = f"M농도: {calc_m:.4f} M | N농도: {calc_n:.4f} N\nppm: {calc_ppm:,.0f} ppm | %농도: {wv_percent:.2f} %"
            
        elif current_mode == "10":
            poh = -math.log10(oh_p * (10 ** oh_e))
            st.session_state.ph_result = f"pH = {14.0 - poh:.2f}"
    except:
        st.session_state.ph_result = "ERROR: 입력 수치를 확인하세요."
    st.rerun()

# 📢 4. 계산 결과 표시창 (버튼 바로 아래에 깔끔하게 배치)
if st.session_state.ph_result:
    st.write("---")
    st.success(f"🎉 계산 결과\n\n{st.session_state.ph_result}")