import pypdf as pd    

path = "Violin 003 Solo fixed.pdf"

writer = pd.PdfWriter()
reader = pd.PdfReader(path)

page = reader.pages[0]
writer.add_page(page)
writer.pages[0].rotate(180)
for a in range(1,len(reader.pages)):
        print(a)
        writer.add_page(reader.pages[a])
writer.write("Violin 003  Solo Fixed.pdf")
