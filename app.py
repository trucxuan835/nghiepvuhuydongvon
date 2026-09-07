import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

# =========================================================
# CẤU HÌNH TRANG
# =========================================================
st.set_page_config(
    page_title="Số tiền gửi - SMARTSAVE 360",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS GIAO DIỆN
# =========================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: "Be Vietnam Pro", sans-serif;
}

/* NỀN */
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(226, 29, 43, 0.08), transparent 25%),
        radial-gradient(circle at 90% 15%, rgba(0, 150, 105, 0.08), transparent 25%),
        linear-gradient(135deg, #ffffff 0%, #f7f7f7 50%, #ffffff 100%);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111111 0%, #242424 100%);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* TIÊU ĐỀ */
.main-title {
    text-align: center;
    font-size: 50px;
    font-weight: 800;
    letter-spacing: 4px;
    color: #111111;
    margin-top: 5px;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    color: #666666;
    font-size: 14px;
    margin-bottom: 18px;
}

/* CHỮ CHẠY */
.marquee-container {
    width: 100%;
    overflow: hidden;
    background: #111111;
    border-radius: 12px;
    padding: 11px 0;
    margin: 15px 0 22px 0;
    box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}

.marquee {
    display: inline-block;
    white-space: nowrap;
    animation: marquee 22s linear infinite;
    color: white;
    font-size: 14px;
    font-weight: 700;
}

@keyframes marquee {
    0% {
        transform: translateX(100%);
    }
    100% {
        transform: translateX(-100%);
    }
}

/* SMARTSAVE 360 */
.smart-card {
    background: linear-gradient(135deg, #e21d2b, #b50918);
    color: white;
    border-radius: 24px;
    padding: 30px;
    margin-bottom: 22px;
    box-shadow: 0 14px 35px rgba(226,29,43,0.25);
    position: relative;
    overflow: hidden;
}

.smart-card:before {
    content: "";
    position: absolute;
    width: 250px;
    height: 250px;
    border: 35px solid rgba(255,255,255,0.06);
    border-radius: 50%;
    right: -80px;
    top: -80px;
}

.smart-title {
    font-size: 36px;
    font-weight: 800;
    letter-spacing: 5px;
}

.smart-subtitle {
    font-size: 14px;
    opacity: 0.9;
    margin-top: 5px;
}

/* Ô XANH */
.green-header {
    background: linear-gradient(90deg, #008b65, #00aa7a);
    color: white;
    padding: 14px 20px;
    border-radius: 12px;
    font-weight: 800;
    font-size: 18px;
    margin: 20px 0 16px 0;
    box-shadow: 0 7px 18px rgba(0,139,101,0.20);
}

/* ĐANG CHỌN */
.selected-box {
    background: #e9f8f2;
    border: 1px solid #b6e5d3;
    color: #006d50;
    padding: 13px 18px;
    border-radius: 12px;
    font-weight: 700;
    margin-bottom: 18px;
}

/* BUTTON */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 700 !important;
    min-height: 42px !important;
    transition: 0.2s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.15);
}

/* CARD METRIC */
div[data-testid="stMetric"] {
    background: white;
    border-radius: 16px;
    padding: 18px;
    border: 1px solid #eeeeee;
    box-shadow: 0 5px 18px rgba(0,0,0,0.06);
}

/* INFO */
.info-card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    border-left: 5px solid #e21d2b;
    box-shadow: 0 5px 18px rgba(0,0,0,0.06);
}

/* FOOTER */
.footer {
    background: #111111;
    color: #dddddd;
    text-align: center;
    padding: 22px;
    border-radius: 15px;
    margin-top: 40px;
    font-size: 13px;
}

/* RADIO */
div[role="radiogroup"] label {
    font-weight: 600;
}

