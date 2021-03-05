from PyPDF2 import PdfFileMerger, PdfFileReader

def merge_pdf(pdf_names,out_file):
    mergedObject = PdfFileMerger()
    for pdf_name in pdf_names:
        try:
            pdf_reader =  PdfFileReader(open(pdf_name,'rb'))
            #print(pdf_name)
        except Exception as e:
            print(e)
            continue

        mergedObject.append(pdf_reader)

    mergedObject.write(out_file)
    mergedObject.close()

if __name__ == '__main__':
    pdf_names = ['generated/1.pdf','generated/2.pdf','generated/4.pdf']

    out_file = "mergedfilesoutput.pdf"
    merge_pdf(pdf_names,out_file)
