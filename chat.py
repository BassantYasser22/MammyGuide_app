import os
import google.generativeai as genai
from PIL import Image
import PyPDF2
import cv2  # OpenCV لمعالجة الفيديو

# 🛑 استبدلي هذا بمفتاح API الخاص بك
API_KEY = "AIzaSyAuWRegcfg9ctF4CKZGYAPf5x0rCzV7jVs"

# ⚙️ تهيئة genai باستخدام المفتاح
genai.configure(api_key=API_KEY)


def process_images(image_dir='image_data'):
    """تحميل الصور من المجلد وتحويلها إلى كائنات PIL Image."""
    if not os.path.exists(image_dir):
        raise FileNotFoundError(f"Error: Directory '{image_dir}' not found.")

    images = [Image.open(os.path.join(image_dir, file))
              for file in os.listdir(image_dir)
              if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    if not images:
        raise FileNotFoundError(f"No image files found in '{image_dir}'.")
    
    return images


def process_file(file_path):
    """تحديد نوع الملف (نص أو PDF) ومعالجته."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: File '{file_path}' not found.")

    return process_pdf(file_path) if file_path.lower().endswith('.pdf') else process_text(file_path)


def process_text(file_path):
    """قراءة الملفات النصية."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def process_pdf(file_path):
    """استخراج النصوص من ملفات PDF."""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        return ''.join(page.extract_text() or '' for page in pdf_reader.pages)


def process_video(video_path):
    """استخراج الإطارات الأساسية من الفيديو وتحويلها إلى صور."""
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Error: Video file '{video_path}' not found.")

    try:
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            raise ValueError(f"Error: Could not open video file '{video_path}'.")

        keyframes = []
        fps = video.get(cv2.CAP_PROP_FPS) or 30
        frame_interval = int(fps)

        frame_count = 0
        while True:
            ret, frame = video.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                keyframes.append(Image.fromarray(frame))

            frame_count += 1

        video.release()
        if not keyframes:
            raise ValueError("Failed to extract keyframes from the video.")
        
        return keyframes

    except Exception as e:
        raise RuntimeError(f"Error processing video: {e}")


def main():
    """البرنامج الرئيسي لمعالجة الملفات بناءً على إدخال المستخدم."""
    file_type = input("Enter file type (image/file/video): ").strip().lower()

    if file_type == "image":
        content = process_images()

    elif file_type == "file":
        file_data_dir = 'file_data'
        if not os.path.exists(file_data_dir):
            raise FileNotFoundError(f"Error: Directory '{file_data_dir}' not found.")

        files = [f for f in os.listdir(file_data_dir) if os.path.isfile(os.path.join(file_data_dir, f))]
        if not files:
            raise FileNotFoundError(f"No files found in '{file_data_dir}'.")

        file_path = os.path.join(file_data_dir, files[0])
        content = process_file(file_path)

    elif file_type == "video":
        video_data_dir = 'video_data'
        if not os.path.exists(video_data_dir):
            raise FileNotFoundError(f"Error: Directory '{video_data_dir}' not found.")

        video_files = [f for f in os.listdir(video_data_dir) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
        if not video_files:
            raise FileNotFoundError(f"No supported video files found in '{video_data_dir}'.")

        video_path = os.path.join(video_data_dir, video_files[0])
        content = process_video(video_path)

    else:
        raise ValueError("Invalid file type. Please choose 'image', 'file', or 'video'.")

    model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")

    user_prompt = input("Enter your prompt: ")

    # معالجة الإدخال حسب نوع الملف
    response = model.generate_content([user_prompt] + content) if file_type in ("image", "video") else model.generate_content([user_prompt, content])

    print(response.text)
   
   


if __name__ == "__main__":
    main()
