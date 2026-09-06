import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة والخطوط
st.set_page_config(
    page_title="منصة المعلم الذكي - المنهج السعودي",
    page_icon="🎓",
    layout="wide"
)

# تطبيق خط Cairo عبر CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# 2. التحقق من وجود مفتاح API في Secrets
if "OPENROUTER_API_KEY" not in st.secrets:
    st.error("خطأ: لم يتم العثور على المفتاح OPENROUTER_API_KEY في قسم Secrets")
    st.stop()

# 3. إعداد العميل (OpenAI Client) المربوط بـ OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"]
)

# 4. واجهة المستخدم والتجانبات
st.title("منصة المعلم الذكي - المنهج السعودي")
st.subheader("مرحباً بك أحمد - مدرسة النجاح")

# الشريط الجانبي للإعدادات
with st.sidebar:
    st.header("إعدادات المعلم والدرس")
    st.subheader("بيانات المعلم")
    teacher_name = st.text_input("اسم المعلم أو المعلمة", value="أحمد")
    school_name = st.text_input("اسم المدرسة", value="مدرسة النجاح")
    gender = st.radio("الجنس", ["معلم", "معلمة"])
    
    st.subheader("بيانات الدرس")
    subject = st.text_input("المادة", value="انجليزي")
    grade = st.selectbox("الصف الدراسي", ["الأول متوسط", "الثاني متوسط", "الثالث متوسط", "الثانوي"])
    lesson_title = st.text_input("عنوان الدرس", value="Are You on a Vacation")
    duration = st.slider("مدة الحصة بالدقائق", 15, 60, 45)

# التبويبات الرئيسية
tab1, tab2, tab3, tab4 = st.tabs([
    "النصيحة اليومية والأدوات", 
    "ربط المناهج والتصدير", 
    "العروض وأوراق العمل", 
    "التمايز وإدارة الفصل"
])

with tab4:
    st.header("ميزات التمايز واستراتيجيات التدريس")
    
    if st.button("توليد خطة التمايز والأسئلة"):
        with st.spinner("جاري التوليد باستخدام الذكاء الاصطناعي..."):
            try:
                # استخدام النموذج المجاني المحدث
                response = client.chat.completions.create(
                    model="meta-llama/llama-3.3-70b-instruct:free",
                    messages=[
                        {
                            "role": "system",
                            "content": "أنت مساعد معلم خبير في المنهج السعودي. قم بإعداد استراتيجيات تدريس وأسئلة تمايز تتناسب مع مرحلة الدرس."
                        },
                        {
                            "role": "user",
                            "content": f"يرجى إعداد خطة تمايز لدرس: '{lesson_title}' لمادة: '{subject}' للصف: '{grade}' لمرحلة زمنية قدرها {duration} دقيقة."
                        }
                    ]
                )
                
                st.success("تم التوليد بنجاح!")
                st.write(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء التوليد: {e}")
