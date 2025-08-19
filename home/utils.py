# Reads the pdf file (extracts the text from pdf)
import pdfplumber
import requests
from django.conf import settings
from django.template.loader import render_to_string
import pdfkit
import os
import uuid

config = pdfkit.configuration(
    wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
)


END_POINT = "https://api.groq.com/openai/v1/chat/completions"

def read_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() or ''
            return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None



def llm_api(text):
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"Summarize the following text and try to make it short as much as possible : \n{text}"

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": "Assistant that Summarizes text"},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(END_POINT, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except requests.exceptions.RequestException as e:
        print(f"Error calling LLM API: {e}")
        return None
    

# def to_pdf(text):
#     try:
#         html = render_to_string('index.html', {'text': text})
#         output_dir = os.path.join(settings.BASE_DIR, 'output_pdfs')
#         os.makedirs(output_dir, exist_ok=True)
#         output_path = os.path.join(output_dir, f'{uuid.uuid4()}.pdf')
#         pdfkit.from_string(html, output_path)
#         print("PDF generated successfully")
#         return output_path
#     except Exception as e:
#         print(f"Error generating PDF: {e}")
#         return None


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def to_pdf(text):
    try:
        output_dir = os.path.join(settings.BASE_DIR, 'output_pdfs')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'{uuid.uuid4()}.pdf')

        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter

        # Break text into lines
        lines = text.split("\n")
        y = height - 50
        for line in lines:
            c.drawString(50, y, line[:1000])  # truncate long lines
            y -= 15
            if y < 50:  # new page
                c.showPage()
                y = height - 50

        c.save()
        print("PDF generated successfully")
        return output_path
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None