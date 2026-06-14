import streamlit as st
import math

# 스마트폰 화면에 맞게 페이지 설정
st.set_page_config(page_title="pH 마스터", layout="centered")

st.title("📱 pH 및 농도 단위환산 마스터")
st.write("농도 계산과 단위환산 문제를 모두 풀 수 있는 종합 도우미입니다.")

st.markdown("---")

# 메뉴 선택 (유형별로 나누기)
menu = st.selectbox(
    "풀고 싶은 문제 유형을 선택하세요:",
    [
        "1. 수소 이온 농도로 수산화 이온 농도 구하기",
        "2. 소수점이 포함된 수소 이온 농도로 pH 구하기",
        "3. 단일 용액(NaOH, H2SO4 등)의 pH 구하기 (N/M 선택 가능)",
        "4. 두 용액을 섞은 혼합 용액의 pH 구하기 (산+염기 또는 같은 액성 혼합)",
        "5. 🧪 용액의 농도 단위환산 (1 → 100 표현 등)",
        "6. 🧪 약산/약염기 전리도를 이용한 pH 구하기 (산/염기 선택)"
    ]
)

st.markdown("---")

# --- 유형 1 ---
if menu == "1. 수소 이온 농도로 수산화 이온 농도 구하기":
    st.subheader("💡 유형 1 계산기")
    st.write("예: H+ 농도가 4.0 x 10^-2 일 때 OH- 농도는?")
    col1, col2 = st.columns(2)
    with col1: prefix = st.number_input("앞의 숫자 (예: 4.0)", value=4.0, step=0.1, key="u1_1")
    with col2: exponent = st.number_input("10의 지수 (예: -2)", value=-2, step=1, key="u1_2")
    if st.button("정답 확인", key="b1"):
        h_conc = prefix * (10 ** exponent)
        oh_conc = 1e-14 / h_conc
        if oh_conc == 0: st.success("정답: OH- 이온 농도 = **0 mole/L**")
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
    with col1: prefix = st.number_input("앞의 숫자 (예: 5.8)", value=5.8, step=0.1, key="u2_1")
    with col2: exponent = st.number_input("10의 지수 (예: -4)", value=-4, step=1, key="u2_2")
    if st.button("정답 확인", key="b2"):
        h_conc = prefix * (10 ** exponent)
        ph = -math.log10(h_conc)
        st.success(f"🎉 정답: pH = **{ph:.2f}**")

# --- --- 유형 3 ---
elif menu == "3. 단일 용액(NaOH, H2SO4 등)의 pH 구하기 (N/M 선택 가능)":
    st.subheader("💡 유형 3 계산기")
    solution_name = st.selectbox("어떤 용액인가요?", ["NaOH (1가 염기)", "HCl (1가 산)", "H2SO4 (2가 산)"])
    unit_type = st.radio("농도 단위를 선택하세요:", ["몰 농도 (M)", "노르말 농도 (N)"])
    raw_conc = st.number_input("농도 숫자를 입력하세요:", value=0.002, format="%.4f", step=0.001)
    if st.button("정답 확인", key="b3"):
        final_n = raw_conc
        if unit_type == "몰 농도 (M)" and solution_name == "H2SO4 (2가 산)":
            final_n = raw_conc * 2
        if "NaOH" in solution_name:
            poh = -math.log10(final_n)
            ph = 14 - poh
        else:
            ph = -math.log10(final_n)
        st.success(f"🎉 정답: pH = **{ph:.2f}**")

