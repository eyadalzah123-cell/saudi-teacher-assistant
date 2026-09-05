import streamlit as st
import google.generativeai as genai
import os

# إعدادات الصفحة
st.set_page_config(page_title="منصة المعلم الذكي", layout="wide")

# تطبيق تنسيقات ملونة مخصصة واستدعاء خط Cairo بدون إيموجي
custom_css = """
<style>
    /* استدعاء خط Cairo من Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');

    /* تطبيق الخط على جميع النصوص في الصفحة */
    html, body, [class*="css"], div, span, button, input, select, textarea {
        font-family: 'Cairo', sans-serif !important;
    }

    /* تصميم التبويبات بألوان مختلفة */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 5px;
        color: #FFFFFF;
        font-weight: bold;
    }
    
    /* ألوان التبويبات الأربعة */
    button[id*="-tab-0"] { background-color: #1E88E5 !important; } /* أزرق */
    button[id*="-tab-1"] { background-color: #43A047 !important; } /* أخضر */
    button[id*="-tab-2"] { background-color: #FB8C00 !important; } /* برتقالي */
    button[id*="-tab-3"] { background-color: #8E24AA !important; } /* بنفسجي */
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# إعداد مفتاح API
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.error("خطأ: لم يتم العثور على المفتاح GEMINI_API_KEY في قسم Secrets")

# الشريط الجانبي للإعدادات
st.sidebar.title("إعدادات المعلم والدرس")

st.sidebar.subheader("بيانات المعلم")
teacher_name = st.sidebar.text_input("اسم المعلم أو المعلمة", "أحمد")
school_name = st.sidebar.text_input("اسم المدرسة", "مدرسة النجاح")
gender = st.sidebar.radio("الجنس", ["معلم", "معلمة"])

st.sidebar.subheader("بيانات الدرس")
subject = st.sidebar.text_input("المادة", "العلوم")
grade = st.sidebar.selectbox("الصف الدراسي", [
    "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي",
    "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي",
    "الأول متوسط", "الثاني متوسط", "الثالث متوسط", "الثانوي"
])
lesson_title = st.sidebar.text_input("عنوان الدرس", "الدورة الدموية")
duration = st.sidebar.slider("مدة الحصة بالدقائق", 30, 60, 45)
