import streamlit as st
from datetime import date
import calendar


# =========================================================
# CÁC HÀM XỬ LÝ NGÀY
# =========================================================

def add_months(start_date, months):
    """
    Cộng số tháng vào một ngày.
    Ví dụ:
    31/01 + 1 tháng = 28/02
    15/01 + 3 tháng = 15/04
    """
    month_index = start_date.month - 1 + months
    year = start_date.year + month_index // 12
    month = month_index % 12 + 1

    day = min(
        start_date.day,
        calendar.monthrange(year, month)[1]
    )

    return date(year, month, day)


def calculate_days(start_date, end_date):
    """
    Tính số ngày từ ngày bắt đầu đến trước ngày kết thúc.
    Ví dụ:
    Gửi 01/01, đáo hạn 01/02
    => 31 ngày
    """
    return (end_date - start_date).days


def format_money(value):
    return f"{value:,.0f} VNĐ"


# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="🏦",
    layout="wide"
)


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.title("🏦 ỨNG DỤNG TÍNH LÃI TIỀN GỬI TIẾT KIỆM")

st.markdown(
    """
    Ứng dụng tính tiền lãi tiền gửi tiết kiệm theo kỳ hạn, 
    hỗ trợ tự động tái tục khi đến hạn và xử lý trường hợp 
    khách hàng rút tiền trước hạn.
    """
)


# =========================================================
# NHẬP THÔNG TIN
# =========================================================

st.subheader("📋 Thông tin tiền gửi")

col1, col2 = st.columns(2)

