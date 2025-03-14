import google.generativeai as genai

# 🛑 استبدل هذا بمفتاح API الخاص بك
API_KEY = "AIzaSyAuWRegcfg9ctF4CKZGYAPf5x0rCzV7jVs"

# ⚙️ تهيئة genai باستخدام المفتاح
genai.configure(api_key=API_KEY)

def main():
    """يتيح للأم إدخال سؤالها والحصول على إجابة من الشات بوت"""
    model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")

    while True:
        user_prompt = input("🤱 اسألي عن أي شيء يخص تربية طفلك (أو اكتبي 'خروج' لإنهاء المحادثة): ").strip()
        
        if user_prompt.lower() == "خروج":
            print("👋 شكراً لاستخدام الشات بوت. نتمنى لك يوماً سعيداً! 💖")
            break

        response = model.generate_content(user_prompt)

        # استخراج النص من الاستجابة
        if response and hasattr(response, "candidates") and response.candidates:
            reply = response.candidates[0].content.parts[0].text
            print(f"🤖 الإجابة: {reply}\n")
        else:
            print("⚠️ لم يتم استلام استجابة صحيحة من النموذج. حاولي مرة أخرى.")

if __name__ == "__main__":
    main()
