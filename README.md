# Steganography-project
A simple image steganography tool using LSB method in python
# 🕵️‍♂️ Image Steganography Project

This project demonstrates **image steganography** using the **Least Significant Bit (LSB)** method. It allows you to hide a secret message inside an image and extract it back later.

## 📌 Features

- Hide secret messages in PNG images.
- Extract hidden messages from stego-images.
- Simple command-line interface.
- Pure Python implementation.

## 🛠️ Requirements

Install dependencies with:

```bash
pip install -r requirements.txt

🚀 Usage
➕ Hide a Message
bash
python steganography.py --encode -i input.png -o output.png -m "This is a hidden message."
🔍 Reveal a Hidden Message
bash
python steganography.py --decode -i output.png
