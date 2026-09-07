import streamlit as st
from datetime import date
from calendar import monthrange
import pandas as pd
from pathlib import Path
import math

# ============================================================
# CẤU HÌNH
# ============================================================

st.set_page_config(
    page_title="Số tiền gửi | SMARTSAVE 360",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS - GIAO DIỆN
# ============================================================

st.markdown("""
<style>

    /* =========================
       NỀN CHUNG
       ========================= */
    .stApp {
        background:
            radial-gradient(circle at top right,
                rgba(255, 0, 0, 0.06),
                transparent 30%),
            linear-gradient(
                135deg,
                #ffffff 0%,
                #fffafa 45%,
                #f7f7f7 100%
            );
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* =========================
       TIÊU ĐỀ
       ========================= */

    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        color: #d71920;
        letter-spacing: 2px;
        margin-top: 10px;
        margin-bottom: 3px;
    }

    .main-subtitle {
        text-align: center;
        color: #555555;
        font-size: 16px;
        margin-bottom: 20px;
    }

    /* =========================
       CHỮ CHẠY
       ========================= */

    .marquee-wrapper {
        width: 100%;
        overflow: hidden;
        background: #d71920;
        border-radius: 10px;
        padding: 10px 0;
        margin-bottom: 25px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.12);
    }

    .marquee {
        display: inline-block;
        white-space: nowrap;
        color: white;
        font-size: 15px;
        font-weight: 700;
        animation: marquee 20s linear infinite;
    }

    @keyframes marquee {
        0% {
            transform: translateX(100%);
        }

        100% {
            transform: translateX(-100%);
        }
    }

    /* =========================
       BẢNG ĐIỀU KHIỂN
       ========================= */

    .control-title {
        background: linear-gradient(
            90deg,
            #c8102e,
            #e21d2d
        );

        color: white;
        font-size: 20px;
        font-weight: 800;

        padding: 13px 20px;

        border-radius: 10px;

        margin-bottom: 15px;

        box-shadow:
            0 5px 14px
            rgba(215,25,32,0.20);
    }

    /* =========================
       SMARTSAVE
       ========================= */

    .smart-card {
        background: white;

        border: 2px solid #d71920;

        border-radius: 20px;

        padding: 25px;

        margin-bottom: 20px;

        box-shadow:
            0 8px 25px
            rgba(0,0,0,0.07);

        position: relative;
        overflow: hidden;
    }

    .smart-card:before {
        content: "";

        position: absolute;

        left: 0;
        top: 0;

        width: 7px;
        height: 100%;

        background: #d71920;
    }

    .smart-logo {
        text-align: center;

        font-size: 32px;

        font-weight: 900;

        color: #111111;

        letter-spacing: 3px;
    }

    .smart-logo span {
        color: #d71920;
    }

    .smart-description {
        text-align: center;

        color: #666666;

        margin-top: 5px;

        font-size: 14px;
    }

    /* =========================
       ĐANG CHỌN
       ========================= */

    .selected-box {

        background: linear-gradient(
            90deg,
            #fff0f1,
            #ffffff
        );

        border-left: 6px solid #d71920;

        padding: 14px 18px;

        border-radius: 10px;

        margin: 15px 0;

        color: #333333;

        font-size: 15px;

        box-shadow:
            0 3px 10px
            rgba(0,0,0,0.05);
    }

    .selected-title {
        color: #d71920;
        font-weight: 900;
        font-size: 17px;
    }

    /* =========================
       CARD KẾT QUẢ
       ========================= */

    .result-card {

        background: white;

        border-radius: 15px;

        padding: 20px;

        text-align: center;

        border: 1px solid #eeeeee;

        min-height: 135px;

        box-shadow:
            0 6px 18px
            rgba(0,0,0,0.07);
    }

    .result-card-main {

        background:
            linear-gradient(
                135deg,
                #fff0f1,
                #ffffff
            );

        border: 2px solid #d71920;
    }

    .result-label {

        color: #666666;

        font-size: 14px;

        margin-bottom: 10px;
    }

    .result-value {

        color: #d71920;

        font-size: 25px;

        font-weight: 900;
    }

    /* =========================
       SECTION
       ========================= */

    .section-title {

        font-size: 22px;

        font-weight: 800;

        color: #222222;

        margin-top: 20px;

        margin-bottom: 12px;

        border-left: 5px solid #d71920;

        padding-left: 12px;
    }

    /* =========================
       CÔNG THỨC
       ========================= */

    .formula {

        background: #fafafa;

        border: 1px dashed #d71920;

        border-radius: 12px;

        padding: 16px;

        margin-top: 15px;

        color: #333333;
    }

    /* =========================
       THÀNH VIÊN
       ========================= */

    .member-card {

        background: white;

        border-radius: 15px;

        padding: 15px;

        text-align: center;

        border: 1px solid #eeeeee;

        box-shadow:
            0 5px 15px
            rgba(0,0,0,0.06);
    }

    .member-name {

        font-weight: 800;

        color: #222222;

        margin-top: 8px;
    }

    .member-role {

        color: #777777;

        font-size: 13px;
    }

    /* =========================
       FOOTER
       ========================= */

    .footer {

        text-align: center;

        padding: 25px 0 10px;

        color: #777777;

        font-size: 13px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# HÀM
# ============================================================

def add_months(d, months):
    """
    Cộng thêm số tháng vào ngày.
    Ví dụ:
    23/08/2026 + 3 tháng = 23/11/2026
    """

    month = d.month - 1 + months

    year = d.year + month // 12

    month = month % 12 + 1

    day = min(
        d.day,
        monthrange(year, month)[1]
    )

    return date(year, month, day)


def simple_interest(principal, rate, days):
    """
    Lãi đơn:
    I = P × r × n / 365
    """

    return (
        principal
        * rate / 100
        * days / 365
    )


def compound_interest(principal, rate, days):
    """
    Lãi kép theo ngày:

    A = P × (1 + r/365)^n

    I = A - P
    """

    if days <= 0:
        return 0

    amount = (
        principal
        * (
            1 + rate / 100 / 365
        ) ** days
    )

    return amount - principal


def calculate_interest(
    principal,
    rate,
    days,
    interest_type
):

    if interest_type == "Lãi đơn":
        return simple_interest(
            principal,
            rate,
            days
        )

    return compound_interest(
        principal,
        rate,
        days
    )


def money(value):
    return f"{value:,.0f} VNĐ"


def fmt_date(d):
    return d.strftime("%d/%m/%Y")


# ============================================================
# SESSION STATE
# ============================================================

if "term" not in st.session_state:
    st.session_state.term = 3

if "method" not in st.session_state:
    st.session_state.method = "Nhận lãi cuối kỳ"

if "interest_type" not in st.session_state:
    st.session_state.interest_type = "Lãi đơn"


# ============================================================
# TIÊU ĐỀ
# ============================================================

st.markdown(
    '<div class="main-title">SỐ TIỀN GỬI</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-subtitle">
        Công cụ mô phỏng tiền gửi tiết kiệm thông minh
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CHỮ CHẠY
# ============================================================

st.markdown(
    """
    <div class="marquee-wrapper">

        <div class="marquee">

            💰 SMARTSAVE 360
            &nbsp;&nbsp; • &nbsp;&nbsp;

            TÍNH LÃI NHANH CHÓNG
            &nbsp;&nbsp; • &nbsp;&nbsp;

            LÃI ĐƠN
            &nbsp;&nbsp; • &nbsp;&nbsp;

            LÃI KÉP
            &nbsp;&nbsp; • &nbsp;&nbsp;

            NHẬN LÃI TRƯỚC
            &nbsp;&nbsp; • &nbsp;&nbsp;

            NHẬN LÃI HÀNG KỲ
            &nbsp;&nbsp; • &nbsp;&nbsp;

            NHẬN LÃI CUỐI KỲ
            &nbsp;&nbsp; • &nbsp;&nbsp;

            TỰ ĐỘNG GIA HẠN
            &nbsp;&nbsp; • &nbsp;&nbsp;

            RÚT TRƯỚC HẠN
            &nbsp;&nbsp; • &nbsp;&nbsp;

            QUẢN LÝ TIỀN GỬI THÔNG MINH
            💰

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SMARTSAVE 360
# ============================================================

st.markdown(
    """
    <div class="smart-card">

        <div class="smart-logo">
            <span>SMART</span>SAVE 360
        </div>

        <div class="smart-description">
            Hệ thống mô phỏng tính tiền gốc và lãi
            tiền gửi tiết kiệm
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# BẢNG ĐIỀU KHIỂN
# ============================================================

st.markdown(
    '<div class="control-title">BẢNG ĐIỀU KHIỂN</div>',
    unsafe_allow_html=True
)


# ============================================================
# ĐANG CHỌN
# ============================================================

st.markdown(
    f"""
    <div class="selected-box">

        <div class="selected-title">
            🟢 Đang chọn
        </div>

        <br>

        📅 Kỳ hạn:
        <b>{st.session_state.term} tháng</b>

        &nbsp;&nbsp; | &nbsp;&nbsp;

        💵 Phương thức:
        <b>{st.session_state.method}</b>

        &nbsp;&nbsp; | &nbsp;&nbsp;

        📈 Cách tính:
        <b>{st.session_state.interest_type}</b>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CHỌN NHANH
# ============================================================

st.markdown(
    '<div class="section-title">⚡ Chọn nhanh</div>',
    unsafe_allow_html=True
)

quick_cols = st.columns(4)

for col, term in zip(
    quick_cols,
    [1, 3, 6, 12]
):

    with col:

        if st.button(
            f"📅 {term} tháng",
            use_container_width=True,
            key=f"term_{term}"
        ):

            st.session_state.term = term

            st.rerun()


# ============================================================
# THÔNG TIN TIỀN GỬI
# ============================================================

st.markdown(
    '<div class="section-title">💰 Thông tin tiền gửi</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)


with left:

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
        step=0.1,
        format="%.2f"
    )

    nonterm_rate = st.number_input(
        "Lãi suất không kỳ hạn (%/năm)",
        min_value=0.0,
        value=0.2,
        step=0.1,
        format="%.2f"
    )


with right:

    deposit_date = st.date_input(
        "Ngày gửi tiền",
        value=date.today()
    )

    # Ngày mặc định theo kỳ hạn đang chọn
    default_withdrawal = add_months(
        deposit_date,
        st.session_state.term
    )

    withdrawal_date = st.date_input(
        "Ngày khách hàng rút tiền",
        value=default_withdrawal
    )

    term_options = [
        1, 3, 6, 9, 12, 18, 24, 36
    ]

    st.session_state.term = st.selectbox(
        "Kỳ hạn gửi tiền",
        options=term_options,

        index=term_options.index(
            st.session_state.term
        ),

        format_func=lambda x:
            f"{x} tháng"
    )


# ============================================================
# PHƯƠNG THỨC NHẬN LÃI
# ============================================================

st.markdown(
    '<div class="section-title">💵 Phương thức nhận tiền lãi</div>',
    unsafe_allow_html=True
)

method_cols = st.columns(3)

method_list = [
    "Nhận lãi trước",
    "Nhận lãi hàng kỳ",
    "Nhận lãi cuối kỳ"
]

for col, method in zip(
    method_cols,
    method_list
):

    with col:

        if st.button(
            method,
            use_container_width=True,
            key=f"method_{method}"
        ):

            st.session_state.method = method

            st.rerun()


# ============================================================
# LÃI ĐƠN / LÃI KÉP
# ============================================================

st.markdown(
    '<div class="section-title">📈 Cách tính lãi</div>',
    unsafe_allow_html=True
)

interest_type = st.radio(
    "Chọn loại lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ],

    index=(
        0
        if st.session_state.interest_type == "Lãi đơn"
        else 1
    ),

    horizontal=True
)

st.session_state.interest_type = interest_type


# ============================================================
# NÚT TÍNH
# ============================================================

st.markdown("---")

calculate = st.button(
    "🧮 TÍNH TOÁN",
    type="primary",
    use_container_width=True
)


# ============================================================
# TÍNH TOÁN
# ============================================================

if calculate:

    # --------------------------------------------------------
    # KIỂM TRA
    # --------------------------------------------------------

    if principal <= 0:

        st.error(
            "❌ Số tiền gửi phải lớn hơn 0."
        )

        st.stop()

    if withdrawal_date < deposit_date:

        st.error(
            "❌ Ngày rút tiền không được "
            "nhỏ hơn ngày gửi tiền."
        )

        st.stop()

    term = st.session_state.term

    # --------------------------------------------------------
    # BIẾN
    # --------------------------------------------------------

    periods = []

    total_fixed_interest_paid = 0

    current_start = deposit_date

    period_number = 1

    exact_maturity = False

    early_withdrawal = False


    # ========================================================
    # XỬ LÝ CÁC KỲ ĐÃ HOÀN THÀNH
    # ========================================================

    while True:

        maturity = add_months(
            current_start,
            term
        )

        # ----------------------------------------------------
        # Nếu khách rút đúng hoặc sau ngày đáo hạn
        # ----------------------------------------------------

        if withdrawal_date >= maturity:

            days = (
                maturity - current_start
            ).days

            period_interest = calculate_interest(
                principal,
                fixed_rate,
                days,
                interest_type
            )

            # Phương thức nhận lãi
            if st.session_state.method == "Nhận lãi trước":

                paid_interest = period_interest

                status = "Đã nhận lãi trước"

            elif st.session_state.method == "Nhận lãi hàng kỳ":

                paid_interest = period_interest

                status = "Đã nhận lãi hàng kỳ"

            else:

                paid_interest = period_interest

                status = "Đã nhận lãi cuối kỳ"


            periods.append({

                "Kỳ":
                    period_number,

                "Ngày bắt đầu":
                    fmt_date(current_start),

                "Ngày đáo hạn":
                    fmt_date(maturity),

                "Số ngày":
                    days,

                "Lãi suất":
                    f"{fixed_rate:.2f}%",

                "Tiền lãi":
                    period_interest,

                "Lãi đã nhận":
                    paid_interest,

                "Trạng thái":
                    status

            })

            total_fixed_interest_paid += (
                paid_interest
            )


            # ------------------------------------------------
            # Rút đúng ngày đáo hạn
            # ------------------------------------------------

            if withdrawal_date == maturity:

                exact_maturity = True

                break


            # ------------------------------------------------
            # Không rút -> tự động gia hạn
            # ------------------------------------------------

            current_start = maturity

            period_number += 1


        else:

            break


    # ========================================================
    # XỬ LÝ RÚT TRƯỚC HẠN
    # ========================================================

    if not exact_maturity:

        current_maturity = add_months(
            current_start,
            term
        )

        if (
            withdrawal_date > current_start
            and withdrawal_date < current_maturity
        ):

            early_withdrawal = True


    # ========================================================
    # RÚT TRƯỚC HẠN
    # ========================================================

    if early_withdrawal:

        # ----------------------------------------------------
        # Tổng số ngày thực gửi
        # ----------------------------------------------------

        total_days = (
            withdrawal_date - deposit_date
        ).days

        # ----------------------------------------------------
        # Tính lại toàn bộ theo lãi suất không kỳ hạn
        # ----------------------------------------------------

        actual_interest = calculate_interest(
            principal,
            nonterm_rate,
            total_days,
            interest_type
        )

        # ----------------------------------------------------
        # Lãi đã nhận trước/hàng kỳ
        # ----------------------------------------------------

        already_paid = (
            total_fixed_interest_paid
        )

        # ----------------------------------------------------
        # Phần điều chỉnh
        # ----------------------------------------------------

        adjustment = (
            actual_interest
            - already_paid
        )

        # ----------------------------------------------------
        # Tiền tất toán
        # ----------------------------------------------------

        settlement_amount = (
            principal
            + adjustment
        )

        # ----------------------------------------------------
        # Tổng khách thực nhận
        # ----------------------------------------------------

        total_customer_received = (
            already_paid
            + settlement_amount
        )

        total_interest = actual_interest

        status_text = "RÚT TRƯỚC HẠN"


        # ----------------------------------------------------
        # Thêm kỳ đang bị rút trước hạn
        # ----------------------------------------------------

        broken_days = (
            withdrawal_date
            - current_start
        ).days

        periods.append({

            "Kỳ":
                period_number,

            "Ngày bắt đầu":
                fmt_date(current_start),

            "Ngày đáo hạn":
                fmt_date(current_maturity),

            "Số ngày":
                broken_days,

            "Lãi suất":
                f"{nonterm_rate:.2f}%",

            "Tiền lãi":
                actual_interest
                - already_paid,

            "Lãi đã nhận":
                0,

            "Trạng thái":
                "Rút trước hạn - tính lại KKH"

        })


        st.warning(
            "⚠️ Khách hàng rút trước hạn. "
            "Toàn bộ thời gian gửi được tính lại "
            "theo lãi suất không kỳ hạn. "
            "Phần lãi đã nhận trước/hàng kỳ "
            "được đối trừ khi tất toán."
        )


    # ========================================================
    # RÚT ĐÚNG HẠN
    # ========================================================

    elif exact_maturity:

        total_interest = (
            total_fixed_interest_paid
        )

        total_customer_received = (
            principal
            + total_interest
        )

        settlement_amount = (
            principal
            + total_interest
        )

        status_text = "RÚT ĐÚNG HẠN"


        st.success(
            "✅ Khách hàng rút đúng ngày đáo hạn. "
            "Khoản tiền được hưởng lãi suất có kỳ hạn."
        )


    # ========================================================
    # TRƯỜNG HỢP ĐẶC BIỆT
    # ========================================================

    else:

        if withdrawal_date == deposit_date:

            total_interest = 0

            total_customer_received = principal

            settlement_amount = principal

            status_text = "RÚT NGAY NGÀY GỬI"

        else:

            total_days = (
                withdrawal_date
                - deposit_date
            ).days

            actual_interest = calculate_interest(
                principal,
                nonterm_rate,
                total_days,
                interest_type
            )

            adjustment = (
                actual_interest
                - total_fixed_interest_paid
            )

            settlement_amount = (
                principal
                + adjustment
            )

            total_customer_received = (
                total_fixed_interest_paid
                + settlement_amount
            )

            total_interest = actual_interest

            status_text = (
                "RÚT SAU KHI ĐÃ GIA HẠN"
            )

            st.warning(
                "⚠️ Khoản tiền đã tự động gia hạn "
                "sang kỳ mới. Ngày rút nằm trong "
                "kỳ mới nên được xử lý như rút trước hạn."
            )


    # ========================================================
    # KẾT QUẢ
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="control-title">'
        '📊 KẾT QUẢ TÍNH TOÁN'
        '</div>',
        unsafe_allow_html=True
    )


    result1, result2, result3 = st.columns(3)


    with result1:

        st.markdown(
            f"""
            <div class="result-card">

                <div class="result-label">
                    💰 TIỀN GỐC
                </div>

                <div class="result-value">
                    {money(principal)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with result2:

        st.markdown(
            f"""
            <div class="result-card">

                <div class="result-label">
                    📈 TỔNG TIỀN LÃI
                </div>

                <div class="result-value">
                    {money(total_interest)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with result3:

        st.markdown(
            f"""
            <div class="result-card result-card-main">

                <div class="result-label">
                    💵 TỔNG SỐ TIỀN KHÁCH NHẬN
                </div>

                <div class="result-value">
                    {money(total_customer_received)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # THÔNG TIN KHOẢN GỬI
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '📋 Thông tin khoản tiền gửi'
        '</div>',
        unsafe_allow_html=True
    )


    info1, info2, info3, info4 = st.columns(4)


    with info1:

        st.metric(
            "Ngày gửi",
            fmt_date(deposit_date)
        )


    with info2:

        st.metric(
            "Ngày rút",
            fmt_date(withdrawal_date)
        )


    with info3:

        st.metric(
            "Tổng số ngày",
            f"{(withdrawal_date - deposit_date).days} ngày"
        )


    with info4:

        st.metric(
            "Trạng thái",
            status_text
        )


    # ========================================================
    # CHI TIẾT TÍNH LÃI
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '🧮 Chi tiết cách tính'
        '</div>',
        unsafe_allow_html=True
    )


    if early_withdrawal:

        st.markdown(
            f"""
            <div class="formula">

                <b>Rút trước hạn</b><br><br>

                Lãi suất áp dụng:
                <b>{nonterm_rate:.2f}%/năm</b>
                <br><br>

                Tổng thời gian thực gửi:
                <b>{(withdrawal_date - deposit_date).days}
                ngày</b>
                <br><br>

                Tiền lãi sau khi tính lại:
                <b>{money(total_interest)}</b>
                <br><br>

                Lãi đã nhận trước/hàng kỳ:
                <b>{money(total_fixed_interest_paid)}</b>
                <br><br>

                Số tiền tất toán:
                <b>{money(settlement_amount)}</b>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="formula">

                <b>Loại lãi:</b>
                {interest_type}
                <br><br>

                <b>Lãi suất có kỳ hạn:</b>
                {fixed_rate:.2f}%/năm
                <br><br>

                <b>Phương thức nhận lãi:</b>
                {st.session_state.method}
                <br><br>

                <b>Kỳ hạn:</b>
                {term} tháng
                <br><br>

                <b>Tổng tiền lãi:</b>
                {money(total_interest)}

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # BẢNG LỊCH SỬ CÁC KỲ
    # ========================================================

    if periods:

        st.markdown(
            '<div class="section-title">'
            '📅 Chi tiết các kỳ gửi'
            '</div>',
            unsafe_allow_html=True
        )

        df = pd.DataFrame(periods)

        df["Tiền lãi"] = (
            df["Tiền lãi"]
            .apply(money)
        )

        df["Lãi đã nhận"] = (
            df["Lãi đã nhận"]
            .apply(money)
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


    # ========================================================
    # GIẢI THÍCH
    # ========================================================

    with st.expander(
        "📖 Quy tắc tính toán của SMARTSAVE 360"
    ):

        st.markdown("""
### 1. Ngày tính lãi

Ngày bắt đầu tính lãi là **ngày khách hàng gửi tiền**.

Ngày kết thúc tính lãi là **trước ngày đáo hạn hoặc trước ngày khách hàng rút tiền**.

Ví dụ:

Gửi ngày **23/08/2026**, đáo hạn ngày **23/11/2026**.

Số ngày tính lãi:

**23/11/2026 - 23/08/2026 = 92 ngày**

---

### 2. Rút trước hạn

Nếu khách hàng rút trước ngày đáo hạn:

**Toàn bộ thời gian gửi được tính lại theo lãi suất không kỳ hạn.**

Nếu khách hàng đã nhận lãi trước hoặc nhận lãi hàng kỳ thì khoản lãi đó được đối trừ khi tất toán.

---

### 3. Tự động gia hạn

Nếu khách hàng không rút khi đến hạn:

**Ngân hàng tự động gia hạn đúng bằng kỳ hạn ban đầu.**

Ví dụ:

**Gửi 3 tháng → đáo hạn → không rút → gia hạn tiếp 3 tháng.**

---

### 4. Lãi đơn

Công thức:

**Tiền lãi = Tiền gốc × Lãi suất × Số ngày / 365**

---

### 5. Lãi kép

App mô phỏng lãi kép theo ngày:

**A = P × (1 + r/365)^n**

Trong đó:

- P: tiền gốc
- r: lãi suất năm
- n: số ngày
- A: giá trị cuối kỳ

---

### 6. Ba phương thức nhận lãi

**Nhận lãi trước:** tiền lãi của kỳ được xác định và nhận ngay đầu kỳ.

**Nhận lãi hàng kỳ:** tiền lãi được nhận trong kỳ.

**Nhận lãi cuối kỳ:** tiền lãi được nhận khi đến ngày đáo hạn.
        """)


# ============================================================
# THÀNH VIÊN NHÓM
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">'
    '👥 Thành viên thực hiện'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "💡 Để chèn ảnh thành viên, tạo thư mục "
    "`members` cùng cấp với file `app.py` và đưa ảnh "
    "vào đó. App sẽ tự động hiển thị."
)


# ============================================================
# ĐỌC ẢNH THÀNH VIÊN
# ============================================================

members_folder = Path("members")

image_extensions = [
    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.webp"
]

member_images = []

if members_folder.exists():

    for ext in image_extensions:

        member_images.extend(
            members_folder.glob(ext)
        )

member_images = sorted(member_images)


if member_images:

    cols = st.columns(
        min(len(member_images), 4)
    )

    for i, image_path in enumerate(
        member_images
    ):

        with cols[
            i % len(cols)
        ]:

            st.markdown(
                '<div class="member-card">',
                unsafe_allow_html=True
            )

            st.image(
                str(image_path),
                use_container_width=True
            )

            st.markdown(
                f"""
                <div class="member-name">
                    Thành viên {i + 1}
                </div>

                <div class="member-role">
                    Nhóm thực hiện SMARTSAVE 360
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

else:

    empty_cols = st.columns(4)

    for i, col in enumerate(empty_cols):

        with col:

            st.markdown(
                f"""
                <div class="member-card">

                    <div style="
                        font-size:55px;
                        margin:10px;
                    ">
                        👤
                    </div>

                    <div class="member-name">
                        Thành viên {i + 1}
                    </div>

                    <div class="member-role">
                        Chưa có ảnh
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        <b>SMARTSAVE 360</b>
        <br>

        Công cụ mô phỏng tính tiền gửi tiết kiệm

        <br><br>

        💰 Tính lãi đơn
        &nbsp; • &nbsp;
        📈 Tính lãi kép
        &nbsp; • &nbsp;
        🔄 Tự động gia hạn
        &nbsp; • &nbsp;
        💵 Rút trước hạn

    </div>
    """,
    unsafe_allow_html=True
)
