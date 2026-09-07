import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta

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
# CSS - PHONG CÁCH TECHCOMBANK
# ============================================================

st.markdown("""
<style>

    /* ===== NỀN CHUNG ===== */
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(230, 0, 0, 0.05), transparent 25%),
            radial-gradient(circle at 90% 90%, rgba(230, 0, 0, 0.04), transparent 25%),
            #f7f7f7;
    }

    /* ===== ẨN MENU STREAMLIT ===== */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* ===== TIÊU ĐỀ ===== */

    .main-title {
        font-size: 42px;
        font-weight: 900;
        text-align: center;
        letter-spacing: 3px;
        color: #e30613;
        margin-bottom: 3px;
    }

    .sub-title {
        text-align: center;
        color: #555;
        font-size: 16px;
        margin-bottom: 25px;
        letter-spacing: 1px;
    }

    /* ===== CHỮ CHẠY ===== */

    .ticker {
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        background: #e30613;
        color: white;
        padding: 10px 0;
        border-radius: 8px;
        margin-bottom: 20px;
        font-weight: 600;
    }

    .ticker-text {
        display: inline-block;
        padding-left: 100%;
        animation: ticker 18s linear infinite;
    }

    @keyframes ticker {
        0% {
            transform: translateX(0%);
        }
        100% {
            transform: translateX(-100%);
        }
    }

    /* ===== KHUNG SMARTSAVE ===== */

    .smart-box {
        background: white;
        border-left: 7px solid #e30613;
        border-radius: 12px;
        padding: 22px 25px;
        margin-bottom: 20px;
        box-shadow: 0 5px 18px rgba(0,0,0,0.07);
    }

    .smart-title {
        font-size: 25px;
        font-weight: 900;
        color: #111;
        letter-spacing: 2px;
    }

    .smart-desc {
        color: #666;
        margin-top: 5px;
    }

    /* ===== Ô XANH BẢNG ĐIỀU KHIỂN ===== */

    .control-title {
        background: #0b7a3b;
        color: white;
        padding: 12px 18px;
        border-radius: 8px;
        font-size: 18px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 15px;
    }

    /* ===== Ô ĐANG CHỌN ===== */

    .selected-box {
        background: #0b7a3b;
        color: white;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        font-weight: 800;
        margin-top: 12px;
        margin-bottom: 12px;
    }

    /* ===== NÚT ===== */

    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: none;
        background: #e30613;
        color: white;
        font-weight: 800;
        min-height: 45px;
        transition: 0.2s;
    }

    .stButton > button:hover {
        background: #b8000d;
        color: white;
        transform: translateY(-1px);
    }

    /* ===== CARD KẾT QUẢ ===== */

    .result-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin-top: 12px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.07);
        border-top: 4px solid #e30613;
    }

    .result-label {
        color: #777;
        font-size: 14px;
    }

    .result-value {
        color: #111;
        font-size: 24px;
        font-weight: 900;
        margin-top: 5px;
    }

    .total-card {
        background: #e30613;
        color: white;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 8px 25px rgba(227,6,19,0.25);
    }

    .total-label {
        font-size: 16px;
        opacity: 0.9;
    }

    .total-value {
        font-size: 36px;
        font-weight: 900;
        margin-top: 5px;
    }

    /* ===== THẺ PHƯƠNG PHÁP ===== */

    .method-card {
        background: white;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #ddd;
        min-height: 110px;
        margin-bottom: 10px;
    }

    .method-title {
        color: #e30613;
        font-weight: 900;
        font-size: 17px;
    }

    .method-text {
        color: #666;
        font-size: 14px;
        margin-top: 5px;
    }

    /* ===== SIDEBAR ===== */

    section[data-testid="stSidebar"] {
        background: #111111;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* ===== INPUT ===== */

    input, textarea {
        border-radius: 7px !important;
    }

    div[data-baseweb="select"] > div {
        border-radius: 7px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# HÀM TIỆN ÍCH
# ============================================================

def money(v):
    return f"{v:,.0f} VNĐ"


def add_months(d, months):
    return d + relativedelta(months=months)


def maturity_date(deposit_date, term_months):
    return add_months(deposit_date, term_months)


def days_between(start, end):
    """
    Tính từ ngày gửi đến trước ngày rút.
    Ví dụ:
    23/08 -> 26/09
    số ngày tính lãi = 34 ngày
    """
    return (end - start).days


def simple_interest(principal, annual_rate, days):
    """
    Lãi đơn:
    Lãi = Gốc × Lãi suất năm × Số ngày / 365
    """
    return principal * (annual_rate / 100) * days / 365


def compound_interest(principal, annual_rate, days):
    """
    Lãi kép theo ngày:
    A = P × (1 + r/365)^n
    """
    if days <= 0:
        return principal

    return principal * (1 + annual_rate / 100 / 365) ** days


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">SMARTSAVE 360</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">CÔNG CỤ TÍNH LÃI TIỀN GỬI TIẾT KIỆM</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="ticker">
    <div class="ticker-text">
        SMARTSAVE 360 • TÍNH LÃI NHANH • LÃI ĐƠN • LÃI KÉP • RÚT TRƯỚC HẠN • TỰ ĐỘNG GIA HẠN
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SMARTSAVE BOX
# ============================================================

st.markdown("""
<div class="smart-box">
    <div class="smart-title">SMARTSAVE 360</div>
    <div class="smart-desc">
        Công cụ mô phỏng tiền gửi tiết kiệm và tính toán tiền lãi
        theo thời gian thực.
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="control-title">BẢNG ĐIỀU KHIỂN</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="selected-box">Đang chọn</div>',
        unsafe_allow_html=True
    )

    quick_term = st.selectbox(
        "Kỳ hạn nhanh",
        [
            "1 tháng",
            "3 tháng",
            "6 tháng",
            "9 tháng",
            "12 tháng",
            "18 tháng",
            "24 tháng",
            "36 tháng"
        ]
    )

    if st.button("Chọn nhanh"):

        term_number = int(quick_term.split()[0])

        st.session_state["quick_term"] = term_number

        st.success(f"Đã chọn kỳ hạn {term_number} tháng")


