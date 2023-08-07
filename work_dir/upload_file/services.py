import tabula

# def extract_text_from_pdf(file):
df = tabula.read_pdf('Tasu Vasile.pdf', pages='3')
print(df[0].columns[0])
print(df[0].columns[1])