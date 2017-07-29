from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from pyqrcode import *
import os
import json
import sys


# Given a Public key and Private key, generates a Boggs paper wallet
def generate_boggs_cold_storage(public_key, private_key, value):
    value_on_wallet = 'BTC: ' + str(value)
    
    # Create the QRcodes and write it out to disk
    public_code = pyqrcode.create(public_key, error='L', version=3, mode='binary')
    public_code.png('public_code.png', scale=3, quiet_zone=2, module_color=[50, 67, 67, 224], background=[0xE3, 0xE3, 0xD2])
    
    private_code = pyqrcode.create(private_key, error='L', version=3, mode='binary')
    private_code.png('private_code.png', scale=3, quiet_zone=2, module_color=[50, 67, 67, 224], background=[0xE3, 0xE3, 0xD2])
    
    # Open our QR Images so we can paste them onto the template
    public_key_qr = Image.open('public_code.png', 'r')
    private_key_qr = Image.open('private_code.png', 'r')
    
    # Open our Template image 
    template_img = Image.open('boggs.png', 'r')
    
    # Get our Template boundaries
    img_w, img_h = template_img.size
    
    # Offset to place the public_key qr
    public_offset = (86, 265)
    # Paste the image and save our output
    template_img.paste(public_key_qr, public_offset)
    
    # Offset to place the public_key qr
    private_offset = (1165, 319)
    # Paste the image and save our output
    template_img.paste(private_key_qr, private_offset)
    
    # Open a font and write our value to the bill
    font = ImageFont.truetype("Roboto-Regular.ttf", 24)
    coords = (185, 330)
    
    dark_color  = (50, 67, 67)
    bg_color = (227, 227, 210)
    
    # Write our value onto the image
    draw = ImageDraw.Draw(template_img)
    draw.text(coords, value_on_wallet, dark_color, font=font)
    
    # Save out our image to the first 8 chars of our publickey12
    template_img.save(public_key[0:8] + '.png')
    
    # Clean up our directory by removing the qrcode images
    os.remove('public_code.png')
    os.remove('private_code.png')

def generate_multiple_from_json(paper_type):
    # For every key in our json file
    with open('keys.json') as data_file:    
        data = json.load(data_file)
    
    # Create a png
    for key in data:
        if paper_type == 'boggs':
            generate_boggs_cold_storage(key['public'], key['private'], key['value'])
        if paper_type == 'juju':
            generate_juju_cold_storage(key['public'], key['private'])


def generate_juju_cold_storage(public_key, private_key):
    
    # Create the QRcodes and write it out to disk
    public_code = pyqrcode.create(public_key, error='L', version=3, mode='binary')
    public_code.png('public_code.png', scale=5, quiet_zone=2, module_color=[0, 0, 0, 224], background=[0xff, 0xff, 0xff])
    
    private_code = pyqrcode.create(private_key, error='L', version=3, mode='binary')
    private_code.png('private_code.png', scale=5, quiet_zone=2, module_color=[0, 0, 0, 224], background=[0xff, 0xff, 0xff])
    
    # Open our QR Images so we can paste them onto the template
    public_key_qr = Image.open('public_code.png', 'r')
    private_key_qr = Image.open('private_code.png', 'r')
    
    # Open our Template image 
    template_img = Image.open('gul.jpg', 'r')
    
    # Get our Template boundaries
    img_w, img_h = template_img.size
    
    p_w, p_h = public_key_qr.size
    # Offset to place the public_key qr
    public_offset = (img_h/4+p_w/2-50, img_h/2-p_w/2)
    # Paste the image and save our output
    template_img.paste(public_key_qr, public_offset)
    
    # Offset to place the public_key qr
    private_offset = (950, img_h/2-p_w/2)
    # Paste the image and save our output
    template_img.paste(private_key_qr, private_offset)
    
    
    bitcoin_logo = Image.open('opengraph.png', 'r')
    # Offset to place the public_key qr
    bitcoin_logo_offset = (img_w/2-130, img_h/2-125)
    bitcoin_logo = bitcoin_logo.resize((bitcoin_logo.size[0]/2, bitcoin_logo.size[1]/2), Image.ANTIALIAS)
    # Paste the image and save our output
    template_img.paste(bitcoin_logo, bitcoin_logo_offset, bitcoin_logo)
    # Open a font and write our value to the bill
    coords = (100, 60)
    
    dark_color  = (0, 0, 0)
    bg_color = (255, 255, 255)
    
    # Write our value onto the image
    draw = ImageDraw.Draw(template_img)
    
    font = ImageFont.truetype("Roboto-Regular.ttf", 36)
    draw.text((230, 210), 'Public', dark_color, font=font)
    font = ImageFont.truetype("Roboto-Regular.ttf", 16)
    draw.text((135, 430), public_key, dark_color, font=font)
    font = ImageFont.truetype("Roboto-Regular.ttf", 64)
    #draw.text((810, 460), '_________ Bitcoin', dark_color, font=font)
    font = ImageFont.truetype("Roboto-Regular.ttf", 36)
    draw.text((970, 210), 'Private', dark_color, font=font)
    # Save out our image to the first 8 chars of our publickey12
    template_img.save(public_key[0:8] + '.png')
    
    # Clean up our directory by removing the qrcode images
    os.remove('public_code.png')
    os.remove('private_code.png')


if len(sys.argv) == 2:
    if sys.argv[1] == 'juju' or sys.argv[1] == 'boggs':
        generate_multiple_from_json(sys.argv[1])
    else:
        generate_multiple_from_json('boggs')
else:
    generate_multiple_from_json('boggs')