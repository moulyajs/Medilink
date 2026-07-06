from pdf2image import convert_from_path

pages = convert_from_path("Dataset_Medilink/user002/lab_report07.pdf")
print(len(pages))
pages[0].save("page.png")