with col1:

    principal = st.number_input(
        "Số tiền khách hàng gửi (VNĐ)",
        min_value=1000.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    fixed_rate = st.number_input(
        "Lãi suất có kỳ hạn (%/năm)",
        min_value=0.0,
        value=6.0,
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
        options=[1, 3, 6, 12, 18, 24, 36],
        format_func=lambda x: f"{x} tháng"
    )


with col2:

    deposit_date = st.date_input(
        "Ngày gửi tiền",
        value=date.today()
    )

    withdrawal_date = st.date_input(
        "Ngày rút tiền",
        value=date.today()
    )

    interest_method = st.radio(
        "Phương thức nhận tiền lãi",
        options=[
            "Nhận lãi trước",
            "Nhận lãi hàng tháng",
            "Nhận lãi cuối kỳ"
        ]
    )


# =========================================================
# KIỂM TRA NGÀY
# =========================================================

if withdrawal_date < deposit_date:
    st.error("⚠️ Ngày rút tiền không được nhỏ hơn ngày gửi tiền.")
    st.stop()


# =========================================================
# NÚT TÍNH TOÁN
# =========================================================

st.divider()

calculate_button = st.button(
    "🧮 TÍNH TOÁN",
    type="primary",
    use_container_width=True
)


# =========================================================
# TÍNH TOÁN
# =========================================================

if calculate_button:

    # -----------------------------------------------------
    # BIẾN KHỞI TẠO
    # -----------------------------------------------------

    current_start = deposit_date
    total_interest = 0
    total_interest_paid = 0
    principal_received = principal
    schedule = []

    # -----------------------------------------------------
    # XÁC ĐỊNH NGÀY ĐÁO HẠN ĐẦU TIÊN
    # -----------------------------------------------------

    maturity_date = add_months(
        deposit_date,
        term_months
    )

    # =====================================================
    # TRƯỜNG HỢP RÚT TRƯỚC HẠN
    # =====================================================

    if withdrawal_date < maturity_date:

        days = calculate_days(
            deposit_date,
            withdrawal_date
        )

        interest = (
            principal
            * non_term_rate / 100
            * days / 365
        )

        total_interest = interest

        schedule.append({
            "Kỳ": "Rút trước hạn",
            "Ngày bắt đầu": deposit_date,
            "Ngày kết thúc": withdrawal_date,
            "Số ngày": days,
            "Lãi suất": non_term_rate,
            "Loại lãi": "Không kỳ hạn",
            "Tiền lãi": interest
        })

        # -------------------------------------------------
        # KẾT QUẢ RÚT TRƯỚC HẠN
        # -------------------------------------------------

        st.subheader("📊 Kết quả tính toán")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "💰 Tiền gốc",
            format_money(principal)
        )

        c2.metric(
            "💵 Tiền lãi",
            format_money(total_interest)
        )

        c3.metric(
            "🏦 Tổng tiền nhận",
            format_money(
                principal + total_interest
            )
        )

        st.warning(
            f"Khách hàng rút trước hạn. "
            f"Tiền gửi được tính theo lãi suất không kỳ hạn "
            f"{non_term_rate:.2f}%/năm."
        )

        st.info(
            f"Thời gian tính lãi: {days} ngày "
            f"(từ {deposit_date.strftime('%d/%m/%Y')} "
            f"đến trước {withdrawal_date.strftime('%d/%m/%Y')})."
        )

        # -------------------------------------------------
        # BẢNG CHI TIẾT
        # -------------------------------------------------

        st.subheader("📑 Chi tiết tính lãi")

        st.dataframe(
            [
                {
                    "Kỳ": x["Kỳ"],
                    "Ngày bắt đầu": x["Ngày bắt đầu"].strftime("%d/%m/%Y"),
                    "Ngày kết thúc": x["Ngày kết thúc"].strftime("%d/%m/%Y"),
                    "Số ngày": x["Số ngày"],
                    "Lãi suất (%/năm)": f'{x["Lãi suất"]:.2f}',
                    "Loại lãi": x["Loại lãi"],
                    "Tiền lãi": format_money(x["Tiền lãi"])
                }
                for x in schedule
            ],
            use_container_width=True,
            hide_index=True
        )


    # =====================================================
    # TRƯỜNG HỢP ĐẾN HẠN HOẶC SAU NGÀY ĐÁO HẠN
    # =====================================================

    else:

        current_start = deposit_date
        cycle = 1

        # Số tiền lãi đã được trả trước / hàng tháng
        interest_already_paid = 0

        while current_start < withdrawal_date:

            current_maturity = add_months(
                current_start,
                term_months
            )

            # -------------------------------------------------
            # XÁC ĐỊNH NGÀY KẾT THÚC CỦA KỲ
            # -------------------------------------------------

            if withdrawal_date <= current_maturity:
                period_end = withdrawal_date
                is_maturity = withdrawal_date == current_maturity
            else:
                period_end = current_maturity
                is_maturity = True

            days = calculate_days(
                current_start,
                period_end
            )

            # -------------------------------------------------
            # NẾU RÚT ĐÚNG NGÀY ĐÁO HẠN
            # -------------------------------------------------

            if withdrawal_date == current_maturity:

                interest = (
                    principal
                    * fixed_rate / 100
                    * days / 365
                )

                # ---------------------------------------------
                # NHẬN LÃI TRƯỚC
                # ---------------------------------------------

                if interest_method == "Nhận lãi trước":

                    # Lãi của kỳ đã được nhận trước
                    interest_received_this_period = interest

                    # Nếu đây là kỳ cuối thì tiền lãi kỳ này
                    # đã nhận trước đó, tổng tiền thực nhận
                    # bao gồm cả khoản lãi đã nhận.
                    total_interest += interest

                    schedule.append({
                        "Kỳ": f"Kỳ {cycle}",
                        "Ngày bắt đầu": current_start,
                        "Ngày kết thúc": period_end,
                        "Số ngày": days,
                        "Lãi suất": fixed_rate,
                        "Loại lãi": "Nhận lãi trước",
                        "Tiền lãi": interest
                    })

                # ---------------------------------------------
                # NHẬN LÃI HÀNG THÁNG
                # ---------------------------------------------

                elif interest_method == "Nhận lãi hàng tháng":

                    monthly_interest = (
                        principal
                        * fixed_rate / 100
                        / 12
                    )

                    months_paid = term_months

                    interest_received_this_period = (
                        monthly_interest * months_paid
                    )

                    total_interest += (
                        interest_received_this_period
                    )

                    schedule.append({
                        "Kỳ": f"Kỳ {cycle}",
                        "Ngày bắt đầu": current_start,
                        "Ngày kết thúc": period_end,
                        "Số ngày": days,
                        "Lãi suất": fixed_rate,
                        "Loại lãi": "Nhận lãi hàng tháng",
                        "Tiền lãi": interest_received_this_period
                    })

                # ---------------------------------------------
                # NHẬN LÃI CUỐI KỲ
                # ---------------------------------------------

                else:

                    interest_received_this_period = interest

                    total_interest += interest

                    schedule.append({
                        "Kỳ": f"Kỳ {cycle}",
                        "Ngày bắt đầu": current_start,
                        "Ngày kết thúc": period_end,
                        "Số ngày": days,
                        "Lãi suất": fixed_rate,
                        "Loại lãi": "Nhận lãi cuối kỳ",
                        "Tiền lãi": interest
                    })

                break

            # -------------------------------------------------
            # KỲ ĐÃ ĐÁO HẠN NHƯNG KHÁCH CHƯA RÚT
            # -------------------------------------------------

            else:

                interest = (
                    principal
                    * fixed_rate / 100
                    * days / 365
                )

                # ---------------------------------------------
                # NHẬN LÃI TRƯỚC
                # ---------------------------------------------

                if interest_method == "Nhận lãi trước":

                    total_interest += interest

                    schedule.append({
                        "Kỳ": f"Kỳ {cycle}",
                        "Ngày bắt đầu": current_start,
                        "Ngày kết thúc": current_maturity,
                        "Số ngày": days,
                        "Lãi suất": fixed_rate,
                        "Loại lãi": "Nhận lãi trước",
                        "Tiền lãi": interest
                    })

                # ---------------------------------------------
                # NHẬN LÃI HÀNG THÁNG
                # ---------------------------------------------

                elif interest_method == "Nhận lãi hàng tháng":

                    monthly_interest = (
                        principal
                        * fixed_rate / 100
                        / 12
                    )

                    interest_for_period = (
                        monthly_interest * term_months
                    )

                    total_interest += (
                        interest_for_period
                    )

                    schedule.append({
                        "Kỳ": f"Kỳ {cycle}",
                        "Ngày bắt đầu": current_start,
                        "Ngày kết thúc": current_maturity,
                        "Số ngày": days,
                        "Lãi suất": fixed_rate,
                        "Loại lãi": "Nhận lãi hàng tháng",
                        "Tiền lãi": interest_for_period
                    })

                # ---------------------------------------------
                # NHẬN LÃI CUỐI KỲ
                # ---------------------------------------------

                else:

                    total_interest += interest

                    schedule.append({
                        "Kỳ": f"Kỳ {cycle}",
                        "Ngày bắt đầu": current_start,
                        "Ngày kết thúc": current_maturity,
                        "Số ngày": days,
                        "Lãi suất": fixed_rate,
                        "Loại lãi": "Nhận lãi cuối kỳ",
                        "Tiền lãi": interest
                    })

                # -------------------------------------------------
                # TỰ ĐỘNG TÁI TỤC
                # -------------------------------------------------

                current_start = current_maturity
                cycle += 1

                # Chống vòng lặp vô hạn
                if cycle > 100:
                    break


        # =====================================================
        # KẾT QUẢ CUỐI CÙNG
        # =====================================================

        total_received = principal + total_interest

        st.subheader("📊 Kết quả tính toán")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "💰 Tiền gốc",
            format_money(principal)
        )

        c2.metric(
            "💵 Tổng tiền lãi",
            format_money(total_interest)
        )

        c3.metric(
            "🏦 Tổng tiền khách hàng nhận",
            format_money(total_received)
        )

        # -----------------------------------------------------
        # THÔNG BÁO
        # -----------------------------------------------------

        if withdrawal_date == maturity_date:

            st.success(
                "✅ Khách hàng rút tiền đúng ngày đáo hạn."
            )

        else:

            number_of_terms = len(schedule)

            st.info(
                f"Khách hàng gửi {term_months} tháng nhưng "
                f"không rút đúng hạn nên tiền gửi được "
                f"tự động tái tục theo đúng kỳ hạn {term_months} tháng. "
                f"Đã tính {number_of_terms} kỳ đến ngày rút."
            )

        # -----------------------------------------------------
        # THỜI GIAN GỬI
        # -----------------------------------------------------

        total_days = calculate_days(
            deposit_date,
            withdrawal_date
        )

        st.write(
            f"📅 **Tổng thời gian gửi:** {total_days} ngày"
        )

        st.write(
            f"📅 **Ngày gửi:** "
            f"{deposit_date.strftime('%d/%m/%Y')}"
        )

        st.write(
            f"📅 **Ngày rút:** "
            f"{withdrawal_date.strftime('%d/%m/%Y')}"
        )

        # -----------------------------------------------------
        # BẢNG CHI TIẾT
        # -----------------------------------------------------

        st.subheader("📑 Lịch tính lãi và tái tục")

        table_data = []

        for item in schedule:

            table_data.append({
                "Kỳ": item["Kỳ"],
                "Ngày bắt đầu":
                    item["Ngày bắt đầu"].strftime("%d/%m/%Y"),
                "Ngày kết thúc":
                    item["Ngày kết thúc"].strftime("%d/%m/%Y"),
                "Số ngày":
                    item["Số ngày"],
                "Lãi suất (%/năm)":
                    f'{item["Lãi suất"]:.2f}',
                "Phương thức nhận lãi":
                    item["Loại lãi"],
                "Tiền lãi":
                    format_money(item["Tiền lãi"])
            })

        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# GHI CHÚ
# =========================================================

st.divider()

st.caption(
    """
    📌 Nguyên tắc tính toán:
    
    • Lãi tiền gửi có kỳ hạn được tính theo số ngày thực tế/365 ngày.
    
    • Số ngày tính lãi được xác định từ ngày gửi đến trước ngày đáo hạn 
      hoặc trước ngày khách hàng rút tiền.
    
    • Nếu khách hàng rút trước hạn thì toàn bộ số tiền gửi được áp dụng 
      lãi suất không kỳ hạn.
    
    • Nếu đến ngày đáo hạn khách hàng không rút, tiền gửi được tự động 
      tái tục theo đúng kỳ hạn ban đầu.
    
    • Lãi suất trong các kỳ tái tục được giả định giữ nguyên theo mức 
      lãi suất người dùng nhập vào ứng dụng.
    """
)
