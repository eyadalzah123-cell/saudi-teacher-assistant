
import os
import streamlit as st
from openai import OpenAI

# ==================================
# إعدادات الموقع
# ==================================

st.set_page_config(
    page_title="المعلم الذكي | مساعد المعلم السعودي",
    page_icon="📗",
    layout="wide"
)

# ==================================
# التصميم والخط والألوان
# ==================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;600;700;800&display=swap');

html, body, [class*="st-"],
[data-testid="stAppViewContainer"],
button, input, textarea, label {
    font-family: 'Tajawal', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    direction: rtl;
    background: #f5f9f6;
}

[data-testid="stSidebar"] {
    direction: rtl;
    background: #ecf6ef;
}

[data-testid="stSidebar"] *,
.stMarkdown, .stTextInput, .stSelectbox,
.stTextArea, .stRadio, .stSlider,
.stTabs, h1, h2, h3, p {
    text-align: right;
}

h1, h2, h3 {
    color: #14532d !important;
}

.stButton > button[kind="primary"],
.stDownloadButton > button {
    background-color: #166534 !important;
    color: white !important;
    border-radius: 11px !important;
    border: 0 !important;
}

.stButton > button {
    border-radius: 11px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    flex-wrap: wrap;
}

.stTabs [data-baseweb="tab"] {
    background: white;
    border-radius: 10px;
    padding: 10px 15px;
}

.stTabs [aria-selected="true"] {
    background: #dcfce7 !important;
    color: #14532d !important;
}

