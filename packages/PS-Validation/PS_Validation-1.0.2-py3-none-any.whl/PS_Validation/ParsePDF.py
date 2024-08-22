import requests
import fitz
import io
from concurrent.futures import ThreadPoolExecutor

def GetPDFResponse(pdf):
    try:
        local_pdf= pdf.replace('http://download.siliconexpert.com', r'\\10.199.104.160').replace('/', '\\')
        with open(local_pdf, 'rb') as file:
            return pdf, file.read()
    except:
        try:
            header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
                "Accept-Language": "en-US,en;q=0.5"}
            response = requests.get(pdf, timeout=10, headers= header)  
            content = io.BytesIO(response.content)
            return pdf, content
        except:
            pass
def GetPDFText(pdfs):
    pdfData= {}
    chunks = [pdfs[i:i+500] for i in range(0, len(pdfs), 500)]
    for chunk in chunks:
        with ThreadPoolExecutor() as excuter:
            result= list(excuter.map(GetPDFResponse, chunk))
        for pdf, byt  in result:
            try:
                with fitz.open(stream=byt) as doc:
                    pdfData[pdf] = [page.get_text() for page in doc.pages()]
            except:
                None
    return pdfData