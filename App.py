# ==========================================
# 1. استيراد المكتبات (Importing Libraries)
# ==========================================
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns

# ==========================================
# 2. إعدادات الصفحة (Page Configuration)
# ==========================================
# يجب أن يكون هذا الأمر أول أمر في كود ستريم ليت
st.set_page_config(
    page_title="Tips Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 3. قاموس الترجمة (Translation Dictionary)
# ==========================================
# هذا القاموس يحتوي على النصوص باللغتين للتبديل بينهما بسهولة
translations = {
    "en": {
        "sidebar_title": "Tips Dashboard",
        "lang_select": "Choose Language / اختر اللغة",
        "filter_title": "Filter Data",
        "cat_filter": "Categorical Filter",
        "num_filter": "Numerical Filter",
        "row_filter": "Row Facet",
        "col_filter": "Column Facet",
        "day_filter": "Select Day",
        "time_filter": "Select Meal Time",
        "overview": "### Project Overview:\nThis dashboard analyzes **Restaurant Tips** data to understand spending behavior based on total bill, demographics, and time.",
        "footer": "Made with 😍 by Eng. Loay Alrazi",
        "preview": "Data Preview",
        "shape": "Data contains {} rows and {} columns.",
        "metrics_title": "Key Metrics",
        "scatter_title": "Total Bill vs. Tips Analysis",
        "bar_title": "Total Bills by Sex",
        "pie_title": "Tips by Smoking Status",
        "donut_title": "Tips Distribution by Day",
        "filtered_metrics": "Filtered Data Metrics",
        "total_rev": "Total Revenue",
        "total_tips": "Total Tips",
        "cust_count": "Customer Count",
        "warning": "No data available for this selection!",
         "labels": {# قاموس ترجمة الاعمدة 
            'total_bill': 'Total Bill',
            'tip': 'Tip',
            'sex': 'Sex',
            'smoker': 'Smoker',
            'day': 'Day',
            'time': 'Time',
            'size': 'Number of People',
            None: 'None'
        }
        
        
    },
    "ar": {
        "sidebar_title": "لوحة تحكم البقشيش",
        "lang_select": "Choose Language / اختر اللغة",
        "filter_title": "تصفية البيانات",
        "cat_filter": "تصفية فئوية",
        "num_filter": "تصفية رقمية",
        "row_filter": "تقسيم بالصفوف",
        "col_filter": "تقسيم بالأعمدة",
        "day_filter": "اختر اليوم",
        "time_filter": "اختر وقت الوجبة",
        "overview": "### نظرة عامة:\nتقوم هذه اللوحة بتحليل بيانات **البقشيش** في المطاعم لفهم سلوك الإنفاق بناءً على الفاتورة، التركيبة السكانية، والوقت.",
        "footer": "تم التطوير بحب 😍 بواسطة م. لؤي الرازي",
        "preview": "معاينة البيانات",
        "shape": "البيانات تحتوي على {} صفاً و {} أعمدة.",
        "metrics_title": "المؤشرات الرئيسية",
        "scatter_title": "تحليل العلاقة بين الفاتورة والبقشيش",
        "bar_title": "إجمالي الفواتير حسب الجنس",
        "pie_title": "البقشيش حسب حالة التدخين",
        "donut_title": "توزيع البقشيش حسب الأيام",
        "filtered_metrics": "مؤشرات البيانات المفلترة",
        "total_rev": "إجمالي الإيرادات",
        "total_tips": "إجمالي البقشيش",
        "cust_count": "عدد الزبائن",
        "warning": "لا توجد بيانات لهذا الاختيار!",
        # قاموس ترجمة الأعمدة داخل اللغة العربية
        "labels": {
            'total_bill': 'إجمالي الفاتورة',
            'tip': 'قيمة البقشيش',
            'sex': 'الجنس',
            'smoker': 'المدخن',
            'day': 'اليوم',
            'time': 'وقت الوجبة',
            'size': 'عدد الأشخاص',
            None: 'لا شيء'
        }
       
        
    }
}

# ==========================================
# 4. الشريط الجانبي واختيار اللغة (Sidebar & Language)
# ==========================================
st.sidebar.header("⚙️ Settings / الإعدادات")
language = st.sidebar.radio("🌐 Language", ["English", "العربية"])
lang_code = "en" if language == "English" else "ar"
txt = translations[lang_code] # اختصار للوصول للنصوص

st.sidebar.markdown("---")
st.sidebar.header(txt["sidebar_title"])

# محاولة عرض الصورة، وفي حال عدم وجودها يتم تجاوز الخطأ
try:
    st.sidebar.image('images/tip.jpg', caption='Data Analysis Concept')
except:
    st.sidebar.warning("⚠️ Image 'tip.jpg' not found.")

st.sidebar.info(txt["overview"])

# ==========================================
# 5. تحميل البيانات (Loading Data)
# ==========================================
@st.cache_data # خاصية لتسريع التحميل وعدم قراءة الملف في كل مرة
def load_data():
    try:
        # محاولة قراءة الملف المحلي
        df = pd.read_csv('data/tip.csv')
    except FileNotFoundError:
        # إذا لم يوجد الملف، نحمله من مكتبة seaborn مباشرة
        df = sns.load_dataset('tips')
    return df

df = load_data()

# ==========================================
# 6. فلاتر البيانات (Data Filters)
# ==========================================
st.sidebar.write(f"### {txt['filter_title']}")



# دالة التنسيق: تأخذ الاسم (مثلاً 'total_bill') وتبحث عنه داخل قسم labels في اللغة الحالية
def format_func(option):
    return txt['labels'].get(option, option)

# خيارات القوائم (أسماء الأعمدة الأصلية في البيانات)
cat_options = [None, 'sex', 'smoker', 'day', 'time']
num_options = [None, 'total_bill', 'tip', 'size'] 

# أدوات التحكم (نمرر دالة format_func)
cat_filter = st.sidebar.selectbox(txt["cat_filter"], cat_options, format_func=format_func)
num_filter = st.sidebar.selectbox(txt["num_filter"], num_options, format_func=format_func)
row_filter = st.sidebar.selectbox(txt["row_filter"], cat_options, format_func=format_func)
col_filter = st.sidebar.selectbox(txt["col_filter"], cat_options, format_func=format_func)

st.sidebar.markdown("---")
st.sidebar.write(txt["footer"])
st.sidebar.markdown("[GitHub](https://github.com/Loai-Alrazi) ")


# ==========================================
# 7. الجسم الرئيسي للتطبيق (Main Body)
# ==========================================

# --- معاينة البيانات ---
st.write(f"### {txt['preview']}")
with st.expander("Show/Hide Data"):
    st.dataframe(df.head())
st.write(txt["shape"].format(df.shape[0], df.shape[1]))
st.markdown("---")

# --- الصف الأول: المؤشرات العامة (General Metrics) ---
st.subheader(txt["metrics_title"])
a1, a2, a3, a4 = st.columns(4)
a1.metric("Max. Total Bill", f"${df['total_bill'].max()}")
a2.metric("Max. Tip", f"${df['tip'].max()}")
a3.metric("Min. Tip", f"${df['tip'].min()}")
a4.metric("Min. Total Bill", f"${df['total_bill'].min()}")

# --- الصف الثاني: المخطط النقطي التفاعلي (Scatter Plot) ---
st.subheader(txt["scatter_title"])
# نستخدم try/except لتجنب الأخطاء إذا اختار المستخدم خيارات متعارضة
try:
    fig_scatter = px.scatter(
        data_frame=df,
        x='total_bill',
        y='tip',
        color=cat_filter,
        size=num_filter,
        facet_col=col_filter,
        facet_row=row_filter,
        title=txt["scatter_title"]
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
except Exception as e:
    st.error(f"Error displaying chart: {e}")

# --- الصف الثالث: الرسوم البيانية المتنوعة ---
c1, c2, c3 = st.columns((4, 3, 3))

with c1:
    st.text(txt["bar_title"])
    fig_bar = px.bar(data_frame=df, x='sex', y='total_bill', color=cat_filter if cat_filter else 'sex')
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.text(txt["pie_title"])
    fig_pie = px.pie(data_frame=df, names='smoker', values='tip', color=cat_filter if cat_filter else 'smoker')
    st.plotly_chart(fig_pie, use_container_width=True)

with c3:
    st.text(txt["donut_title"])
    fig_donut = px.pie(data_frame=df, names='day', values='tip', color=cat_filter if cat_filter else 'day', hole=0.4)
    st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("---")

# --- الصف الرابع: فلترة تفاعلية للنتائج النهائية ---
st.subheader(txt["filtered_metrics"])

# فلاتر إضافية داخل الصفحة
col_d1, col_d2 = st.columns(2)
day_sel = col_d1.selectbox(txt["day_filter"], df['day'].unique())
time_sel = col_d2.radio(txt["time_filter"], df['time'].unique(), horizontal=True)

# تطبيق الفلترة
filtered_df = df[(df['day'] == day_sel) & (df['time'] == time_sel)]

# عرض النتائج
if not filtered_df.empty:
    revenue = filtered_df['total_bill'].sum()
    tips = filtered_df['tip'].sum()
    count = len(filtered_df)

    d1, d2, d3 = st.columns(3)
    d1.metric(txt["total_rev"], f"${revenue:,.2f}")
    d2.metric(txt["total_tips"], f"${tips:,.2f}")
    d3.metric(txt["cust_count"], count)
else:
    st.warning(txt["warning"])