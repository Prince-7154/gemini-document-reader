from PIL import Image
import base64
import io
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINIAI_API_KEY = os.getenv("GEMINIAI_API_KEY")

genai.configure(api_key=GEMINIAI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")
    return {
        "mime_type": "image/png",
        "data": img_b64,
    }

def load_schema(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def extract_data_as_json(image_path, schema_file, output_file):
    image = Image.open(image_path)
    img_data = image_to_base64(image)
    schema_text = load_schema(schema_file)

    prompt = f"""Extract the data from the given image document which in in nepali and convert it into a JSON object based on the JSON Schema provided below.

    Please strictly follow the structure and field names defined in the schema. Only return the filled JSON object with values extracted from the document. Do not include any explanation or extra text.

    JSON Schema:
    {schema_text}
    """ 

    # prompt = f"""Analyze the given nepali document and create a JSON Schema that accurately represents its structure and data fields.

    # Only return the JSON Schema. Do not include any explanation or sample data.

    # Use appropriate field types (e.g., string, integer, boolean, object) and include descriptions in nepali where possible.
    # """

    response = model.generate_content([
        prompt.strip(),
        img_data
    ])
    
    result = response.text.strip()
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)

    print(f" JSON data extracted and saved to: {output_file}")


extract_data_as_json("3.jpg", "schema_2.json", "extracted_j_3.json")
