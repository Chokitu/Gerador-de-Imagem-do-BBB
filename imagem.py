import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFile
from rembg.bg import remove
import io
import os
from io import BytesIO
import base64
import uuid



def imagembbb(nome, idade, profissao, cidade, uuidimage):
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    input_path = (uuidimage +'.png')

    snome = nome
    sidade = idade
    sprofissao = profissao
    scidade = cidade

    sidade = idade + " anos"


    f = np.fromfile(input_path)
    result = remove(f)
    img = Image.open(io.BytesIO(result)).convert("RGBA")

    altura = 1000
    altura_percentual = (altura / float(img.size[1]))
    largura = int((float(img.size[0]) * float(altura_percentual)))
    img = img.resize((largura, altura),Image.ANTIALIAS)
    background = Image.open("bg.png")



    open_cv_image = np.array(img) 

    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)




    # binarize image
    retval, bw = cv2.threshold(gray, 0, 1, cv2.ADAPTIVE_THRESH_MEAN_C)

    # find contour
    contours, hierarchy = cv2.findContours(bw, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)



    # sort by area
    contours.sort(key=cv2.contourArea, reverse=True)
            
    if len(contours[0]) > 0:
        contour = contours[0]

    
        epsilon = cv2.arcLength(contour,True)
        approx = cv2.approxPolyDP(contour,
                                0.003*epsilon, 
                                True)
        cv2.drawContours(open_cv_image, [approx], -1, (255, 0, 247, 255), 3)





    # OpenCV to Pillow
    pil_image = Image.fromarray(open_cv_image)

    nome= ImageDraw.Draw(background)
    idade = ImageDraw.Draw(background)
    profissao = ImageDraw.Draw(background)
    cidade = ImageDraw.Draw(background)
    myFont = ImageFont.truetype('BebasNeue.otf', 60)


    nome.text((603, 153), snome, font=myFont, fill =(157, 111, 207))
    idade.text((603, 213), sidade, font=myFont, fill =(157, 111, 207))
    profissao.text((603, 273), sprofissao, font=myFont, fill =(157, 111, 207))
    cidade.text((603, 333), scidade, font=myFont, fill =(157, 111, 207))

    nome.text((600, 150), snome, font=myFont, fill =(6, 181, 250))
    idade.text((600, 210), sidade, font=myFont, fill =(255, 211, 47))
    profissao.text((600, 270), sprofissao, font=myFont, fill =(6, 181, 250))
    cidade.text((600, 330), scidade, font=myFont, fill =(255, 211, 47))

    background.paste(pil_image, (0, 0), pil_image)




    buffered = BytesIO()
    background.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    imagem64 = str(img_str).replace("'", "")
    imagem64 = imagem64[1:]
    return "data:image/png;base64," + imagem64