import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
import math

# ============================================================
# CẤU HÌNH TRANG
# ============================================================

st.set_page_config(
    page_title="SMARTSAVE 360",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS - GIAO DIỆN
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Be Vietnam Pro', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(220,0,0,0.08), transparent 30%),
        radial-gradient(circle at bottom right, rgba(0,0,0,0.06), transparent 30%),
        #f7f7f7;
}

/* Header */

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #c8102e;
    margin-top: 5px;
    margin-bottom: 0px;
}

.subtitle {
    text-align: center;
    color: #555;
    font-size: 15px;
    margin-bottom: 20px;
}

/* Chữ chạy */

.marquee-box {
    width: 100%;
    overflow: hidden;
    background: #111111;
    color: white;
    padding: 9px 0;
    border-radius: 10px;
    margin-bottom: 22px;
}

.marquee-text {
    display: inline-block;
    white-space: nowrap;
    padding-left: 100%;
    animation: marquee 18s linear infinite;
    font-weight: 600;
    letter-spacing: 1px;
}

@keyframes marquee {
    0% {
        transform: translateX(0);
    }
    100% {
        transform: translateX(-100%);
    }
}

/* SMARTSAVE */

.smart-box {
    background: linear-gradient(135deg, #111111, #292929);
    color: white;
    padding: 22px;
    border-radius: 18px;
    margin-bottom: 20px;
    border-left: 7px solid #c8102e;
    box-shadow: 0 7px 20px rgba(0,0,0,0.12);
}

.smart-title {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: 3px;
}

.smart-content {
    margin-top: 5px;
    font-size: 14px;
    color: #dddddd;
}

/* Section */

.section-title {
    background: #c8102e;
    color: white;
    padding: 12px 18px;
    border-radius: 10px;
    font-size: 19px;
    font-weight: 700;
    margin-top: 12px;
    margin-bottom: 15px;
}

/* Điều khiển */

.control-box {
    background: #c8102e;
    color: white;
    padding: 13px 18px;
    border-radius: 10px;
    font-size: 19px;
    font-weight: 700;
    margin-bottom: 15px;
}

/* Đang chọn */

.selected-box {
    background: white;
    border: 2px solid #c8102e;
    border-radius: 12px;
    padding: 14px 18px;
    margin: 10px 0 18px 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.07);
}

.selected-label {
    color: #777;
    font-size: 13px;
}

.selected-value {
    color: #c8102e;
    font-size: 21px;
    font-weight: 800;
}

/* Input */

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    border-radius: 9px !important;
}

/* Button */

.stButton > button {
    width: 100%;
    background: #c8102e;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 20px;
    font-weight: 700;
    font-size: 16px;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #a90020;
    transform: translateY(-1px);
}

/* Kết quả */

.result-card {
    background: white;
    border-radius: 16px;
    padding: 22px;
    margin: 8px 0;
    border-top: 5px solid #c8102e;
    box-shadow: 0 5px 18px rgba(0,0,0,0.08);
}

.result-label {
    color: #777;
    font-size: 13px;
    font-weight: 600;
}

.result-value {
    color: #111;
    font-size: 25px;
    font-weight: 800;
    margin-top: 5px;
}

