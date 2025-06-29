
---

### 📄 `steganography.py`

```python
from PIL import Image
import argparse

def encode_image(input_image_path, output_image_path, message):
    image = Image.open(input_image_path)
    encoded = image.copy()
    width, height = image.size
    index = 0
    binary_message = ''.join(format(ord(c), '08b') for c in message) + '1111111111111110'  # Delimiter

    for row in range(height):
        for col in range(width):
            if index < len(binary_message):
                pixel = list(image.getpixel((col, row)))
                for n in range(3):  # R, G, B
                    if index < len(binary_message):
                        pixel[n] = pixel[n] & ~1 | int(binary_message[index])
                        index += 1
                encoded.putpixel((col, row), tuple(pixel))
            else:
                encoded.save(output_image_path)
                return
    encoded.save(output_image_path)

def decode_image(image_path):
    image = Image.open(image_path)
    binary_data = ''
    for row in range(image.height):
        for col in range(image.width):
            pixel = image.getpixel((col, row))
            for n in range(3):  # R, G, B
                binary_data += str(pixel[n] & 1)
    chars = [chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)]
    message = ''
    for c in chars:
        if message[-2:] == '\xFF\xFE':  # delimiter
            break
        message += c
    return message[:-2]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Image Steganography using LSB method')
    parser.add_argument('--encode', action='store_true', help='Encode message into image')
    parser.add_argument('--decode', action='store_true', help='Decode message from image')
    parser.add_argument('-i', '--input', required=True, help='Input image path')
    parser.add_argument('-o', '--output', help='Output image path (for encoding)')
    parser.add_argument('-m', '--message', help='Message to hide (for encoding)')

    args = parser.parse_args()

    if args.encode:
        if not args.output or not args.message:
            print("Encoding requires --output and --message arguments.")
        else:
            encode_image(args.input, args.output, args.message)
            print("Message encoded successfully!")
    elif args.decode:
        message = decode_image(args.input)
        print("Decoded message:", message)
