from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# استبدل هذا بمفتاح API الخاص بك
API_KEY = "AIzaSyAuWRegcfg9ctF4CKZGYAPf5x0rCzV7jVs"
genai.configure(api_key=API_KEY)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    child_age = data.get("child_age")
    user_prompt = data.get("user_prompt")
    language = data.get("language")
    
    # تكوين رسالة تفصيلية للموديل
    if language == "Arabic":
        full_prompt = f"طفلي عمره {child_age} عامًا. {user_prompt} الإجابة يجب أن تكون قصيرة ومختصة بتربية الأطفال فقط."
    else:
        full_prompt = f"My child is {child_age} years old. {user_prompt} Please provide a brief response related only to parenting."
    
    # إنشاء النموذج
    model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")
    
    # توليد الإجابة
    response = model.generate_content(full_prompt)

    if response and hasattr(response, "candidates") and response.candidates:
        reply = response.candidates[0].content.parts[0].text
        
        # تقليص الإجابة إذا كانت طويلة
        max_length = 100  # عدد الكلمات
        words = reply.split()
        if len(words) > max_length:
            reply = " ".join(words[:max_length]) + "..."
        
        return jsonify({"response": reply})
    else:
        return jsonify({"error": "No valid response received. Please try again."}), 400


if __name__ == "__main__":
    app.run(debug=True)
