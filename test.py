from google import genai
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

load_dotenv()
GEMINIAI_API_KEY = os.getenv("GEMINIAI_API_KEY")


class DeceasedDetails(BaseModel):
    name: str
    occupation: str
    address: str
    policyNumber: Optional[str]
    dateOfBirthBS: str
    placeOfBirth: str
    citizenshipNumber: str


class ClaimantDetails(BaseModel):
    name: str
    address: str
    relationshipToDeceased: str
    phoneNumber: str


class DeathDetails(BaseModel):
    dateOfDeathAD: str
    timeOfDeath: str
    placeOfDeath: str
    causeOfDeath: str


class ClaimForm(BaseModel):
    title: Optional[str]
    description: Optional[str]
    policyNumber: str
    deceasedDetails: DeceasedDetails
    claimantDetails: ClaimantDetails
    deathDetails: DeathDetails
    claimingCapacity: str
    branchOffice: str
    full_address: str
    authorized_person_name: str
    authorized_person_rank: str
    signature_present: bool
    date: str
    phone_number: str
    office_seal_present: bool

client = genai.Client(api_key=GEMINIAI_API_KEY)

my_image = client.files.upload(file="2.jpg")


response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=[my_image,"""
You are a helpful assistant that extracts structured data from Nepali insurance documents.

Extract and convert the document into JSON as per the given schema, including all required fields such as policy number, deceased details, claimant details, date, branch office, etc.
"""],
    config={
        "response_mime_type": "application/json",
        "response_schema": ClaimForm,
    },
)

with open("test.json","w",encoding="utf-8") as f:
    f.write(response.text)

print(f"JSON data extracted and saved")
print(response.text)

claim_data: ClaimForm = response.parsed