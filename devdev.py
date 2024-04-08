import pdfplumber
from google.cloud import generativeai

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ''
        for page in pdf.pages:
            full_text += page.extract_text() + '\n'
    return full_text

def process_text_with_generativeai(text, project_id, location, model_name):
    client = generativeai.CompletionsClient()
    parent = f"projects/{project_id}/locations/{location}/models/{model_name}"

    response = client.complete_text(
        parent=parent,
        prompt=text,
        max_length=2048  # Adjust based on your requirement
    )
    return response.completions[0].text

def main(pdf_path, project_id, location, model_name):
    text = extract_text_from_pdf(pdf_path)
    completion = process_text_with_generativeai(text, project_id, location, model_name)

    # Process the completion as needed, for example, printing or saving to a file
    print(completion)

if __name__ == "__main__":
    pdf_path = 'raw_stcc_data.pdf'
    project_id = 'benderbeattyexport02'
    location = 'us-central1'  # e.g., 'us-central1'
    model_name = 'gemini-pro'  # Model name as per the Generative AI setup

    main(pdf_path, project_id, location, model_name)
