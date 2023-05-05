import re


def preprocess_and_tokenize(text):
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = text.lower()
    tokens = text.split()
    return tokens


# Chunk the tokenized text into smaller pieces
def chunk_text(tokens, chunk_size):
    return [tokens[i : i + chunk_size] for i in range(0, len(tokens), chunk_size)]


# process the extracted text by iterating over the ingested data
def process_extracted_text(ingested_data, chunk_size=100):
    processed_data = {}

    for bank, bank_data in ingested_data.items():
        processed_data[bank] = []

        for data in bank_data:
            tokens = preprocess_and_tokenize(data["text"])
            chunks = chunk_text(tokens, chunk_size)

            for i, chunk in enumerate(chunks):
                processed_data[bank].append(
                    {"file_name": data["file_name"], "chunk_id": i, "tokens": chunk}
                )

    return processed_data


# Call this function on the ingested data and save the processed data to a new JSON file
def save_processed_data(data, output_file):
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    processed_data_output_file = "processed_data.json"

    processed_data = process_extracted_text(ingested_data)
    save_processed_data(processed_data, processed_data_output_file)
