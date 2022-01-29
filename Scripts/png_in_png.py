from os import path
import numpy as np
from PIL import Image


def message_to_bits(message: str, stop_marker: str = "$END$") -> str:
    message += stop_marker
    bits = ''.join(f"{ord(c):08b}" for c in message)
    return bits


def bits_to_message(bits, stop_marker: str = "$END$") -> None:
    message_ints = [int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)]
    message = ''.join([chr(i) for i in message_ints])
    if stop_marker in message:
        print(message[0:message.index(stop_marker)])
    else:
        print('No secret message found.')


def image_to_bits(path_to_image: str) -> str:
    image = Image.open(path_to_image, 'r')
    width, height = image.size
    img_arr = np.array(list(image.getdata()))

    if image.mode != 'RGB':
        print("Can't handle non-RGB images !")
        exit()
    else:
        channels = 3
        pixels = img_arr.size // channels

        # adding the width, height and channels ints to the beginning of the bit string
        image_bits = format(int(width), '020b') + format(int(height), '020b') + format(int(channels), '020b')

        for i in range(pixels):
            for j in range(0, 3):
                image_bits += format(img_arr[i][j], '08b')

        return image_bits


def bits_to_image(bits: str, path_to_save: str):
    width = int(bits[0:20], 2)
    height = int(bits[20:40], 2)
    channels = int(bits[40:60], 2)
    pixels = width * height
    img_arr = np.zeros((pixels, channels))

    image_bits = bits[60:]

    idx = 0
    for i in range(pixels):
        for j in range(0, 3):
            img_arr[i][j] = int(image_bits[idx:idx+8], 2)
            idx += 8

    img_arr = img_arr.reshape((height, width, channels))
    encoded_image = Image.fromarray(img_arr.astype('uint8'), mode='RGB')
    encoded_image.save(path_to_save)


def image_lsb_encoding(path_to_image: str, path_to_save: str, message_bits: str):
    print('... Image Encoding ...')
    image = Image.open(path_to_image, 'r')
    width, height = image.size
    img_arr = np.array(list(image.getdata()))

    if image.mode == 'P':
        print("Can't handle image mode P")
        exit()

    channels = 4 if image.mode == "RGBA" else 3
    pixels = img_arr.size // channels

    message_bits_length = len(message_bits)

    if message_bits_length > pixels:
        print("The image does not have enough pixels to store message!")
        exit()

    idx = 0
    for i in range(pixels):
        for j in range(0, 3):
            if idx < message_bits_length:
                img_arr[i][j] = int(bin(img_arr[i][j])[2:-1] + message_bits[idx], 2)
                idx += 1

    img_arr = img_arr.reshape((height, width, channels))
    encoded_image = Image.fromarray(img_arr.astype('uint8'), image.mode)
    encoded_image.save(path_to_save)


def image_lsb_decoding(path_to_image: str):
    print('... Image Decoding ...')
    new_image = Image.open(path_to_image, 'r')
    img_arr = np.array(list(new_image.getdata()))

    if new_image.mode == "P":
        print("Can't handle image mode P")
        exit()

    channels = 4 if new_image.mode == 'RGBA' else 3
    pixels = img_arr.size // channels

    lsb_bits = ''
    for i in range(pixels):
        for j in range(0, 3):
            lsb_bits += bin(img_arr[i][j])[-1]

    return lsb_bits


if __name__ == '__main__':
    secrete_message_example = False
    secrete_image_example = True

    if secrete_message_example:
        path_to_dir = "../Assets"
        image_name = "Indiana_street.png"
        encoded_image_name = "Indiana_street_message_encoded.png"
        stop_marker = '&END&'
        secret_message = 'You know that everything you think and do is thought and done by you. But what is a "you"? ' \
                         'What kinds of smaller entities cooperate inside your mind to do your work? (Minsky, 1988)'

        # hiding the message in the image
        bits = message_to_bits(secret_message, stop_marker=stop_marker)
        image_lsb_encoding(path_to_image=path.join(path_to_dir, image_name),
                           path_to_save=path.join(path_to_dir, encoded_image_name),
                           message_bits=bits)

        # extracting the message from the image
        bits = image_lsb_decoding(path_to_image=path.join(path_to_dir, encoded_image_name))
        bits_to_message(bits, stop_marker=stop_marker)

    if secrete_image_example:
        path_to_dir = "../Assets"
        image_name = "Indiana_street.png"
        secrete_image_name = "street_night.png"
        encoded_image_name = "Indiana_street_image_encoded.png"
        decoded_secrete_image_name = "street_night_decoded.png"

        # hiding the secrete image inside the original image
        bits = image_to_bits(path_to_image=path.join(path_to_dir, secrete_image_name))
        image_lsb_encoding(path_to_image=path.join(path_to_dir, image_name),
                           path_to_save=path.join(path_to_dir, encoded_image_name),
                           message_bits=bits)

        # extracting the secrete image from the decoded image
        bits = image_lsb_decoding(path_to_image=path.join(path_to_dir, encoded_image_name))
        bits_to_image(bits, path_to_save=path.join(path_to_dir, decoded_secrete_image_name))



