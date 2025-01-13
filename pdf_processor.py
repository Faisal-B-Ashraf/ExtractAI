import pdfplumber
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

# def split_text_by_tokens(text, max_tokens=100000):
#     encoded_text = encoding.encode(text)
#     chunks = []
#     while len(encoded_text) > max_tokens:
#         chunks.append(encoding.decode(encoded_text[:max_tokens]))
#         encoded_text = encoded_text[max_tokens:]
#     chunks.append(encoding.decode(encoded_text))
#     return chunks
