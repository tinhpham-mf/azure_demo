from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.document import DocumentTranslationClient
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential
import os
import random
from pathlib import Path
import pymysql
app = FastAPI()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn gốc
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP (GET, POST, v.v.)
    allow_headers=["*"],  # Cho phép tất cả các headers
)


DBHOST = os.getenv("DBHOST")
DBUSER = os.getenv("DBUSER")
DBPASS = os.getenv("DBPASS")
DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv("DOCUMENT_INTELLIGENCE_ENDPOINT")
TRANSLATOR_ENDPOINT = os.getenv("TRANSLATOR_ENDPOINT")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
print(f"Document Intelligence Endpoint: {DOCUMENT_INTELLIGENCE_ENDPOINT}")
print(f"Translator Endpoint: {TRANSLATOR_ENDPOINT}")
print(f"OpenAI Endpoint: {OPENAI_ENDPOINT}")
# Cấu hình Azure OpenAI
default_credential = DefaultAzureCredential()

# Cấu hình Azure OpenAI với Azure AD
client = AzureOpenAI(
    azure_endpoint = os.getenv("OPENAI_ENDPOINT"),
    api_version = "2023-05-15",
    azure_ad_token = default_credential.get_token("https://cognitiveservices.azure.com/.default").token
)
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}

@app.get("/api/random-number")
def get_random_number():
    number = random.randint(1, 100)
    return {"random_number": number}

@app.get("/api/read-file")
def read_file():
    file_path = Path("/mnt/efs/test/wellcome.txt")
    
    if file_path.exists():
        try:
            with file_path.open("r") as file:
                content = file.read()
            return {"file_content": content}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail="File not found.")
    

@app.get("/api/test-document-intelligence")
def test_document_intelligence():
    try:
        # Create a DocumentAnalysisClient
        client = DocumentAnalysisClient(
            endpoint=DOCUMENT_INTELLIGENCE_ENDPOINT,
            credential=default_credential
        )
        # Dummy call to check connection (e.g., list models)
        models = client.list_models()
        return {"status": "connected", "models": [model.model_id for model in models]}
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"Failed to connect to Document Intelligence: {str(e)}")

@app.get("/api/test-translator")
def test_translator():
    try:
        # Create a DocumentTranslationClient
        client = DocumentTranslationClient(
            endpoint=TRANSLATOR_ENDPOINT,
            credential=default_credential
        )
        # Dummy call to check connection (e.g., list glossary)
        operations = client.list_translation_statuses()
        return {"status": "connected", "operations": [op.id for op in operations]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Translator: {str(e)}")

@app.get("/test-connection")
async def test_connection():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Thay đổi tên model nếu cần
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What's the meaning of life?"}
            ]
        )
        return {"message": "Success", "response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@app.get("/test-mysql")
async def test_mysql():
    try:
        connection = pymysql.connect(
            host=DBHOST,
            user=DBUSER,
            password=DBPASS,
            port=3306,
            database="pymysqldbnonprod"
        )
        connection.close()
        return {"message": "MySQL connection successful!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))