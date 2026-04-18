from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification
from pdf2image import convert_from_path
import torch

# Load model
processor = LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base", apply_ocr=True)
model = LayoutLMv3ForTokenClassification.from_pretrained("microsoft/layoutlmv3-base")

# Convert PDF → images
images = convert_from_path("Dataset_Medilink/user003/lab_report2.pdf")

# Take first page (you can loop later)
image = images[0]

# Process
encoding = processor(image, return_tensors="pt")

# Inference
with torch.no_grad():
    outputs = model(**encoding)

logits = outputs.logits
predictions = torch.argmax(logits, dim=-1)

tokens = processor.tokenizer.convert_ids_to_tokens(encoding.input_ids[0])

# Print
for token, pred in zip(tokens, predictions[0]):
    print(f"{token:15} -> {pred.item()}")
    