/* SELECTBOX / INPUT */
.stSelectbox, .stNumberInput, .stDateInput {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM XỬ LÝ
# =========================================================

def format_money(value):
    return f"{value:,.0f} VNĐ"


def maturity_date(start_date, months):
    """Tính ngày đến hạn theo kỳ hạn tháng."""
    return start_date + relativedelta(months=months)


def simple_interest(principal, annual_rate, days):
    """
    Lãi đơn:
    I = P x r x n / 365
    """
    return principal * (annual_rate / 100) * days / 365


def compound_interest(principal, annual_rate, days):
    """
    Lãi kép mô phỏng ghép lãi theo ngày.
    """
    if days <= 0:
        return 0

    daily_rate = annual_rate / 100 / 365

    future_value = principal * ((1 + daily_rate) ** days)

    return future_value - principal


def calculate_interest(
    principal,
    annual_rate,
    days,
    interest_type
):
    if days <= 0:
        return 0

    if interest_type == "Lãi đơn":
        return simple_interest(
            principal,
            annual_rate,
            days
        )

    return compound_interest(
        principal,
        annual_rate,
        days
    )


# =========================================================
# TÍNH CÁC KỲ GỬI
# =========================================================

def calculate_periods(
    principal,
    deposit_date,
    withdrawal_date,
    term_months,
    fixed_rate,
    nonterm_rate,
    interest_type
):

    periods = []

    current_start = deposit_date

    period_number = 1

    total_interest = 0

    while current_start < withdrawal_date:

        current_maturity = maturity_date(
            current_start,
            term_months
        )

        # -------------------------------------------------
        # RÚT TRƯỚC HẠN
        # -------------------------------------------------
        if withdrawal_date < current_maturity:

            days = (
                withdrawal_date - current_start
            ).days

            interest = calculate_interest(
                principal,
                nonterm_rate,
                days,
                interest_type
            )

            periods.append({
                "Kỳ": period_number,
                "Từ ngày": current_start,
                "Đến ngày": withdrawal_date,
                "Số ngày": days,
                "Trạng thái": "Rút trước hạn",
                "Lãi suất": nonterm_rate,
                "Tiền lãi": interest
            })

            total_interest += interest

            break

        # -------------------------------------------------
        # ĐỦ KỲ HẠN
        # -------------------------------------------------
        days = (
            current_maturity - current_start
        ).days

        interest = calculate_interest(
            principal,
            fixed_rate,
            days,
            interest_type
        )

        periods.append({
            "Kỳ": period_number,
            "Từ ngày": current_start,
            "Đến ngày": current_maturity,
            "Số ngày": days,
            "Trạng thái": "Đủ kỳ hạn - tự động gia hạn",
            "Lãi suất": fixed_rate,
            "Tiền lãi": interest
        })

        total_interest += interest

        # Tự động gia hạn cùng kỳ hạn
        current_start = current_maturity

        period_number += 1

    return periods, total_interest


# =========================================================
# LỊCH NHẬN LÃI
# =========================================================

def interest_schedule(
    principal,
    deposit_date,
    withdrawal_date,
    term_months,
    fixed_rate,
    nonterm_rate,
    interest_type,
    payment_method
):

    schedule = []

    # =====================================================
    # NHẬN LÃI TRƯỚC
    # =====================================================

    if payment_method == "Nhận lãi trước":

        current_start = deposit_date
        period_number = 1

        while current_start < withdrawal_date:

            current_maturity = maturity_date(
                current_start,
                term_months
            )

            # Rút trước hạn
            if withdrawal_date < current_maturity:

                days = (
                    withdrawal_date - current_start
                ).days

                interest = calculate_interest(
                    principal,
                    nonterm_rate,
                    days,
                    interest_type
                )

                schedule.append({
                    "Kỳ": period_number,
                    "Ngày nhận": withdrawal_date,
                    "Nội dung": "Quyết toán rút trước hạn",
                    "Số ngày": days,
                    "Lãi suất": nonterm_rate,
                    "Tiền lãi": interest
                })

                break

            # Đủ kỳ hạn
            days = (
                current_maturity - current_start
            ).days

            interest = calculate_interest(
                principal,
                fixed_rate,
                days,
                interest_type
            )

            schedule.append({
                "Kỳ": period_number,
                "Ngày nhận": current_start,
                "Nội dung": "Nhận lãi trước",
                "Số ngày": days,
                "Lãi suất": fixed_rate,
                "Tiền lãi": interest
            })

            current_start = current_maturity

            period_number += 1


    # =====================================================
    # NHẬN LÃI HÀNG THÁNG
    # =====================================================

    elif payment_method == "Nhận lãi hàng tháng":

        current_start = deposit_date
        period_number = 1

        while current_start < withdrawal_date:

            current_term_end = maturity_date(
                current_start,
                term_months
            )

            # Nếu rút trước kỳ hạn
            if withdrawal_date < current_term_end:

                days = (
                    withdrawal_date - current_start
                ).days

                if days > 0:

                    interest = calculate_interest(
                        principal,
                        nonterm_rate,
                        days,
                        interest_type
                    )

                    schedule.append({
                        "Kỳ": period_number,
                        "Ngày nhận": withdrawal_date,
                        "Nội dung": "Quyết toán rút trước hạn",
                        "Số ngày": days,
                        "Lãi suất": nonterm_rate,
                        "Tiền lãi": interest
                    })

                break

            # ---------------------------------------------
            # Tạo từng tháng trong kỳ
            # ---------------------------------------------

            month_start = current_start

            while month_start < current_term_end:

                month_end = month_start + relativedelta(
                    months=1
                )

                if month_end > current_term_end:
                    month_end = current_term_end

                days = (
                    month_end - month_start
                ).days

                if days > 0:

                    interest = calculate_interest(
                        principal,
                        fixed_rate,
                        days,
                        interest_type
                    )

                    schedule.append({
                        "Kỳ": period_number,
                        "Ngày nhận": month_end,
                        "Nội dung": "Nhận lãi hàng tháng",
                        "Số ngày": days,
                        "Lãi suất": fixed_rate,
                        "Tiền lãi": interest
                    })

                month_start = month_end

                period_number += 1

            current_start = current_term_end


    # =====================================================
    # NHẬN LÃI CUỐI KỲ
    # =====================================================

    else:

        periods, _ = calculate_periods(
            principal,
            deposit_date,
            withdrawal_date,
            term_months,
            fixed_rate,
            nonterm_rate,
            interest_type
        )

        for p in periods:

            if p["Trạng thái"] == "Rút trước hạn":

                content = "Quyết toán rút trước hạn"

            else:

                content = "Nhận lãi cuối kỳ"

            schedule.append({
                "Kỳ": p["Kỳ"],
                "Ngày nhận": p["Đến ngày"],
                "Nội dung": content,
                "Số ngày": p["Số ngày"],
                "Lãi suất": p["Lãi suất"],
                "Tiền lãi": p["Tiền lãi"]
            })

    return schedule


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">SỐ TIỀN GỬI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'SMARTSAVE 360 • HỆ THỐNG MÔ PHỎNG TIỀN GỬI TIẾT KIỆM'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# CHỮ CHẠY
# =========================================================

st.markdown("""
<div class="marquee-container">

    <div class="marquee">

        💰 GỬI TIẾT KIỆM THÔNG MINH
        &nbsp;&nbsp; • &nbsp;&nbsp;
        📊 TÍNH LÃI NHANH
        &nbsp;&nbsp; • &nbsp;&nbsp;
        🔄 TỰ ĐỘNG GIA HẠN
        &nbsp;&nbsp; • &nbsp;&nbsp;
        💵 NHẬN LÃI LINH HOẠT
        &nbsp;&nbsp; • &nbsp;&nbsp;
        🧮 LÃI ĐƠN & LÃI KÉP
        &nbsp;&nbsp; • &nbsp;&nbsp;
        🚀 SMARTSAVE 360

    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SMARTSAVE 360
# =========================================================

st.markdown("""
<div class="smart-card">

    <div class="smart-title">
        SMARTSAVE 360
    </div>

    <div class="smart-subtitle">
        GIẢI PHÁP MÔ PHỎNG VÀ TÍNH TOÁN TIỀN GỬI TIẾT KIỆM
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 💰 SMARTSAVE 360")

    st.markdown("---")

    st.markdown("### ⚡ CHỌN NHANH")

    if "quick_term" not in st.session_state:
        st.session_state.quick_term = 3

    col_a, col_b = st.columns(2)

    with col_a:

        if st.button(
            "1 tháng",
            use_container_width=True
        ):
            st.session_state.quick_term = 1

        if st.button(
            "6 tháng",
            use_container_width=True
        ):
            st.session_state.quick_term = 6

    with col_b:

        if st.button(
            "3 tháng",
            use_container_width=True
        ):
            st.session_state.quick_term = 3

        if st.button(
            "12 tháng",
            use_container_width=True
        ):
            st.session_state.quick_term = 12

    st.markdown("---")

    st.markdown("### 📌 QUY TẮC")

    st.write(
        "• Rút trước hạn → lãi suất không kỳ hạn"
    )

    st.write(
        "• Rút đúng hạn → lãi suất có kỳ hạn"
    )

    st.write(
        "• Không rút khi đến hạn → tự động gia hạn"
    )

    st.write(
        "• Kỳ hạn gia hạn = kỳ hạn ban đầu"
    )


# =========================================================
# BẢNG ĐIỀU KHIỂN
# =========================================================

st.markdown(
    '<div class="green-header">BẢNG ĐIỀU KHIỂN</div>',
    unsafe_allow_html=True
)


st.markdown(
    f"""
    <div class="selected-box">

        🟢 ĐANG CHỌN:
        KỲ HẠN {st.session_state.quick_term} THÁNG

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# INPUT
# =========================================================

col1, col2, col3 = st.columns(3)


# =========================================================
# CỘT 1
# =========================================================

with col1:

    st.markdown("### 💰 THÔNG TIN TIỀN GỬI")

    principal = st.number_input(
        "Số tiền khách hàng gửi (VNĐ)",
        min_value=0.0,
        value=500_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    fixed_rate = st.number_input(
        "Lãi suất có kỳ hạn (%/năm)",
        min_value=0.0,
        value=5.0,
        step=0.1
    )

    nonterm_rate = st.number_input(
        "Lãi suất không kỳ hạn (%/năm)",
        min_value=0.0,
        value=0.2,
        step=0.1
    )


# =========================================================
# CỘT 2
# =========================================================

with col2:

    st.markdown("### 📅 THỜI GIAN GỬI")

    deposit_date = st.date_input(
        "Ngày gửi tiền",
        value=date(2026, 8, 23)
    )

    term_options = [1, 3, 6, 12]

    default_index = term_options.index(
        st.session_state.quick_term
    )

    term_months = st.selectbox(
        "Kỳ hạn gửi tiền",
        term_options,
        index=default_index,
        format_func=lambda x: f"{x} tháng"
    )

    default_withdrawal = maturity_date(
        deposit_date,
        term_months
    )

    withdrawal_date = st.date_input(
        "Ngày rút tiền",
        value=default_withdrawal
    )


# =========================================================
# CỘT 3
# =========================================================

with col3:

    st.markdown("### 💵 CÁCH NHẬN LÃI")

    payment_method = st.radio(
        "Chọn phương thức nhận lãi",
        [
            "Nhận lãi trước",
            "Nhận lãi hàng tháng",
            "Nhận lãi cuối kỳ"
        ]
    )

    st.markdown("### 🧮 PHƯƠNG PHÁP TÍNH")

    interest_type = st.radio(
        "Chọn cách tính",
        [
            "Lãi đơn",
            "Lãi kép"
        ],
        horizontal=True
    )


# =========================================================
# THÔNG TIN NGÀY ĐẾN HẠN
# =========================================================

current_maturity = maturity_date(
    deposit_date,
    term_months
)

st.markdown(
    f"""
    <div class="info-card">

        <b>📅 NGÀY ĐẾN HẠN KỲ HIỆN TẠI:</b>
        {current_maturity.strftime("%d/%m/%Y")}

        <br><br>

        <b>⏱ NGUYÊN TẮC TÍNH NGÀY:</b>
        Tính từ ngày gửi đến trước ngày đến hạn
        hoặc trước ngày khách hàng rút tiền.

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# NÚT TÍNH TOÁN
# =========================================================

st.markdown("")

calculate = st.button(
    "🧮  TÍNH TOÁN TIỀN GỬI",
    type="primary",
    use_container_width=True
)


# =========================================================
# KẾT QUẢ
# =========================================================

if calculate:

    # -----------------------------------------------------
    # KIỂM TRA DỮ LIỆU
    # -----------------------------------------------------

    if principal <= 0:

        st.error(
            "❌ Số tiền gửi phải lớn hơn 0."
        )

    elif withdrawal_date <= deposit_date:

        st.error(
            "❌ Ngày rút phải lớn hơn ngày gửi."
        )

    else:

        # -------------------------------------------------
        # TÍNH CÁC KỲ
        # -------------------------------------------------

        periods, total_interest = calculate_periods(
            principal=principal,
            deposit_date=deposit_date,
            withdrawal_date=withdrawal_date,
            term_months=term_months,
            fixed_rate=fixed_rate,
            nonterm_rate=nonterm_rate,
            interest_type=interest_type
        )

        total_received = (
            principal + total_interest
        )

        actual_days = (
            withdrawal_date - deposit_date
        ).days

        # -------------------------------------------------
        # XÁC ĐỊNH TRẠNG THÁI
        # -------------------------------------------------

        if withdrawal_date < current_maturity:

            status = "RÚT TRƯỚC HẠN"

            st.warning(
                "⚠️ KHÁCH HÀNG RÚT TRƯỚC HẠN. "
                "Tiền lãi được tính theo lãi suất không kỳ hạn."
            )

        elif withdrawal_date == current_maturity:

            status = "RÚT ĐÚNG HẠN"

            st.success(
                "✅ KHÁCH HÀNG RÚT ĐÚNG NGÀY ĐẾN HẠN. "
                "Khách hàng được hưởng lãi suất có kỳ hạn."
            )

        else:

            status = "TỰ ĐỘNG GIA HẠN"

            st.info(
                "🔄 KHÁCH HÀNG RÚT SAU HẠN. "
                "Hệ thống đã tự động gia hạn theo đúng kỳ hạn ban đầu."
            )


        # =================================================
        # KẾT QUẢ TÍNH TOÁN
        # =================================================

        st.markdown(
            '<div class="green-header">KẾT QUẢ TÍNH TOÁN</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "💰 TIỀN GỐC",
                format_money(principal)
            )

        with c2:

            st.metric(
                "📅 SỐ NGÀY",
                f"{actual_days} ngày"
            )

        with c3:

            st.metric(
                "💵 TIỀN LÃI",
                format_money(total_interest)
            )

        with c4:

            st.metric(
                "🏦 TỔNG KHÁCH NHẬN",
                format_money(total_received)
            )


        # =================================================
        # TÓM TẮT
        # =================================================

        st.markdown(
            "### 📋 TÓM TẮT GIAO DỊCH"
        )

        left, right = st.columns(2)

        with left:

            st.write(
                f"**Số tiền gửi:** "
                f"{format_money(principal)}"
            )

            st.write(
                f"**Ngày gửi:** "
                f"{deposit_date.strftime('%d/%m/%Y')}"
            )

            st.write(
                f"**Ngày rút:** "
                f"{withdrawal_date.strftime('%d/%m/%Y')}"
            )

            st.write(
                f"**Kỳ hạn:** "
                f"{term_months} tháng"
            )

            st.write(
                f"**Trạng thái:** {status}"
            )

        with right:

            st.write(
                f"**Lãi suất có kỳ hạn:** "
                f"{fixed_rate:.2f}%/năm"
            )

            st.write(
                f"**Lãi suất không kỳ hạn:** "
                f"{nonterm_rate:.2f}%/năm"
            )

            st.write(
                f"**Cách nhận lãi:** "
                f"{payment_method}"
            )

            st.write(
                f"**Phương pháp:** "
                f"{interest_type}"
            )

            st.write(
                f"**Ngày đến hạn:** "
                f"{current_maturity.strftime('%d/%m/%Y')}"
            )


        # =================================================
        # CHI TIẾT KỲ TÍNH LÃI
        # =================================================

        st.markdown(
            '<div class="green-header">'
            '📊 CHI TIẾT CÁC KỲ TÍNH LÃI'
            '</div>',
            unsafe_allow_html=True
        )

        df_periods = pd.DataFrame(periods)

        if not df_periods.empty:

            df_periods["Từ ngày"] = (
                pd.to_datetime(
                    df_periods["Từ ngày"]
                ).dt.strftime("%d/%m/%Y")
            )

            df_periods["Đến ngày"] = (
                pd.to_datetime(
                    df_periods["Đến ngày"]
                ).dt.strftime("%d/%m/%Y")
            )

            df_periods["Lãi suất"] = (
                df_periods["Lãi suất"]
                .apply(
                    lambda x:
                    f"{x:.2f}%/năm"
                )
            )

            df_periods["Tiền lãi"] = (
                df_periods["Tiền lãi"]
                .apply(format_money)
            )

            st.dataframe(
                df_periods,
                use_container_width=True,
                hide_index=True
            )


        # =================================================
        # LỊCH NHẬN LÃI
        # =================================================

        st.markdown(
            '<div class="green-header">'
            '💵 LỊCH NHẬN TIỀN LÃI'
            '</div>',
            unsafe_allow_html=True
        )

        schedule = interest_schedule(
            principal=principal,
            deposit_date=deposit_date,
            withdrawal_date=withdrawal_date,
            term_months=term_months,
            fixed_rate=fixed_rate,
            nonterm_rate=nonterm_rate,
            interest_type=interest_type,
            payment_method=payment_method
        )

        df_schedule = pd.DataFrame(schedule)

        if not df_schedule.empty:

            df_schedule["Ngày nhận"] = (
                pd.to_datetime(
                    df_schedule["Ngày nhận"]
                ).dt.strftime("%d/%m/%Y")
            )

            df_schedule["Lãi suất"] = (
                df_schedule["Lãi suất"]
                .apply(
                    lambda x:
                    f"{x:.2f}%/năm"
                )
            )

            df_schedule["Tiền lãi"] = (
                df_schedule["Tiền lãi"]
                .apply(format_money)
            )

            st.dataframe(
                df_schedule,
                use_container_width=True,
                hide_index=True
            )


        # =================================================
        # CÔNG THỨC
        # =================================================

        st.markdown(
            '<div class="green-header">'
            '🧮 CÔNG THỨC TÍNH'
            '</div>',
            unsafe_allow_html=True
        )

        if interest_type == "Lãi đơn":

            st.markdown("""
### Lãi đơn

**Tiền lãi = Tiền gốc × Lãi suất × Số ngày / 365**

Trong đó:

- Tiền gốc = số tiền khách hàng gửi
- Lãi suất = lãi suất năm
- Số ngày = số ngày thực tế tính lãi
            """)

        else:

            st.markdown("""
### Lãi kép

**FV = P × (1 + r/365)^n**

**Tiền lãi = FV - P**

Trong đó:

- P = tiền gốc
- r = lãi suất năm
- n = số ngày
- FV = giá trị nhận được sau khi ghép lãi
            """)


        # =================================================
        # QUY TẮC HOẠT ĐỘNG
        # =================================================

        with st.expander(
            "📚 XEM QUY TẮC XỬ LÝ CỦA SMARTSAVE 360"
        ):

            st.markdown("""
### 1. Rút trước hạn

Nếu khách hàng rút trước ngày đến hạn,
hệ thống tính tiền lãi theo **lãi suất không kỳ hạn**.

### 2. Rút đúng hạn

Nếu khách hàng rút đúng ngày đến hạn,
khách hàng được hưởng **lãi suất có kỳ hạn**.

### 3. Rút sau hạn

Nếu khách hàng không rút khi đến hạn,
khoản tiền gửi được **tự động gia hạn bằng đúng kỳ hạn ban đầu**.

### 4. Nhận lãi trước

Tiền lãi được xác định và chi trả trước kỳ hạn.

### 5. Nhận lãi hàng tháng

Tiền lãi được tính và chi trả theo từng tháng.

### 6. Nhận lãi cuối kỳ

Tiền lãi được nhận khi kết thúc kỳ hạn.
            """)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

    <b>SMARTSAVE 360</b>
    <br><br>

    Ứng dụng mô phỏng tính tiền gửi tiết kiệm
    <br>

    Phục vụ mục đích học tập và trình bày dự án

</div>
""", unsafe_allow_html=True)
