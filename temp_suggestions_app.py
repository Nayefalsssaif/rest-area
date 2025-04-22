
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="استراحة الثمامة", layout="wide")
st.title("🧠 صفحة المقترحات - استراحة الثمامة")

# استخدام session_state لتخزين المقترحات مؤقتًا
if "suggestions" not in st.session_state:
    st.session_state.suggestions = pd.DataFrame(columns=["المقترح", "الاسم", "التاريخ"])

# نموذج إضافة مقترح
with st.form("suggestion_form"):
    suggestion = st.text_area("✏️ اكتب مقترحك هنا:")
    name = st.text_input("👤 اسمك:")
    date = st.date_input("📅 التاريخ", value=datetime.date.today())
    submitted = st.form_submit_button("➕ إرسال المقترح")
    if submitted and suggestion and name:
        new_row = pd.DataFrame([[suggestion, name, date]], columns=["المقترح", "الاسم", "التاريخ"])
        st.session_state.suggestions = pd.concat([st.session_state.suggestions, new_row], ignore_index=True)
        st.success("✅ تم إرسال المقترح بنجاح!")

# عرض جميع المقترحات المضافة
st.write("📋 المقترحات السابقة:")
st.dataframe(st.session_state.suggestions)