.hero {
    background: linear-gradient(110deg,#14532d,#23844d);
    color: white;
    border-radius: 18px;
    padding: 25px 30px;
    margin-bottom: 22px;
}

.hero h1 {
    color: white !important;
    margin: 0;
}

.hero p {
    color: #e5ffec;
    margin: 5px 0 0;
}
</style>
""", unsafe_allow_html=True)

# ==================================
# الصفوف والمواد الدراسية
# ==================================

GRADES = [
    "الأول الابتدائي",
    "الثاني الابتدائي",
    "الثالث الابتدائي",
    "الرابع الابتدائي",
    "الخامس الابتدائي",
    "السادس الابتدائي",
    "الأول المتوسط",
    "الثاني المتوسط",
    "الثالث المتوسط",
    "الأول الثانوي",
    "الثاني الثانوي",
    "الثالث الثانوي",
]

SUBJECTS = [
    "لغتي",
    "اللغة العربية",
    "الرياضيات",
    "العلوم",
    "اللغة الإنجليزية",
    "الدراسات الإسلامية",
    "الدراسات الاجتماعية",
    "المهارات الرقمية",
    "التربية الفنية",
    "التربية البدنية",
    "الفيزياء",
    "الكيمياء",
    "الأحياء",
    "التفكير الناقد",
    "أخرى",
]

# ==================================
# الأدوات التعليمية
# ==================================

TASKS = {
    "التحضير والشرح": {
        "تحضير درس متكامل":
            "صمم تحضير درس عمليًا يتضمن الأهداف "
            "القابلة للقياس، التهيئة، خطوات التدريس "
            "موزعة على زمن الحصة، الوسائل، التمايز، "
            "التقويم، والواجب المنزلي.",

        "شرح مبسط للدرس":
            "اكتب شرحًا تدريجيًا مناسبًا لعمر الطلاب، "
            "بأمثلة واضحة وتطبيقات وتمارين تحقق الفهم.",

        "ملخص الدرس":
            "قدّم ملخصًا دقيقًا للدرس بنقاط واضحة، "
            "ومفاهيم أساسية، وأسئلة مراجعة قصيرة.",

        "نواتج التعلم":
            "اقترح نواتج تعلم محددة قابلة للقياس "
            "وأفعال أداء مناسبة، مع مؤشرات تحققها.",
    },

    "الأنشطة وأوراق العمل": {
        "ورقة عمل مع نموذج الإجابة":
            "أنشئ ورقة عمل جاهزة للطباعة مع تعليمات "
            "واضحة، وأسئلة متنوعة، ونموذج إجابة منفصل.",

        "أنشطة صفية تفاعلية":
            "اقترح أنشطة تعلم نشط، مع خطوات التنفيذ "
            "والزمن والأدوات وطريقة تقييم المشاركة.",

        "خطة التمايز":
            "جهز أنشطة وأسئلة لثلاثة مستويات "
            "(دعم، مستوى أساسي، إثراء) مع توضيح "
            "احتياج كل مستوى.",

        "محتوى عرض تقديمي":
            "جهّز نص عرض شرائح مرتبًا: عنوان كل "
            "شريحة، المحتوى المختصر، مثال أو نشاط، "
            "ثم خاتمة وتقويم.",
    },

    "التقويم والمتابعة": {
        "اختبار قصير مع الإجابات":
            "أنشئ اختبارًا قصيرًا مناسبًا للصف "
            "يضم أنماطًا متنوعة، ومفتاح إجابة "
            "ودرجات لكل سؤال.",

        "أسئلة حسب مستويات التفكير":
            "أنشئ أسئلة تدرجية من التذكر والفهم "
            "إلى التطبيق والتحليل، مع إجابات إرشادية.",

        "بطاقة خروج":
            "اكتب بطاقة خروج من 3 أسئلة تقيس فهم "
            "أهم نقاط الدرس خلال آخر خمس دقائق.",

        "سلم تقدير (Rubric)":
            "صمم سلم تقدير واضحًا بأربعة مستويات "
            "أداء ومعايير قابلة للملاحظة.",
    },

    "أدوات المعلم": {
        "استراتيجية تدريس مناسبة":
            "اقترح استراتيجية تدريس واحدة مناسبة "
            "للدرس، وفسر اختيارها، ثم خطوات تنفيذها "
            "ضمن زمن الحصة.",

        "معالجة المفاهيم الخاطئة":
            "حدد المفاهيم الخاطئة المتوقعة وكيف "
            "يكتشفها المعلم ويصححها بأنشطة وأسئلة قصيرة.",

        "رسالة لولي الأمر":
            "صغ رسالة ودية رسمية موجزة إلى ولي الأمر "
            "توضح موضوع الدرس وكيف يمكن دعمه منزليًا.",

        "خطة علاجية وإثرائية":
            "أنشئ خطة دعم للمتعثرين وإثراء للمتقدمين، "
            "مع أنشطة قابلة للتنفيذ وأداة تقويم.",
    },
}

# ==================================
# الاتصال بالذكاء الاصطناعي
# ==================================

def get_api_key():
    try:
        secret = st.secrets.get(
            "OPENROUTER_API_KEY", ""
        )
    except (
        FileNotFoundError,
        KeyError,
        AttributeError
    ):
        secret = ""

    return secret or os.environ.get(
        "OPENROUTER_API_KEY", ""
    )


def generate_content(api_key, model, prompt):

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        timeout=65.0
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "أنت مساعد تربوي متخصص في التدريس "
                    "في المملكة العربية السعودية. "
                    "أجب بالعربية السليمة بتنسيق واضح، "
                    "وراعِ عمر الطلاب وزمن الحصة. "
                    "لا تدّعِ الرجوع إلى كتاب مدرسي "
                    "محدد أو مطابقته حرفيًا إلا إن "
                    "قُدّم لك نصه. "
                    "إذا لم تتوفر تفاصيل الدرس "
                    "فاقترح محتوى تعليميًا مناسبًا "
                    "واذكر أنه يحتاج مراجعة المعلم."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
        max_tokens=2400
    )

    return (
        response.choices[0].message.content or ""
    ).strip()


# ==================================
# القائمة الجانبية
# ==================================

with st.sidebar:

    st.header("⚙️ إعدادات الدرس")

    teacher_name = st.text_input(
        "اسم المعلم أو المعلمة",
        value=""
    )

    school_name = st.text_input(
        "اسم المدرسة",
        value=""
    )

    st.divider()

    grade = st.selectbox(
        "الصف الدراسي",
        GRADES
    )

    subject = st.selectbox(
        "المادة الدراسية",
        SUBJECTS
    )

    if subject == "أخرى":
        subject = st.text_input(
            "اكتب اسم المادة",
            placeholder="اسم المادة الدراسية"
        )

    term = st.selectbox(
        "الفصل الدراسي",
        [
            "الفصل الأول",
            "الفصل الثاني",
            "غير محدد"
        ]
    )

    if grade.endswith("الثانوي"):
        track = st.text_input(
            "المسار (إن وجد)",
            placeholder="مثل المسار العام"
        )
    else:
        track = ""

    lesson_title = st.text_input(
        "عنوان الدرس",
        placeholder="اكتب عنوان الدرس كما في الكتاب"
    )

    duration = st.slider(
        "مدة الحصة بالدقائق",
        min_value=20,
        max_value=90,
        value=45,
        step=5
    )

    notes = st.text_area(
        "تعليمات إضافية (اختياري)",
        placeholder=(
            "مثال: الطلاب مبتدئون وأريد "
            "أمثلة من الحياة اليومية"
        ),
        height=90
    )

    st.divider()

    st.caption("إعدادات الذكاء الاصطناعي")

    model = st.text_input(
        "نموذج OpenRouter",
        value="openrouter/free",
        help="يمكن تغيير النموذج إذا كان متوفرًا"
    )

    api_key = get_api_key()

    if api_key:
        st.success("مفتاح OpenRouter موجود")
    else:
        st.warning(
            "أضف OPENROUTER_API_KEY "
            "في إعدادات Secrets على Streamlit"
        )


# ==================================
# الواجهة الرئيسية
# ==================================

st.markdown(
    '''
    <div class="hero">
        <h1>📗 المعلم الذكي</h1>
        <p>
        مساعد المعلم السعودي في التحضير
        والشرح والأنشطة والتقويم
        </p>
    </div>
    ''',
    unsafe_allow_html=True
)

if teacher_name:
    welcome = f"مرحبًا {teacher_name}"
    if school_name:
        welcome += f" — {school_name}"
    st.caption(welcome)

st.info(
    "اختر بيانات الدرس من القائمة الجانبية، "
    "ثم اختر الأداة المناسبة واضغط إنشاء المحتوى."
)

# ==================================
# التبويبات
# ==================================

tabs = st.tabs(list(TASKS.keys()))

for index, (category, tasks) in enumerate(
    TASKS.items()
):

    with tabs[index]:

        st.subheader(category)

        task = st.selectbox(
            "اختر الأداة التعليمية",
            list(tasks.keys()),
            key=f"task_{index}"
        )

        if st.button(
            "✨ إنشاء المحتوى",
            type="primary",
            key=f"go_{index}"
        ):

            if not api_key:

                st.error(
                    "مفتاح OpenRouter غير موجود. "
                    "أضفه في إعدادات Secrets."
                )

            elif not lesson_title.strip():

                st.warning(
                    "اكتب عنوان الدرس في "
                    "القائمة الجانبية أولًا."
                )

            elif not subject.strip():

                st.warning(
                    "حدد المادة الدراسية أولًا."
                )

            else:

                prompt = (
                    f"الصف: {grade}\n"
                    f"المادة: {subject}\n"
                    f"الفصل: {term}\n"
                    f"المسار: {track or 'لا ينطبق'}\n"
                    f"الدرس: {lesson_title}\n"
                    f"زمن الحصة: {duration} دقيقة\n"
                    f"المطلوب: {task}\n"
                    f"التعليمات: {tasks[task]}\n"
                    f"ملاحظات المعلم: "
                    f"{notes or 'لا يوجد'}\n"
                    "اربط المقترح بموضوع الدرس "
                    "دون الادعاء بنقل نص من الكتاب الرسمي. "
                    "قدم الناتج منظمًا وجاهزًا للاستخدام، "
                    "واذكر الحاجة للتحقق عند الضرورة."
                )

                with st.spinner(
                    "يتم إعداد المحتوى..."
                ):

                    try:

                        result = generate_content(
                            api_key,
                            model,
                            prompt
                        )

                        if not result:

                            st.error(
                                "لم يرجع النموذج نصًا. "
                                "جرّب مرة أخرى أو غيّر النموذج."
                            )

                        else:

                            st.session_state[
                                f"result_{index}"
                            ] = (task, result)

                    except Exception as exc:

                        msg = str(exc)

                        if "401" in msg:
                            st.error(
                                "رفض OpenRouter مفتاح API. "
                                "راجع المفتاح في Secrets."
                            )

                        elif "404" in msg:
                            st.error(
                                "النموذج غير متاح. "
                                "جرّب openrouter/free."
                            )

                        elif "429" in msg:
                            st.error(
                                "وصلت إلى حد الطلبات مؤقتًا. "
                                "حاول لاحقًا."
                            )

                        elif "402" in msg:
                            st.error(
                                "هناك مشكلة رصيد أو صلاحية "
                                "لاستخدام النموذج."
                            )

                        else:
                            st.error(
                                "تعذر توليد المحتوى: "
                                f"{type(exc).__name__}. "
                                "تحقق من سجلات التطبيق."
                            )

        # عرض النتيجة والاحتفاظ بها

        if f"result_{index}" in st.session_state:

            last_task, result = st.session_state[
                f"result_{index}"
            ]

            st.success(
                f"تم إعداد: {last_task}"
            )

            st.markdown(result)

            st.download_button(
                "⬇️ تنزيل المحتوى (TXT)",
                data=result,
                file_name=(
                    f"teacher_content_{index + 1}.txt"
                ),
                mime="text/plain; charset=utf-8",
                key=f"download_{index}"
            )

# ==================================
# التذييل
# ==================================

st.divider()

st.caption(
    "تنبيه: المحتوى مولّد بالذكاء الاصطناعي "
    "ويحتاج إلى مراجعة المعلم قبل الاستخدام. "
    "لم تُربط الكتب الرسمية بهذه النسخة بعد."
)
