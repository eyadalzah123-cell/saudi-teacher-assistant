import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="منصة المعلم الذكي - المنهج السعودي",
    page_icon="🎓",
    layout="wide"
)

# 2. تنسيق الواجهة والخطوط باستخدام CSS نظيف ومباشر
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [class*="css"], div, span, button, input, select, textarea {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    
    /* تحسين شكل التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 3. التحقق من مفتاح API
if "OPENROUTER_API_KEY" not in st.secrets:
    st.error("خطأ: لم يتم العثور على المفتاح OPENROUTER_API_KEY في قسم Secrets")
    st.stop()

# 4. إعداد الاتصال بـ OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"]
)

# 5. الشريط الجانبي للإعدادات
with st.sidebar:
    st.header("إعدادات المعلم والدرس")
    
    st.subheader("بيانات المعلم")
    teacher_name = st.text_input("اسم المعلم أو المعلمة", value="أحمد")
    school_name = st.text_input("اسم المدرسة", value="مدرسة النجاح")
    gender = st.radio("الجنس", ["معلم", "معلمة"])
    
    st.divider()
    
    st.subheader("بيانات الدرس")
    subject = st.text_input("المادة", value="انجليزي")
    grade = st.selectbox("الصف الدراسي", ["الأول متوسط", "الثاني متوسط", "الثالث متوسط", "الثانوي"])
    lesson_title = st.text_input("عنوان الدرس", value="Are You on a Vacation")
    duration = st.slider("مدة الحصة بالدقائق", 15, 60, 45)

# 6. الهيدر الرئيسي للمنصة
st.title("منصة المعلم الذكي - المنهج السعودي")
st.caption(f"مرحباً بك {teacher_name} - {school_name}")
st.divider()

# 7. التبويبات الرئيسية
tab1, tab2, tab3, tab4 = st.tabs([
    "النصيحة اليومية والأدوات", 
    "ربط المناهج والتصدير", 
    "العروض وأوراق العمل", 
    "التمايز وإدارة الفصل"
])

with tab1:
    st.info("مرحباً بك في قسم النصيحة اليومية والأدوات.")

with tab2:
    st.info("قسم ربط المناهج والتصدير.")

with tab3:
    st.info("قسم العروض وأوراق العمل.")

with tab4:
    st.header("ميزات التمايز واستراتيجيات التدريس")
    
    if st.button("توليد خطة التمايز والأسئلة", type="primary"):
        with st.spinner("جاري التوليد باستخدام الذكاء الاصطناعي..."):
            try:
                # استخدام النموذج المجاني الشغال والمضمون
                response = client.chat.completions.create(
                    model="google/gemini-2.0-flash-lite-001:free",
                    messages=[
                        {
                            "role": "system",
                            "content": "أنت مساعد معلم خبير في المنهج السعودي. قم بإعداد استراتيجيات تدريس وأسئلة تمايز تتناسب مع مرحلة الدرس بأسلوب مهني ومنظم."
                        },
                        {
                            "role": "user",
                            "content": f"يرجى إعداد خطة تمايز لدرس: '{lesson_title}' لمادة: '{subject}' للصف: '{grade}' لمرحلة زمنية قدرها {duration} دقيقة."
                        }
                    ]
                )
                
                st.success("تم التوليد بنجاح!")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء التوليد: {e}")