# --- 🌟 [업그레이드] 유형 4: 혼합 용액 종합 계산기 🌟 ---
elif menu == "4. 두 용액을 섞은 혼합 용액의 pH 구하기 (산+염기 또는 같은 액성 혼합)":
    st.subheader("🧪 혼합 용액의 pH 계산기")
    
    mix_type = st.radio(
        "어떤 용액끼리 섞으시나요?",
        ["[타입 A] 산성 용액 + 염기성 용액 (중화 반응)", "[타입 B] 같은 성질의 용액끼리 믹스 (산+산 또는 염기+염기)"]
    )
    
    if mix_type == "[타입 A] 산성 용액 + 염기성 용액 (중화 반응)":
        st.markdown("### 🔴 산성 용액 입력")
        acid_n = st.number_input("산성 노르말 농도 (N)", value=0.1, step=0.01, key="ta_an")
        acid_v = st.number_input("산성 부피 (mL)", value=50, step=1, key="ta_av")
        
        st.markdown("### 🔵 염기성 용액 입력")
        base_n = st.number_input("염기성 노르말 농도 (N)", value=0.2, step=0.01, key="ta_bn")
        base_v = st.number_input("염기성 부피 (mL)", value=50, step=1, key="ta_bv")
        
        if st.button("혼합 용액 정답 확인", key="b4_a"):
            total_volume_l = (acid_v + base_v) / 1000
            acid_eq = acid_n * (acid_v / 1000)
            base_eq = base_n * (base_v / 1000)
            
            if acid_eq > base_eq:
                ph = -math.log10((acid_eq - base_eq) / total_volume_l)
                st.warning("산이 더 많아서 '산성'입니다.")
            elif base_eq > acid_eq:
                ph = 14 - (-math.log10((base_eq - acid_eq) / total_volume_l))
                st.info("염기가 더 많아서 '염기성'입니다.")
            else: 
                ph = 7.0
                st.success("완전 중화되었습니다!")
            st.success(f"🎉 최종 혼합 용액의 정답: pH = **{ph:.2f}**")
            
    else:
        # 이미지의 문제를 해결하는 [타입 B] 공간
        st.write("두 용액의 각각의 pH와 부피를 입력하면 혼합 pH를 자동으로 유도합니다.")
        
        sol_kind = st.radio("섞으려는 용액의 성질은 무엇인가요?", ["산성 용액끼리 섞음 (pH 7 미만)", "염기성 용액끼리 섞음 (pH 7 초과)"])
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("### 1번 용액")
            ph1 = st.number_input("1번 용액의 pH", value=3.0, step=0.1, format="%.1f")
            v1 = st.number_input("1번 용액의 부피 (mL)", value=100, step=10)
        with col_m2:
            st.markdown("### 2번 용액")
            ph2 = st.number_input("2번 용액의 pH", value=4.0, step=0.1, format="%.1f")
            v2 = st.number_input("2번 용액의 부피 (mL)", value=100, step=10)
            
        if st.button("혼합 용액 정답 확인", key="b4_b", type="primary"):
            # 전체 부피 (L 단위로 변환)
            total_v_l = (v1 + v2) / 1000.0
            
            if sol_kind == "산성 용액끼리 섞음 (pH 7 미만)":
                # pH를 수소이온농도[H+]로 역산: [H+] = 10^(-pH)
                h1 = 10 ** (-ph1)
                h2 = 10 ** (-ph2)
                
                # 각각의 용액에 들어있던 수소이온 총 몰수 (농도 * 부피L)
                total_h_mol = (h1 * (v1 / 1000.0)) + (h2 * (v2 / 1000.0))
                
                # 혼합 후 최종 [H+] 농도 = 총 몰수 / 총 부피
                final_h_conc = total_h_mol / total_v_l
                final_ph = -math.log10(final_h_conc)
                
                st.info(f"🧬 혼합 후 최종 수소 이온 농도 [H⁺] = **{final_h_conc:.6f} mol/L**")
                st.success(f"🎉 **최종 혼합 용액의 정답: pH = {final_ph:.2f}**")
                
            else:
                # 염기성 용액끼리 섞을 때
                poh1 = 14.0 - ph1
                poh2 = 14.0 - ph2
                
                oh1 = 10 ** (-poh1)
                oh2 = 10 ** (-poh2)
                
                total_oh_mol = (oh1 * (v1 / 1000.0)) + (oh2 * (v2 / 1000.0))
                final_oh_conc = total_oh_mol / total_v_l
                final_poh = -math.log10(final_oh_conc)
                final_ph = 14.0 - final_poh
                
                st.info(f"🧬 혼합 후 최종 수산화 이온 농도 [OH⁻] = **{final_oh_conc:.6f} mol/L**")
                st.success(f"🎉 **최종 혼합 용액의 정답: pH = {final_ph:.2f}**")

