import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعدادات واجهة المستخدم لتتناسب مع الهواتف الذكية وتدعم اللغة العربية
st.set_page_config(
    page_title="مساعد التاجر وصانع المحتوى الذكي",
    page_icon="🚀",
    layout="centered"
)

# تنسيق مخصص لتصميم انسيابي ومتجاوب مع الهواتف الذكية
st.markdown("""
    <style>
    .reportview-container { text-align: right; direction: RTL; }
    .main-title { color: #1E3A8A; text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 10px; }
    .sub-title { color: #4B5563; text-align: center; font-size: 14px; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🚀 مساعد التاجر وصانع المحتوى الذكي</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">التقط صورة لمنتجك، اكتب مواصفاته، واصنع محتواك التسويقي بلمسة واحدة</div>', unsafe_allow_html=True)

# صندوق إدخال مفتاح الـ API لتفعيل الذكاء الاصطناعي
api_key = st.text_input("أدخل مفتاح الـ API الخاص بك من Google AI Studio:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    st.markdown("### 📸 1. صورة المنتج (اختياري)")
    # ميزة التقاط الصورة أو رفعها المتوافقة مع كاميرا الموبايل (كما في واجهة AI Studio أمامك)
    uploaded_file = st.file_uploader("التقط صورة المنتج أو ارفعها من معرض الصور (PNG, JPG)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="تم رفع صورة المنتج بنجاح", use_container_width=True)
    else:
        image = None

    st.markdown("### 📝 2. تفاصيل المنتج والمحتوى")
    # إدخال اسم المنتج أولاً لتنظيم النتيجة
    product_name = st.text_input("اسم المنتج / العنوان الرئيسي:", placeholder="مثال: ساعة ذكية Ultra")
    
    # صندوق المواصفات والمستهدفات (الموجود في صورتك)
    product_features = st.text_area("مواصفات / ميزات المنتج والمستهدفات (سهلة واختيارية):", 
                                    placeholder="مثال: مقاومة للماء، بطارية تدوم 10 أيام، قياس نبضات القلب، مناسبة للرياضيين...")

    # تحديد نوع المحتوى المطلوب (ميزة إضافية مخصصة لأصحاب المتاجر وصنّاع المحتوى)
    content_type = st.selectbox(
        "اختر نوع المحتوى الذي تريد توليده:",
        ["وصف منتج لمتجر إلكتروني (سلة / زد / Shopify)", 
         "منشور تسويقي لـ إنستغرام وفيسبوك (مع الهاشتاقات)", 
         "سكربت / سيناريو فيديو قصير (تيك توك / ريلز)"]
    )

    # حفظ النص المولد في الذاكرة لمنع اختفائه عند التفاعل
    if 'final_result' not in st.session_state:
        st.session_state.final_result = ""

    # زر التشغيل الرئيسي المماثل للزر الأخضر في صورتك
    if st.button("🔥 تشغيل الذكاء الاصطناعي وتوليد الوصف", use_container_width=True):
        if not product_name.strip() and not product_features.strip() and image is None:
            st.warning("الرجاء إدخال اسم المنتج، مواصفاته، أو رفع صورة له على الأقل!")
        else:
            with st.spinner("جاري تحليل البيانات وصناعة المحتوى الاحترافي..."):
                try:
                    # استخدام نموذج Gemini 1.5 Flash القادر على فهم النصوص والصور معاً
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # صياغة الأمر الموجه للذكاء الاصطناعي بناءً على الخيارات المحددة
                    prompt = f"""
                    أنت خبير تسويق رقمي محترف. قم بكتابة {content_type} باللغة العربية.
                    اسم المنتج: {product_name}
                    المواصفات والمميزات: {product_features}
                    اجعل الأسلوب مشوقاً، جذاباً، ويدفع العميل للشراء، واقترح أفكاراً ذكية للتسويق بناءً على المعطيات.
                    """
                    
                    # إذا قام المستخدم برفع صورة، يتم إرسالها مع النص ليقوم الذكاء الاصطناعي بتحليلها
                    if image:
                        response = model.generate_content([prompt, image])
                    else:
                        response = model.generate_content(prompt)
                        
                    st.session_state.final_result = response.text
                    st.success("تم توليد المحتوى التسويقي بنجاح! 🎉")
                except Exception as e:
                    st.error(f"حدث خطأ أثناء معالجة الطلب: {e}")

    # عرض النتيجة النهائية داخل صندوق نصي قابل للتعديل والنسخ السريع عبر الهاتف
    if st.session_state.final_result:
        st.markdown("### 📋 المحتوى الجاهز للاستخدام:")
        final_output = st.text_area("", value=st.session_state.final_result, height=250)
        
        # كود جافا سكريبت المطور المخصص للهواتف لنسخ النص بلمسة واحدة
        copy_html = f"""
        <div style="text-align: center; margin-top: 5px;">
            <button onclick="navigator.clipboard.writeText(`{final_output}`).then(() => alert('📋 تم نسخ المحتوى بنجاح! جاهز للصقه في متجرك أو حسابك.'));" 
                style="background-color: #10B981; color: white; border: none; padding: 12px 20px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; width: 100%; box-shadow: 0px 4px 6px rgba(0,0,0,0.1);">
                📋 اضغط هنا لنسخ المحتوى بالكامل بلمسة واحدة
            </button>
        </div>
        """
        st.components.v1.html(copy_html, height=65)

else:
    st.info("الرجاء وضع مفتاح الـ API الخاص بك المستخرج من Google AI Studio في الأعلى لتفعيل التطبيق والبدء في استخدامه.")

st.markdown("<hr><p style='text-align: center; color: #9CA3AF;'>تصميم متجاوب واحترافي مخصص بالكامل لخدمة المتاجر الإلكترونية وصنّاع المحتوى</p>", unsafe_allow_html=True)
