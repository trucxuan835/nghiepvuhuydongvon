import streamlit as st
from datetime import date
import calendar


# ============================================================
# CẤU HÌNH
# ============================================================

st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="🏦",
    layout="wide"
)


# ============================================================
# HÀM XỬ LÝ
# ============================================================

def add_months(d, months):
    """
    Cộng số tháng vào ngày d.
    Nếu ngày không tồn tại trong tháng mới
    thì lấy ngày cuối cùng của tháng.
    """
    month_index = d.month - 1 + months

    year = d.year + month_index // 12
    month = month_index % 12 + 1

    last_day = calendar.monthrange(year, month)[1]

    day = min(d.day, last_day)

    return date(year, month, day)


def interest_by_days(principal, rate, days):
    """
    Tính lãi theo số ngày thực tế / 365.
    """
    return principal * rate / 100 * days / 365


def money(value):
    return f"{value:,.0f} VNĐ"


def date_text(d):
    return d.strftime("%d/%m/%Y")


# ============================================================
# TIÊU ĐỀ
# ============================================================

st.title("🏦 TÍNH LÃI TIỀN GỬI TIẾT KIỆM")

st.markdown(
    """
    **Ứng dụng mô phỏng tiền gửi tiết kiệm** với 3 phương thức nhận lãi:
    
    - Nhận lãi trước
    - Nhận lãi hàng tháng
    - Nhận lãi cuối kỳ
    
    Ứng dụng hỗ trợ tự động tái tục khi đến hạn và xử lý rút tiền trước hạn.
    """
)


# ============================================================
# NHẬP THÔNG TIN
# ============================================================

st.subheader("📋 THÔNG TIN TIỀN GỬI")

col1, col2 = st.columns(2)

