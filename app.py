import streamlit as st
import pandas as pd
import calendar
from datetime import date, timedelta

# =========================================================
# CẤU HÌNH TRANG
# =========================================================
st.set_page_config(
    page_title="Số tiền gửi - SMARTSAVE 360",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS - GIAO DIỆN
# =========================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Be Vietnam Pro', sans-serif;
}

.stApp {
    background:
        linear-gradient(135deg, #ffffff 0%, #fff7f7 45%, #f7faf8 100%);
}

/* Ẩn menu */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Tiêu đề */
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #111111;
    margin-top: 5px;
    margin-bottom: 0px;
}

.sub-title {
    text-align: center;
    color: #666666;
    font-size: 16px;
    margin-bottom: 15px;
}

/* Chữ chạy */
.marquee-box {
    width: 100%;
    overflow: hidden;
    background: #111111;
    color: white;
    padding: 9px 0;
    border-radius: 10px;
    margin-bottom: 18px;
    font-weight: 600;
}

.marquee-text {
    display: inline-block;
    white-space: nowrap;
    animation: marquee 18s linear infinite;
}

@keyframes marquee {
    0% {
        transform: translateX(100%);
    }
    100% {
        transform: translateX(-100%);
    }
}

/* SMARTSAVE */
.smart-card {
    background: linear-gradient(135deg, #c8102e, #e3263f);
    color: white;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0px 8px 25px rgba(200,16,46,0.25);
    margin-bottom: 20px;
}

.smart-title {
    font-size: 31px;
    font-weight: 800;
    letter-spacing: 2px;
}

.smart-desc {
    font-size: 14px;
    opacity: 0.95;
    margin-top: 5px;
}

/* Ô xanh */
.green-title {
    background: linear-gradient(90deg, #087f45, #12a05a);
    color: white;
    padding: 12px 18px;
    border-radius: 12px;
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 15px;
    box-shadow: 0px 5px 15px rgba(0,120,65,0.15);
}

/* Đang chọn */
.selected-box {
    background: #effaf4;
    border: 1.5px solid #0b8f4d;
    border-radius: 12px;
    padding: 13px 18px;
    margin-bottom: 15px;
}

.selected-title {
    color: #087f45;
    font-weight: 800;
    font-size: 17px;
}

/* Khung */
.card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #eeeeee;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

/* Kết quả */
.result-card {
    background: linear-gradient(135deg, #111111, #292929);
    color: white;
    padding: 25px;
    border-radius: 20px;
    margin-top: 20px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.18);
}

.result-big {
    font-size: 34px;
    font-weight: 800;
    color: #ffffff;
}

.result-interest {
    font-size: 25px;
    font-weight: 700;
    color: #ffffff;
}

/* Thành viên */
.member-card {
    background: white;
    border-radius: 16px;
    border: 1px solid #eeeeee;
    padding: 15px;
    text-align: center;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.05);
}

/* Nút */
.stButton > button {
    border-radius: 10px;
    font-weight: 700;
    border: 1px solid #dddddd;
    min-height: 42px;
}

.stButton > button:hover {
    border-color: #c8102e;
    color: #c8102e;
}

/* Nút tính */
.calculate-btn button {
    background: linear-gradient(90deg, #c8102e, #e3263f) !important;
    color: white !important;
    border: none !important;
    font-size: 18px !important;
    font-weight: 800 !important;
    min-height: 52px !important;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid #eeeeee;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM TÍNH TOÁN
# =========================================================

def add_months(d, months):
    """
    Cộng số tháng vào ngày.
    Nếu ngày cuối tháng không tồn tại thì lấy ngày cuối tháng.
    """
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1

    day = min(d.day, calendar.monthrange(year, month)[1])

    return date(year, month, day)


def simple_interest(principal, annual_rate, days):
    """
    Lãi đơn theo số ngày.
    """
    return principal * (annual_rate / 100) * days / 365


def compound_interest(principal, annual_rate, days):
    """
    Lãi kép theo ngày.
    Đây là mô phỏng lãi nhập gốc hằng ngày.
    """
    if days <= 0:
        return 0

    rate = annual_rate / 100

    return principal * ((1 + rate / 365) ** days - 1)


def calculate_interest(principal, rate, days, interest_type):
    if interest_type == "Lãi đơn":
        return simple_interest(principal, rate, days)

    return compound_interest(principal, rate, days)


def format_money(value):
    return f"{value:,.0f} VNĐ"


# =========================================================
# SESSION STATE
# =========================================================

if "term" not in st.session_state:
    st.session_state.term = 3

if "payment_method" not in st.session_state:
    st.session_state.payment_method = "Nhận lãi cuối kỳ"


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">SỐ TIỀN GỬI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'SMARTSAVE 360 – Công cụ mô phỏng tiền gửi tiết kiệm'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="marquee-box">
    <div class="marquee-text">
        💰 SMARTSAVE 360 &nbsp; • &nbsp;
        TÍNH LÃI TIẾT KIỆM &nbsp; • &nbsp;
        LÃI ĐƠN &nbsp; • &nbsp;
        LÃI KÉP &nbsp; • &nbsp;
        RÚT TRƯỚC HẠN &nbsp; • &nbsp;
        TỰ ĐỘNG GIA HẠN
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SMARTSAVE 360
# =========================================================

st.markdown("""
<div class="smart-card">
    <div class="smart-title">SMARTSAVE 360</div>
    <div class="smart-desc">
        Giải pháp mô phỏng tiền gửi – tính lãi – theo dõi ngày đáo hạn
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# BẢNG ĐIỀU KHIỂN
# =========================================================

st.markdown(
    '<div class="green-title">⚙️ BẢNG ĐIỀU KHIỂN</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# ĐANG CHỌN
# ---------------------------------------------------------

st.markdown(
    f"""
    <div class="selected-box">
        <div class="selected-title">✓ Đang chọn</div>
        <div style="margin-top:7px;">
            <b>Kỳ hạn:</b> {st.session_state.term} tháng
            &nbsp;&nbsp; | &nbsp;&nbsp;
            <b>Phương thức:</b> {st.session_state.payment_method}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CHỌN NHANH
# =========================================================

st.markdown("### ⚡ Chọn nhanh kỳ hạn")

quick_cols = st.columns(4)

terms = [1, 3, 6, 12]

for col, term_value in zip(quick_cols, terms):
    with col:
        if st.button(
            f"{term_value} tháng",
            use_container_width=True,
            key=f"quick_{term_value}"
        ):
            st.session_state.term = term_value
            st.rerun()


# =========================================================
# NHẬP THÔNG TIN
# =========================================================

st.markdown("### 📝 Thông tin tiền gửi")

col1, col2 = st.columns(2)

with col1:

    principal = st.number_input(
        "💰 Số tiền khách hàng gửi",
        min_value=0.0,
        value=500_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    fixed_rate = st.number_input(
        "📈 Lãi suất có kỳ hạn (%/năm)",
        min_value=0.0,
        value=5.0,
        step=0.1
    )

    nonterm_rate = st.number_input(
        "📉 Lãi suất không kỳ hạn (%/năm)",
        min_value=0.0,
        value=0.2,
        step=0.1
    )

with col2:

    deposit_date = st.date_input(
        "📅 Ngày gửi tiền",
        value=date.today()
    )

    withdrawal_date = st.date_input(
        "📅 Ngày rút tiền",
        value=add_months(date.today(), st.session_state.term)
    )

    selected_term = st.selectbox(
        "⏳ Kỳ hạn gửi tiền",
        options=[1, 3, 6, 12, 18, 24, 36],
        index=[1, 3, 6, 12, 18, 24, 36].index(
            st.session_state.term
        )
    )

    st.session_state.term = selected_term


# =========================================================
# PHƯƠNG THỨC NHẬN LÃI
# =========================================================

st.markdown("### 💳 Phương thức nhận tiền lãi")

method_cols = st.columns(3)

methods = [
    "Nhận lãi trước",
    "Nhận lãi hàng tháng",
    "Nhận lãi cuối kỳ"
]

for col, method in zip(method_cols, methods):

    with col:

        if st.button(
            method,
            use_container_width=True,
            key=f"method_{method}"
        ):
            st.session_state.payment_method = method
            st.rerun()


# =========================================================
# CHỌN LÃI ĐƠN / LÃI KÉP
# =========================================================

st.markdown("### 📊 Phương pháp tính lãi")

interest_type = st.radio(
    "Chọn phương pháp:",
    ["Lãi đơn", "Lãi kép"],
    horizontal=True
)


# =========================================================
# KIỂM TRA DỮ LIỆU
# =========================================================

if withdrawal_date < deposit_date:

    st.error(
        "❌ Ngày rút tiền không được nhỏ hơn ngày gửi tiền."
    )

    st.stop()

if principal <= 0:

    st.error(
        "❌ Số tiền gửi phải lớn hơn 0."
    )

    st.stop()


# =========================================================
# TÍNH TOÁN
# =========================================================

if st.button(
    "🧮 TÍNH TOÁN TIỀN GỬI",
    use_container_width=True,
    key="calculate"
):

    total_days = (withdrawal_date - deposit_date).days

    # -----------------------------------------------------
    # TẠO CÁC KỲ GỬI
    # -----------------------------------------------------

    periods = []

    current_start = deposit_date
    period_number = 1

    total_fixed_interest = 0
    total_paid_interest = 0

    # Kiểm tra có rút đúng ngày đáo hạn hay không
    while True:

        current_maturity = add_months(
            current_start,
            selected_term
        )

        # ---------------------------------------------
        # Trường hợp rút trước ngày đáo hạn
        # ---------------------------------------------

        if withdrawal_date < current_maturity:

            days = (
                withdrawal_date - current_start
            ).days

            # Rút trước hạn:
            # TOÀN BỘ thời gian gửi tính theo
            # lãi suất không kỳ hạn.
            interest = calculate_interest(
                principal,
                nonterm_rate,
                days,
                interest_type
            )

            periods.append({
                "Kỳ": period_number,
                "Ngày bắt đầu": current_start.strftime("%d/%m/%Y"),
                "Ngày kết thúc": withdrawal_date.strftime("%d/%m/%Y"),
                "Số ngày": days,
                "Lãi suất": f"{nonterm_rate:.2f}%",
                "Tiền lãi": interest,
                "Trạng thái": "Rút trước hạn"
            })

            total_interest = interest

            early_withdrawal = True

            break

        # ---------------------------------------------
        # Đúng ngày đáo hạn
        # ---------------------------------------------

        elif withdrawal_date == current_maturity:

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
                "Ngày bắt đầu": current_start.strftime("%d/%m/%Y"),
                "Ngày kết thúc": current_maturity.strftime("%d/%m/%Y"),
                "Số ngày": days,
                "Lãi suất": f"{fixed_rate:.2f}%",
                "Tiền lãi": interest,
                "Trạng thái": "Đáo hạn"
            })

            total_fixed_interest += interest

            early_withdrawal = False

            break

        # ---------------------------------------------
        # Đã qua đáo hạn -> tự động gia hạn
        # ---------------------------------------------

        else:

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
                "Ngày bắt đầu": current_start.strftime("%d/%m/%Y"),
                "Ngày kết thúc": current_maturity.strftime("%d/%m/%Y"),
                "Số ngày": days,
                "Lãi suất": f"{fixed_rate:.2f}%",
                "Tiền lãi": interest,
                "Trạng thái": "Đã tự động gia hạn"
            })

            total_fixed_interest += interest

            current_start = current_maturity
            period_number += 1

    # =====================================================
    # TÍNH LẠI CHO 3 PHƯƠNG THỨC NHẬN LÃI
    # =====================================================

    schedule = pd.DataFrame(periods)

    # -----------------------------------------------------
    # RÚT TRƯỚC HẠN
    # -----------------------------------------------------

    if early_withdrawal:

        total_interest = schedule["Tiền lãi"].sum()

        # Tổng khách nhận:
        total_received = principal + total_interest

        payment_note = (
            "Rút trước hạn: toàn bộ thời gian gửi "
            "được tính theo lãi suất không kỳ hạn."
        )

    # -----------------------------------------------------
    # ĐÚNG / QUA HẠN
    # -----------------------------------------------------

    else:

        total_interest = total_fixed_interest

        total_received = principal + total_interest

        payment_note = (
            "Đến hạn hoặc sau hạn: khoản tiền được "
            "tự động gia hạn đúng kỳ hạn đã chọn."
        )


    # =====================================================
    # HIỂN THỊ KẾT QUẢ
    # =====================================================

    st.markdown("""
    <div class="result-card">
        <div style="font-size:18px;font-weight:700;">
            💰 KẾT QUẢ TÍNH TOÁN
        </div>
    </div>
    """, unsafe_allow_html=True)

    r1, r2, r3 = st.columns(3)

    with r1:

        st.metric(
            "Tiền gốc",
            format_money(principal)
        )

    with r2:

        st.metric(
            "Tổng tiền lãi",
            format_money(total_interest)
        )

    with r3:

        st.metric(
            "TỔNG KHÁCH NHẬN",
            format_money(total_received)
        )


    # =====================================================
    # THÔNG TIN CHI TIẾT
    # =====================================================

    st.markdown("### 📌 Thông tin chi tiết")

    d1, d2, d3, d4 = st.columns(4)

    with d1:
        st.info(
            f"**Ngày gửi**\n\n"
            f"{deposit_date.strftime('%d/%m/%Y')}"
        )

    with d2:
        st.info(
            f"**Ngày rút**\n\n"
            f"{withdrawal_date.strftime('%d/%m/%Y')}"
        )

    with d3:
        st.info(
            f"**Tổng số ngày gửi**\n\n"
            f"{total_days} ngày"
        )

    with d4:
        st.info(
            f"**Phương thức**\n\n"
            f"{st.session_state.payment_method}"
        )


    # =====================================================
    # CẢNH BÁO
    # =====================================================

    if early_withdrawal:

        st.warning(
            "⚠️ Rút trước hạn: theo quy tắc của bài toán, "
            "toàn bộ số ngày thực gửi được tính theo "
            "lãi suất không kỳ hạn."
        )

    else:

        st.success(
            "✅ " + payment_note
        )


    # =====================================================
    # BẢNG CHI TIẾT CÁC KỲ
    # =====================================================

    st.markdown("### 📋 Bảng theo dõi kỳ gửi")

    display_df = schedule.copy()

    display_df["Tiền lãi"] = display_df["Tiền lãi"].apply(
        lambda x: f"{x:,.0f} VNĐ"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # CÔNG THỨC
    # =====================================================

    with st.expander("📚 Xem công thức tính"):

        if interest_type == "Lãi đơn":

            st.markdown("""
            **Lãi đơn:**

            `Tiền lãi = Tiền gốc × Lãi suất × Số ngày / 365`

            Trong đó:

            - Tiền gốc: số tiền khách hàng gửi
            - Lãi suất: %/năm
            - Số ngày: số ngày thực tế gửi tiền
            - Quy ước: 365 ngày/năm
            """)

        else:

            st.markdown("""
            **Lãi kép:**

            Lãi được nhập vào gốc theo từng ngày trong mô hình mô phỏng:

            `Tiền cuối kỳ = Tiền gốc × (1 + lãi suất/365)^số ngày`

            `Tiền lãi = Tiền cuối kỳ - Tiền gốc`
            """)


    # =====================================================
    # KẾT LUẬN
    # =====================================================

    st.markdown("### 📝 Kết luận")

    st.write(
        f"Khách hàng gửi **{format_money(principal)}**, "
        f"với kỳ hạn **{selected_term} tháng**, "
        f"lãi suất có kỳ hạn **{fixed_rate:.2f}%/năm** "
        f"và lãi suất không kỳ hạn **{nonterm_rate:.2f}%/năm**."
    )

    st.write(
        f"Với phương thức **{st.session_state.payment_method}** "
        f"và phương pháp **{interest_type}**, "
        f"tổng tiền khách hàng nhận được là "
        f"**{format_money(total_received)}**."
    )


# =========================================================
# KHU VỰC THÀNH VIÊN
# =========================================================

st.markdown("---")

st.markdown(
    '<div class="green-title">👥 THÀNH VIÊN NHÓM</div>',
    unsafe_allow_html=True
)

st.write(
    "Có thể tải ảnh thành viên lên trực tiếp bên dưới."
)

uploaded_images = st.file_uploader(
    "📸 Chèn hình ảnh các thành viên",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_images:

    member_cols = st.columns(min(4, len(uploaded_images)))

    for i, image in enumerate(uploaded_images):

        with member_cols[i % len(member_cols)]:

            st.image(
                image,
                use_container_width=True
            )

            st.markdown(
                f"""
                <div class="member-card">
                    <b>Thành viên {i + 1}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

else:

    st.info(
        "📷 Chưa có ảnh. Nhấn nút phía trên để chèn "
        "hình ảnh thành viên nhóm."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown("""
<div style="
    text-align:center;
    color:#777;
    padding:15px;
    font-size:13px;
">
    <b>SMARTSAVE 360</b> – Ứng dụng mô phỏng tính tiền gửi tiết kiệm<br>
    Giao diện lấy cảm hứng từ tông màu đỏ – trắng của ngân hàng.
</div>
""", unsafe_allow_html=True)
