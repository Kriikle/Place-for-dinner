import qrcode


def generate_qr_goods(good_id):
    url = "http://192.168.198.242:5000/good/edit/?id= "+str(good_id)
    img = qrcode.make(url)
    # img = qrcode.make("/goods/" + str(good_id))
    type(img)  # qrcode.image.pil.PilImage
    img_path = "static/qr/good_" + str(good_id) + ".png"

    img.save(img_path)
    return img_path
