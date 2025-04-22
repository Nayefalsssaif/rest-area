# Rest Area Manager - Python App for Friends (موسع بإدخال بيانات الأفراد والمصروفات)

import pandas as pd
import streamlit as st
import datetime

st.set_page_config(page_title="استراحة الأصدقاء", layout="wide")
st.title("📋 نظام إدارة الاستراحة")

# أقسام البيانات
sections = ["الاشتراكات الشهرية", "الأعمال", "المطبخ", "الطلبات"]
section = st.sidebar.selectbox("اختر القسم", sections)

# البيانات الأساسية للأفراد (مع جدول شهري)
def initialize_subscriptions():
    months = ["Mar-25", "Apr-25", "May-25", "Jun-25", "Jul-25", "Aug-25", "Sep-25", "Oct-25", "Nov-25", "Dec-25"]
    members = [
        "سلطان الغبيوي", "محمد الحافي", "تركي الغبيوي", "يوسف الحربي", "نواف الغضباني", "عبدالله الطويل",
        "نايف الحافي", "بدر السبيعي", "عبدالرحمن الغنامي", "دليم الحمادي", "نايف الحافي", "باصر المطيري", "عبدالعزيز الشمري"
    ]
    df = pd.DataFrame(0, index=members, columns=months)
    df.loc[:, "Mar-25"] = 300
    df.index.name = "الأفراد"
    return df.reset_index()

# بيانات الأعمال والمطبخ الأساسية
def default_list_data(items):
    return pd.DataFrame({"العنصر": items, "القيمة": [0] * len(items)})

# تحميل البيانات أو البدء من الصفر
@st.cache_data
def load_or_create(sheet, _default_func):
    try:
        df = pd.read_excel("rest_data.xlsx", sheet_name=sheet)
    except:
        df = _default_func()
    return df

# حفظ البيانات
def save_data(df, sheet):
    with pd.ExcelWriter("rest_data.xlsx", engine="openpyxl", mode="a", if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=sheet, index=False)

# قسم الاشتراكات الشهرية
if section == "الاشتراكات الشهرية":
    st.header("💳 الاشتراكات الشهرية")
    df = load_or_create("الاشتراكات", initialize_subscriptions)
    edited = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    if st.button("💾 حفظ الاشتراكات"):
        save_data(edited, "الاشتراكات")
        st.success("تم حفظ البيانات بنجاح")

# قسم الأعمال
elif section == "الأعمال":
    st.header("🛠️ مصروفات الأعمال")
    items = ["كهرباء", "زراعة", "اثاث", "بلاستيكيات", "مناديل", "راتب العامل", "غاز"]
    df = load_or_create("الأعمال", lambda: default_list_data(items))
    edited = st.data_editor(df, use_container_width=True)
    if st.button("💾 حفظ الأعمال"):
        save_data(edited, "الأعمال")
        st.success("تم حفظ البيانات")

# قسم المطبخ
elif section == "المطبخ":
    st.header("🍽️ مصروفات المطبخ")
    items = ["ماء", "شاهي", "قهوه", "بهارات", "رز", "دجاج", "خضار"]
    df = load_or_create("المطبخ", lambda: default_list_data(items))
    edited = st.data_editor(df, use_container_width=True)
    if st.button("💾 حفظ المطبخ"):
        save_data(edited, "المطبخ")
        st.success("تم حفظ البيانات")

# الطلبات: للمشتريات المستقبلية أو الطلبات الخاصة
elif section == "الطلبات":
    st.header("🛒 الطلبات")
    df = load_or_create("الطلبات", lambda: pd.DataFrame(columns=["الصنف", "الكمية", "الحالة", "التاريخ"]))
    item = st.text_input("الصنف")
    qty = st.number_input("الكمية", min_value=1, step=1)
    status = st.selectbox("الحالة", ["مطلوب", "تم الشراء"])
    date = st.date_input("التاريخ", value=datetime.date.today())
    if st.button("➕ إضافة طلب"):
        new_row = pd.DataFrame([[item, qty, status, date]], columns=["الصنف", "الكمية", "الحالة", "التاريخ"])
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df, "الطلبات")
        st.success("تمت الإضافة")
    st.dataframe(df)
