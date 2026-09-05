import streamlit as st
import google.generativeai as genai
import os

# إعدادات الصفحة
st.set_page_config(page_title="منصة المعلم الذكي المتكاملة", page_icon="🏫", layout="wide")

# جلب المفتاح الآمن
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # استخدام اسم النموذج المستقر
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.error("⚠️ لم يتم العثور على المفتاح GEMINI_API_KEY في قسم Secrets!")

# --- 1. الشريط الجانبي (Sidebar) للإعدادات ---
st.sidebar.title("⚙️ إعدادات المعلم والدرس")

# بيانات المعلم والمدرسة
st.sidebar.subheader("👤 بيانات المعلم")
teacher_name = st.sidebar.text_input("اسم المعلم/المعلمة", "أحمد")
school_name = st.sidebar.text_input("اسم المدرسة", "مدرسة النجاح")
gender = st.sidebar.radio("الجنس:", ["معلم 👨‍🏫", "معلمة 👩‍🏫"])

# بيانات الدرس
st.sidebar.subheader("📚 بيانات الدرس")
subject = st.sidebar.text_input("المادة", "العلوم")
grade = st.sidebar.selectbox("الصف الدراسي", [
    "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي",
    "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي",
    "الأول متوسط", "الثاني متوسط", "الثالث متوسط", "الثانوي"
])
lesson_title = st.sidebar.text_input("عنوان الدرس", "الدورة الدموية")
duration = st.sidebar.slider("مدة الحصة (دقائق)", 30, 60, 45)

# --- 2. الواجهة الرئيسية والتبويبات (Tabs) ---
st.title("🏫 منصة المعلم الذكي - المنهج السعودي")
st.caption(f"مرحباً بك ({teacher_name}) - {school_name}")

# إنشاء التبويبات لتنظيم الميزات الـ 12
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 التمايز وإدارة الفصل", 
    "🎨 العروض وأوراق العمل", 
    "📌 ربط المناهج والتصدير", 
    "💡 النصيحة اليومية والأدوات"
])

with tab1:
    st.header("🎯 ميزات التمايز واستراتيجيات التدريس")
    st.write("هنا ستكون ميزات التمايز، الاستراتيجيات النشطة، وبنك الأسئلة.")

with tab2:
    st.header("🎨 الأدوات التفاعلية والعروض")
    st.write("هنا ستكون ميزات العروض التقديمية، أوراق العمل، وأنشطة كسر الجليد.")

with tab3:
    st.header("📌 المناهج، التقييم والتصدير")
    st.write("هنا ستكون ميزات نواتج التعلم، سلم التقييم، وتصدير خطة الدرس.")

with tab4:
    st.header("💡 النصيحة اليومية والمساعد الصوتي")
    st.write("هنا ستكون النصيحة اليومية وسيناريو الشرح.")
