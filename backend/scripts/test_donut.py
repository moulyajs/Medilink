from transformers import DonutProcessor, VisionEncoderDecoderModel
from pdf2image import convert_from_path
import torch

MODEL_NAME = "naver-clova-ix/donut-base-finetuned-docvqa"

processor = DonutProcessor.from_pretrained(MODEL_NAME)
model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME)

images = convert_from_path("Dataset_Medilink/user003/lab_report2.pdf")
image = images[0]

pixel_values = processor(image, return_tensors="pt").pixel_values

task_prompt = "<s_docvqa><s_question>Extract all text</s_question><s_answer>"

decoder_input_ids = processor.tokenizer(
    task_prompt,
    add_special_tokens=False,
    return_tensors="pt"
).input_ids

with torch.no_grad():
    outputs = model.generate(
        pixel_values,
        decoder_input_ids=decoder_input_ids,
        max_length=512
    )

result = processor.batch_decode(outputs, skip_special_tokens=True)[0]
print(result)