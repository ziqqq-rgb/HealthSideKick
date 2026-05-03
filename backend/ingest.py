import os
from dotenv import load_dotenv
from llama_parse import LlamaParse

load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMAPARSE_API_KEY")

def parse_document(file_path: str) -> str:

    try:

        parser = LlamaParse(
            api_key = LLAMA_API_KEY,
            result_type="markdown",
            verbose=True
        )

        documents = parser.load_data(file_path)

        return documents
    
    except Exception as e:
        print(f"Error initializing LlamaParse: {e}")
        return None

if __name__ == "__main__":

    file_path = "./data/sample_guideline.pdf" 

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")

    else:
        parsed_content = parse_document(file_path)
        if parsed_content:
            print("Parsed Document Content:")
            print(parsed_content)
        else:
            print("Failed to parse the document.")