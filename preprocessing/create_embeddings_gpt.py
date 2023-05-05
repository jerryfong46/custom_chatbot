import openai
import os

# Define the path to the file containing API keys and descriptions
api_key_file = os.path.join("config", "api_keys.txt")

# Read the file and split the lines by newline
with open(api_key_file, "r") as f:
    api_key_lines = f.read().split("\n")

# Parse the lines into a dictionary
api_keys = {}
for line in api_key_lines:
    if line.strip():
        key_description, api_key = line.split()
        api_keys[key_description.strip("[]")] = api_key

# API Keys
openai.api_key = api_keys["openai"]


# Function to generate embeddings for each chunk of text
def generate_embeddings(processed_data):
    embeddings = {}

    for bank, bank_data in processed_data.items():
        embeddings[bank] = []
        for item in bank_data:
            text_chunk = item["text"]

            # Use OpenAI API to create embeddings
            response = openai.Embed.create(
                model="text-davinci-002",
                prompt=text_chunk,
                n=1,
            )

            # Get the embeddings from the response
            embedding = response.choices[0].embed
            embeddings[bank].append(embedding)

    return embeddings


# Generate the embeddings
embeddings = generate_embeddings(processed_data)

# Save the embeddings to a file
with open("embeddings.json", "w") as f:
    json.dump(embeddings, f)
