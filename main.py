import streamlit as st
import os
from openai import OpenAI

# إعدادات الصفحة
st.set_page_config(page_title="منصة المعلم الذكي", layout="wide")

# تطبيق تنسيقات ملونة مخصصة واستدعاء خط Cairo بدون إيموجي
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');

    html, body, [class*="css"], div, span, button, input, select, textarea {
        font-family: 'Cairo', sans-serif !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 5px;
        color: #FFFFFF;
        font-weight: bold;
    }
    
    button[id*="-tab-0"] { background-color: #1E88E5 !important; }
    button[id*="-tab-1"] { background-color: #43A047 !important; }
    button[id*="-tab-2"] { background-color: #FB8C00 !important; }
    button[id*="-tab-3"] { background-color: #8E24AA !important; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# إعداد مفتاح OpenRouter API
openrouter_key = os.environ.get("OPENROUTER_API_KEY")

if openrouter_key:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_key,
    )
else:
    st.error("خطأ: لم يتم العثور على المفتاح OPENROUTER_API_KEY في قسم Secrets")

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

# الواجهة الرئيسية
st.title("منصة المعلم الذكي - المنهج السعودي")
st.write(f"مرحباً بك {teacher_name} - {school_name}")

# دالة مساعدة لإرسال الأوامر عبر OpenRouter
def generate_ai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[
                {"role": "system", "content": "أنت مساعد معلم احترافي متخصص في المنهج السعودي."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"حدث خطأ أثناء التوليد: {e}"

# التبويبات الأربعة
tab1, tab2, tab3, tab4 = st.tabs([
    "التمايز وإدارة الفصل", 
    "العروض وأوراق العمل", 
    "ربط المناهج والتصدير", 
    "النصيحة اليومية والأدوات"
])

with tab1:
    st.header("ميزات التمايز واستراتيجيات التدريس")
    if st.button("توليد خطة التمايز والأسئلة"):
        if openrouter_key:
            with st.spinner("جاري التوليد..."):
                prompt = f"قم بصياغة شرح لدرس {lesson_title} في مادة {subject} للصف {grade} لثلاث مستويات (مبتدئ، متوسط، متفوق) مع استراتيجية تدريس نشطة وبنك أسئلة."
                result = generate_ai_response(prompt)
                st.write(result)

with tab2:
    st.header("توليد أدوات التدريس والعروض")
    if st.button("توليد محتوى العرض ورقة العمل"):
        if openrouter_key:
            with st.spinner("جاري التوليد..."):
                prompt = f"أنشئ محتوى عرض تقديمي PPT ورقة عمل مع نموذج الإجابة ونشاط كسر الجليد لدرس {lesson_title} في مادة {subject}."
                result = generate_ai_response(prompt)
                st.write(result)

with tab3:
    st.header("التكامل ومعايير المناهج")
    if st.button("ربط المناهج وسلم التقييم"):
        if openrouter_key:
            with st.spinner("جاري التوليد..."):
                prompt = f"ربط درس {lesson_title} في مادة {subject} مع نواتج التعلم وسلم التقييم Rubric وملاحظة المفاهيم الخاطئة الشائعة."
                result = generate_ai_response(prompt)
                st.write(result)

with tab4:
    st.header("النصيحة اليومية وأدوات الإغلاق")
    if st.button("توليد النصيحة وسيناريو الشرح"):
        if openrouter_key:
            with st.spinner("جاري التوليد..."):
                prompt = f"قدم نصيحة تربوية يومية للمعلم، وسيناريو صوتي للشرح، وبطاقة خروج Exit Ticket لدرس {lesson_title}."
                result = generate_ai_response(prompt)
                st.write(result)