# --- 유형 5 ---
elif menu == "5. 🧪 용액의 농도 단위환산 (1 → 100 표현 등)":
    st.subheader("📊 용액의 농도 단위환산기")
    st.write("`NaOH (1 → 100)` 같은 표현법 및 다양한 단위 변환을 수행합니다.")
    st.info("ℹ️ 약전 표기법 지식: `(1 → 100)`은 고체 용질 1g을 녹여 총 용액 100mL를 만들었다는 뜻이며, 이는 정확히 **1 W/V %** 농도와 같습니다.")
    col_a, col_b = st.columns(2)
    with col_a: solute_g = st.number_input("용질의 양 (g)", value=1.0, step=0.1)
    with col_b: solution_ml = st.number_input("전체 용액의 부피 (mL)", value=100.0, step=10.0)
    molecular_weight = st.number_input("용질의 분자량 (예: NaOH는 40)", value=40.0, step=1.0)
    st.markdown("---")
    if st.button("🔄 단위환산 결과 보기", type="primary"):
        wv_percent = (solute_g / solution_ml) * 100
        g_per_liter = (solute_g / solution_ml) * 1000
        mol_per_liter = g_per_liter / molecular_weight
        mg_per_liter = g_per_liter * 1000
        st.markdown("### 📋 변환 결과 리스트")
        st.success(f"1️⃣ **몰농도 (mol/ℓ):** {mol_per_liter:.4f} mol/L")
        st.success(f"2️⃣ **ppm 농도 (mg/ℓ):** {mg_per_liter:,.0f} ppm")
        st.success(f"3️⃣ **W/V % 농도:** {wv_percent:.2f} W/V %")

# --- 유형 6 ---
elif menu == "6. 🧪 약산/약염기 전리도를 이용한 pH 구하기 (산/염기 선택)":
    st.subheader("🧪 전리도(해리도) 기반 pH 종합 계산기")
    acid_base_type = st.radio("용액의 성질을 고르세요:", ["약산성 용액 (CH3COOH 등)", "약염기성 용액 (NH4OH 등)"])
    molarity = st.number_input("용액의 몰 농도 (M)", value=0.100, format="%.4f", step=0.001)
    ionization_input = st.number_input("전리도(해리도) 입력 (값 또는 %)", value=0.0001, format="%.5f", step=0.0001)
    input_type = st.radio("전리도 입력 단위를 선택하세요:", ["소수점 단위 (0~1 사이의 값)", "퍼센트 단위 (%)"])
    st.markdown("---")
    if st.button("🎉 정답 확인", type="primary"):
        if input_type == "퍼센트 단위 (%)": alpha = ionization_input / 100.0
        else: alpha = ionization_input
        if alpha <= 0 or alpha > 1: st.error("❌ 전리도 값이 올바르지 않습니다.")
        else:
            ion_conc = molarity * alpha
            st.markdown("### 📋 계산 프로세스 및 결과")
            if acid_base_type == "약산성 용액 (CH3COOH 등)":
                ph = -math.log10(ion_conc)
                st.info(f"🧬 **수소 이온 농도 [H⁺]** = {molarity} M × {alpha} = **{ion_conc:.5f} mol/L**")
                st.success(f"🎉 **최종 정답 pH = {ph:.2f}**")
            else:
                poh = -math.log10(ion_conc)
                ph = 14.0 - poh
                st.info(f"🧬 **수산화 이온 농도 [OH⁻]** = {molarity} M × {alpha} = **{ion_conc:.5f} mol/L**")
                st.info(f"🧪 **pOH** = -log10({ion_conc:.5f}) = **{poh:.2f}**")
                st.success(f"🎉 **최종 정답 pH (14 - pOH) = {ph:.2f}**")