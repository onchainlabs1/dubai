from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

csv_path = "geocoded_sample.csv"
json_path = "dubai_properties.json"

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Data file missing: {csv_path}")

print("Converting data to supported format...")
df = pd.read_csv(csv_path)
df.to_json(json_path, orient='records', indent=2)


with open(json_path, "rb") as f:
    data_file = client.files.create(file=f, purpose="assistants")
print(f"Data uploaded (File ID: {data_file.id})")

# 2. Define the knowledge schema and instructions
schema_description = """
The CSV contains Dubai real estate transaction records. Here's the schema:

- transaction_id (string): unique identifier
- procedure_id (int): type of legal procedure  
- trans_group_en (string): transaction group
- procedure_name_en (string): specific procedure name
- instance_date (string): DD-MM-YYYY format
- property_type_en (string): property type
- area_name_en (string): neighborhood/area
- procedure_area (float): area in sqm
- actual_worth (float): transaction amount (AED)
- meter_sale_price (float): price per sqm
- rent_value (float): rental value
- latitude, longitude (float): coordinates
- no_of_parties_role_X (float): parties per role
"""

instructions = f"""
You are a Dubai real estate expert with these capabilities:

1. DATA ANALYSIS:
- Analyze transaction records thoroughly
- Provide specific numbers and comparisons
- Calculate metrics like averages and trends

2. GEOCODING:
For unknown locations, use:
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="dubai_re")
location = geolocator.geocode("LOCATION, Dubai, UAE")

3. RESPONSE RULES:
- Never say "based on the dataset"
- Never ask for files - you already have them
- For missing data, say "Data not available"
- Include specific numbers when possible

DATA SCHEMA:
{schema_description}
"""

assistant = client.beta.assistants.create(
    name="Dubai Property Expert",
    instructions=instructions,
    model="gpt-4.1",
    tools=[{"type": "code_interpreter"}, {"type": "file_search"}],
)

print(f"Assistant ready (ID: {assistant.id})")

with open(".env", "w") as f:
    f.write(f"ASSISTANT_ID={assistant.id}\n")
    f.write(f"FILE_ID={data_file.id}\n")