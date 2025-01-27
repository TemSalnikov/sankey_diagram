import read_pdf as rp
import os

if __name__ == '__main__':
    pre_path = os. getcwd()
    text = rp.extract_text_from_pdf(pdf_path=pre_path+'/read_pdf/pdf/Выписка по счёту дебетовой карты.pdf')
    print(text)