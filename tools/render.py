import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parent / "pylib"))
import pypdfium2 as pdfium
from PIL import Image
pdf=pdfium.PdfDocument(sys.argv[1]); pages=[int(x) for x in sys.argv[3].split(",")]
ims=[pdf[p-1].render(scale=1.1).to_pil() for p in pages]
w,h=ims[0].size; cols=min(4,len(ims)); rows=(len(ims)+cols-1)//cols
sheet=Image.new("RGB",(cols*w+(cols-1)*8,rows*h+(rows-1)*8),"#888")
for i,im in enumerate(ims): sheet.paste(im,((i%cols)*(w+8),(i//cols)*(h+8)))
sheet.save(sys.argv[2])
