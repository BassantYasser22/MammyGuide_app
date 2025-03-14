import google.generativeai as genai

# 🛑 استبدل هذا بمفتاح API الخاص بك
API_KEY = "AIzaSyAuWRegcfg9ctF4CKZGYAPf5x0rCzV7jVs"

# ⚙️ تهيئة genai باستخدام المفتاح
genai.configure(api_key=API_KEY)

def main():
    """إرسال رسالة إلى نموذج Gemini وعرض الاستجابة النصية فقط"""
    model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")

    user_prompt = "كيفيه التعامل مع الطفل العصبي"
    response = model.generate_content(user_prompt)

    # استخراج النص من الاستجابة
    if response and hasattr(response, "candidates") and response.candidates:
        reply = response.candidates[0].content.parts[0].text
        print(reply)
    else:
        print("⚠️ لم يتم استلام استجابة صحيحة من النموذج.")

if __name__ == "__main__":
    main()
