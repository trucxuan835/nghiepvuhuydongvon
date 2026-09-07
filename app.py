import streamlit as st
from datetime import date
import calendar


# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="SMARTSAVE 360",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CSS - TRANG TRÍ GIAO DIỆN
# =========================================================

st.markdown("""
<style>

    /* Nền tổng thể */
    .stApp {
        background: linear-gradient(135deg, #f4fff7 0%, #ffffff 55%, #eafff0 100%);
    }

    /* Ẩn menu mặc định */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* Tiêu đề */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 900;
        color: #087f3f;
        margin-top: 10px;
        margin-bottom: 5px;
        letter-spacing: 1px;
    }

    .sub-title {
        text-align: center;
        color: #555;
        font-size: 17px;
        margin-bottom: 25px;
    }

    /* Ô BẢNG ĐIỀU KHIỂN */
    .control-title {
        background: linear-gradient(90deg, #087f3f, #12a454);
        color: white;
        padding: 14px 20px;
        border-radius: 12px;
        font-size: 21px;
        font-weight: 800;
        text-align: center;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.12);
        margin-bottom: 18px;
    }

    /* Khung SMARTSAVE */
    .smart-box {
        background: white;
        border: 2px solid #0a9b4b;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0px 8px 25px rgba(0, 100, 50, 0.12);
        margin-bottom: 20px;
    }

    .smart-title {
        text-align: center;
        color: #087f3f;
        font-size: 30px;
        font-weight: 900;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }

    .smart-description {
        text-align: center;
        color: #666;
        font-size: 14px;
        margin-bottom: 15px;
    }

    /* Ô đang chọn */
    .selected-box {
        background: #e9fff1;
        border-left: 6px solid #079447;
        padding: 14px 18px;
        border-radius: 10px;
        margin-top: 10px;
        margin-bottom: 15px;
        color: #08733a;
        font-weight: 700;
    }

    /* Kết quả */
    .result-box {
        background: white;
        border-radius: 18px;
        padding: 20px;
        border: 2px solid #0b9748;
        box-shadow: 0px 7px 22px rgba(0,0,0,0.10);
    }

    .result-label {
        color: #666;
        font-size: 14px;
        text-align: center;
    }

    .result-value {
        color: #087f3f;
        font-size: 27px;
        font-weight: 900;
        text-align: center;
    }

    /* Thông báo */
    .notice {
        padding: 15px 20px;
        border-radius: 12px;
        background: #ecfff3;
        border: 1px solid #8bd5a8;
        color: #075d2e;
        margin-top: 15px;
    }

    /* Chữ chạy */
    .marquee-container {
        overflow: hidden;
        white-space: nowrap;
        background: #087f3f;
        color: white;
        border-radius: 8px;
        padding: 9px 0;
        margin: 10px 0 25px 0;
        font-weight: 600;
    }

    .marquee-text {
        display: inline-block;
        padding-left: 100%;
        animation: marquee 18s linear infinite;
    }

    @keyframes marquee {
        0% {
            transform: translateX(0);
        }
        100% {
            transform: translateX(-100%);
        }
    }

    /* Nút */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        border: none;
        background: linear-gradient(90deg, #087f3f, #10a653);
        color: white;
        font-size: 17px;
        font-weight: 800;
        padding: 12px;
        transition: 0.3s;
    }

    div.stButton > button:hover {
        transform: scale(1.02);
        background: linear-gradient(90deg, #066b35, #087f3f);
        color: white;
    }

    /* Input */
    div[data-baseweb="input"] {
        border-radius: 9px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM TÍNH NGÀY
# =========================================================

def add_months(d, months):
    """
    Cộng số tháng vào ngày.
    Ví dụ:
    23/08 + 3 tháng = 23/11
    """

    month_index = d.month - 1 + months

    year = d.year + month_index // 12

    month = month_index % 12 + 1

    last_day = calendar.monthrange(year, month)[1]

    day = min(d.day, last_day)

    return date(year, month, day)


def calculate_interest(principal, rate, days):
    """
    Công thức:
    Lãi = Gốc × Lãi suất năm × Số ngày / 365
    """

    return principal * (rate / 100) * days / 365


def money(number):
    return f"{number:,.0f} VNĐ"


def dmy(d):
    return d.strftime("%d/%m/%Y")


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">💰 SỐ TIỀN GỬI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Ứng dụng mô phỏng tính lãi tiền gửi tiết kiệm</div>',
    unsafe_allow_html=True
)


# =========================================================
# CHỮ CHẠY
# =========================================================

st.markdown("""
<div class="marquee-container">
    <div class="marquee-text">
        🏦 SMARTSAVE 360 • TÍNH LÃI TIỀN GỬI TIẾT KIỆM • 
        NHANH CHÓNG • CHÍNH XÁC • DỄ SỬ DỤNG • 
        TỰ ĐỘNG TÁI TỤC KHI ĐẾN HẠN •
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# BẢNG ĐIỀU KHIỂN
# =========================================================

st.markdown(
    '<div class="control-title">⚙️ BẢNG ĐIỀU KHIỂN</div>',
    unsafe_allow_html=True
)


# =========================================================
# KHUNG SMARTSAVE 360
# =========================================================

st.markdown("""
<div class="smart-box">
    <div class="smart-title">
        SMARTSAVE 360
    </div>
    <div class="smart-description">
        Công cụ tính toán tiền lãi tiền gửi tiết kiệm
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# NHẬP DỮ LIỆU
# =========================================================

left, right = st.columns(2)

with left:

    st.markdown("### 💰 Thông tin tiền gửi")

    principal = st.number_input(
        "Số tiền khách hàng gửi (VNĐ)",
        min_value=1000.0,
        value=500_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    fixed_rate = st.number_input(
        "Lãi suất có kỳ hạn (%/năm)",
        min_value=0.0,
        value=5.0,
        step=0.01,
        format="%.2f"
    )

    non_term_rate = st.number_input(
        "Lãi suất không kỳ hạn (%/năm)",
        min_value=0.0,
        value=0.20,
        step=0.01,
        format="%.2f"
    )

    term_months = st.selectbox(
        "Kỳ hạn gửi tiền",
        [1, 3, 6, 12, 18, 24, 36],
        format_func=lambda x: f"{x} tháng"
    )


with right:

    st.markdown("### 📅 Thời gian gửi")

    deposit_date = st.date_input(
        "Ngày gửi tiền",
        value=date.today()
    )

    withdrawal_date = st.date_input(
        "Ngày rút tiền",
        value=add_months(date.today(), term_months)
    )

    interest_method = st.radio(
        "💵 Phương thức nhận tiền lãi",
        [
            "Nhận lãi trước",
            "Nhận lãi hàng tháng",
            "Nhận lãi cuối kỳ"
        ]
    )


# =========================================================
# ĐANG CHỌN
# =========================================================

st.markdown(
    f"""
    <div class="selected-box">
        🟢 Đang chọn:
        <b>{term_months} tháng</b>
        &nbsp; | &nbsp;
        <b>{interest_method}</b>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# NÚT CHỌN NHANH
# =========================================================

st.markdown("### ⚡ Chọn nhanh")

q1, q2, q3, q4 = st.columns(4)

with q1:
    quick_1 = st.button("1 tháng")

with q2:
    quick_3 = st.button("3 tháng")

with q3:
    quick_6 = st.button("6 tháng")

with q4:
    quick_12 = st.button("12 tháng")


if quick_1:
    term_months = 1
    st.rerun()

if quick_3:
    term_months = 3
    st.rerun()

if quick_6:
    term_months = 6
    st.rerun()

if quick_12:
    term_months = 12
    st.rerun()


# =========================================================
# NÚT TÍNH TOÁN
# =========================================================

st.markdown("---")

calculate = st.button(
    "🧮 TÍNH TOÁN TIỀN LÃI",
    type="primary"
)


# =========================================================
# XỬ LÝ TÍNH TOÁN
# =========================================================

if calculate:

    if withdrawal_date < deposit_date:

        st.error(
            "❌ Ngày rút tiền phải lớn hơn hoặc bằng ngày gửi tiền."
        )

        st.stop()


    # =====================================================
    # ĐÁO HẠN ĐẦU TIÊN
    # =====================================================

    first_maturity = add_months(
        deposit_date,
        term_months
    )


    # =====================================================
    # TRƯỜNG HỢP RÚT TRƯỚC HẠN
    # =====================================================

    if withdrawal_date < first_maturity:

        days = (
            withdrawal_date - deposit_date
        ).days

        interest = calculate_interest(
            principal,
            non_term_rate,
            days
        )

        total = principal + interest

        st.subheader("📊 KẾT QUẢ")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                f"""
                <div class="result-box">
                    <div class="result-label">TIỀN GỐC</div>
                    <div class="result-value">
                        {money(principal)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                f"""
                <div class="result-box">
                    <div class="result-label">TIỀN LÃI</div>
                    <div class="result-value">
                        {money(interest)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                f"""
                <div class="result-box">
                    <div class="result-label">TỔNG TIỀN NHẬN</div>
                    <div class="result-value">
                        {money(total)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        st.markdown(
            f"""
            <div class="notice">
                ⚠️ <b>Khách hàng rút trước hạn</b><br><br>

                Thời gian gửi:
                <b>{days} ngày</b><br>

                Lãi suất áp dụng:
                <b>{non_term_rate:.2f}%/năm</b><br><br>

                Tiền lãi = Tiền gốc × Lãi suất không kỳ hạn
                × Số ngày / 365.
            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # ĐÚNG HẠN / SAU HẠN
    # =====================================================

    else:

        current_start = deposit_date

        total_interest = 0

        periods = []

        period_number = 1


        # =================================================
        # TÍNH TỪNG KỲ
        # =================================================

        while current_start < withdrawal_date:

            maturity = add_months(
                current_start,
                term_months
            )


            # ---------------------------------------------
            # RÚT ĐÚNG HẠN Ở KỲ NÀY
            # ---------------------------------------------

            if withdrawal_date == maturity:

                days = (
                    maturity - current_start
                ).days

                interest = calculate_interest(
                    principal,
                    fixed_rate,
                    days
                )

                total_interest += interest

                periods.append({
                    "Kỳ": period_number,
                    "Ngày bắt đầu": current_start,
                    "Ngày đáo hạn": maturity,
                    "Số ngày": days,
                    "Lãi suất": fixed_rate,
                    "Tiền lãi": interest,
                    "Trạng thái": "Rút đúng hạn"
                })

                break


            # ---------------------------------------------
            # KHÁCH CHƯA RÚT → TÁI TỤC
            # ---------------------------------------------

            elif withdrawal_date > maturity:

                days = (
                    maturity - current_start
                ).days

                interest = calculate_interest(
                    principal,
                    fixed_rate,
                    days
                )

                total_interest += interest

                periods.append({
                    "Kỳ": period_number,
                    "Ngày bắt đầu": current_start,
                    "Ngày đáo hạn": maturity,
                    "Số ngày": days,
                    "Lãi suất": fixed_rate,
                    "Tiền lãi": interest,
                    "Trạng thái": "Đã tái tục"
                })

                current_start = maturity

                period_number += 1


            # ---------------------------------------------
            # RÚT TRƯỚC HẠN TRONG KỲ TÁI TỤC
            # ---------------------------------------------

            else:

                total_days = (
                    withdrawal_date - deposit_date
                ).days

                interest = calculate_interest(
                    principal,
                    non_term_rate,
                    total_days
                )

                total_interest = interest

                periods.append({
                    "Kỳ": period_number,
                    "Ngày bắt đầu": current_start,
                    "Ngày đáo hạn": withdrawal_date,
                    "Số ngày": (
                        withdrawal_date - current_start
                    ).days,
                    "Lãi suất": non_term_rate,
                    "Tiền lãi": interest,
                    "Trạng thái": "Rút trước hạn"
                })

                break


            # Chống vòng lặp vô hạn
            if period_number > 100:

                st.error(
                    "Không thể tính quá 100 kỳ tái tục."
                )

                break


        # =================================================
        # TỔNG TIỀN
        # =================================================

        total_received = (
            principal + total_interest
        )


        # =================================================
        # HIỂN THỊ KẾT QUẢ
        # =================================================

        st.subheader("📊 KẾT QUẢ TÍNH TOÁN")

        c1, c2, c3 = st.columns(3)


        with c1:

            st.markdown(
                f"""
                <div class="result-box">
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


        with c2:

            st.markdown(
                f"""
                <div class="result-box">
                    <div class="result-label">
                        💵 TỔNG TIỀN LÃI
                    </div>
                    <div class="result-value">
                        {money(total_interest)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with c3:

            st.markdown(
                f"""
                <div class="result-box">
                    <div class="result-label">
                        🏦 TỔNG TIỀN KHÁCH NHẬN
                    </div>
                    <div class="result-value">
                        {money(total_received)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        # =================================================
        # TRẠNG THÁI
        # =================================================

        if withdrawal_date == first_maturity:

            st.success(
                "✅ Khách hàng rút đúng ngày đáo hạn kỳ đầu tiên."
            )

        elif withdrawal_date > first_maturity:

            st.success(
                f"""
                🔄 Tiền gửi đã được tự động tái tục.

                Kỳ hạn tái tục:
                **{term_months} tháng**

                Số kỳ đã tính:
                **{len(periods)} kỳ**
                """
            )


        # =================================================
        # THÔNG TIN
        # =================================================

        total_days = (
            withdrawal_date - deposit_date
        ).days

        st.markdown(
            f"""
            <div class="notice">

            📥 Ngày gửi:
            <b>{dmy(deposit_date)}</b>

            <br><br>

            📤 Ngày rút:
            <b>{dmy(withdrawal_date)}</b>

            <br><br>

            ⏱️ Tổng thời gian gửi:
            <b>{total_days} ngày</b>

            <br><br>

            📈 Lãi suất có kỳ hạn:
            <b>{fixed_rate:.2f}%/năm</b>

            <br><br>

            📉 Lãi suất không kỳ hạn:
            <b>{non_term_rate:.2f}%/năm</b>

            <br><br>

            💳 Phương thức nhận lãi:
            <b>{interest_method}</b>

            </div>
            """,
            unsafe_allow_html=True
        )


        # =================================================
        # BẢNG CHI TIẾT
        # =================================================

        st.subheader("📑 LỊCH TÍNH LÃI")

        table = []

        for p in periods:

            table.append({
                "Kỳ": p["Kỳ"],
                "Ngày bắt đầu": dmy(
                    p["Ngày bắt đầu"]
                ),
                "Ngày kết thúc": dmy(
                    p["Ngày đáo hạn"]
                ),
                "Số ngày": p["Số ngày"],
                "Lãi suất (%/năm)": f'{p["Lãi suất"]:.2f}',
                "Tiền lãi": money(
                    p["Tiền lãi"]
                ),
                "Trạng thái": p["Trạng thái"]
            })

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# CHÂN TRANG
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;color:#087f3f;font-weight:700;">
        🏦 SMARTSAVE 360
    </div>

    <div style="text-align:center;color:#777;font-size:13px;">
        Công cụ mô phỏng tính lãi tiền gửi tiết kiệm
    </div>
    """,
    unsafe_allow_html=True
)