# ============================================================
# THÔNG TIN TIỀN GỬI
# ============================================================

st.subheader("Số tiền gửi")

col1, col2, col3 = st.columns(3)

with col1:

    amount = st.number_input(
        "Số tiền khách hàng gửi (VNĐ)",
        min_value=0.0,
        value=500_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

with col2:

    fixed_rate = st.number_input(
        "Lãi suất có kỳ hạn (%/năm)",
        min_value=0.0,
        value=5.0,
        step=0.1
    )

with col3:

    non_term_rate = st.number_input(
        "Lãi suất không kỳ hạn (%/năm)",
        min_value=0.0,
        value=0.2,
        step=0.1
    )


# ============================================================
# NGÀY VÀ KỲ HẠN
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    deposit_date = st.date_input(
        "Ngày gửi tiền",
        value=date.today()
    )

with col2:

    withdrawal_date = st.date_input(
        "Ngày rút tiền",
        value=add_months(date.today(), 3)
    )

with col3:

    default_term = st.session_state.get("quick_term", 3)

    term = st.selectbox(
        "Kỳ hạn gửi tiền",
        [1, 3, 6, 9, 12, 18, 24, 36],
        index=[1, 3, 6, 9, 12, 18, 24, 36].index(default_term),
        format_func=lambda x: f"{x} tháng"
    )


# ============================================================
# NGÀY ĐÁO HẠN
# ============================================================

maturity = maturity_date(
    deposit_date,
    term
)

st.info(
    f"📅 Ngày đáo hạn dự kiến: **{maturity.strftime('%d/%m/%Y')}**"
)


# ============================================================
# PHƯƠNG THỨC NHẬN LÃI
# ============================================================

st.subheader("Phương thức nhận tiền lãi")

method = st.radio(
    "Chọn phương thức",
    [
        "Nhận lãi trước",
        "Nhận lãi hàng kỳ",
        "Nhận lãi cuối kỳ"
    ],
    horizontal=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="method-card">
        <div class="method-title">NHẬN LÃI TRƯỚC</div>
        <div class="method-text">
            Tiền lãi được xác định ngay khi khách hàng gửi tiền.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="method-card">
        <div class="method-title">NHẬN LÃI HÀNG KỲ</div>
        <div class="method-text">
            Tiền lãi được chi trả định kỳ trong thời gian gửi.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="method-card">
        <div class="method-title">NHẬN LÃI CUỐI KỲ</div>
        <div class="method-text">
            Tiền lãi được thanh toán khi kết thúc kỳ hạn.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# KIỂU TÍNH LÃI
# ============================================================

st.subheader("Phương pháp tính lãi")

interest_type = st.radio(
    "Chọn phương pháp",
    [
        "Lãi đơn",
        "Lãi kép"
    ],
    horizontal=True
)


# ============================================================
# NÚT TÍNH TOÁN
# ============================================================

calculate = st.button(
    "TÍNH TOÁN TIỀN LÃI"
)


# ============================================================
# TÍNH TOÁN
# ============================================================

if calculate:

    if amount <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")

    elif withdrawal_date <= deposit_date:
        st.error(
            "Ngày rút tiền phải lớn hơn ngày gửi tiền."
        )

    else:

        # ----------------------------------------------------
        # TRƯỜNG HỢP RÚT TRƯỚC HẠN
        # ----------------------------------------------------

        if withdrawal_date < maturity:

            status = "RÚT TRƯỚC HẠN"

            interest_rate_used = non_term_rate

            interest_days = days_between(
                deposit_date,
                withdrawal_date
            )

            # Tính lãi
            if interest_type == "Lãi đơn":

                interest = simple_interest(
                    amount,
                    interest_rate_used,
                    interest_days
                )

                total = amount + interest

            else:

                total = compound_interest(
                    amount,
                    interest_rate_used,
                    interest_days
                )

                interest = total - amount

            st.warning(
                f"⚠️ Khách hàng **rút trước hạn**. "
                f"Lãi suất áp dụng: **{non_term_rate:.2f}%/năm**."
            )

            renewal_count = 0

        # ----------------------------------------------------
        # TRƯỜNG HỢP ĐÚNG HẠN
        # ----------------------------------------------------

        elif withdrawal_date == maturity:

            status = "RÚT ĐÚNG HẠN"

            interest_rate_used = fixed_rate

            interest_days = days_between(
                deposit_date,
                withdrawal_date
            )

            if interest_type == "Lãi đơn":

                interest = simple_interest(
                    amount,
                    interest_rate_used,
                    interest_days
                )

                total = amount + interest

            else:

                total = compound_interest(
                    amount,
                    interest_rate_used,
                    interest_days
                )

                interest = total - amount

            renewal_count = 0

            st.success(
                "✅ Khách hàng rút đúng ngày đáo hạn."
            )

        # ----------------------------------------------------
        # TRƯỜNG HỢP SAU HẠN
        # ----------------------------------------------------

        else:

            status = "SAU NGÀY ĐÁO HẠN"

            interest_rate_used = fixed_rate

            # Tính số kỳ gia hạn
            renewal_count = 0

            temp_date = maturity

            while add_months(
                temp_date,
                term
            ) <= withdrawal_date:

                renewal_count += 1

                temp_date = add_months(
                    temp_date,
                    term
                )

            # Số ngày của phần kỳ hiện tại
            elapsed_days = days_between(
                deposit_date,
                withdrawal_date
            )

            # ------------------------------------------------
            # LÃI ĐƠN
            # ------------------------------------------------

            if interest_type == "Lãi đơn":

                interest = simple_interest(
                    amount,
                    interest_rate_used,
                    elapsed_days
                )

                total = amount + interest

            # ------------------------------------------------
            # LÃI KÉP
            # ------------------------------------------------

            else:

                total = compound_interest(
                    amount,
                    interest_rate_used,
                    elapsed_days
                )

                interest = total - amount

            interest_days = elapsed_days

            st.info(
                f"🔄 Khoản tiền đã quá hạn. "
                f"Ngân hàng thực hiện **tự động gia hạn đúng kỳ hạn {term} tháng**."
            )


        # ====================================================
        # HIỂN THỊ KẾT QUẢ
        # ====================================================

        st.markdown("---")

        st.subheader("Kết quả tính toán")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-label">TIỀN GỐC</div>
                    <div class="result-value">
                        {money(amount)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                f"""
                <div class="result-card">
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
                <div class="result-card">
                    <div class="result-label">SỐ NGÀY TÍNH LÃI</div>
                    <div class="result-value">
                        {interest_days} ngày
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        # ====================================================
        # TỔNG TIỀN
        # ====================================================

        st.markdown(
            f"""
            <div class="total-card">
                <div class="total-label">
                    TỔNG SỐ TIỀN KHÁCH HÀNG NHẬN ĐƯỢC
                </div>

                <div class="total-value">
                    {money(total)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


        # ====================================================
        # THÔNG TIN CHI TIẾT
        # ====================================================

        st.markdown("---")

        st.subheader("Chi tiết khoản tiền gửi")

        detail_col1, detail_col2 = st.columns(2)

        with detail_col1:

            st.write(
                f"**Trạng thái:** {status}"
            )

            st.write(
                f"**Ngày gửi:** {deposit_date.strftime('%d/%m/%Y')}"
            )

            st.write(
                f"**Ngày rút:** {withdrawal_date.strftime('%d/%m/%Y')}"
            )

            st.write(
                f"**Ngày đáo hạn:** {maturity.strftime('%d/%m/%Y')}"
            )

        with detail_col2:

            st.write(
                f"**Kỳ hạn:** {term} tháng"
            )

            st.write(
                f"**Lãi suất áp dụng:** {interest_rate_used:.2f}%/năm"
            )

            st.write(
                f"**Phương thức nhận lãi:** {method}"
            )

            st.write(
                f"**Phương pháp:** {interest_type}"
            )


        # ====================================================
        # THÔNG TIN GIA HẠN
        # ====================================================

        if renewal_count > 0:

            st.markdown("---")

            st.subheader("Thông tin gia hạn")

            st.write(
                f"Khoản tiền đã được gia hạn: **{renewal_count} kỳ**."
            )

            st.write(
                f"Kỳ hạn tự động gia hạn: **{term} tháng/kỳ**."
            )


        # ====================================================
        # CÔNG THỨC
        # ====================================================

        st.markdown("---")

        st.subheader("Công thức tính")

        if interest_type == "Lãi đơn":

            st.latex(
                r"""
                I=P\times r\times\frac{n}{365}
                """
            )

            st.caption(
                "Trong đó: P là tiền gốc, r là lãi suất năm, "
                "n là số ngày tính lãi."
            )

        else:

            st.latex(
                r"""
                A=P\left(1+\frac{r}{365}\right)^n
                """
            )

            st.caption(
                "Trong đó: P là tiền gốc, r là lãi suất năm, "
                "n là số ngày tính lãi."
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#777;
        padding:15px;
        font-size:13px;
    ">
        SMARTSAVE 360 • Công cụ mô phỏng tính lãi tiền gửi tiết kiệm
    </div>
    """,
    unsafe_allow_html=True
)
