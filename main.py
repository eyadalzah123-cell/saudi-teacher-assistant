"""المعلم الذكي — واجهة عربية محسنة لـ Streamlit + OpenRouter."""
import os
import re
from datetime import datetime

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="المعلم الذكي | مساعد المعلم السعودي", page_icon="📗", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;600;700;800&display=swap');
:root { --green:#166534; --mint:#edf8f0; --ink:#17372b; }
html, body, [class*="css"], [data-testid="stApp"], button, input, textarea, select,
[data-testid="stWidgetLabel"] { font-family:'Tajawal',sans-serif !important; }
.stApp {direction:rtl; color:var(--ink); background:linear-gradient(180deg,#f3faf5 0%,#fff 45%); }
[data-testid="stSidebar"] {background:#f1f8f2; border-left:1px solid #d7e7d9; }
[data-testid="stSidebar"] * {text-align:right;}
[data-testid="stHeader"] {background:transparent;}
h1,h2,h3 {color:#174a32!important; letter-spacing:0;}
h1 {font-weight:800!important; font-size:2.15rem!important;}
[data-testid="stMarkdownContainer"] {text-align:right;}
[data-testid="stTabs"] [data-baseweb="tab-list"] {gap:.5rem;flex-wrap:wrap;justify-content:flex-start;}
[data-testid="stTabs"] button[role="tab"] {border-radius:12px 12px 0 0; padding:.75rem 1rem; color:#24563a; font-weight:700; background:#f2f8f3;}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {background:#166534;color:white;}
.stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] button {background:#166534!important;color:white!important;border:1px solid #166534!important;border-radius:11px!important;font-weight:700;}
.stButton > button, [data-testid="stDownloadButton"] button {border-radius:11px!important;}
[data-testid="stAlert"] {border-radius:12px;}
[data-baseweb="select"] *, input, textarea {text-align:right!important;}
.hero {border:1px solid #d4e9d9;background:linear-gradient(110deg,#e8f7ed,#f8fcf9);padding:24px;border-radius:20px;margin-bottom:20px;}
.hero .eyebrow {font-size:.84rem;color:#408156;font-weight:700;}
.hero .heading {font-size:2rem;font-weight:800;color:#14532d;line-height:1.5;}
.hero .sub {color:#516b5a;line-height:1.85;}
.small-note {font-size:.84rem;color:#637a6c;}
</style>
""", unsafe_allow_html=True)

GRADES = ["الأول الابتدائي","الثاني الابتدائي","الثالث الابتدائي","الرابع الابتدائي","الخامس الابتدائي","السادس الابتدائي","الأول المتوسط","الثاني المتوسط","الثالث المتوسط","الأول الثانوي","الثاني الثانوي","الثالث الثانوي"]
SUBJECTS = ["اللغة العربية","الرياضيات","العلوم","الدراسات الإسلامية","اللغة الإنجليزية","الدراسات الاجتماعية","المهارات الرقمية","التقنية الرقمية","الفيزياء","الكيمياء","الأحياء","المهارات الحياتية والأسرية","التفكير الناقد","التربية الفنية","التربية البدنية والدفاع عن النفس","مادة أخرى"]
TOOLS = {
    "تحضير الدرس": "أنشئ تحضيرًا متكاملًا للحصة يشمل الأهداف السلوكية القابلة للقياس، التهيئة، المتطلبات السابقة، سير الدرس موزعًا على الدقائق، طرائق التدريس، التقويم الختامي، الواجب المنزلي.",
    "شرح الدرس": "قدّم شرحًا واضحًا ومتدرجًا مع أمثلة مناسبة للعمر، وتساؤلات لتنشيط الطلاب، ثم لخص المفاهيم الأساسية.",
    "ملخص الدرس": "أنشئ ملخصًا مركزًا ومنظمًا للمفاهيم الأساسية، مع أمثلة بسيطة وأسئلة مراجعة قصيرة.",
    "أهداف التعلم": "اقترح نواتج تعلم واضحة وقابلة للقياس، وبيّن كيف يمكن التحقق من تحقق كل ناتج.",
    "أنشطة صفية": "اقترح 3 أنشطة صفية تفاعلية متنوعة، مع طريقة التنفيذ والزمن والأدوات اللازمة والتقويم.",
    "ورقة عمل": "أنشئ ورقة عمل قابلة للطباعة متنوعة الأسئلة، ثم أضف قسمًا مستقلًا لنموذج الإجابة.",
    "اختبار قصير": "أنشئ اختبارًا قصيرًا من 10 أسئلة متنوعة، ووزع درجاته وأضف مفتاح الإجابة بشكل مستقل.",
    "أسئلة متدرجة": "أنشئ أسئلة بمستويات التذكر والفهم والتطبيق والتحليل مع إجابات نموذجية ومراعاة الفروق الفردية.",
    "خطة التمايز": "صمم خطة تمايز لثلاث فئات: من يحتاج إلى دعم، والمستوى المتوسط، والمتقدم؛ مع أمثلة وتقويم لكل فئة.",
    "استراتيجيات التدريس": "اقترح استراتيجيات تدريس نشطة مناسبة للموضوع، مع خطوات تطبيق كل استراتيجية والزمن المتوقع.",
    "شرائح عرض": "صمم محتوى عرض تقديمي مقسمًا إلى 8 شرائح قصيرة، مع عنوان ونقاط رئيسية وفكرة بصرية لكل شريحة. لا تدّع إنشاء ملف PPTX.",
    "بطاقة خروج": "أنشئ بطاقة خروج قصيرة تشمل سؤال فهم وسؤال تطبيق وتأمل ذاتي، مع إرشاد سريع للمعلم لتفسير النتائج.",
    "سلّم تقدير الأداء": "أنشئ سلم تقدير تحليليًا Rubric بمستويات أداء واضحة ومعايير قابلة للملاحظة.",
    "نصيحة للمعلم": "قدم نصيحة تربوية واقعية حول تقديم هذا الدرس وإدارة الوقت والتفاعل مع الطلاب.",
}

@st.cache_resource(show_spinner=False)
def make_client(key):
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key, timeout=60.0, max_retries=1)


def get_key():
    key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if key:
        return key
    try:
        return str(st.secrets.get("OPENROUTER_API_KEY", "")).strip()
    except Exception:
        return ""


def generate(kind, data, additional):
    key = get_key()
    if not key:
        st.error("لم يُضبط مفتاح OpenRouter. أضف OPENROUTER_API_KEY في Secrets الخاصة بالتطبيق.")
        return
    task = TOOLS[kind]
    context = f"الصف: {data['grade']}\nالمادة: {data['subject']}\nالفصل الدراسي: {data['semester']}\nالوحدة: {data['unit']}\nعنوان الدرس: {data['lesson']}\nمدة الحصة: {data['duration']} دقيقة\nاسم المعلم: {data['teacher']}\nملاحظات إضافية: {additional or 'لا يوجد'}"
    messages = [
        {"role":"system", "content": "أنت مساعد تربوي محترف لدعم معلمي المدارس السعودية. اكتب بالعربية السليمة مع عناوين وتنظيم مناسب. التزم بالفئة العمرية وزمن الحصة. لا تدّع الاطلاع على كتاب مدرسي أو صفحاته أو توافقًا رسميًا دون أن تُزوَّد بنص الكتاب. إن كان محتوى المقرر غير مرفق، قدم اقتراحًا تعليميًا عامًا واذكر ضرورة مطابقته مع الكتاب المعتمد. اجعل المخرجات عملية ومحددة، وتجنب المقدمات الطويلة."},
        {"role":"user", "content": f"المهمة: {task}\n\nبيانات الدرس:\n{context}"}
    ]
    try:
        with st.spinner("يجري إعداد المحتوى التعليمي..."):
            response = make_client(key).chat.completions.create(model=os.getenv("OPENROUTER_MODEL", "openrouter/free"),messages=messages, temperature=0.5, max_tokens=2600)
        content = response.choices[0].message.content
        if not content:
            st.error("لم يرجع النموذج محتوى. حاول إعادة التوليد.")
            return
        st.session_state['last_result'] = content
        st.session_state['last_tool'] = kind
    except Exception as e:
        message = str(e)
        if any(s in message.lower() for s in ('401','invalid api key','unauthorized')):
            st.error("تعذر التحقق من مفتاح API. راجع إعدادات Secrets.")
