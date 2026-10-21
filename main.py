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
        elif '429' in message:
            st.error("تم بلوغ حد الطلبات. حاول لاحقًا أو غيّر النموذج.")
        elif '404' in message or 'model' in message.lower() and 'unavailable' in message.lower():
            st.error("النموذج المحدد غير متاح حاليًا. تحقق من OPENROUTER_MODEL.")
        else:
            st.error("تعذر إتمام طلب الذكاء الاصطناعي.")
            with st.expander("التفاصيل التقنية"):
                st.code(re.sub(r'sk-[A-Za-z0-9_-]+', '[HIDDEN_KEY]', message)[:900])

with st.sidebar:
    st.markdown("### إعدادات المعلم")
    teacher = st.text_input("اسم المعلم أو المعلمة", placeholder="مثال: أحمد")
    school = st.text_input("اسم المدرسة (اختياري)", placeholder="اسم المدرسة")
    st.divider()
    st.markdown("### بيانات الدرس")
    grade = st.selectbox("الصف الدراسي", GRADES)
    subject = st.selectbox("المادة الدراسية", SUBJECTS)
    if subject == "مادة أخرى":
        subject = st.text_input("اسم المادة", placeholder="اكتب اسم المادة")
    semester = st.selectbox("الفصل الدراسي", ["الأول", "الثاني", "الثالث", "غير محدد"])
    unit = st.text_input("الوحدة (اختياري)", placeholder="اكتب اسم الوحدة")
    lesson = st.text_input("عنوان الدرس", placeholder="اكتب عنوان الدرس كما يظهر في الكتاب")
    duration = st.slider("مدة الحصة (بالدقائق)", 20, 90, 45, 5)
    st.divider()
    if get_key():
        st.success("تم العثور على إعدادات الاتصال بالذكاء الاصطناعي")
    else:
        st.warning("مفتاح OpenRouter غير مضبوط")
    st.caption("قوائم المواد استرشادية. لم تُربط كتب المناهج أو فهارسها رسميًا بهذه النسخة.")

data = {'teacher':teacher or 'المعلم', 'grade':grade, 'subject':subject, 'semester':semester, 'unit':unit or 'غير محددة', 'lesson':lesson, 'duration':duration}
st.markdown("""<div class='hero'><div class='eyebrow'>منصة تعليمية ذكية للمعلم السعودي</div><div class='heading'>المعلم الذكي</div><div class='sub'>من فكرة الدرس إلى محتوى تعليمي جاهز للتطوير — تحضير، شرح، أنشطة، تقويم، وموارد صفية في مكان واحد.</div></div>""", unsafe_allow_html=True)
if school:
    st.caption(f"{school}  •  {grade}  •  {subject}")
else:
    st.caption(f"{grade}  •  {subject}")
if not lesson.strip():
    st.info("ابدأ بكتابة عنوان الدرس في القائمة الجانبية، ثم اختر الأداة المطلوبة.")

labels = ["التحضير والشرح", "الأنشطة وأوراق العمل", "التقويم والمتابعة", "أدوات المعلم"]
tabs = st.tabs(labels)
groups = [
    ["تحضير الدرس", "شرح الدرس", "ملخص الدرس", "أهداف التعلم"],
    ["أنشطة صفية", "ورقة عمل", "أسئلة متدرجة", "خطة التمايز"],
    ["اختبار قصير", "بطاقة خروج", "سلّم تقدير الأداء"],
    ["استراتيجيات التدريس", "شرائح عرض", "نصيحة للمعلم"],
]
for tab, options in zip(tabs, groups):
    with tab:
        selected = st.selectbox("اختر الأداة", options, key=f"sel_{options[0]}")
        st.markdown(f"**ماذا ستنجز؟** {TOOLS[selected]}")
        extra = st.text_area("تعليمات إضافية (اختياري)", height=95, placeholder="مثل: ركّز على التعلم التعاوني أو قدّم أسئلة أسهل", key=f"extra_{options[0]}")
        if st.button("إنشاء المحتوى", type="primary", key=f"go_{options[0]}", use_container_width=True):
            if not lesson.strip():
                st.warning("يرجى كتابة عنوان الدرس أولًا.")
            elif not subject.strip():
                st.warning("يرجى إدخال اسم المادة.")
            else:
                generate(selected, data, extra)

if st.session_state.get('last_result'):
    st.divider()
    st.subheader(f"النتيجة: {st.session_state.get('last_tool', 'المحتوى')}")
    st.markdown(st.session_state['last_result'])
    st.download_button("تنزيل المحتوى كنص", data=st.session_state['last_result'].encode('utf-8-sig'), file_name=f"teacher_result_{datetime.now():%Y%m%d_%H%M}.txt", mime="text/plain", use_container_width=True)
    st.caption("راجع المحتوى قبل استخدامه مع الطلاب، وطابق التفاصيل العلمية مع الكتاب المعتمد.")