with col1:

    principal = st.number_input(
        "💰 Số tiền khách hàng gửi (VNĐ)",
        min_value=1000.0,
        value=500_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    fixed_rate = st.number_input(
        "📈 Lãi suất có kỳ hạn (%/năm)",
        min_value=0.0,
        value=5.0,
        step=0.01,
        format="%.2f"
    )

    non_term_rate = st.number_input(
        "📉 Lãi suất không kỳ hạn (%/năm)",
        min_value=0.0,
        value=0.20,
        step=0.01,
        format="%.2f"
    )

    term_months = st.selectbox(
        "📅 Kỳ hạn gửi tiền",
        [1, 3, 6, 12, 18, 24, 36],
        format_func=lambda x: f"{x} tháng"
    )


with col2:

    deposit_date = st.date_input(
        "📥 Ngày gửi tiền",
        value=date.today()
    )

    withdrawal_date = st.date_input(
        "📤 Ngày rút tiền",
        value=add_months(date.today(), 3)
    )

    interest_method = st.radio(
        "💵 Phương thức nhận tiền lãi",
        [
            "Nhận lãi trước",
            "Nhận lãi hàng tháng",
            "Nhận lãi cuối kỳ"
        ]
    )


# ============================================================
# KIỂM TRA DỮ LIỆU
# ============================================================

if withdrawal_date < deposit_date:

    st.error(
        "❌ Ngày rút tiền không được nhỏ hơn ngày gửi tiền."
    )

    st.stop()


# ============================================================
# NÚT TÍNH
# ============================================================

st.divider()

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
    # BIẾN
    # --------------------------------------------------------

    current_start = deposit_date

    total_interest_entitled = 0.0

    total_interest_already_paid = 0.0

    schedule = []

    period_number = 1

    # --------------------------------------------------------
    # ĐÁO HẠN ĐẦU TIÊN
    # --------------------------------------------------------

    first_maturity = add_months(
        deposit_date,
        term_months
    )


    # ========================================================
    # TRƯỜNG HỢP RÚT TRƯỚC HẠN TRONG KỲ ĐẦU TIÊN
    # ========================================================

    if withdrawal_date < first_maturity:

        days = (
            withdrawal_date - deposit_date
        ).days

        # Lãi thực tế được hưởng khi rút trước hạn
        actual_interest = interest_by_days(
            principal,
            non_term_rate,
            days
        )

        # ----------------------------------------------------
        # XÁC ĐỊNH LÃI ĐÃ NHẬN TRƯỚC / HÀNG THÁNG
        # ----------------------------------------------------

        interest_paid_before = 0.0

        # ----------------------------------------------------
        # NHẬN LÃI TRƯỚC
        # ----------------------------------------------------

        if interest_method == "Nhận lãi trước":

            full_period_days = (
                first_maturity - deposit_date
            ).days

            full_period_interest = interest_by_days(
                principal,
                fixed_rate,
                full_period_days
            )

            # Lãi kỳ hạn đã trả trước ngay ngày gửi
            interest_paid_before = full_period_interest


        # ----------------------------------------------------
        # NHẬN LÃI HÀNG THÁNG
        # ----------------------------------------------------

        elif interest_method == "Nhận lãi hàng tháng":

            payment_date = add_months(
                deposit_date,
                1
            )

            while payment_date < withdrawal_date:

                month_days = (
                    payment_date - current_start
                ).days

                month_interest = interest_by_days(
                    principal,
                    fixed_rate,
                    month_days
                )

                interest_paid_before += month_interest

                current_start = payment_date

                payment_date = add_months(
                    deposit_date,
                    interest_paid_before_months := (
                        len(
                            [
                                x for x in []
                            ]
                        )
                    ) + 1
                )

                # Không sử dụng đoạn trên để tính lại ngày.
                # Thoát vòng lặp để dùng phương pháp an toàn bên dưới.
                break


            # Tính lại lãi đã trả hàng tháng một cách chính xác
            interest_paid_before = 0.0

            month_index = 1

            while True:

                payment_date = add_months(
                    deposit_date,
                    month_index
                )

                if payment_date >= withdrawal_date:
                    break

                previous_date = add_months(
                    deposit_date,
                    month_index - 1
                )

                month_days = (
                    payment_date - previous_date
                ).days

                interest_paid_before += interest_by_days(
                    principal,
                    fixed_rate,
                    month_days
                )

                month_index += 1


        # ----------------------------------------------------
        # LÃI CUỐI KỲ
        # ----------------------------------------------------

        else:

            interest_paid_before = 0.0


        # ----------------------------------------------------
        # TIỀN LÃI KHÁCH ĐƯỢC HƯỞNG
        # ----------------------------------------------------

        total_interest_entitled = actual_interest

        total_interest_already_paid = interest_paid_before

        # Khoản điều chỉnh khi rút trước hạn
        adjustment = (
            actual_interest
            - interest_paid_before
        )

        # Tổng tiền khách thực nhận tại thời điểm tất toán
        settlement_amount = (
            principal + adjustment
        )

        # Tổng số tiền khách đã nhận tính cả lãi đã nhận trước
        total_customer_received = (
            principal + actual_interest
        )


        schedule.append({
            "Kỳ": "Kỳ 1 - Rút trước hạn",
            "Ngày bắt đầu": deposit_date,
            "Ngày kết thúc": withdrawal_date,
            "Số ngày": days,
            "Lãi suất áp dụng": non_term_rate,
            "Tiền lãi được hưởng": actual_interest,
            "Lãi đã trả trước": interest_paid_before,
            "Điều chỉnh": adjustment
        })


        # ====================================================
        # HIỂN THỊ KẾT QUẢ
        # ====================================================

        st.subheader("📊 KẾT QUẢ")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "💰 Tiền gốc",
            money(principal)
        )

        c2.metric(
            "💵 Tiền lãi được hưởng",
            money(actual_interest)
        )

        c3.metric(
            "🏦 Tổng tiền khách được hưởng",
            money(total_customer_received)
        )


        st.warning(
            f"""
            ⚠️ Khách hàng rút trước hạn.

            Số ngày thực gửi: **{days} ngày**

            Lãi suất áp dụng: **{non_term_rate:.2f}%/năm**

            Phần lãi có kỳ hạn đã trả trước/hàng tháng được điều chỉnh
            theo mức lãi suất không kỳ hạn.
            """
        )


        if interest_paid_before > 0:

            st.info(
                f"""
                Lãi có kỳ hạn đã nhận trước/hàng tháng:
                **{money(interest_paid_before)}**

                Số tiền điều chỉnh khi tất toán:
                **{money(adjustment)}**
                """
            )


        # ----------------------------------------------------
        # BẢNG
        # ----------------------------------------------------

        st.subheader("📑 CHI TIẾT")

        display_data = []

        for x in schedule:

            display_data.append({
                "Kỳ": x["Kỳ"],
                "Ngày bắt đầu": date_text(x["Ngày bắt đầu"]),
                "Ngày kết thúc": date_text(x["Ngày kết thúc"]),
                "Số ngày": x["Số ngày"],
                "Lãi suất (%/năm)": f'{x["Lãi suất áp dụng"]:.2f}',
                "Lãi được hưởng": money(
                    x["Tiền lãi được hưởng"]
                ),
                "Lãi đã trả": money(
                    x["Lãi đã trả trước"]
                ),
                "Điều chỉnh": money(
                    x["Điều chỉnh"]
                )
            })

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )


    # ========================================================
    # TRƯỜNG HỢP ĐẾN HẠN / TÁI TỤC
    # ========================================================

    else:

        current_start = deposit_date

        while current_start < withdrawal_date:

            # ------------------------------------------------
            # NGÀY ĐÁO HẠN CỦA KỲ HIỆN TẠI
            # ------------------------------------------------

            current_maturity = add_months(
                current_start,
                term_months
            )

            # ------------------------------------------------
            # XÁC ĐỊNH NGÀY KẾT THÚC
            # ------------------------------------------------

            if withdrawal_date <= current_maturity:

                period_end = withdrawal_date

            else:

                period_end = current_maturity


            days = (
                period_end - current_start
            ).days


            # =================================================
            # KỲ KẾT THÚC BẰNG NGÀY RÚT
            # =================================================

            if withdrawal_date <= current_maturity:

                # ------------------------------------------------
                # KHÁCH RÚT ĐÚNG NGÀY ĐÁO HẠN
                # ------------------------------------------------

                if withdrawal_date == current_maturity:

                    period_interest = interest_by_days(
                        principal,
                        fixed_rate,
                        days
                    )

                    # --------------------------------------------
                    # NHẬN LÃI TRƯỚC
                    # --------------------------------------------

                    if interest_method == "Nhận lãi trước":

                        # Kỳ này đã được nhận từ đầu kỳ
                        interest_paid = period_interest

                        total_interest_entitled += (
                            period_interest
                        )

                        total_interest_already_paid += (
                            interest_paid
                        )


                    # --------------------------------------------
                    # NHẬN LÃI HÀNG THÁNG
                    # --------------------------------------------

                    elif interest_method == "Nhận lãi hàng tháng":

                        interest_paid = 0.0

                        month_start = current_start

                        month_number = 1

                        while month_number <= term_months:

                            month_end = add_months(
                                current_start,
                                month_number
                            )

                            month_end = min(
                                month_end,
                                current_maturity
                            )

                            month_days = (
                                month_end - month_start
                            ).days

                            month_interest = interest_by_days(
                                principal,
                                fixed_rate,
                                month_days
                            )

                            interest_paid += month_interest

                            month_start = month_end

                            month_number += 1

                        total_interest_entitled += (
                            interest_paid
                        )

                        total_interest_already_paid += (
                            interest_paid
                        )


                    # --------------------------------------------
                    # NHẬN LÃI CUỐI KỲ
                    # --------------------------------------------

                    else:

                        interest_paid = period_interest

                        total_interest_entitled += (
                            period_interest
                        )


                    schedule.append({
                        "Kỳ": f"Kỳ {period_number}",
                        "Ngày bắt đầu": current_start,
                        "Ngày kết thúc": current_maturity,
                        "Số ngày": days,
                        "Lãi suất": fixed_rate,
                        "Lãi kỳ này": period_interest,
                        "Lãi đã trả": interest_paid
                    })

                    break


                # ------------------------------------------------
                # TRƯỜNG HỢP RÚT TRƯỚC HẠN TRONG MỘT KỲ TÁI TỤC
                # ------------------------------------------------

                else:

                    # Lãi theo không kỳ hạn cho TOÀN BỘ
                    # khoảng thời gian gửi
                    total_days = (
                        withdrawal_date - deposit_date
                    ).days

                    actual_interest = interest_by_days(
                        principal,
                        non_term_rate,
                        total_days
                    )


                    # --------------------------------------------
                    # TÍNH TỔNG LÃI ĐÃ NHẬN TRƯỚC
                    # --------------------------------------------

                    already_paid = 0.0

                    for item in schedule:

                        already_paid += item["Lãi đã trả"]


                    # Nếu kỳ hiện tại là "lãi trước"
                    if interest_method == "Nhận lãi trước":

                        full_current_period_interest = interest_by_days(
                            principal,
                            fixed_rate,
                            (
                                current_maturity
                                - current_start
                            ).days
                        )

                        already_paid += (
                            full_current_period_interest
                        )


                    # Nếu nhận lãi hàng tháng
                    elif interest_method == "Nhận lãi hàng tháng":

                        month_index = 1

                        while True:

                            payment_date = add_months(
                                current_start,
                                month_index
                            )

                            if payment_date >= withdrawal_date:
                                break

                            previous_date = add_months(
                                current_start,
                                month_index - 1
                            )

                            month_days = (
                                payment_date - previous_date
                            ).days

                            already_paid += interest_by_days(
                                principal,
                                fixed_rate,
                                month_days
                            )

                            month_index += 1


                    # --------------------------------------------
                    # ĐIỀU CHỈNH
                    # --------------------------------------------

                    adjustment = (
                        actual_interest
                        - already_paid
                    )

                    total_customer_received = (
                        principal
                        + actual_interest
                    )

                    schedule.append({
                        "Kỳ": f"Kỳ {period_number} - Rút trước hạn",
                        "Ngày bắt đầu": current_start,
                        "Ngày kết thúc": withdrawal_date,
                        "Số ngày": (
                            withdrawal_date - current_start
                        ).days,
                        "Lãi suất": non_term_rate,
                        "Lãi kỳ này": actual_interest,
                        "Lãi đã trả": already_paid
                    })


                    # --------------------------------------------
                    # KẾT QUẢ
                    # --------------------------------------------

                    st.subheader("📊 KẾT QUẢ")

                    c1, c2, c3 = st.columns(3)

                    c1.metric(
                        "💰 Tiền gốc",
                        money(principal)
                    )

                    c2.metric(
                        "💵 Tổng lãi được hưởng",
                        money(actual_interest)
                    )

                    c3.metric(
                        "🏦 Tổng khách hàng được hưởng",
                        money(total_customer_received)
                    )

                    st.warning(
                        f"""
                        ⚠️ Khách hàng rút trước hạn trong kỳ tái tục.

                        Toàn bộ thời gian gửi được tính theo
                        lãi suất không kỳ hạn **{non_term_rate:.2f}%/năm**.

                        Tổng thời gian gửi: **{total_days} ngày**.

                        Lãi có kỳ hạn đã nhận trước/hàng tháng:
                        **{money(already_paid)}**

                        Phần điều chỉnh:
                        **{money(adjustment)}**
                        """
                    )

                    # Bảng
                    st.subheader("📑 CHI TIẾT")

                    display_data = []

                    for x in schedule:

                        display_data.append({
                            "Kỳ": x["Kỳ"],
                            "Ngày bắt đầu":
                                date_text(x["Ngày bắt đầu"]),
                            "Ngày kết thúc":
                                date_text(x["Ngày kết thúc"]),
                            "Số ngày":
                                x["Số ngày"],
                            "Lãi suất (%/năm)":
                                f'{x["Lãi suất"]:.2f}',
                            "Lãi kỳ này":
                                money(x["Lãi kỳ này"]),
                            "Lãi đã trả":
                                money(x["Lãi đã trả"])
                        })

                    st.dataframe(
                        display_data,
                        use_container_width=True,
                        hide_index=True
                    )

                    break


            # =================================================
            # KỲ ĐÃ ĐÁO HẠN NHƯNG KHÁCH KHÔNG RÚT
            # =================================================

            else:

                period_interest = interest_by_days(
                    principal,
                    fixed_rate,
                    days
                )


                # ---------------------------------------------
                # NHẬN LÃI TRƯỚC
                # ---------------------------------------------

                if interest_method == "Nhận lãi trước":

                    interest_paid = period_interest

                    total_interest_entitled += (
                        period_interest
                    )

                    total_interest_already_paid += (
                        period_interest
                    )


                # ---------------------------------------------
                # NHẬN LÃI HÀNG THÁNG
                # ---------------------------------------------

                elif interest_method == "Nhận lãi hàng tháng":

                    interest_paid = 0.0

                    month_start = current_start

                    for m in range(1, term_months + 1):

                        month_end = add_months(
                            current_start,
                            m
                        )

                        month_days = (
                            month_end - month_start
                        ).days

                        month_interest = interest_by_days(
                            principal,
                            fixed_rate,
                            month_days
                        )

                        interest_paid += month_interest

                        month_start = month_end

                    total_interest_entitled += (
                        interest_paid
                    )

                    total_interest_already_paid += (
                        interest_paid
                    )


                # ---------------------------------------------
                # NHẬN LÃI CUỐI KỲ
                # ---------------------------------------------

                else:

                    interest_paid = period_interest

                    total_interest_entitled += (
                        period_interest
                    )


                # ---------------------------------------------
                # LƯU KỲ
                # ---------------------------------------------

                schedule.append({
                    "Kỳ": f"Kỳ {period_number}",
                    "Ngày bắt đầu": current_start,
                    "Ngày kết thúc": current_maturity,
                    "Số ngày": days,
                    "Lãi suất": fixed_rate,
                    "Lãi kỳ này": period_interest,
                    "Lãi đã trả": interest_paid
                })


                # ---------------------------------------------
                # TỰ ĐỘNG TÁI TỤC
                # ---------------------------------------------

                current_start = current_maturity

                period_number += 1


        # =====================================================
        # TỔNG KẾT
        # =====================================================

        total_received = (
            principal
            + total_interest_entitled
        )


        # =====================================================
        # KẾT QUẢ
        # =====================================================

        st.subheader("📊 KẾT QUẢ TÍNH TOÁN")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "💰 TIỀN GỐC",
            money(principal)
        )

        c2.metric(
            "💵 TỔNG TIỀN LÃI",
            money(total_interest_entitled)
        )

        c3.metric(
            "🏦 TỔNG TIỀN KHÁCH NHẬN",
            money(total_received)
        )


        # =====================================================
        # THÔNG TIN TÁI TỤC
        # =====================================================

        if withdrawal_date > first_maturity:

            st.success(
                f"""
                🔄 Tiền gửi đã được tự động tái tục.

                Kỳ hạn tái tục: **{term_months} tháng**

                Số kỳ đã tính: **{len(schedule)} kỳ**

                Tiền gốc được giữ nguyên: **{money(principal)}**
                """
            )

        else:

            st.success(
                "✅ Khách hàng rút đúng ngày đáo hạn."
            )


        # =====================================================
        # BẢNG LỊCH SỬ GIAO DỊCH
        # =====================================================

        st.subheader("📑 LỊCH TÍNH LÃI VÀ TÁI TỤC")

        display_data = []

        for x in schedule:

            display_data.append({
                "Kỳ": x["Kỳ"],
                "Ngày bắt đầu":
                    date_text(x["Ngày bắt đầu"]),
                "Ngày kết thúc":
                    date_text(x["Ngày kết thúc"]),
                "Số ngày":
                    x["Số ngày"],
                "Lãi suất (%/năm)":
                    f'{x["Lãi suất"]:.2f}',
                "Tiền lãi kỳ":
                    money(x["Lãi kỳ này"]),
                "Lãi đã trả":
                    money(x["Lãi đã trả"])
            })

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )


        # =====================================================
        # TỔNG QUAN
        # =====================================================

        st.subheader("📌 TÓM TẮT")

        total_days = (
            withdrawal_date - deposit_date
        ).days

        st.write(
            f"📅 Ngày gửi: **{date_text(deposit_date)}**"
        )

        st.write(
            f"📅 Ngày rút: **{date_text(withdrawal_date)}**"
        )

        st.write(
            f"⏱️ Tổng thời gian gửi: **{total_days} ngày**"
        )

        st.write(
            f"📈 Lãi suất có kỳ hạn: "
            f"**{fixed_rate:.2f}%/năm**"
        )

        st.write(
            f"📉 Lãi suất không kỳ hạn: "
            f"**{non_term_rate:.2f}%/năm**"
        )

        st.write(
            f"💳 Phương thức nhận lãi: "
            f"**{interest_method}**"
        )


# ============================================================
# NGUYÊN TẮC
# ============================================================

st.divider()

st.caption(
    """
    NGUYÊN TẮC TÍNH:

    1. Số ngày tính lãi = Ngày kết thúc - Ngày bắt đầu.
       Ngày kết thúc không được tính vào số ngày hưởng lãi.

    2. Công thức:
       Tiền lãi = Tiền gốc × Lãi suất năm × Số ngày / 365.

    3. Rút trước hạn:
       Toàn bộ thời gian thực gửi được tính theo lãi suất không kỳ hạn.

    4. Nếu khách hàng đã nhận lãi trước hoặc lãi hàng tháng,
       khi rút trước hạn phần lãi đã nhận sẽ được điều chỉnh
       theo mức lãi suất không kỳ hạn.

    5. Nếu khách hàng không rút khi đến hạn,
       tiền gửi tự động tái tục đúng kỳ hạn ban đầu.

    6. Khi tái tục, phương thức nhận lãi được giữ nguyên.
    """
)
