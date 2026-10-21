import os
import json
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import streamlit as st

st.set_page_config(
    page_title="المعلم الذكي | مساعد المعلم السعودي",
    page_icon="📗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;600;700;800&display=swap');

html, body, .stApp, button, input, textarea {
    font-family: 'Tajawal', Arial, sans-serif !important;
}
.stApp {direction: rtl;}
[data-testid="stSidebar"] {direction: rtl;}
[data-testid="stMarkdownContainer"] {text-align: right;}
.stButton button[kind="primary"] {
    background: #166534 !important;
    color: white !important;
    border: 0;
    border-radius: 10px;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #166534 !important;
    font-weight: 800;
}
.hero {
    background: linear-gradient(110deg,#14532d,#24824e);
    color: white;
    padding: 25px;
    border-radius: 16px;
    margin: 7px 0 20px;
}
.hero h1 {color: white !important; margin: 0; font-size: 2.1rem;}
.hero p {color: #e9fff0; margin: 8px 0 0;}
</style>
""", unsafe_allow_html=True)

GRADES = [
    "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي",
    "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي",
    "الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط",
    "الأول الثانوي", "الثاني الثانوي", "الثالث الثانوي"
]

PRIMARY = [
    "لغتي", "الرياضيات", "العلوم", "الدراسات الإسلامية",
    "اللغة الإنجليزية", "الدراسات الاجتماعية", "المهارات الرقمية",
    "التربية الفنية", "التربية البدنية", "المهارات الحياتية والأسرية",
    "مادة أخرى"
]

MIDDLE = [
    "لغتي الخالدة", "الرياضيات", "العلوم", "الدراسات الإسلامية",
    "اللغة الإنجليزية", "الدراسات الاجتماعية", "المهارات الرقمية",
    "التربية الفنية", "التربية البدنية", "مادة أخرى"
]

SECONDARY = [
    "الرياضيات", "اللغة الإنجليزية", "الكيمياء", "الفيزياء",
    "الأحياء", "الدراسات الإسلامية", "اللغة العربية",
    "التقنية الرقمية", "التفكير الناقد", "العلوم البيئية",
    "مادة أخرى"
]

TASKS = {
    "التحضير والشرح": {
        "تحضير درس متكامل": "أعد خطة درس بأهداف قابلة للقياس وتهيئة وشرح وأنشطة وتقويم وواجب مع توزيع الزمن.",
        "شرح مبسط للدرس": "اشرح الدرس تدريجيًا بلغة مناسبة للطلاب مع أمثلة وأسئلة للتحقق من الفهم.",
        "ملخص الدرس": "اكتب ملخصًا منظمًا بأهم الأفكار والمفاهيم والأمثلة وأسئلة المراجعة.",
        "نواتج التعلم": "اقترح نواتج تعلم قابلة للقياس مع مؤشرات تحققها."
    },
    "الأنشطة وأوراق العمل": {
        "ورقة عمل مع الإجابات": "أنشئ ورقة عمل متنوعة الأسئلة مع نموذج إجابة منفصل.",
        "أنشطة صفية تفاعلية": "اقترح أنشطة تعلم نشط مع الزمن والأدوات وطريقة التنفيذ.",
        "خطة التمايز": "جهز أنشطة لمستويات الدعم والأساسي والإثراء.",
        "محتوى عرض تقديمي": "أنشئ محتوى شرائح عرض منظمة بعناوين وأمثلة وأنشطة، دون الادعاء بإنشاء ملف PPTX."
    },
    "التقويم والمتابعة": {
        "اختبار قصير مع الإجابات": "أنشئ عشرة أسئلة متنوعة مع الدرجات ومفتاح الإجابة.",
        "أسئلة مستويات التفكير": "أنشئ أسئلة للتذكر والفهم والتطبيق والتحليل مع الإجابات.",
        "بطاقة خروج": "أنشئ بطاقة خروج من ثلاثة أسئلة لقياس فهم الدرس.",
        "سلم تقدير الأداء": "صمم سلم تقدير بأربعة مستويات أداء ومعايير واضحة."
    },
    "أدوات المعلم": {
        "استراتيجية تدريس": "اقترح استراتيجية تدريس مناسبة وخطوات تطبيقها.",
        "معالجة المفاهيم الخاطئة": "حدد الأخطاء المتوقعة وكيفية اكتشافها ومعالجتها.",
        "خطة علاجية وإثرائية": "أعد أنشطة للطلاب المتعثرين والمتقدمين مع تقويم.",
        "رسالة لولي الأمر": "اكتب رسالة مهنية مختصرة لدعم تعلم الطالب."
    }
}

def get_setting(name, default=""):
    value = os.environ.get(name, "")
    if value:
        return value.strip()
    try:
        return str(st.secrets.get(name, default)).strip()
    except Exception:
        return default

def generate(api_key, model, prompt):
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "أنت مساعد تربوي متخصص في التعليم السعودي. "
                    "اكتب بالعربية بشكل واضح وعملي يناسب الصف الدراسي. "
                    "لا تخترع نصوصًا أو صفحات من الكتب المدرسية. "
                    "إذا لم يتوفر النص الأصلي، وضح أن المحتوى مقترح "
                    "ويحتاج مراجعة المعلم ومطابقته مع الكتاب."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 2200
    }

    request = Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json",
            "HTTP-Referer": "https://saudi-teacher-assistant.streamlit.app",
            "X-Title": "Saudi Teacher Assistant"
        },
        method="POST"
    )

    try:
        with urlopen(request, timeout=55) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        messages = {
            401: "مفتاح API غير صالح.",
            402: "الرصيد غير كافٍ أو النموذج يحتاج إلى رصيد.",
            404: "النموذج غير متاح. جرّب openrouter/free.",
            429: "تم تجاوز حد الطلبات. حاول لاحقًا."
        }
        raise RuntimeError(
            messages.get(error.code, f"خطأ في الخدمة: {error.code}")
        ) from None
    except (URLError, TimeoutError):
        raise RuntimeError("تعذر الاتصال بـ OpenRouter.") from None
    except (ValueError, UnicodeDecodeError):
        raise RuntimeError("تعذر قراءة استجابة OpenRouter.") from None

    choices = result.get("choices") or []
    if not choices:
        raise RuntimeError("لم يرجع الذكاء الاصطناعي إجابة.")

    content = (choices[0].get("message") or {}).get("content")
    if isinstance(content, list):
        content = "\n".join(
            item.get("text", "") for item in content
            if isinstance(item, dict)
        )
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("الإجابة فارغة. حاول مرة أخرى.")

    return content.strip()

st.markdown(
    '<div class="hero"><h1>المعلم الذكي</h1>'
    '<p>مساعدك في التحضير والشرح والأنشطة والتقويم</p></div>',
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("إعدادات المعلم والدرس")

    teacher = st.text_input("اسم المعلم أو المعلمة")
    school = st.text_input("اسم المدرسة")

    st.divider()

    grade = st.selectbox("الصف الدراسي", GRADES)

    if "الابتدائي" in grade:
        subjects = PRIMARY
    elif "المتوسط" in grade:
        subjects = MIDDLE
    else:
        subjects = SECONDARY

    subject = st.selectbox("المادة الدراسية", subjects)

    if subject == "مادة أخرى":
        subject = st.text_input("اكتب اسم المادة")

    term = st.selectbox(
        "الفصل الدراسي",
        ["الأول", "الثاني", "غير محدد"]
    )

    track = ""
    if "الثانوي" in grade:
        track = st.text_input("المسار الدراسي")

    unit = st.text_input("اسم الوحدة (اختياري)")
    lesson = st.text_input("عنوان الدرس")

    duration = st.slider(
        "مدة الحصة بالدقائق",
        20, 90, 45, 5
    )

    notes = st.text_area(
        "ملاحظات المعلم",
        placeholder="اكتب تعليمات إضافية إن وجدت"
    )

    source = st.text_area(
        "نص الدرس من الكتاب (اختياري)",
        placeholder="الصق نص الدرس لنتائج أكثر دقة"
    )

    st.divider()

    api_key = get_setting("OPENROUTER_API_KEY")
    model = get_setting("OPENROUTER_MODEL", "openrouter/free")

    with st.expander("حالة النظام"):
        st.write("الواجهة: جاهزة")
        st.write("مفتاح API: " + ("موجود" if api_key else "غير موجود"))
        st.write("النموذج: " + model)

if not api_key:
    st.warning(
        "مفتاح OpenRouter غير موجود. أضفه في Streamlit Secrets."
    )

if not lesson.strip():
    st.info("اختر الصف والمادة واكتب عنوان الدرس للبدء.")

tabs = st.tabs(list(TASKS.keys()))

for tab, (section, options) in zip(tabs, TASKS.items()):
    with tab:
        st.subheader(section)

        selected = st.selectbox(
            "اختر الأداة التعليمية",
            list(options.keys()),
            key="tool_" + section
        )

        st.caption(options[selected])

        if st.button(
            "إنشاء المحتوى",
            key="generate_" + section,
            type="primary"
        ):
            if not api_key:
                st.error("أضف مفتاح OpenRouter أولًا.")
            elif not lesson.strip() or not subject.strip():
                st.warning("أدخل عنوان الدرس والمادة أولًا.")
            else:
                prompt = (
                    f"الصف: {grade}\n"
                    f"المادة: {subject}\n"
                    f"الفصل: {term}\n"
                    f"المسار: {track or 'غير محدد'}\n"
                    f"الوحدة: {unit or 'غير محددة'}\n"
                    f"عنوان الدرس: {lesson}\n"
                    f"مدة الحصة: {duration} دقيقة\n"
                    f"المهمة: {selected}\n"
                    f"التعليمات: {options[selected]}\n"
                    f"ملاحظات المعلم: {notes or 'لا يوجد'}\n"
                    f"نص الدرس المتوفر: {source[:12000] or 'غير مرفق'}\n"
                    "قدم إجابة منظمة وقابلة للاستخدام، "
                    "واذكر الحاجة لمراجعة المنهج عند غياب نص الكتاب."
                )

                with st.spinner("جاري إعداد المحتوى..."):
                    try:
                        result = generate(api_key, model, prompt)
                        st.session_state["result"] = result
                        st.session_state["result_title"] = selected
                        st.success("تم إنشاء المحتوى بنجاح.")
                    except RuntimeError as exc:
                        st.error(str(exc))
                    except Exception:
                        st.error(
                            "حدث خطأ غير متوقع. راجع سجلات Streamlit."
                        )

if st.session_state.get("result"):
    st.divider()
    st.subheader(
        "المحتوى الناتج: " +
        st.session_state.get("result_title", "")
    )
    st.markdown(st.session_state["result"])

    st.download_button(
        "تنزيل المحتوى",
        data=st.session_state["result"].encode("utf-8-sig"),
        file_name="teacher_" + datetime.now().strftime("%Y%m%d") + ".txt",
        mime="text/plain"
    )

st.divider()
st.caption(
    "المحتوى مولّد بالذكاء الاصطناعي ويحتاج مراجعة المعلم. "
    "لم تُربط الكتب الرسمية بالموقع بعد."
)
