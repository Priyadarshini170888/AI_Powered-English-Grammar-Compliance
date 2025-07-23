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
