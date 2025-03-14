from sentence_transformers import SentenceTransformer

#  تحميل النموذج وحفظه في الجهاز
model = SentenceTransformer("aubmindlab/bert-base-arabertv02")
model.save("E:/Models/arabert")  # احفظ النموذج في هذا المسار

print("✅ تم تحميل النموذج وحفظه بنجاح في E:/Models/arabert")
