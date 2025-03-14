import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

#  تحميل النموذج من المسار المحلي
model = SentenceTransformer("E:/Models/arabert")

#  تحميل بيانات الفيديوهات
video_titles = np.load("E:/Models/video_titles.npy", allow_pickle=True)
video_embeddings = np.load("E:/Models/video_embeddings.npy")

#  دالة البحث الذكي
def search_videos(query, top_n=5):
    #  تحويل البحث إلى تمثيل عددي
    query_embedding = model.encode([query])

    #  حساب التشابه بين البحث وعناوين الفيديوهات
    similarities = cosine_similarity(query_embedding, video_embeddings)[0]

    #  ترتيب النتائج بناءً على أعلى تشابه
    sorted_indices = np.argsort(similarities)[::-1]

    #  عرض أفضل النتائج
    print("\n أفضل النتائج للبحث:")
    for idx in sorted_indices[:top_n]:
        print(f"🎥 {video_titles[idx]} (التشابه: {similarities[idx]:.2f})")

#  تكرار البحث حتى يخرج المستخدم
while True:
    search_query = input("\n أدخل جملة البحث (أو اكتب 'خروج' لإنهاء البحث): ")
    
    if search_query.lower() == "خروج":
        print("\n تم إنهاء البحث. شكرًا لاستخدامك البرنامج!")
        break
    
    search_videos(search_query)
