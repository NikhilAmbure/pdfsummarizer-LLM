import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdfsummarizer.settings')

app = Celery('pdfsummarizer')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps
app.autodiscover_tasks()

from home.utils import read_pdf, llm_api, to_pdf


@app.task(bind=True, soft_time_limit=150, time_limit=180)
def summarize_pdf(self, file_path):
    """
    Task to summarize a PDF file
    """
    try:
        print(f"[summarize_pdf] Started. file_path={file_path}")
        text = read_pdf(file_path)
        if not text:
            print("[summarize_pdf] No text extracted from PDF")
            return "Error: Failed to read PDF file"

        print(f"[summarize_pdf] Text extracted. length={len(text)}")
        summarized_text = llm_api(text)
        if not summarized_text:
            print("[summarize_pdf] No summary returned from LLM API")
            return "Error: Failed to generate summary"

        print("[summarize_pdf] Summary generated. Converting to PDF...")
        output_path = to_pdf(summarized_text)
        if not output_path:
            print("[summarize_pdf] PDF generation failed")
            return "Error: Failed to generate output PDF"

        print(f"[summarize_pdf] Completed. output_path={output_path}")
        return output_path
    except Exception as e:
        print(f"Error in summarize_pdf task: {e}")
        return f"Error: {str(e)}"