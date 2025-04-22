
# Rest Area Manager - Cloud-Compatible Version (بدون تخزين محلي)

import pandas as pd
import streamlit as st
import datetime

st.set_page_config(page_title="استراحة الأصدقاء", layout="wide")
st.title("📋 نظام إدارة الاستراحة")

# أقسام البيانات
sections = ["الاشتراكات الشهرية", "الأعمال", "المطبخ", "الطلبات"]
section = st.sidebar.selectbox("اختر القسم", sections)

# بيانات الاشتراكات مؤقتة
def initialize_subscriptions():
    months = ["Mar-25", "Apr-25", "May-25", "Jun-25", "Jul-25", "Aug-25", "Sep-25", "Oct-25", "Nov-25", "Dec-25"]
    members = [
        "سلطان الغبيوي", "محمد الحافي", "تركي الغبيوي", "يوسف الحربي", "نواف الغضباني", "عبدالله الطويل",
        "نايف الحافي", "بدر السبيعي", "عبدالرحمن الغنامي", "دليم الحمادي", "باصر المطيري", "عبدالعزيز الشمري"
    ]
    df = pd.DataFrame(0, index=members, columns=months)
    df.loc[:, "Mar-25"] = 300
    df.index.name = "الأفراد"
    return df.reset_index()

def default_list_data(items):
    return pd.DataFrame({"العنصر": items, "القيمة": [0] * len(items)})

# ====== استخدام session_state لتخزين مؤقت ======
if "data" not in st.session_state:
    st.session_state.data = {
        "الاشتراكات": initialize_subscriptions(),
        "الأعمال": default_list_data(["كهرباء", "زراعة", "اثاث", "بلاستيكيات", "مناديل", "راتب العامل", "غاز"]),
        "المطبخ": default_list_data(["ماء", "شاهي", "قهوه", "بهارات", "رز", "دجاج", "خضار"]),
        "الطلبات": pd.DataFrame(columns=["الصنف", "الكمية", "الحالة", "التاريخ"])
    }

# عرض صفحة الاشتراكات
if section == "الاشتراكات الشهرية":
    st.header("💳 الاشتراكات الشهرية")
    df = st.session_state.data["الاشتراكات"]
    edited = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    if st.button("💾 تحديث الاشتراكات"):
        st.session_state.data["الاشتراكات"] = edited
        st.success("تم تحديث الاشتراكات مؤقتًا")

# عرض صفحة الأعمال
elif section == "الأعمال":
    st.header("🛠️ مصروفات الأعمال")
    df = st.session_state.data["الأعمال"]
    edited = st.data_editor(df, use_container_width=True)
    if st.button("💾 تحديث الأعمال"):
        st.session_state.data["الأعمال"] = edited
        st.success("تم تحديث البيانات مؤقتًا")

# عرض صفحة المطبخ
elif section == "المطبخ":
    st.header("🍽️ مصروفات المطبخ")
    df = st.session_state.data["المطبخ"]
    edited = st.data_editor(df, use_container_width=True)
    if st.button("💾 تحديث المطبخ"):
        st.session_state.data["المطبخ"] = edited
        st.success("تم تحديث البيانات مؤقتًا")

# عرض صفحة الطلبات
elif section == "الطلبات":
    st.header("🛒 الطلبات")
    df = st.session_state.data["الطلبات"]
    item = st.text_input("الصنف")
    qty = st.number_input("الكمية", min_value=1, step=1)
    status = st.selectbox("الحالة", ["مطلوب", "تم الشراء"])
    date = st.date_input("التاريخ", value=datetime.date.today())
    if st.button("➕ إضافة طلب"):
        new_row = pd.DataFrame([[item, qty, status, date]], columns=["الصنف", "الكمية", "الحالة", "التاريخ"])
        st.session_state.data["الطلبات"] = pd.concat([df, new_row], ignore_index=True)
        st.success("تمت الإضافة مؤقتًا")
    st.dataframe(st.session_state.data["الطلبات"])
