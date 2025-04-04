import re
import nltk
import requests
from camel_tools.utils.normalize import normalize_unicode

# Ensure the necessary NLTK data is downloaded
nltk.download('punkt')

# Function to normalize Arabic text (remove diacritics, normalize alefs, etc.)
def normalize_arabic(text):
    if not text:
        return ""

    # Normalize Unicode form
    text = normalize_unicode(text)

    # Replace different forms of alef with simple alef
    text = re.sub("[إأآا]", "ا", text)

    # Replace different forms of hamza
    text = re.sub("ؤ", "و", text)
    text = re.sub("ئ", "ي", text)

    # Remove diacritics (tashkeel)
    text = re.sub("[\u064B-\u0652]", "", text)

    return text

# Function to get synonyms from Al-Maany API
def get_arabic_synonyms(word):
    url = f"https://api.almaany.com/search/{word}/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        synonyms = [entry['definition'] for entry in data.get('synonyms', [])]
        if not synonyms:
            return [word]
        return synonyms
    else:
        return [word]

# Function to handle Arabic word variations
def get_word_variations(word):
    variations = [word]
    normalized_word = normalize_arabic(word)
    if normalized_word != word:
        variations.append(normalized_word)

    if ' ' in word:
        parts = word.split()
        variations.extend(parts)
        normalized_parts = [normalize_arabic(part) for part in parts]
        variations.extend(normalized_parts)

    for base_word in [word, normalized_word]:
        if base_word.startswith('ال'):
            variations.append(base_word[2:])
        else:
            variations.append('ال' + base_word)

    prefixes = ['ي', 'ت', 'ن', 'أ', 'ا', 'م', 'ال']
    suffixes = ['ون', 'ان', 'ين', 'ات', 'ة']

    base_word = word[2:] if word.startswith('ال') else word
    norm_base = normalize_arabic(base_word)

    variations.append(base_word)
    variations.append(norm_base)

    if len(base_word) >= 3:
        variations.append('م' + base_word)
        variations.append('م' + norm_base)
        variations.append('م' + base_word + 'ين')
        variations.append('م' + norm_base + 'ين')
        variations.append('يت' + base_word)
        variations.append('يت' + norm_base)
        variations.append('ت' + base_word)
        variations.append('ت' + norm_base)

    base_forms = [base_word, norm_base]
    for base in base_forms:
        if ' ' not in base:
            for prefix in prefixes:
                variations.append(prefix + base)
            for suffix in suffixes:
                variations.append(base + suffix)

    variations = list(set(filter(None, variations)))

    return variations

# Function to search sentences containing the word or its variants
def search_word_and_synonyms_in_content(content, search_word):
    normalized_content = normalize_arabic(content)
    word_variations = get_word_variations(search_word)

    all_forms = []
    for variation in word_variations:
        all_forms.append(variation)
        all_forms.append(normalize_arabic(variation))

    all_forms = sorted(list(set(all_forms)), key=len, reverse=True)

    original_sentences = re.split(r'(?<=[.؟!])\s+', content)
    normalized_sentences = re.split(r'(?<=[.؟!])\s+', normalized_content)

    relevant_sentences = []
    for norm_sentence, orig_sentence in zip(normalized_sentences, original_sentences):
        found = False

        for form in all_forms:
            pattern = r'\b' + re.escape(form) + r'\b'
            if re.search(pattern, orig_sentence) or re.search(pattern, norm_sentence):
                relevant_sentences.append(orig_sentence)
                found = True
                break

        if found:
            continue

        for form in all_forms:
            if len(form) >= 3 and (form in orig_sentence or form in norm_sentence):
                relevant_sentences.append(orig_sentence)
                found = True
                break

        if not found and ' ' in search_word:
            parts = search_word.split()
            norm_parts = [normalize_arabic(part) for part in parts]

            if (all(part in orig_sentence for part in parts) or
                all(part in norm_sentence for part in norm_parts)):
                relevant_sentences.append(orig_sentence)

    unique_sentences = []
    for sentence in relevant_sentences:
        if sentence not in unique_sentences:
            unique_sentences.append(sentence)

    if not unique_sentences:
        return f"لم يتم العثور على الكلمة '{search_word}' أو مرادفاتها في النص."
    else:
        result = f"\nالجمل التي تحتوي على الكلمة '{search_word}' أو مرادفاتها:"
        for sentence in unique_sentences:
            result += f"\n- {sentence}"
        return result

def main():
    file_path = 'C:/Users/HFCS/Desktop/Project/Search_Posts/posts.txt'
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            arabic_text = file.read()
        while True:
            search_word = input("من فضلك، أدخل الكلمة التي تريد البحث عنها (أو اكتب 'خروج' للخروج): ").strip()
            if search_word == 'خروج':
                print("تم الخروج من البرنامج.")
                break
            result = search_word_and_synonyms_in_content(arabic_text, search_word)
            print(result)

    except FileNotFoundError:
        print(f"لم يتم العثور على الملف في المسار {file_path}. تأكد من أن الملف موجود.")
    except Exception as e:
        print(f"حدث خطأ: {str(e)}")

if __name__ == "__main__":
    main()