import streamlit as st
import google.generativeai as genai
import os

# إعدادات الصفحة
st.set_page_config(page_title="مساعد المعلم الذكي", page_icon="📚", layout="wide")

# جلب المفتاح الآمن من Secrets
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ لم يتم العثور على المفتاح GEMINI_API_KEY في قسم Secrets!")

# اختيار جنس المستخدم لتعديل الواجهة
st.sidebar.title("⚙️ الإعدادات والبيانات")
gender = st.sidebar.radio("صفة المستخدم:", ["معلم 👨‍🏫", "معلمة 👩‍🏫"])

# تخصيص النصوص والترحيب حسب الجنس
if "معلمة" in gender:
    welcome_msg = "أهلاً بكِ يا أستاذة! دعينَا نعدّ درساً مميزاً اليوم ✨"
    btn_text = "🚀 تحضير الدرس الآن يا أستاذة"
    pronoun_text = "أعدّته المعلمة"
else:
    welcome_msg = "أهلاً بك يا أستاذ! دعنا نعد درساً مميزاً اليوم ✨"
    btn_text = "🚀 تحضير الدرس الآن يا أستاذ"
    pronoun_text = "أعدّه المعلم"

st.title("📚 مساعد المعلم الذكي - المنهج السعودي")
st.subheader(welcome_msg)

# مدخلات الدرس
with st.sidebar:
    subject = st.text_input("اسم المادة", "العلوم")
    grade = st.selectbox("الصف الدراسي", [
        "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي",
        "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي",
        "الأول متوسط", "الثاني متوسط", "الثالث متوسط", "الثانوي"
    ])
    lesson_title = st.text_input("عنوان الدرس", "الدورة الدموية")
    duration = st.slider("مدة الحصة (بالدقائق)", 30, 60, 45)
    generate_btn = st.button(btn_text)

# التوليد عبر Gemini
if generate_btn:
    if not api_key:
        st.error("يرجى التأكد من إضافة GEMINI_API_KEY في قسم Secrets قبل البدء.")
    else:
        with st.spinner("جاري التواصل مع الذكاء الاصطناعي وصياغة التحضير وفق المنهج السعودي... ⏳"):
            prompt = f"""
            بصفتك خبيراً في المنهج الوطني السعودي، قم بإعداد خطة درس متكاملة ومفصلة.
            بيانات الدرس:
            - المادة: {subject}
            - الصف: {grade}
            - عنوان الدرس: {lesson_title}
            - مدة الحصة: {duration} دقيقة
            - الصيغة الموجهة: {gender}

            قم بتضمين العناصر التالية بوضوح:
            1. أهداف الدرس ونواتج التعلم المعتمدة.
            2. نشاط التمهيد وكسر الجليد (5 دقائق).
            3. الشرح المكتوب واستراتيجيات التدريس النشط والتعديلات للتمايز (مبتدئ، متوسط، متقدم).
            4. بنك أسئلة فحص الفهم أثناء الشرح مع الإجابات النموذجية.
            5. المفاهيم الخاطئة الشائعة وكيفية معالجتها.
            6. نشاط الغلق وبطاقات الخروج (Exit Tickets).
            """
            
            try:
                response = model.generate_content(prompt)
                st.success(f"تم إعداد التحضير بنجاح! ({pronoun_text})")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بـ Gemini: {e}")
