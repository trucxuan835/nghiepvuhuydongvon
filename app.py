import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd

# =========================================================
# CẤU HÌNH TRANG
# =========================================================
st.set_page_config(
    page_title="SMARTSAVE 360",
    page_icon="💰",
    layout="wide"
)

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>
    .main-title {
        font-size: 38px;
        font-weight: 800;
        text-align: center;
        color: #0B7A3E;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #666;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .control-box {
        background-color: #0B7A3E;
        color: white;
        padding: 12px 18px;
        border-radius: 8px;
        font-size: 21px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .section-title {
        background-color: #0B7A3E;
        color: white;
        padding: 10px 15px;
        border-radius: 7px;
        font-size: 18px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 12px;
    }

    .smart-box {
        border: 2px solid #0B7A3E;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 20px;
        background-color: #F8FFFB;
    }

    .selected-box {
        background-color: #DFF5E8;
        color: #075C30;
        padding: 10px 15px;
        border-radius: 7px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .result-box {
        border: 2px solid #0B7A3E;
        border-radius: 12px;
        padding: 20px;
        background-color: #F8FFFB;
    }

    .result-number {
        color: #0B7A3E;
        font-size: 28px;
        font-weight: 800;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 7px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM TIỆN ÍCH
# =========================================================
def format_money(value):
    return f"{value:,.0f} VNĐ"


def calculate_end_date(start_date, months):
    return start_date + relativedelta(months=months)


def interest_by_days(principal, annual_rate, days):
    """
    Lãi đơn theo số ngày:
    Tiền lãi = Gốc x lãi suất năm x số ngày / 365
    """
    return principal * annual_rate / 100 * days / 365


def get_periods(start_date, end_date, term_months):
    """
    Tạo các kỳ tính lãi.
    Mỗi kỳ đúng bằng kỳ hạn gửi.
    """
    periods = []

    period_start = start_date
    period_number = 1

    while period_start < end_date:
        period_end = period_start + relativedelta(months=term_months)

        actual_end = min(period_end, end_date)

        days = (actual_end - period_start).days

        if days > 0:
            periods.append({
                "Kỳ": period_number,
                "Từ ngày": period_start,
                "Đến trước ngày": actual_end,
                "Số ngày": days
            })

        period_start = period_end
        period_number += 1

    return periods


# =========================================================
# TIÊU ĐỀ
# =========================================================
st.markdown(
    '<div class="main-title">SMARTSAVE 360</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Công cụ tính tiền lãi tiền gửi tiết kiệm</div>',
    unsafe_allow_html=True
)


# =========================================================
# KHUNG SMARTSAVE 360
# =========================================================
st.markdown("""
<div class="smart-box">
    <h2 style="color:#0B7A3E; margin-bottom:5px;">
        SMARTSAVE 360
    </h2>
    <p style="margin-bottom:0;">
        Tính toán tiền gốc và tiền lãi tiền gửi theo kỳ hạn,
        lãi không kỳ hạn và phương thức nhận lãi.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# BẢNG ĐIỀU KHIỂN
# =========================================================
st.markdown(
    '<div class="control-box">BẢNG ĐIỀU KHIỂN</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        '<div class="selected-box">Đang chọn</div>',
        unsafe_allow_html=True
    )

    quick_term = st.selectbox(
        "Kỳ hạn nhanh",
        [1, 3, 6, 9, 12, 18, 24, 36],
        index=2,
        format_func=lambda x: f"{x} tháng"
    )

with col2:
    st.markdown(
        '<div class="selected-box">Chọn nhanh</div>',
        unsafe_allow_html=True
    )

    quick_interest = st.number_input(
        "Lãi suất nhanh (%/năm)",
        min_value=0.0,
        value=5.0,
        step=0.1
    )

with col3:
    st.markdown(
        '<div class="selected-box">Chọn nhanh</div>',
        unsafe_allow_html=True
    )

    quick_method = st.selectbox(
        "Phương thức nhận lãi",
        [
            "Nhận lãi trước",
            "Nhận lãi hàng kỳ",
            "Nhận lãi cuối kỳ"
        ]
    )


# =========================================================
# THÔNG TIN SỔ TIẾT KIỆM
# =========================================================
st.markdown(
    '<div class="section-title">Số tiền gửi</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
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
        value=quick_interest,
        step=0.01
    )

    non_term_rate = st.number_input(
        "Lãi suất không kỳ hạn (%/năm)",
        min_value=0.0,
        value=0.2,
        step=0.01
    )

with col2:
    deposit_date = st.date_input(
        "Ngày gửi tiền",
        value=date.today()
    )

    withdrawal_date = st.date_input(
        "Ngày rút tiền",
        value=calculate_end_date(date.today(), quick_term)
    )

    term_months = st.selectbox(
        "Kỳ hạn gửi tiền",
        [1, 3, 6, 9, 12, 18, 24, 36],
        index=[1, 3, 6, 9, 12, 18, 24, 36].index(quick_term),
        format_func=lambda x: f"{x} tháng"
    )


# =========================================================
# PHƯƠNG THỨC NHẬN LÃI
# =========================================================
st.markdown(
    '<div class="section-title">Phương thức nhận tiền lãi</div>',
    unsafe_allow_html=True
)

interest_method = st.radio(
    "Chọn cách nhận tiền lãi",
    [
        "Nhận lãi trước",
        "Nhận lãi hàng kỳ",
        "Nhận lãi cuối kỳ"
    ],
    horizontal=True,
    index=[
        "Nhận lãi trước",
        "Nhận lãi hàng kỳ",
        "Nhận lãi cuối kỳ"
    ].index(quick_method)
)


# =========================================================
# TÍNH TOÁN
# =========================================================
if st.button("TÍNH TOÁN", type="primary"):

    if principal <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if withdrawal_date <= deposit_date:
        st.error("Ngày rút tiền phải sau ngày gửi tiền.")
        st.stop()

    # Ngày đáo hạn ban đầu
    maturity_date = calculate_end_date(
        deposit_date,
        term_months
    )

    # -----------------------------------------------------
    # TRƯỜNG HỢP RÚT TRƯỚC HẠN
    # -----------------------------------------------------
    if withdrawal_date < maturity_date:

        days = (withdrawal_date - deposit_date).days

        interest = interest_by_days(
            principal,
            non_term_rate,
            days
        )

        total = principal + interest

        st.warning(
            "Khách hàng rút trước hạn → toàn bộ số tiền được "
            "tính theo lãi suất không kỳ hạn."
        )

        st.markdown(
            '<div class="section-title">Kết quả tính lãi không kỳ hạn</div>',
            unsafe_allow_html=True
        )

        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:
            st.metric(
                "Số ngày thực gửi",
                f"{days} ngày"
            )

        with result_col2:
            st.metric(
                "Tiền lãi",
                format_money(interest)
            )

        with result_col3:
            st.metric(
                "Tổng tiền nhận",
                format_money(total)
            )

        data = [{
            "Kỳ": "Không kỳ hạn - Kỳ 1",
            "Từ ngày": deposit_date.strftime("%d/%m/%Y"),
            "Đến trước ngày": withdrawal_date.strftime("%d/%m/%Y"),
            "Số ngày": days,
            "Lãi suất": f"{non_term_rate:.2f}%/năm",
            "Tiền lãi": round(interest)
        }]

        st.dataframe(
            pd.DataFrame(data),
            use_container_width=True,
            hide_index=True
        )

    # -----------------------------------------------------
    # TRƯỜNG HỢP ĐÚNG HẠN HOẶC SAU HẠN
    # -----------------------------------------------------
    else:

        # Số kỳ đã hoàn thành
        full_periods = 0
        temp_date = deposit_date

        while True:
            next_date = calculate_end_date(
                temp_date,
                term_months
            )

            if next_date <= withdrawal_date:
                full_periods += 1
                temp_date = next_date
            else:
                break

        # Ngày tính lãi thực tế
        # Tính từ ngày gửi đến trước ngày rút
        periods = get_periods(
            deposit_date,
            withdrawal_date,
            term_months
        )

        detail = []
        total_interest = 0

        # -------------------------------------------------
        # TÍNH TỪNG KỲ
        # -------------------------------------------------
        for p in periods:

            period_start = p["Từ ngày"]
            period_end = p["Đến trước ngày"]
            days = p["Số ngày"]

            # Nếu đủ một kỳ → lãi suất có kỳ hạn
            if days == (
                period_end - period_start
            ).days:

                rate = fixed_rate
                interest_type = f"Lãi định kỳ - Kỳ {p['Kỳ']}"

            else:
                # Phần thời gian chưa đủ một kỳ:
                # áp dụng lãi suất không kỳ hạn
                rate = non_term_rate
                interest_type = f"Lãi không kỳ hạn - Kỳ {p['Kỳ']}"

            interest = interest_by_days(
                principal,
                rate,
                days
            )

            total_interest += interest

            detail.append({
                "Kỳ tính lãi": interest_type,
                "Từ ngày": period_start.strftime("%d/%m/%Y"),
                "Đến trước ngày": period_end.strftime("%d/%m/%Y"),
                "Số ngày": days,
                "Lãi suất (%/năm)": rate,
                "Tiền lãi (VNĐ)": round(interest)
            })

        # -------------------------------------------------
        # XỬ LÝ PHƯƠNG THỨC NHẬN LÃI
        # -------------------------------------------------

        if interest_method == "Nhận lãi trước":

            # Lãi được nhận ngay từ đầu.
            # Tổng giá trị cuối kỳ vẫn bằng gốc + lãi,
            # nhưng số tiền nhận trước đã được chi trả.

            upfront_interest = interest_by_days(
                principal,
                fixed_rate,
                (maturity_date - deposit_date).days
            )

            amount_received_now = upfront_interest

            amount_at_maturity = principal

            total_customer_received = (
                amount_received_now +
                amount_at_maturity
            )

            method_note = (
                "Tiền lãi của kỳ hạn được trả ngay khi gửi. "
                "Khi đáo hạn khách hàng nhận lại tiền gốc."
            )

        elif interest_method == "Nhận lãi hàng kỳ":

            # Tổng tiền khách hàng nhận gồm:
            # tiền lãi từng kỳ + tiền gốc
            amount_received_now = 0
            amount_at_maturity = principal
            total_customer_received = principal + total_interest

            method_note = (
                "Tiền lãi được trả sau mỗi kỳ hạn hoàn thành. "
                "Tiền gốc được nhận khi rút/đáo hạn."
            )

        else:

            # Nhận toàn bộ lãi khi đáo hạn/rút tiền
            amount_received_now = 0
            amount_at_maturity = principal + total_interest
            total_customer_received = principal + total_interest

            method_note = (
                "Tiền lãi được cộng cùng tiền gốc và nhận "
                "khi khách hàng rút tiền."
            )

        # -------------------------------------------------
        # KẾT QUẢ
        # -------------------------------------------------
        st.success(
            "Khoản tiền đã đến hạn hoặc sau ngày đáo hạn. "
            "Các kỳ hoàn thành được tính theo lãi suất có kỳ hạn."
        )

        st.markdown(
            '<div class="section-title">Kết quả tính tiền</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Tiền gốc",
                format_money(principal)
            )

        with col2:
            st.metric(
                "Tổng tiền lãi",
                format_money(total_interest)
            )

        with col3:
            st.metric(
                "Số kỳ hoàn thành",
                f"{full_periods} kỳ"
            )

        with col4:
            st.metric(
                "Tổng tiền khách nhận",
                format_money(total_customer_received)
            )

        st.info(method_note)

        # -------------------------------------------------
        # BẢNG CHI TIẾT KỲ TÍNH LÃI
        # -------------------------------------------------
        st.markdown(
            '<div class="section-title">Chi tiết kỳ tính lãi</div>',
            unsafe_allow_html=True
        )

        df = pd.DataFrame(detail)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Lãi suất (%/năm)": st.column_config.NumberColumn(
                    format="%.2f%%"
                ),
                "Tiền lãi (VNĐ)": st.column_config.NumberColumn(
                    format="%d"
                )
            }
        )

        # -------------------------------------------------
        # THÔNG TIN GIA HẠN
        # -------------------------------------------------
        if withdrawal_date > maturity_date:

            number_of_renewals = full_periods

            st.markdown(
                '<div class="section-title">Thông tin gia hạn</div>',
                unsafe_allow_html=True
            )

            st.write(
                f"Ngày đáo hạn kỳ đầu: "
                f"**{maturity_date.strftime('%d/%m/%Y')}**"
            )

            st.write(
                f"Số lần gia hạn theo kỳ hạn: "
                f"**{number_of_renewals - 1 if number_of_renewals > 0 else 0} lần**"
            )

            st.write(
                f"Kỳ hạn gia hạn: **{term_months} tháng/kỳ**"
            )

            st.info(
                "Nếu khách hàng không rút khi đến hạn, "
                "hệ thống tự động gia hạn bằng đúng kỳ hạn đã chọn."
            )


# =========================================================
# GHI CHÚ
# =========================================================
st.markdown("---")

st.caption(
    "SMARTSAVE 360 | Công cụ mô phỏng tính lãi tiền gửi tiết kiệm"
)
