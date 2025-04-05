pip install pyodbc
import pyodbc

# الاتصال بـ SQL Server (تأكد من ملء التفاصيل الصحيحة)
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=اسم_الخادم;'
    'DATABASE=اسم_قاعدة_البيانات;'
    'UID=اسم_المستخدم;'
    'PWD=كلمة_المرور'
)

cursor = conn.cursor()

# تنفيذ استعلام لجلب البيانات من الجدول
cursor.execute("SELECT title, description FROM videos")  # استبدل 'videos' باسم الجدول الصحيح

# جلب جميع البيانات
rows = cursor.fetchall()

# استخراج العناوين والوصف
video_titles = [row[0] for row in rows]
video_descriptions = [row[1] for row in rows]
video_texts = [f"{title}. {desc}" for title, desc in zip(video_titles, video_descriptions)]

# لو حابب تعرض البيانات لتتأكد إن كل حاجة تمام
print(video_titles[:5])  # عرض أول 5 عناوين
print(video_descriptions[:5])  # عرض أول 5 أوصاف
