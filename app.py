import calendar
from datetime import date, timedelta
from typing import Tuple

import streamlit as st


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Age Calculator",
    page_icon="🎂",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        .main {
            background-color: #f8fafc;
        }

        .app-container {
            max-width: 850px;
            margin: 0 auto;
        }

        .hero {
            text-align: center;
            padding: 1.5rem 0 1rem 0;
        }

        .hero-icon {
            font-size: 3.5rem;
        }

        .hero-title {
            font-size: 2.5rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 0.25rem;
        }

        .hero-subtitle {
            color: #64748b;
            font-size: 1.05rem;
        }

        .age-card {
            background: linear-gradient(135deg, #2563eb, #7c3aed);
            padding: 2rem;
            border-radius: 24px;
            text-align: center;
            color: white;
            margin: 1.5rem 0;
            box-shadow: 0 12px 35px rgba(37, 99, 235, 0.22);
        }

        .age-label {
            font-size: 1rem;
            opacity: 0.9;
            margin-bottom: 0.5rem;
        }

        .age-number {
            font-size: 2.6rem;
            font-weight: 800;
            line-height: 1.2;
        }

        .age-detail {
            font-size: 1.15rem;
            margin-top: 0.6rem;
            opacity: 0.95;
        }

        .section-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: #0f172a;
            margin: 1.5rem 0 0.8rem 0;
        }

        .stat-card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            padding: 1.2rem;
            text-align: center;
            margin-bottom: 1rem;
            box-shadow: 0 4px 15px rgba(15, 23, 42, 0.05);
        }

        .stat-icon {
            font-size: 1.5rem;
        }

        .stat-value {
            font-size: 1.45rem;
            font-weight: 750;
            color: #0f172a;
            margin-top: 0.25rem;
        }

        .stat-label {
            color: #64748b;
            font-size: 0.9rem;
            margin-top: 0.15rem;
        }

        .birthday-card {
            background: #fff7ed;
            border: 1px solid #fed7aa;
            border-radius: 20px;
            padding: 1.5rem;
            text-align: center;
            margin: 1rem 0;
        }

        .birthday-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: #9a3412;
        }

        .birthday-date {
            font-size: 1.4rem;
            font-weight: 700;
            color: #431407;
            margin-top: 0.5rem;
        }

        .birthday-days {
            color: #c2410c;
            margin-top: 0.3rem;
        }

        .info-box {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 14px;
            padding: 0.9rem 1rem;
            color: #1e3a8a;
            font-size: 0.9rem;
            margin-top: 1rem;
        }

        .footer {
            text-align: center;
            color: #94a3b8;
            font-size: 0.8rem;
            padding: 2rem 0 1rem 0;
        }

        @media (max-width: 600px) {
            .hero-title {
                font-size: 2rem;
            }

            .age-number {
                font-size: 2rem;
            }

            .age-card {
                padding: 1.5rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Age Calculation Functions
# ---------------------------------------------------------

def calculate_exact_age(
    birth_date: date,
    current_date: date
) -> Tuple[int, int, int]:
    """
    Calculate exact age in years, months, and days.

    This uses calendar arithmetic rather than dividing the
    total number of days by 365.
    """

    if birth_date > current_date:
        raise ValueError("Date of birth cannot be in the future.")

    years = current_date.year - birth_date.year
    months = current_date.month - birth_date.month
    days = current_date.day - birth_date.day

    if days < 0:
        months -= 1

        previous_month = current_date.month - 1
        previous_year = current_date.year

        if previous_month == 0:
            previous_month = 12
            previous_year -= 1

        days_in_previous_month = calendar.monthrange(
            previous_year,
            previous_month
        )[1]

        days += days_in_previous_month

    if months < 0:
        years -= 1
        months += 12

    return years, months, days


def get_birthday_date(
    birth_date: date,
    year: int
) -> date:
    """
    Return the birthday date for a specific year.

    For February 29 birthdays, February 28 is used
    during non-leap years.
    """

    if birth_date.month == 2 and birth_date.day == 29:
        if calendar.isleap(year):
            return date(year, 2, 29)

        return date(year, 2, 28)

    return date(year, birth_date.month, birth_date.day)


def calculate_next_birthday(
    birth_date: date,
    current_date: date
) -> Tuple[date, int, bool]:
    """
    Calculate the next birthday, days remaining,
    and whether today is the birthday.
    """

    birthday_this_year = get_birthday_date(
        birth_date,
        current_date.year
    )

    if birthday_this_year == current_date:
        return birthday_this_year, 0, True

    if birthday_this_year > current_date:
        next_birthday = birthday_this_year
    else:
        next_birthday = get_birthday_date(
            birth_date,
            current_date.year + 1
        )

    days_remaining = (next_birthday - current_date).days

    return next_birthday, days_remaining, False


def calculate_total_values(
    birth_date: date,
    current_date: date,
    years: int,
    months: int
) -> Tuple[int, int, int, int]:
    """
    Calculate total completed months, days, weeks,
    hours, and minutes.

    Hours and minutes are based on whole elapsed days
    because no birth time is collected.
    """

    total_days = (current_date - birth_date).days
    total_months = (years * 12) + months
    total_weeks = total_days // 7
    total_hours = total_days * 24
    total_minutes = total_hours * 60

    return (
        total_months,
        total_days,
        total_weeks,
        total_hours,
        total_minutes,
    )


# ---------------------------------------------------------
# UI Helper Functions
# ---------------------------------------------------------

def display_stat_card(
    icon: str,
    value: str,
    label: str
) -> None:
    """Display a styled statistic card."""

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-icon">{icon}</div>
            <div class="stat-value">{value}</div>
            <div class="stat-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-icon">🎂</div>
        <div class="hero-title">Age Calculator</div>
        <div class="hero-subtitle">
            Calculate your exact age and discover important birthday information.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Date Input
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">📅 Date of Birth</div>',
    unsafe_allow_html=True,
)

today = date.today()

birth_date = st.date_input(
    "Select your date of birth",
    value=None,
    min_value=date(1900, 1, 1),
    max_value=today,
    format="DD/MM/YYYY",
    label_visibility="collapsed",
)


# ---------------------------------------------------------
# Buttons
# ---------------------------------------------------------

calculate_col, reset_col = st.columns(2)

with calculate_col:
    calculate_button = st.button(
        "🎯 Calculate My Age",
        type="primary",
        use_container_width=True,
    )

with reset_col:
    reset_button = st.button(
        "🔄 Reset",
        use_container_width=True,
    )


# ---------------------------------------------------------
# Reset
# ---------------------------------------------------------

if reset_button:
    st.session_state.pop("calculated", None)
    st.session_state.pop("birth_date", None)
    st.rerun()


# ---------------------------------------------------------
# Calculate
# ---------------------------------------------------------

if calculate_button:

    if birth_date is None:
        st.error("Please select your date of birth.")

    elif birth_date > today:
        st.error("Date of birth cannot be in the future.")

    else:
        st.session_state["calculated"] = True
        st.session_state["birth_date"] = birth_date


# ---------------------------------------------------------
# Results
# ---------------------------------------------------------

if st.session_state.get("calculated"):

    selected_birth_date = st.session_state.get("birth_date")

    if selected_birth_date is None:
        st.error("Please select a valid date of birth.")
        st.stop()

    # Always get today's date dynamically.
    current_date = date.today()

    try:
        years, months, days = calculate_exact_age(
            selected_birth_date,
            current_date
        )

        (
            total_months,
            total_days,
            total_weeks,
            total_hours,
            total_minutes,
        ) = calculate_total_values(
            selected_birth_date,
            current_date,
            years,
            months,
        )

        (
            next_birthday,
            days_remaining,
            is_birthday,
        ) = calculate_next_birthday(
            selected_birth_date,
            current_date
        )

    except ValueError as error:
        st.error(str(error))
        st.stop()

    except Exception:
        st.error(
            "Something went wrong while calculating your age. "
            "Please check your date of birth and try again."
        )
        st.stop()

    # -----------------------------------------------------
    # Main Age Result
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="age-card">
            <div class="age-label">YOUR AGE</div>
            <div class="age-number">{years} Years</div>
            <div class="age-detail">
                {months} Months &nbsp;•&nbsp; {days} Days
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # Total Age
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">📊 Your Age in Numbers</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        display_stat_card(
            "📆",
            f"{total_months:,}",
            "Total Completed Months",
        )

    with col2:
        display_stat_card(
            "📅",
            f"{total_weeks:,}",
            "Total Completed Weeks",
        )

    col3, col4 = st.columns(2)

    with col3:
        display_stat_card(
            "☀️",
            f"{total_days:,}",
            "Total Days",
        )

    with col4:
        display_stat_card(
            "⏰",
            f"{total_hours:,}",
            "Approx. Hours",
        )

    col5, col6 = st.columns(2)

    with col5:
        display_stat_card(
            "⏱️",
            f"{total_minutes:,}",
            "Approx. Minutes",
        )

    with col6:
        display_stat_card(
            "🎂",
            f"{years:,}",
            "Completed Years",
        )

    # -----------------------------------------------------
    # Birthday
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">🎉 Birthday Information</div>',
        unsafe_allow_html=True,
    )

    if is_birthday:

        st.markdown(
            f"""
            <div class="birthday-card">
                <div class="birthday-title">
                    🎉 Happy Birthday!
                </div>
                <div class="birthday-date">
                    You are celebrating your {years}th birthday today!
                </div>
                <div class="birthday-days">
                    Have a wonderful birthday! 🎈
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        birthday_text = next_birthday.strftime("%d %B %Y")

        st.markdown(
            f"""
            <div class="birthday-card">
                <div class="birthday-title">
                    🎂 Next Birthday
                </div>
                <div class="birthday-date">
                    {birthday_text}
                </div>
                <div class="birthday-days">
                    {days_remaining:,} days remaining
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------
    # Information
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="info-box">
            ℹ️ <strong>Calculation note:</strong>
            Your age in years, months, and days is calculated using
            calendar dates. Hours and minutes are approximate because
            the application only asks for your date of birth, not your
            exact birth time.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if selected_birth_date.month == 2 and selected_birth_date.day == 29:
        st.markdown(
            """
            <div class="info-box">
                🗓️ <strong>February 29 birthday:</strong>
                In non-leap years, your birthday is treated as
                February 28 for the next-birthday calculation.
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        🎂 Age Calculator • Your date stays within the application
    </div>
    """,
    unsafe_allow_html=True,
)
