import os
import json
import pdfreader
from pdfreader import SimplePDFViewer
from pathlib import Path


def ingest_pdfs(data_folder):
    banks_data = {}

    for bank_folder in os.listdir(data_folder):
        bank_path = os.path.join(data_folder, bank_folder)
        if os.path.isdir(bank_path):
            banks_data[bank_folder] = []

            for pdf_file in os.listdir(bank_path):
                if pdf_file.endswith(".pdf"):
                    pdf_path = os.path.join(bank_path, pdf_file)

                    with open(pdf_path, "rb") as f:
                        viewer = SimplePDFViewer(f)
                        text = ""

                        for canvas in viewer:
                            viewer.render()
                            text += " ".join(viewer.canvas.strings)

                        banks_data[bank_folder].append(
                            {"file_name": pdf_file, "text": text}
                        )

    return banks_data


def save_ingested_data(data, output_file):
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    data_folder = "data"
    output_file = "ingested_data.json"

    ingested_data = ingest_pdfs(data_folder)
    save_ingested_data(ingested_data, output_file)
