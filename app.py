import streamlit as st
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd

# =========================================================
# CẤU HÌNH TRANG
# =========================================================
st.set_page_config(
    page_title="SMARTSAVE 360",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
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
    background: linear-gradient(135deg, #ffffff 0%, #fff7f7 45%, #f5f5f5 100%);
}

/* Header */
.main-title {
    background: linear-gradient(90deg, #E31837, #b4001b);
    color: white;
    padding: 22px 30px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(227,24,55,0.25);
    margin-bottom: 15px;
}

.main-title h1 {
    font-size: 38px;
    font-weight: 800;
    margin: 0;
    letter-spacing: 2px;
}

.main-title p {
    margin: 6px 0 0 0;
    font-size: 15px;
    opacity: 0.95;
}

/* Chữ chạy */
.marquee {
    background: #111111;
    color: white;
    padding: 9px 0;
    overflow: hidden;
    white-space: nowrap;
    border-radius: 10px;
    margin-bottom: 20px;
}

.marquee-text {
    display: inline-block;
    padding-left: 100%;
    animation: marquee 18s linear infinite;
    font-weight: 600;
    color: #ffffff;
}

@keyframes marquee {
    0% {
        transform: translateX(0%);
    }
    100% {
        transform: translateX(-100%);
    }
}

/* Box */
.section-box {
    background: white;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 18px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    border: 1px solid #eeeeee;
}

.section-title {
    background: linear-gradient(90deg, #E31837, #c90020);
    color: white;
    padding: 12px 18px;
    border-radius: 10px;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 18px;
}

/* SMARTSAVE */
.smart-box {
    background: linear-gradient(135deg, #111111, #2a2a2a);
    color: white;
    border-radius: 18px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    margin-bottom: 20px;
}

.smart-box .smart-name {
    color: #E31837;
    font-size: 31px;
    font-weight: 800;
    letter-spacing: 3px;
}

.smart-box .smart-sub {
    font-size: 14px;
    margin-top: 7px;
    color: #dddddd;
}

/* Đang chọn */
.selected-box {
    background: #fff1f3;
    border-left: 6px solid #E31837;
    border-radius: 10px;
    padding: 13px 18px;
    margin: 10px 0 18px 0;
}

.selected-box span {
    color: #E31837;
    font-weight: 800;
}

/* Input */
div[data-baseweb="input"] {
    border-radius: 9px;
}

div[data-baseweb="select"] {
    border-radius: 9px;
}

/* Button */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    border: none;
    background: linear-gradient(90deg, #E31837, #b8001d);
    color: white;
    font-weight: 800;
    padding: 12px;
    font-size: 16px;
    transition: 0.3s;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #b8001d, #E31837);
    transform: translateY(-2px);
    box-shadow: 0 7px 18px rgba(227,24,55,0.3);
}

/* Metrics */
.metric-box {
    background: white;
    border-radius: 15px;
    padding: 18px;
    text-align: center;
    border-top: 5px solid #E31837;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
}

.metric-label {
    color: #666;
    font-size: 14px;
    font-weight: 600;
}

.metric-value {
    color: #E31837;
    font-size: 25px;
    font-weight: 800;
    margin-top: 5px;
}

/* Kết quả */
.result-main {
    background: linear-gradient(135deg, #111111, #272727);
    color: white;
    border-radius: 18px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 8px 30px rgba(0,0,0,0.18);
}

.result-main .amount {
    color: #ff294d;
    font-size: 36px;
    font-weight: 800;
}

.result-main .label {
    color: #eeeeee;
    font-size: 15px;
}

/* Footer */
.footer {
    text-align: center;
    color: #777;
    padding: 20px;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM HỖ TRỢ
# =========================================================

def money(value):
    return f"{value:,.0f} VNĐ"


def add_months(d, months):
    return d + relativedelta(months=months)


def maturity_date(deposit_date, term_months):
    return add_months(deposit_date, term_months)


def calculate_days(start, end):
    """
    Tính số ngày từ ngày gửi đến ngày rút.
    Ngày gửi được tính, ngày rút không tính.
    """
    return max((end - start).days, 0)


def simple_interest(principal, rate, days):
    """
    Lãi đơn theo số ngày thực tế / 365.
    """
    return principal * rate / 100 * days / 365


def compound_period(principal, rate, months):
    """
    Lãi kép cho một kỳ hạn.
    Lãi được nhập vào gốc khi gia hạn.
    """
    return principal * ((1 + rate / 100) ** (months / 12)) - principal


def calculate_deposit(
    principal,
    fixed_rate,
    nonterm_rate,
    deposit_date,
    withdrawal_date,
    term_months,
    method,
    interest_type
):

    maturity = maturity_date(deposit_date, term_months)

    rows = []

    # =====================================================
    # TRƯỜNG HỢP RÚT TRƯỚC HẠN
    # =====================================================
    if withdrawal_date < maturity:

        days = calculate_days(deposit_date, withdrawal_date)

        # Rút trước hạn -> toàn bộ thời gian hưởng lãi không kỳ hạn
        interest = simple_interest(
            principal,
            nonterm_rate,
            days
        )

        rows.append({
            "Kỳ": "Kỳ rút trước hạn",
            "Loại lãi": "Lãi không kỳ hạn",
            "Từ ngày": deposit_date.strftime("%d/%m/%Y"),
            "Đến trước ngày": withdrawal_date.strftime("%d/%m/%Y"),
            "Số ngày": days,
            "Số dư tính lãi": principal,
            "Lãi suất": nonterm_rate,
            "Tiền lãi": interest
        })

        total_interest = interest
        total_received = principal + total_interest

        return {
            "maturity": maturity,
            "days": days,
            "total_interest": total_interest,
            "total_received": total_received,
            "rows": rows,
            "status": "Rút trước hạn – áp dụng lãi suất không kỳ hạn"
        }

    # =====================================================
    # TRƯỜNG HỢP RÚT ĐÚNG HẠN
    # =====================================================
    if withdrawal_date == maturity:

        days = calculate_days(deposit_date, maturity)

        if interest_type == "Lãi đơn":
            interest = simple_interest(
                principal,
                fixed_rate,
                days
            )
        else:
            interest = compound_period(
                principal,
                fixed_rate,
                term_months
            )

        rows.append({
            "Kỳ": "Kỳ 1",
            "Loại lãi": "Lãi có kỳ hạn",
            "Từ ngày": deposit_date.strftime("%d/%m/%Y"),
            "Đến trước ngày": maturity.strftime("%d/%m/%Y"),
            "Số ngày": days,
            "Số dư tính lãi": principal,
            "Lãi suất": fixed_rate,
            "Tiền lãi": interest
        })

        total_interest = interest

        # -------------------------------------------------
        # Nhận lãi trước
        # -------------------------------------------------
        if method == "Nhận lãi trước":
            total_received = principal + interest

        # -------------------------------------------------
        # Nhận lãi hàng kỳ
        # -------------------------------------------------
        elif method == "Nhận lãi hàng kỳ":
            total_received = principal + interest

        # -------------------------------------------------
        # Nhận lãi cuối kỳ
        # -------------------------------------------------
        else:
            total_received = principal + interest

        return {
            "maturity": maturity,
            "days": days,
            "total_interest": total_interest,
            "total_received": total_received,
            "rows": rows,
            "status": "Rút đúng hạn – áp dụng lãi suất có kỳ hạn"
        }

    # =====================================================
    # TRƯỜNG HỢP RÚT SAU HẠN
    # NGÂN HÀNG TỰ ĐỘNG GIA HẠN ĐÚNG KỲ HẠN
    # =====================================================

    current_start = deposit_date
    current_end = maturity
    current_principal = principal
    total_interest = 0
    period = 1

    # -----------------------------------------------------
    # XỬ LÝ CÁC KỲ ĐÃ ĐỦ HẠN
    # -----------------------------------------------------
    while current_end <= withdrawal_date:

        days = calculate_days(current_start, current_end)

        if interest_type == "Lãi đơn":
            interest = simple_interest(
                current_principal,
                fixed_rate,
                days
            )
        else:
            interest = compound_period(
                current_principal,
                fixed_rate,
                term_months
            )

        rows.append({
            "Kỳ": f"Kỳ {period}",
            "Loại lãi": "Lãi có kỳ hạn",
            "Từ ngày": current_start.strftime("%d/%m/%Y"),
            "Đến trước ngày": current_end.strftime("%d/%m/%Y"),
            "Số ngày": days,
            "Số dư tính lãi": current_principal,
            "Lãi suất": fixed_rate,
            "Tiền lãi": interest
        })

        total_interest += interest

        # -------------------------------------------------
        # LÃI KÉP:
        # Lãi được nhập gốc khi gia hạn
        # -------------------------------------------------
        if interest_type == "Lãi kép":
            current_principal += interest

        current_start = current_end
        current_end = add_months(current_end, term_months)
        period += 1

    # =====================================================
    # PHẦN LẺ SAU KỲ HẠN CUỐI
    # =====================================================

    if current_start < withdrawal_date:

        remaining_days = calculate_days(
            current_start,
            withdrawal_date
        )

        # Phần sau hạn hưởng lãi không kỳ hạn
        interest = simple_interest(
            current_principal,
            nonterm_rate,
            remaining_days
        )

        rows.append({
            "Kỳ": f"Kỳ {period}",
            "Loại lãi": "Lãi không kỳ hạn",
            "Từ ngày": current_start.strftime("%d/%m/%Y"),
            "Đến trước ngày": withdrawal_date.strftime("%d/%m/%Y"),
            "Số ngày": remaining_days,
            "Số dư tính lãi": current_principal,
            "Lãi suất": nonterm_rate,
            "Tiền lãi": interest
        })

        total_interest += interest

    # =====================================================
    # TÍNH TỔNG TIỀN NHẬN
    # =====================================================

    if interest_type == "Lãi kép":

        # current_principal đã bao gồm lãi của các kỳ đủ hạn
        # nhưng chưa cộng phần lãi không kỳ hạn cuối
        total_received = current_principal + (
            rows[-1]["Tiền lãi"]
            if rows[-1]["Loại lãi"] == "Lãi không kỳ hạn"
            else 0
        )

    else:
        total_received = principal + total_interest

    return {
        "maturity": maturity,
        "days": calculate_days(deposit_date, withdrawal_date),
        "total_interest": total_interest,
        "total_received": total_received,
        "rows": rows,
        "status": "Rút sau hạn – ngân hàng tự động gia hạn theo đúng kỳ hạn"
    }


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="main-title">
    <h1>💰 SMARTSAVE 360</h1>
    <p>HỆ THỐNG TÍNH LÃI TIỀN GỬI TIẾT KIỆM</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="marquee">
    <div class="marquee-text">
        SMARTSAVE 360  •  TÍNH LÃI NHANH  •  MINH BẠCH  •  CHÍNH XÁC  •
        LÃI ĐƠN  •  LÃI KÉP  •  LÃI CÓ KỲ HẠN  •  LÃI KHÔNG KỲ HẠN
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SMARTSAVE 360
# =========================================================

st.markdown("""
<div class="smart-box">
    <div class="smart-name">SMARTSAVE 360</div>
    <div class="smart-sub">
        Công cụ mô phỏng tiền gửi tiết kiệm và tiền lãi khách hàng nhận được
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div class="section-title">
        BẢNG ĐIỀU KHIỂN
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="selected-box">
        <span>Đang chọn:</span><br>
        Tính tiền lãi tiết kiệm
    </div>
    """, unsafe_allow_html=True)

    if st.button("Chọn nhanh"):
        st.session_state["quick"] = True
    else:
        st.session_state.setdefault("quick", False)

    st.markdown("---")

    st.markdown("### Loại tính lãi")

    interest_type = st.radio(
        "Chọn phương pháp",
        [
            "Lãi đơn",
            "Lãi kép"
        ],
        index=0
    )

    st.markdown("---")

    st.info(
        "Rút trước hạn: áp dụng lãi suất không kỳ hạn.\n\n"
        "Rút sau hạn: hệ thống tự động gia hạn theo đúng kỳ hạn."
    )


# =========================================================
# THÔNG TIN TIỀN GỬI
# =========================================================

st.markdown("""
<div class="section-box">
<div class="section-title">Số tiền gửi</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    principal = st.number_input(
        "Số tiền khách hàng gửi (VNĐ)",
        min_value=0.0,
        value=500_000_000.0,
        step=10_000_000.0,
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
    nonterm_rate = st.number_input(
        "Lãi suất không kỳ hạn (%/năm)",
        min_value=0.0,
        value=0.2,
        step=0.1
    )


# =========================================================
# NGÀY GỬI - NGÀY RÚT
# =========================================================

st.markdown("""
<div class="section-box">
<div class="section-title">Thời gian gửi tiền</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    deposit_date = st.date_input(
        "Ngày gửi tiền",
        value=date(2026, 8, 23)
    )

with col2:
    withdrawal_date = st.date_input(
        "Ngày rút tiền",
        value=date(2026, 11, 23)
    )

with col3:
    term_months = st.selectbox(
        "Kỳ hạn gửi tiền",
        [1, 2, 3, 6, 9, 12, 18, 24, 36],
        index=2,
        format_func=lambda x: f"{x} tháng"
    )


# =========================================================
# PHƯƠNG THỨC NHẬN LÃI
# =========================================================

st.markdown("""
<div class="section-box">
<div class="section-title">Phương thức nhận tiền lãi</div>
</div>
""", unsafe_allow_html=True)

method = st.radio(
    "Khách hàng lựa chọn",
    [
        "Nhận lãi trước",
        "Nhận lãi hàng kỳ",
        "Nhận lãi cuối kỳ"
    ],
    horizontal=True
)

st.markdown("""
<div class="selected-box">
    <span>Đang chọn:</span>
    """ + method + """
</div>
""", unsafe_allow_html=True)


# =========================================================
# NÚT TÍNH
# =========================================================

st.markdown("")

calculate = st.button("🧮 TÍNH TOÁN TIỀN GỬI")


# =========================================================
# KẾT QUẢ
# =========================================================

if calculate:

    if principal <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")

    elif withdrawal_date <= deposit_date:
        st.error("Ngày rút tiền phải sau ngày gửi tiền.")

    else:

        result = calculate_deposit(
            principal=principal,
            fixed_rate=fixed_rate,
            nonterm_rate=nonterm_rate,
            deposit_date=deposit_date,
            withdrawal_date=withdrawal_date,
            term_months=term_months,
            method=method,
            interest_type=interest_type
        )

        st.markdown("---")

        # =================================================
        # TRẠNG THÁI
        # =================================================

        if "trước hạn" in result["status"]:
            st.warning("⚠️ " + result["status"])

        elif "đúng hạn" in result["status"]:
            st.success("✅ " + result["status"])

        else:
            st.info("🔄 " + result["status"])

        # =================================================
        # THÔNG TIN TỔNG QUAN
        # =================================================

        st.markdown("""
        <div class="section-title">
            KẾT QUẢ TÍNH TOÁN
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">TIỀN GỐC</div>
                <div class="metric-value">{money(principal)}</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">TỔNG TIỀN LÃI</div>
                <div class="metric-value">{money(result["total_interest"])}</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">SỐ NGÀY TÍNH LÃI</div>
                <div class="metric-value">{result["days"]} ngày</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        # =================================================
        # TỔNG TIỀN NHẬN
        # =================================================

        st.markdown(f"""
        <div class="result-main">
            <div class="label">
                TỔNG SỐ TIỀN KHÁCH HÀNG NHẬN ĐƯỢC
            </div>
            <div class="amount">
                {money(result["total_received"])}
            </div>
            <div class="label">
                Gồm tiền gốc + tiền lãi
            </div>
        </div>
        """, unsafe_allow_html=True)

        # =================================================
        # THÔNG TIN KỲ HẠN
        # =================================================

        st.markdown("")
        st.markdown("""
        <div class="section-title">
            THÔNG TIN KỲ HẠN
        </div>
        """, unsafe_allow_html=True)

        maturity = result["maturity"]

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Ngày gửi",
                deposit_date.strftime("%d/%m/%Y")
            )

        with c2:
            st.metric(
                "Ngày đáo hạn đầu tiên",
                maturity.strftime("%d/%m/%Y")
            )

        with c3:
            st.metric(
                "Ngày rút",
                withdrawal_date.strftime("%d/%m/%Y")
            )

        with c4:
            st.metric(
                "Phương pháp",
                interest_type
            )

        # =================================================
        # BẢNG CHI TIẾT TỪNG KỲ
        # =================================================

        st.markdown("")
        st.markdown("""
        <div class="section-title">
            CHI TIẾT KỲ TÍNH LÃI
        </div>
        """, unsafe_allow_html=True)

        df = pd.DataFrame(result["rows"])

        if not df.empty:

            df["Số dư tính lãi"] = df["Số dư tính lãi"].apply(
                lambda x: f"{x:,.0f}"
            )

            df["Lãi suất"] = df["Lãi suất"].apply(
                lambda x: f"{x:.2f}%/năm"
            )

            df["Tiền lãi"] = df["Tiền lãi"].apply(
                lambda x: f"{x:,.0f}"
            )

            df = df.rename(columns={
                "Kỳ": "Kỳ tính lãi",
                "Loại lãi": "Loại lãi áp dụng",
                "Từ ngày": "Từ ngày",
                "Đến trước ngày": "Đến trước ngày",
                "Số ngày": "Số ngày",
                "Số dư tính lãi": "Số dư tính lãi (VNĐ)",
                "Lãi suất": "Lãi suất",
                "Tiền lãi": "Tiền lãi (VNĐ)"
            })

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        # =================================================
        # GIẢI THÍCH
        # =================================================

        st.markdown("")
        st.markdown("""
        <div class="section-title">
            DIỄN GIẢI CÁCH TÍNH
        </div>
        """, unsafe_allow_html=True)

        if withdrawal_date < maturity:

            st.error(
                "Khách hàng rút trước hạn nên toàn bộ thời gian gửi "
                "được tính theo lãi suất không kỳ hạn."
            )

        elif withdrawal_date == maturity:

            st.success(
                "Khách hàng rút đúng ngày đáo hạn nên được hưởng "
                "lãi suất có kỳ hạn."
            )

        else:

            st.info(
                "Khách hàng rút sau ngày đáo hạn. Hệ thống đã tự động "
                "gia hạn tiền gửi theo đúng kỳ hạn ban đầu. Các kỳ đủ "
                "hạn được tính lãi có kỳ hạn; phần ngày còn lại sau "
                "kỳ hạn cuối được tính lãi không kỳ hạn."
            )

        if method == "Nhận lãi trước":

            st.write(
                "• Nhận lãi trước: tiền lãi của kỳ được xác định và "
                "chi trả ngay từ đầu kỳ."
            )

        elif method == "Nhận lãi hàng kỳ":

            st.write(
                "• Nhận lãi hàng kỳ: tiền lãi được xác định theo từng "
                "kỳ tính lãi."
            )

        else:

            st.write(
                "• Nhận lãi cuối kỳ: tiền lãi được thanh toán cùng "
                "tiền gốc khi kết thúc kỳ gửi."
            )

        if interest_type == "Lãi đơn":

            st.write(
                "• Lãi đơn: tiền lãi được tính trên số tiền gốc ban đầu."
            )

        else:

            st.write(
                "• Lãi kép: tiền lãi của mỗi kỳ đủ hạn được nhập vào "
                "gốc để tiếp tục tính lãi cho kỳ tiếp theo."
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    SMARTSAVE 360 • Công cụ mô phỏng tính lãi tiền gửi tiết kiệm
</div>
""", unsafe_allow_html=True)
