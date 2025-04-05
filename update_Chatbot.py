import google.generativeai as genai

# استبدل هذا بمفتاح API الخاص بك
API_KEY = "AIzaSyAuWRegcfg9ctF4CKZGYAPf5x0rCzV7jVs"

# تهيئة genai باستخدام المفتاح
genai.configure(api_key=API_KEY)

def main():
    """يتيح للأم إدخال سؤالها حول تربية الطفل والحصول على إجابة مناسبة"""
    model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")

    print("\nمرحبًا بك في mammyguide")
    print("يمكنك اختيار اللغة التي تفضلينها للتواصل.")
    
    # اختيار اللغة
    while True:
        lang_choice = input("\nاختاري لغة التواصل: 1- العربية | 2- English: ").strip()
        if lang_choice == "1":
            language = "Arabic"
            break
        elif lang_choice == "2":
            language = "English"
            break
        else:
            print("يرجى إدخال 1 للعربية أو 2 للإنجليزية.")

    # إدخال عمر الطفل
    if language == "Arabic":
        child_age = input("\nأدخلي عمر طفلك بالأعوام: ").strip()
    else:
        child_age = input("\nEnter your child's age (in years): ").strip()

    while True:
        # إدخال السؤال
        if language == "Arabic":
            user_prompt = input("\nاكتبي سؤالك حول تربية طفلك (أو اكتبي 'خروج' لإنهاء المحادثة): ").strip()
        else:
            user_prompt = input("\nAsk your question about parenting (or type 'exit' to end the conversation): ").strip()
        
        if user_prompt.lower() in ["خروج", "exit"]:
            if language == "Arabic":
                print("\nشكراً لاستخدام mammyguide. نتمنى لك يومًا سعيدًا.")
            else:
                print("\nThank you for using mammyguide. Have a great day.")
            break

        # تكوين رسالة تفصيلية للموديل تشمل عمر الطفل
        if language == "Arabic":
            full_prompt = f"طفلي عمره {child_age} عامًا. {user_prompt} الإجابة يجب أن تكون قصيرة ومختصة بتربية الأطفال فقط."
        else:
            full_prompt = f"My child is {child_age} years old. {user_prompt} Please provide a brief response related only to parenting."

        # توليد الإجابة
        response = model.generate_content(full_prompt)

        # استخراج النص من الاستجابة وعرضه بتنسيق واضح
        if response and hasattr(response, "candidates") and response.candidates:
            reply = response.candidates[0].content.parts[0].text

            # تقليص الإجابة إذا كانت طويلة
            max_length = 100  # عدد الكلمات
            words = reply.split()
            if len(words) > max_length:
                reply = " ".join(words[:max_length]) + "..."
            
            print("\n----------------------------------------")
            print(reply)
            print("----------------------------------------")
        else:
            if language == "Arabic":
                print("لم يتم استلام استجابة صحيحة. حاولي مرة أخرى.")
            else:
                print("No valid response received. Please try again.")

if __name__ == "__main__":
    main()
