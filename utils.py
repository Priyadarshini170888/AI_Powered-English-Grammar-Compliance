# utils.py
# import os
# import docx2txt
# import fitz  # PyMuPDF
# import requests

# GINGER_API_URL = "http://services.gingersoftware.com/Ginger/correct/jsonSecured"


# def extract_text_from_file(filepath):
#     ext = os.path.splitext(filepath)[1].lower()
#     if ext == '.pdf':
#         return extract_text_from_pdf(filepath)
#     elif ext == '.docx':
#         return docx2txt.process(filepath)
#     return ''

# def extract_text_from_pdf(filepath):
#     text = ""
#     with fitz.open(filepath) as doc:
#         for page in doc:
#             text += page.get_text()
#     return text

# def analyze_text(text):
#     corrected_text, issues = grammar_check(text)
#     return {'total_issues': len(issues), 'issues': issues}

# def correct_text(text):
#     corrected_text, _ = grammar_check(text)
    # return corrected_text

# def grammar_check(text):
#     params = {
#         "lang": "US",
#         "clientVersion": "2.0",
#         "text": text
#     }
#     response = requests.get(GINGER_API_URL, params=params)
#     data = response.json()
#     suggestions = data.get("Corrections", [])

#     corrected_text = list(text)
#     issues = []
#     offset_shift = 0

#     for suggestion in suggestions:
#         start = suggestion["From"] + offset_shift
#         end = suggestion["To"] + 1 + offset_shift
#         new_word = suggestion["Suggestions"][0]["Text"]

#         original_word = text[suggestion["From"]:suggestion["To"] + 1]
#         issues.append({
#             "error": original_word,
#             "suggestion": new_word,
#             "position": [start, end]
#         })

#         corrected_text[start:end] = new_word
#         offset_shift += len(new_word) - (end - start)

#     return ("".join(corrected_text), issues)


# -------------------------------------------------------------------


# def grammar_check(text):
#     if not text.strip():
#         return text, []

#     try:
#         params = {
#             "lang": "US",
#             "clientVersion": "2.0",
#             "text": text
#         }
#         response = requests.get(GINGER_API_URL, params=params)

#         # Safeguard against non-200 or empty response
#         if response.status_code != 200 or not response.text.strip():
#             print("❌ Ginger API failed. Status:", response.status_code)
#             print("❌ Raw response:", response.text)
#             return text, []

#         try:
#             data = response.json()
#         except Exception as e:
#             print("❌ Failed to decode JSON:", e)
#             print("❌ Raw response:", response.text)
#             return text, []

#         suggestions = data.get("Corrections", [])
#         corrected_text = list(text)
#         issues = []
#         offset_shift = 0

#         for suggestion in suggestions:
#             from_pos = suggestion["From"] + offset_shift
#             to_pos = suggestion["To"] + 1 + offset_shift
#             new_word = suggestion["Suggestions"][0]["Text"]
#             original_word = text[suggestion["From"]:suggestion["To"] + 1]

#             issues.append({
#                 "error": original_word,
#                 "suggestion": new_word,
#                 "position": [from_pos, to_pos]
#             })

#             corrected_text[from_pos:to_pos] = new_word
#             offset_shift += len(new_word) - (to_pos - from_pos)

#         return "".join(corrected_text), issues

#     except requests.exceptions.RequestException as e:
#         print("❌ Network error during Ginger API call:", e)


# def save_text_to_file(text, original_filename, output_folder):
#     name, _ = os.path.splitext(original_filename)
#     output_path = os.path.join(output_folder, f"{name}_corrected.txt")
#     with open(output_path, 'w', encoding='utf-8') as f:
#         f.write(text)
#     return output_path





# utils.py
# import os
# import docx2txt
# import fitz  # PyMuPDF
# import openai

# openai.api_key = os.getenv("OPENAI_API_KEY")  # Set this environment variable securely

# from openai import OpenAI

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# client = OpenAI(api_key="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")


# def extract_text_from_file(filepath):
#     ext = os.path.splitext(filepath)[1].lower()
#     if ext == '.pdf':
#         return extract_text_from_pdf(filepath)
#     elif ext == '.docx':
#         return docx2txt.process(filepath)
#     return ''

# def extract_text_from_pdf(filepath):
#     text = ""
#     with fitz.open(filepath) as doc:
#         for page in doc:
#             text += page.get_text()
#     return text

# def analyze_text(text):
#     corrected_text = correct_text(text)
#     issues = []
#     if corrected_text.strip() != text.strip():
#         issues.append({"message": "Text corrected by GPT"})
#     return {"total_issues": len(issues), "issues": issues}

# def correct_text(text):
#     try:
#         prompt = f"Correct the grammar, punctuation, and sentence structure of the following text:\n\n{text}"
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant that corrects grammar."},
#                 {"role": "user", "content": prompt}
#                 ],
#             temperature=0.2,
#              max_tokens=2048
#         )
#         corrected = response.choices[0].message.content

#         return corrected
#     except Exception as e:
#         print("GPT Correction Error:", e)
#         return text

# def save_text_to_file(text, original_filename, output_folder):
#     name, _ = os.path.splitext(original_filename)
#     output_path = os.path.join(output_folder, f"{name}_corrected.txt")
#     with open(output_path, 'w', encoding='utf-8') as f:
#         f.write(text)
#     return output_path



import os
import docx2txt
import fitz  # PyMuPDF
import requests

LANGUAGETOOL_API_URL = "https://api.languagetool.org/v2/check"

def extract_text_from_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(filepath)
    elif ext == '.docx':
        return docx2txt.process(filepath)
    return ''

def extract_text_from_pdf(filepath):
    text = ""
    with fitz.open(filepath) as doc:
        for page in doc:
            text += page.get_text()
    return text

def analyze_text(text):
    corrected_text, issues = grammar_check(text)
    return {'total_issues': len(issues), 'issues': issues}

def correct_text(text):
    corrected_text, _ = grammar_check(text)
    return corrected_text

def grammar_check(text):
    try:
        data = {
            'text': text,
            'language': 'en-US'
        }
        response = requests.post(LANGUAGETOOL_API_URL, data=data)
        result = response.json()
        matches = result.get("matches", [])

        corrected_text = list(text)
        offset_shift = 0
        issues = []

        for match in matches:
            offset = match["offset"] + offset_shift
            length = match["length"]
            replacement = match["replacements"][0]["value"] if match["replacements"] else None

            if replacement:
                corrected_text[offset:offset+length] = replacement
                offset_shift += len(replacement) - length
                issues.append({
                    "error": text[offset:offset+length],
                    "suggestion": replacement,
                    "context": match.get("context", {}).get("text", "")
                })

        return ("".join(corrected_text), issues)

    except Exception as e:
        print("LanguageTool API Error:", e)
        return text, []

def save_text_to_file(text, original_filename, output_folder):
    name, _ = os.path.splitext(original_filename)
    output_path = os.path.join(output_folder, f"{name}_corrected.txt")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return output_path
