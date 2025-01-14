import pdfplumber
import re
# import tiktoken

# encoding = tiktoken.encoding_for_model("gpt-4o-mini")

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text



def split_text_by_tokens(text, max_tokens=100000):
    text = text.replace("\t", " ")
    sentences = [s.lstrip() for s in text.splitlines() if s]
    sentences = [re.sub(" +", " ", x) for x in sentences]
    sentences = [x.replace(". \n", ".\n") for x in sentences]

    ret = []
    sen = ""
    for line in sentences:
        # if not "." in line:
        if "." not in line.lower()[-5:]:
            sen += line + "\n"
            # if line.lower() in sections_to_skip:
        else:
            sen += line
            ret.append(sen)
            sen = ""

    return ret
