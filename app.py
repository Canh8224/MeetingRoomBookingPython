import streamlit as st
import requests
from datetime import date, time, datetime

# =========================
# CẤU HÌNH
# =========================
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Meeting Room Booking",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Ảnh lấy từ Unsplash; máy cần có Internet để tải ảnh.
HERO_IMAGE = (
    "https://images.unsplash.com/photo-1497366754035-f200968a6e72"
    "?auto=format&fit=crop&w=2000&q=85"
)

ROOM_IMAGES = [
    "https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1497366412874-3415097a27e7?auto=format&fit=crop&w=900&q=80",
]

# =========================
# CSS: GIAO DIỆN SÁNG + MENU NGANG + ẢNH NỀN
# =========================
st.markdown(
    f"""
    <style>
    :root {{
        --blue: #2878f0;
        --dark-blue: #173b70;
        --muted: #64748b;
        --page: #f3f7fc;
    }}

    .stApp {{
        background:
            linear-gradient(rgba(244,248,253,0.88), rgba(244,248,253,0.94)),
            url("{HERO_IMAGE}");
        background-size: cover;
        background-position: center top;
        background-attachment: fixed;
    }}

    [data-testid="stHeader"] {{
        background: rgba(255,255,255,0.92);
    }}

    [data-testid="stMainBlockContainer"] {{
        max-width: 1500px;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }}

    .topbar {{
        background: rgba(255,255,255,0.97);
        border: 1px solid #e5edf8;
        border-radius: 16px;
        padding: 14px 22px;
        margin-bottom: 18px;
        box-shadow: 0 5px 22px rgba(31,67,116,0.08);
    }}

    .brand {{
        font-size: 23px;
        font-weight: 800;
        color: #173b70;
        white-space: nowrap;
        padding-top: 7px;
    }}

    .hero {{
        background:
            linear-gradient(90deg, rgba(255,255,255,0.96) 0%,
            rgba(255,255,255,0.82) 48%, rgba(255,255,255,0.12) 100%),
            url("{HERO_IMAGE}");
        background-size: cover;
        background-position: center;
        border: 1px solid #e2ebf6;
        border-radius: 20px;
        min-height: 220px;
        padding: 34px 36px;
        margin-bottom: 20px;
        box-shadow: 0 8px 26px rgba(31,67,116,0.10);
    }}

    .hero-kicker {{
        color: #2878f0;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 8px;
    }}

    .hero h1 {{
        color: #173b70;
        font-size: clamp(28px, 3.2vw, 42px);
        line-height: 1.18;
        margin: 0 0 12px 0;
        font-weight: 850;
    }}

    .hero p {{
        color: #435a78;
        font-size: 16px;
        max-width: 620px;
        margin: 0;
    }}

    .section-heading {{
        color: #173b70;
        font-size: 23px;
        font-weight: 800;
        margin: 12px 0 14px 0;
    }}

    .stat-card {{
        background: rgba(255,255,255,0.96);
        border: 1px solid #e3ebf6;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 5px 18px rgba(31,67,116,0.07);
        min-height: 112px;
    }}

    .stat-label {{
        color: #64748b;
        font-size: 14px;
        margin-bottom: 8px;
    }}

    .stat-value {{
        color: #173b70;
        font-size: 30px;
        font-weight: 800;
    }}

    .panel {{
        background: rgba(255,255,255,0.96);
        border: 1px solid #e3ebf6;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 5px 18px rgba(31,67,116,0.07);
        margin-bottom: 18px;
    }}

    .room-card {{
        background: #ffffff;
        border: 1px solid #e4ebf5;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 5px 18px rgba(31,67,116,0.09);
        margin-bottom: 12px;
    }}

    .room-card img {{
        width: 100%;
        height: 160px;
        object-fit: cover;
        display: block;
    }}

    .room-card-body {{
        padding: 14px;
    }}

    .room-name {{
        color: #173b70;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 8px;
    }}

    .room-detail {{
        color: #64748b;
        font-size: 13px;
        margin: 5px 0;
    }}

    .status {{
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 8px;
    }}

    .status-ok {{
        background: #dcfce7;
        color: #15803d;
    }}

    .status-no {{
        background: #fee2e2;
        color: #b91c1c;
    }}

    div.stButton > button,
    div.stFormSubmitButton > button {{
        border-radius: 10px;
        border: 0;
        background: var(--blue);
        color: white;
        font-weight: 700;
        min-height: 42px;
    }}

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {{
        background: #1764d5;
        color: white;
        border: 0;
    }}

    div[data-testid="stMetric"] {{
        background: #fff;
        border: 1px solid #e3ebf6;
        border-radius: 15px;
        padding: 15px 18px;
        box-shadow: 0 5px 18px rgba(31,67,116,0.06);
    }}

    div[data-testid="stMetricLabel"] {{
        color: #64748b;
    }}

    div[data-testid="stMetricValue"] {{
        color: #173b70;
    }}

    .footer {{
        color: #718096;
        text-align: center;
        font-size: 13px;
        padding: 22px 0 6px 0;
    }}

    @media (max-width: 800px) {{
        .hero {{ padding: 24px 20px; }}
        .brand {{ font-size: 18px; }}
        .room-card img {{ height: 130px; }}
    }}
    
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# HÀM GỌI BACKEND
# =========================
def get_api(path):
    try:
        response = requests.get(f"{API_URL}{path}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        st.error(
            "Không kết nối được Backend FastAPI. "
            "Hãy kiểm tra API tại http://127.0.0.1:8000/docs."
        )
        return None


def format_datetime(value):
    try:
        return datetime.fromisoformat(value).strftime("%d/%m/%Y %H:%M")
    except (ValueError, TypeError):
        return str(value)


def room_image(index):
    return ROOM_IMAGES[index % len(ROOM_IMAGES)]


if "pending_navigation" in st.session_state:
    st.session_state["top_navigation"] = st.session_state.pop(
        "pending_navigation"
    )

if "top_navigation" not in st.session_state:
    st.session_state["top_navigation"] = "Trang chủ"


# =========================
# MENU BÊN TRÁI
# =========================
menu = st.sidebar.radio(
    "🏢 Meeting Room Booking",
    [
        "Trang chủ",
        "Danh sách phòng họp",
        "Đặt phòng họp",
        "Quản lý lịch đặt",
    ],
    key="top_navigation",
)


# =========================
# TRANG CHỦ
# =========================
if menu == "Trang chủ":
    st.markdown(
        """
        <section class="hero">
            <div class="hero-kicker">CHÀO MỪNG BẠN ĐẾN VỚI</div>
            <h1>Hệ thống đặt phòng họp</h1>
            <p>
                Quản lý phòng họp và lịch đặt phòng một cách nhanh chóng,
                tiện lợi và hiệu quả.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    rooms = get_api("/rooms/")
    bookings = get_api("/bookings/")

    if rooms is not None and bookings is not None:
        available_rooms = [room for room in rooms if room.get("available")]
        pending_bookings = [
            booking for booking in bookings
            if booking.get("status") == "PENDING"
        ]

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🏢 Tổng số phòng", len(rooms))
        c2.metric("✅ Phòng khả dụng", len(available_rooms))
        c3.metric("📅 Tổng lịch đặt", len(bookings))
        c4.metric("⏳ Lịch chờ xử lý", len(pending_bookings))

        left, right = st.columns([3.2, 1.25], gap="large")

        with left:
            st.markdown(
                '<div class="section-heading">🏢 Phòng họp nổi bật</div>',
                unsafe_allow_html=True,
            )

            if not rooms:
                st.info("Chưa có phòng họp trong hệ thống.")
            else:
                room_cols = st.columns(3)
                for index, room in enumerate(rooms[:6]):
                    with room_cols[index % 3]:
                        status_class = (
                            "status-ok" if room.get("available")
                            else "status-no"
                        )
                        status_text = (
                            "Đang khả dụng" if room.get("available")
                            else "Không khả dụng"
                        )
                        st.markdown(
                            f"""
                            <div class="room-card">
                                <img src="{room_image(index)}"
                                     alt="Ảnh phòng họp">
                                <div class="room-card-body">
                                    <div class="room-name">
                                        {room.get("room_name", "Phòng họp")}
                                    </div>
                                    <span class="status {status_class}">
                                        {status_text}
                                    </span>
                                    <div class="room-detail">
                                        📍 {room.get("location", "Chưa cập nhật")}
                                    </div>
                                    <div class="room-detail">
                                        👥 Sức chứa: {room.get("capacity", "—")} người
                                    </div>
                                    <div class="room-detail">
                                        📝 {room.get("note") or "Chưa có ghi chú"}
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        if st.button(
                                "📅 Đặt phòng",
                                key=f"home_book_{room.get('room_id', index)}",
                                use_container_width=True,
                                disabled=not room.get("available", False),
                        ):
                            st.session_state["selected_room_id"] = room["room_id"]
                            st.session_state["pending_navigation"] = "Đặt phòng họp"
                            st.rerun()

        with right:
            st.markdown(
                '<div class="section-heading">📅 Lịch đặt gần đây</div>',
                unsafe_allow_html=True,
            )
            if not bookings:
                st.info("Chưa có lịch đặt.")
            else:
                recent = sorted(
                    bookings,
                    key=lambda item: item.get("booking_id", 0),
                    reverse=True,
                )[:5]

                room_names = {
                    room.get("room_id"): room.get("room_name", "Phòng họp")
                    for room in rooms
                }

                for booking in recent:
                    status = booking.get("status", "PENDING")
                    if status == "CANCELLED":
                        badge = "🔴 Đã hủy"
                    elif status == "PENDING":
                        badge = "🟠 Chờ xử lý"
                    else:
                        badge = f"🟢 {status}"

                    st.markdown(
                        f"""
                        <div class="panel" style="padding:13px; margin-bottom:10px;">
                            <b style="color:#173b70;">
                                {room_names.get(booking.get("room_id"), "Phòng họp")}
                            </b><br>
                            <span style="color:#64748b;font-size:13px;">
                                🕒 {format_datetime(booking.get("start_time"))}
                            </span><br>
                            <span style="font-size:13px;">{badge}</span>
                            <span style="color:#94a3b8;font-size:12px;">
                                &nbsp; Mã lịch: {booking.get("booking_id")}
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        st.markdown(
            '<div class="footer">Chung tay xây dựng môi trường làm việc hiện đại và hiệu quả.</div>',
            unsafe_allow_html=True,
        )

# =========================
# DANH SÁCH PHÒNG HỌP
# =========================
elif menu == "Danh sách phòng họp":
    st.markdown('<div class="section-heading">🏢 Danh sách phòng họp</div>',
                unsafe_allow_html=True)
    rooms = get_api("/rooms/")

    if rooms is not None:
        col1, col2 = st.columns([2, 1])
        with col1:
            keyword = st.text_input("🔍 Tìm theo tên hoặc vị trí")
        with col2:
            availability_filter = st.selectbox(
                "Trạng thái",
                ["Tất cả", "Khả dụng", "Không khả dụng"],
            )

        filtered = []
        for room in rooms:
            searchable = (
                str(room.get("room_name", "")) + " "
                + str(room.get("location", ""))
            ).lower()
            if keyword.lower() not in searchable:
                continue
            if availability_filter == "Khả dụng" and not room.get("available"):
                continue
            if availability_filter == "Không khả dụng" and room.get("available"):
                continue
            filtered.append(room)

        st.caption(f"Tìm thấy {len(filtered)} phòng họp")
        if filtered:
            cols = st.columns(3)
            for index, room in enumerate(filtered):
                with cols[index % 3]:
                    st.image(room_image(index), use_container_width=True)
                    st.subheader(room.get("room_name", "Phòng họp"))
                    st.write(f"📍 Vị trí: {room.get('location', '—')}")
                    st.write(f"👥 Sức chứa: {room.get('capacity', '—')} người")
                    st.write(
                        "🟢 Khả dụng" if room.get("available")
                        else "🔴 Không khả dụng"
                    )
                    st.caption(room.get("note") or "Chưa có ghi chú")
                    if st.button(
                        "Đặt phòng này",
                        key=f"room_book_{room.get('room_id', index)}",
                        use_container_width=True,
                        disabled=not room.get("available", False),
                    ):
                        st.session_state["selected_room_id"] = room["room_id"]
                        st.session_state["pending_navigation"] = "Đặt phòng họp"
                        st.rerun()
        else:
            st.info("Không tìm thấy phòng phù hợp.")

# =========================
# ĐẶT PHÒNG
# =========================
elif menu == "Đặt phòng họp":
    if st.button("⬅️ Quay lại trang chủ"):
        st.session_state["pending_navigation"] = "Trang chủ"
        st.session_state.pop("selected_room_id", None)
        st.rerun()

    # Code xử lý đặt phòng hiện có của bạn tiếp tục ở đây
    st.markdown('<div class="section-heading">📅 Đặt phòng họp</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="panel">Điền thông tin cuộc họp của bạn.</div>',
                unsafe_allow_html=True)

    rooms = get_api("/rooms/")
    if rooms is not None:
        available = [room for room in rooms if room.get("available")]

        if not available:
            st.warning("Hiện không có phòng họp khả dụng.")
        else:
            room_map = {
                f"{room.get('room_name', 'Phòng')} — {room.get('location', '')} (ID {room['room_id']})":
                room["room_id"]
                for room in available
            }
            selected_room_id = st.session_state.get("selected_room_id")
            default_index = 0
            if selected_room_id is not None:
                for i, room in enumerate(available):
                    if room["room_id"] == selected_room_id:
                        default_index = i
                        break

            with st.form("booking_form", clear_on_submit=False):
                room_labels = list(room_map.keys())
                chosen_label = st.selectbox(
                    "Chọn phòng họp",
                    room_labels,
                    index=default_index,
                )
                c1, c2 = st.columns(2)
                with c1:
                    user_id = st.number_input(
                        "ID người đặt (phải tồn tại trong hệ thống)",
                        min_value=1,
                        value=1,
                        step=1,
                    )
                    booking_date = st.date_input(
                        "Ngày họp",
                        min_value=date.today(),
                        value=date.today(),
                    )
                with c2:
                    start_time = st.time_input("Giờ bắt đầu", value=time(9, 0))
                    end_time = st.time_input("Giờ kết thúc", value=time(10, 0))

                purpose = st.text_area("Mục đích cuộc họp")
                submitted = st.form_submit_button(
                    "✅ Xác nhận đặt phòng",
                    use_container_width=True,
                )

                if submitted:
                    start_dt = datetime.combine(booking_date, start_time)
                    end_dt = datetime.combine(booking_date, end_time)

                    if end_dt <= start_dt:
                        st.error("Giờ kết thúc phải sau giờ bắt đầu.")
                    else:
                        payload = {
                            "room_id": room_map[chosen_label],
                            "user_id": int(user_id),
                            "start_time": start_dt.isoformat(),
                            "end_time": end_dt.isoformat(),
                            "purpose": purpose.strip() or None,
                        }
                        try:
                            response = requests.post(
                                f"{API_URL}/bookings/",
                                json=payload,
                                timeout=10,
                            )
                            if response.status_code in (200, 201):
                                st.success("Đặt phòng thành công!")
                                st.session_state.pop("selected_room_id", None)
                            else:
                                try:
                                    detail = response.json().get("detail", response.text)
                                except ValueError:
                                    detail = response.text
                                st.error(f"Không đặt được phòng: {detail}")
                        except requests.RequestException:
                            st.error("Không kết nối được Backend FastAPI.")

# =========================
# QUẢN LÝ LỊCH ĐẶT
# =========================
elif menu == "Quản lý lịch đặt":
    st.markdown('<div class="section-heading">📋 Quản lý lịch đặt</div>',
                unsafe_allow_html=True)
    bookings = get_api("/bookings/")
    rooms = get_api("/rooms/")

    if bookings is not None and rooms is not None:
        room_names = {
            room.get("room_id"): room.get("room_name", "Phòng họp")
            for room in rooms
        }
        user_filter = st.selectbox(
            "Lọc trạng thái",
            ["Tất cả", "PENDING", "CANCELLED"],
        )

        filtered = [
            booking for booking in bookings
            if user_filter == "Tất cả"
            or booking.get("status") == user_filter
        ]

        display_rows = []
        for booking in filtered:
            display_rows.append({
                "Mã lịch": booking.get("booking_id"),
                "Phòng họp": room_names.get(booking.get("room_id"), "Phòng họp"),
                "ID người đặt": booking.get("user_id"),
                "Bắt đầu": format_datetime(booking.get("start_time")),
                "Kết thúc": format_datetime(booking.get("end_time")),
                "Mục đích": booking.get("purpose") or "",
                "Trạng thái": booking.get("status"),
            })

        if display_rows:
            st.dataframe(display_rows, use_container_width=True, hide_index=True)
        else:
            st.info("Không có lịch đặt phù hợp.")

        cancellable = [
            booking for booking in bookings
            if booking.get("status") != "CANCELLED"
        ]
        st.markdown('<div class="section-heading">Hủy lịch đặt</div>',
                    unsafe_allow_html=True)

        if cancellable:
            booking_options = {
                f"Mã {booking['booking_id']} — "
                f"{room_names.get(booking.get('room_id'), 'Phòng họp')} — "
                f"{format_datetime(booking.get('start_time'))}":
                booking["booking_id"]
                for booking in cancellable
            }

            with st.form("cancel_form"):
                selected_booking = st.selectbox(
                    "Chọn lịch muốn hủy",
                    list(booking_options.keys()),
                )
                cancel_submitted = st.form_submit_button(
                    "🗑️ Hủy lịch đặt",
                    use_container_width=True,
                )

            if cancel_submitted:
                booking_id = booking_options[selected_booking]
                try:
                    response = requests.put(
                        f"{API_URL}/bookings/{booking_id}/cancel",
                        timeout=10,
                    )
                    if response.status_code == 200:
                        st.success("Đã hủy lịch đặt.")
                        st.rerun()
                    else:
                        st.error(f"Không hủy được lịch: {response.text}")
                except requests.RequestException:
                    st.error("Không kết nối được Backend FastAPI.")
        else:
            st.info("Không còn lịch đặt nào cần hủy.")