.total-card {
    background: linear-gradient(135deg, #c8102e, #e51c3b);
    color: white;
    border-radius: 18px;
    padding: 28px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(200,16,46,0.25);
    margin-top: 18px;
}

.total-label {
    font-size: 15px;
    opacity: 0.9;
}

.total-value {
    font-size: 38px;
    font-weight: 800;
    margin-top: 5px;
}

/* Formula */

.formula-box {
    background: #111;
    color: #fff;
    border-radius: 12px;
    padding: 18px;
    margin-top: 15px;
    line-height: 1.8;
}

.formula-title {
    color: #ffccd4;
    font-weight: 800;
    font-size: 18px;
}

/* Status */

.status-normal {
    background: #e9f8ef;
    color: #18743b;
    padding: 12px 15px;
    border-radius: 10px;
    font-weight: 700;
}

.status-warning {
    background: #fff4df;
    color: #9a6100;
    padding: 12px 15px;
    border-radius: 10px;
    font-weight: 700;
}

.status-danger {
    background: #ffe8eb;
    color: #b00020;
    padding: 12px 15px;
    border-radius: 10px;
    font-weight: 700;
}

/* Footer */

.footer {
    text-align: center;
    color: #777;
    margin-top: 35px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HÀM XỬ LÝ
# ============================================================

def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


def maturity_date(deposit_date, months):
    return deposit_date + relativedelta(months=months)


def calculate_days(start_date, end_date):
    """
    Tính số ngày từ ngày gửi đến trước ngày kết thúc.
    Ví dụ:
    23/08 -> 23/11
    số ngày tính lãi = 92 ngày
    """
    return (end_date - start_date).days


def simple_interest(principal, annual_rate, days):
    return principal * annual_rate / 100 * days / 365


def compound_interest(principal, annual_rate, days):
    """
    Lãi kép theo ngày.
    """
    daily_rate = annual_rate / 100 / 365
    return principal * ((1 + daily_rate) ** days - 1)


def monthly_compound_interest(principal, annual_rate, months):
    """
    Lãi kép theo kỳ tháng.
    """
    monthly_rate = annual_rate / 100 / 12
    return principal * ((1 + monthly_rate) ** months - 1)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">SMARTSAVE 360</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">CÔNG CỤ TÍNH LÃI TIỀN GỬI TIẾT KIỆM</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="marquee-box">
    <div class="marquee-text">
        ✦ SMARTSAVE 360  •  TÍNH LÃI NHANH  •  MINH BẠCH  •  CHÍNH XÁC  •  LÃI ĐƠN  •  LÃI KÉP  •  3 PHƯƠNG THỨC NHẬN LÃI
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SMARTSAVE 360
# ============================================================

st.markdown("""
<div class="smart-box">
    <div class="smart-title">SMARTSAVE 360</div>
    <div class="smart-content">
        Công cụ mô phỏng tiền gửi tiết kiệm và tính toán tiền lãi theo thời gian.
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR - BẢNG ĐIỀU KHIỂN
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="control-box">BẢNG ĐIỀU KHIỂN</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="selected-box">'
        '<div class="selected-label">Đang chọn</div>'
        '<div class="selected-value">SMARTSAVE 360</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("### Chọn nhanh")

    quick_choice = st.radio(
        "Phương thức tính",
        [
            "Lãi đơn",
            "Lãi kép"
        ],
        index=0
    )

    st.markdown("---")

    quick_term = st.selectbox(
        "Kỳ hạn nhanh",
        [1, 2, 3, 6, 9, 12, 18, 24, 36],
        index=2
    )

    quick_method = st.selectbox(
        "Cách nhận lãi",
        [
            "Nhận lãi trước",
            "Nhận lãi hàng kỳ",
            "Nhận lãi cuối kỳ"
        ],
        index=2
    )


# ============================================================
# THÔNG TIN TIỀN GỬI
# ============================================================

st.markdown(
    '<div class="section-title">Số tiền gửi</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    principal = st.number_input(
        "Số tiền khách hàng gửi (VNĐ)",
        min_value=0,
        value=500_000_000,
        step=1_000_000,
        format="%d"
    )

    fixed_rate = st.number_input(
        "Lãi suất có kỳ hạn (%/năm)",
        min_value=0.0,
        value=5.0,
        step=0.1,
        format="%.2f"
    )

    non_term_rate = st.number_input(
        "Lãi suất không kỳ hạn (%/năm)",
        min_value=0.0,
        value=0.2,
        step=0.1,
        format="%.2f"
    )

with col2:

    deposit_date = st.date_input(
        "Ngày gửi tiền",
        value=date(2026, 8, 23),
        format="DD/MM/YYYY"
    )

    withdrawal_date = st.date_input(
        "Ngày rút tiền",
        value=date(2026, 11, 23),
        format="DD/MM/YYYY"
    )

    term_months = st.selectbox(
        "Kỳ hạn gửi tiền",
        [1, 2, 3, 6, 9, 12, 18, 24, 36],
        index=2
    )


# ============================================================
# PHƯƠNG THỨC NHẬN LÃI
# ============================================================

st.markdown(
    '<div class="section-title">Phương thức nhận tiền lãi</div>',
    unsafe_allow_html=True
)

interest_method = st.radio(
    "Khách hàng lựa chọn",
    [
        "Nhận lãi trước",
        "Nhận lãi hàng kỳ",
        "Nhận lãi cuối kỳ"
    ],
    horizontal=True,
    index=2
)


# ============================================================
# PHƯƠNG PHÁP TÍNH
# ============================================================

st.markdown(
    '<div class="section-title">Phương pháp tính lãi</div>',
    unsafe_allow_html=True
)

calc_method = st.radio(
    "Chọn phương pháp",
    [
        "Lãi đơn",
        "Lãi kép"
    ],
    horizontal=True,
    index=0
)


# ============================================================
# TÍNH NGÀY ĐẾN HẠN
# ============================================================

maturity = maturity_date(deposit_date, term_months)


# ============================================================
# NÚT TÍNH
# ============================================================

st.markdown("")

calculate = st.button(
    "TÍNH TOÁN TIỀN LÃI",
    type="primary"
)


# ============================================================
# TÍNH TOÁN
# ============================================================

if calculate:

    if principal <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")

    elif withdrawal_date < deposit_date:
        st.error("Ngày rút tiền không được trước ngày gửi tiền.")

    else:

        # ----------------------------------------------------
        # TRƯỜNG HỢP 1: RÚT TRƯỚC HẠN
        # ----------------------------------------------------

        if withdrawal_date < maturity:

            status = "RÚT TRƯỚC HẠN"

            interest_days = calculate_days(
                deposit_date,
                withdrawal_date
            )

            if interest_days < 0:
                interest_days = 0

            rate_used = non_term_rate

            if calc_method == "Lãi đơn":

                interest = simple_interest(
                    principal,
                    rate_used,
                    interest_days
                )

            else:

                interest = compound_interest(
                    principal,
                    rate_used,
                    interest_days
                )

            total = principal + interest

            st.markdown(
                f'<div class="status-danger">⚠️ {status} — áp dụng lãi suất không kỳ hạn {non_term_rate:.2f}%/năm</div>',
                unsafe_allow_html=True
            )

            # ------------------------------------------------
            # KẾT QUẢ
            # ------------------------------------------------

            st.markdown(
                '<div class="section-title">Kết quả tính toán</div>',
                unsafe_allow_html=True
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-label">TIỀN GỐC</div>
                        <div class="result-value">{format_money(principal)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c2:
                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-label">TIỀN LÃI</div>
                        <div class="result-value">{format_money(interest)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c3:
                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-label">SỐ NGÀY GỬI</div>
                        <div class="result-value">{interest_days} ngày</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown(
                f"""
                <div class="total-card">
                    <div class="total-label">TỔNG SỐ TIỀN KHÁCH HÀNG NHẬN</div>
                    <div class="total-value">{format_money(total)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # ------------------------------------------------
            # CÁCH TÍNH
            # ------------------------------------------------

            st.markdown(
                f"""
                <div class="formula-box">
                    <div class="formula-title">
                        CÁCH TÍNH LÃI KHÔNG KỲ HẠN
                    </div>
                    <br>
                    Lãi suất áp dụng = {non_term_rate:.2f}%/năm
                    <br>
                    Số ngày thực tế = {interest_days} ngày
                    <br><br>
                    <b>Lãi đơn:</b>
                    <br>
                    Tiền lãi = Tiền gốc × Lãi suất × Số ngày / 365
                    <br>
                    = {format_money(principal)} × {non_term_rate:.2f}% × {interest_days} / 365
                    <br>
                    = <b>{format_money(interest)}</b>
                    <br><br>
                    Tổng tiền nhận = Tiền gốc + Tiền lãi
                    <br>
                    = <b>{format_money(total)}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

            if calc_method == "Lãi kép":

                st.info(
                    "Bạn đang chọn lãi kép. Trong trường hợp rút trước hạn, "
                    "mô hình mô phỏng áp dụng lãi suất không kỳ hạn và ghép lãi theo ngày."
                )


        # ----------------------------------------------------
        # TRƯỜNG HỢP 2: RÚT ĐÚNG HẠN
        # ----------------------------------------------------

        elif withdrawal_date == maturity:

            status = "RÚT ĐÚNG HẠN"

            interest_days = calculate_days(
                deposit_date,
                maturity
            )

            rate_used = fixed_rate

            if calc_method == "Lãi đơn":

                interest = simple_interest(
                    principal,
                    rate_used,
                    interest_days
                )

            else:

                interest = monthly_compound_interest(
                    principal,
                    rate_used,
                    term_months
                )

            total = principal + interest

            st.markdown(
                f'<div class="status-normal">✓ {status} — áp dụng lãi suất có kỳ hạn {fixed_rate:.2f}%/năm</div>',
                unsafe_allow_html=True
            )

            # ------------------------------------------------
            # KẾT QUẢ
            # ------------------------------------------------

            st.markdown(
                '<div class="section-title">Kết quả tính toán</div>',
                unsafe_allow_html=True
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-label">TIỀN GỐC</div>
                        <div class="result-value">{format_money(principal)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c2:

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-label">TIỀN LÃI</div>
                        <div class="result-value">{format_money(interest)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c3:

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-label">SỐ NGÀY GỬI</div>
                        <div class="result-value">{interest_days} ngày</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # ------------------------------------------------
            # XỬ LÝ 3 PHƯƠNG THỨC
            # ------------------------------------------------

            if interest_method == "Nhận lãi trước":

                receive_now = interest
                maturity_principal = principal

                st.markdown(
                    f"""
                    <div class="total-card">
                        <div class="total-label">TIỀN LÃI NHẬN TRƯỚC</div>
                        <div class="total-value">{format_money(receive_now)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.info(
                    f"Khách hàng nhận tiền lãi trước: {format_money(receive_now)}. "
                    f"Tiền gốc khi đáo hạn: {format_money(maturity_principal)}."
                )

            elif interest_method == "Nhận lãi hàng kỳ":

                periods = term_months

                monthly_interest = interest / periods

                st.markdown(
                    f"""
                    <div class="total-card">
                        <div class="total-label">LÃI NHẬN MỖI KỲ</div>
                        <div class="total-value">{format_money(monthly_interest)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.info(
                    f"Tổng tiền lãi trong toàn bộ kỳ hạn: {format_money(interest)}."
                )

            else:

                st.markdown(
                    f"""
                    <div class="total-card">
                        <div class="total-label">TỔNG TIỀN NHẬN KHI ĐẾN HẠN</div>
                        <div class="total-value">{format_money(total)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # ------------------------------------------------
            # CÁCH TÍNH
            # ------------------------------------------------

            if calc_method == "Lãi đơn":

                st.markdown(
                    f"""
                    <div class="formula-box">
                        <div class="formula-title">
                            CÁCH TÍNH LÃI CÓ KỲ HẠN — LÃI ĐƠN
                        </div>
                        <br>
                        Ngày gửi: {deposit_date.strftime("%d/%m/%Y")}
                        <br>
                        Ngày đến hạn: {maturity.strftime("%d/%m/%Y")}
                        <br>
                        Số ngày tính lãi: {interest_days} ngày
                        <br>
                        Lãi suất: {fixed_rate:.2f}%/năm
                        <br><br>
                        Tiền lãi =
                        Tiền gốc × Lãi suất × Số ngày / 365
                        <br><br>
                        = {format_money(principal)}
                        × {fixed_rate:.2f}%
                        × {interest_days}
                        / 365
                        <br><br>
                        = <b>{format_money(interest)}</b>
                        <br><br>
                        Tổng tiền =
                        {format_money(principal)}
                        + {format_money(interest)}
                        = <b>{format_money(total)}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class="formula-box">
                        <div class="formula-title">
                            CÁCH TÍNH LÃI CÓ KỲ HẠN — LÃI KÉP
                        </div>
                        <br>
                        Tiền gốc ban đầu: {format_money(principal)}
                        <br>
                        Lãi suất năm: {fixed_rate:.2f}%
                        <br>
                        Kỳ hạn: {term_months} tháng
                        <br><br>
                        Công thức:
                        <br>
                        FV = PV × (1 + r/12)^n
                        <br><br>
                        Trong đó:
                        <br>
                        PV = {format_money(principal)}
                        <br>
                        r = {fixed_rate:.2f}%/năm
                        <br>
                        n = {term_months} kỳ tháng
                        <br><br>
                        Tiền lãi =
                        FV − PV
                        <br>
                        = <b>{format_money(interest)}</b>
                        <br><br>
                        Tổng tiền nhận =
                        <b>{format_money(total)}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


        # ----------------------------------------------------
        # TRƯỜNG HỢP 3: RÚT SAU HẠN
        # ----------------------------------------------------

        else:

            status = "RÚT SAU HẠN"

            # Số kỳ hạn hoàn thành
            completed_terms = 0
            current_start = deposit_date

            while True:

                next_maturity = maturity_date(
                    current_start,
                    term_months
                )

                if next_maturity <= withdrawal_date:
                    completed_terms += 1
                    current_start = next_maturity
                else:
                    break

            # Ngày bắt đầu kỳ đang chạy
            current_period_start = current_start

            # Ngày đáo hạn của kỳ hiện tại
            current_period_end = maturity_date(
                current_period_start,
                term_months
            )

            # Nếu rút đúng ngày đáo hạn cuối thì không vào đây
            completed_days = calculate_days(
                deposit_date,
                current_period_start
            )

            remaining_days = calculate_days(
                current_period_start,
                withdrawal_date
            )

            # ------------------------------------------------
            # TÍNH LÃI CÁC KỲ ĐÃ GIA HẠN
            # ------------------------------------------------

            if calc_method == "Lãi đơn":

                completed_interest = simple_interest(
                    principal,
                    fixed_rate,
                    completed_days
                )

            else:

                completed_interest = (
                    principal *
                    (
                        (1 + fixed_rate / 100 / 12) ** completed_terms
                        - 1
                    )
                )

            principal_after_renewal = principal + completed_interest

            # ------------------------------------------------
            # LÃI KỲ ĐANG CHẠY
            # ------------------------------------------------

            extension_interest = simple_interest(
                principal_after_renewal,
                non_term_rate,
                remaining_days
            )

            total_interest = (
                completed_interest +
                extension_interest
            )

            total = principal + total_interest

            st.markdown(
                f'<div class="status-warning">↻ {status} — sổ tiết kiệm đã tự động gia hạn {completed_terms} kỳ, kỳ đang chạy áp dụng xử lý theo lãi suất không kỳ hạn cho phần thời gian dư</div>',
                unsafe_allow_html=True
            )

            # ------------------------------------------------
            # KẾT QUẢ
            # ------------------------------------------------

            st.markdown(
                '<div class="section-title">Kết quả tính toán</div>',
                unsafe_allow_html=True
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-label">SỐ KỲ ĐÃ GIA HẠN</div>
                        <div class="result-value">{completed_terms} kỳ</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c2:

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-label">LÃI CÁC KỲ ĐÃ HOÀN THÀNH</div>
                        <div class="result-value">{format_money(completed_interest)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c3:

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-label">LÃI PHẦN DƯ</div>
                        <div class="result-value">{format_money(extension_interest)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown(
                f"""
                <div class="total-card">
                    <div class="total-label">TỔNG SỐ TIỀN KHÁCH HÀNG NHẬN</div>
                    <div class="total-value">{format_money(total)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # ------------------------------------------------
            # GIẢI THÍCH
            # ------------------------------------------------

            st.markdown(
                f"""
                <div class="formula-box">
                    <div class="formula-title">
                        CHI TIẾT CÁCH TÍNH KHI RÚT SAU HẠN
                    </div>
                    <br>
                    Kỳ hạn ban đầu:
                    <b>{term_months} tháng</b>
                    <br>
                    Số kỳ đã hoàn thành:
                    <b>{completed_terms} kỳ</b>
                    <br>
                    Ngày bắt đầu kỳ hiện tại:
                    <b>{current_period_start.strftime("%d/%m/%Y")}</b>
                    <br>
                    Ngày khách hàng rút:
                    <b>{withdrawal_date.strftime("%d/%m/%Y")}</b>
                    <br>
                    Số ngày của phần dư:
                    <b>{remaining_days} ngày</b>
                    <br><br>

                    <b>Bước 1 — Tính lãi các kỳ đã hoàn thành:</b>
                    <br>
                    Lãi các kỳ = <b>{format_money(completed_interest)}</b>
                    <br><br>

                    <b>Bước 2 — Tính lãi phần thời gian dư:</b>
                    <br>
                    Tiền gốc sau các kỳ gia hạn =
                    {format_money(principal_after_renewal)}
                    <br>
                    Lãi suất áp dụng =
                    {non_term_rate:.2f}%/năm
                    <br>
                    Số ngày =
                    {remaining_days} ngày
                    <br><br>

                    Lãi phần dư =
                    Gốc × Lãi suất × Số ngày / 365
                    <br>
                    =
                    {format_money(principal_after_renewal)}
                    × {non_term_rate:.2f}%
                    × {remaining_days}
                    / 365
                    <br>
                    =
                    <b>{format_money(extension_interest)}</b>

                    <br><br>

                    <b>Tổng tiền lãi:</b>
                    <br>
                    {format_money(completed_interest)}
                    +
                    {format_money(extension_interest)}
                    =
                    <b>{format_money(total_interest)}</b>

                    <br><br>

                    <b>Tổng tiền khách hàng nhận:</b>
                    <br>
                    Gốc + Tổng lãi =
                    <b>{format_money(total)}</b>
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# GHI CHÚ
# ============================================================

st.markdown("---")

st.markdown("""
### Lưu ý về mô hình tính

- **Rút trước hạn:** sử dụng lãi suất không kỳ hạn.
- **Rút đúng hạn:** sử dụng lãi suất có kỳ hạn.
- **Rút sau hạn:** hệ thống xác định số kỳ đã hoàn thành và mô phỏng việc tự động gia hạn.
- Ngày tính lãi bắt đầu từ **ngày gửi** và kết thúc **trước ngày rút/đáo hạn**.
- **Lãi đơn:** tiền lãi được tính trên số tiền gốc ban đầu.
- **Lãi kép:** tiền lãi được nhập vào vốn để tiếp tục tính lãi.
- Các công thức trên là **mô hình mô phỏng phục vụ học tập/tham khảo**; quy định thực tế của từng ngân hàng về ngày tính lãi, phương pháp ghép lãi, tất toán trước hạn và tự động tái tục có thể khác.
""")

st.markdown(
    '<div class="footer">SMARTSAVE 360 • Công cụ mô phỏng tính lãi tiền gửi tiết kiệm</div>',
    unsafe_allow_html=True
)
