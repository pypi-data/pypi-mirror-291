import tempfile
import fitz  # PyMuPDF
from PIL import Image
import easyocr

def pdf_to_images(pdf_path, dpi=300):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    images_paths = []
    temp = tempfile.mkdtemp(prefix="pre_",suffix="_suf")
    # Loop through all pages
    for page_number in range(len(pdf_document)):
        # Select the page
        page = pdf_document.load_page(page_number)
        # Convert page to a pixmap (image)
        zoom = dpi / 72  # DPI conversion factor
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        # Save the pixmap as an image
        img_path = f'{temp}\\page_{page_number+1}.png'
        pix.save(img_path)
        images_paths.append(img_path)
    return images_paths

def crop_image(image_path, crop_box):
    # Open the image
    temp = tempfile.mkdtemp(prefix="pre_",suffix="_suf")
    with Image.open(image_path) as img:
        # Crop the image
        cropped_img = img.crop(crop_box)
        # Save the cropped image
        cropped_img_path = f'{temp}\\page.png'
        cropped_img.save(cropped_img_path, dpi=(img.info['dpi']))
    return cropped_img_path

# Example usagepy
class MultiPdf :
    def MultiOcr(pdf_path,crop_box,dpi=300):
        AllResult = []
        # pdf_path = './p16.pdf'
        # dpi = 300
        # Convert PDF pages to images
        images_paths = pdf_to_images(pdf_path, dpi)
        # print(images_paths)
        # Define crop box (left, upper, right, lower)
        # crop_box = (2000, 550, 2200, 640) 
        # Crop and save each image
        cropped_images_paths = [crop_image(image_path, crop_box) for image_path in images_paths]
        for page,path in enumerate(cropped_images_paths):
            reader = easyocr.Reader(['en'])
            allResults = reader.readtext(path)
            AllResult.append(allResults)
            # print(allResults)
        return AllResult

# print(MultiPdf.MultiOcr('./p16.pdf',(2000, 550, 2200, 640) ,300))