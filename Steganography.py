#-------- steganography tool ---------
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

# ---------- Encoding Function ----------
def encode_image(input_path, message, output_path):
    image = Image.open(input_path).convert("RGB")
    encoded = image.copy()
    width, height = image.size
    index = 0
    binary_message = ''.join(format(ord(char), '08b') for char in message) + '1111111111111110'

    for y in range(height):
        for x in range(width):
            if index < len(binary_message):
                r, g, b = encoded.getpixel((x, y))
                r = (r & ~1) | int(binary_message[index])
                encoded.putpixel((x, y), (r, g, b))
                index += 1
            else:
                encoded.save(output_path)
                return True
    return False

# ---------- Decoding Function ----------
def decode_image(path):
    image = Image.open(path).convert("RGB")
    binary_data = ''
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            r, g, b = image.getpixel((x, y))
            binary_data += str(r & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ''
    for byte in all_bytes:
        if byte == '11111110':  # EOF marker
            break
        message += chr(int(byte, 2))
    return message

# ---------- GUI App ----------
def run_gui():
    def browse_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)

    def encode_action():
        image_path = entry_path.get()
        message = text_input.get("1.0", tk.END).strip()
        if not image_path or not message:
            messagebox.showwarning("Error", "Please select image and enter a message.")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".png")
        if output_path:
            success = encode_image(image_path, message, output_path)
            if success:
                messagebox.showinfo("Success", "Message encoded successfully.")
            else:
                messagebox.showerror("Failed", "Message too long or image too small.")

    def decode_action():
        image_path = entry_path.get()
        if not image_path:
            messagebox.showwarning("Error", "Please select image to decode.")
            return
        result = decode_image(image_path)
        text_input.delete("1.0", tk.END)
        text_input.insert(tk.END, result)

    # Tkinter window
    app = tk.Tk()
    app.title("Steganography Tool - Hide Message in Image")
    app.geometry("700x550")
    app.configure(bg="#2e003e")

    title_label = tk.Label(app, text="Image Steganography", fg="white", bg="#2e003e", font=("Helvetica", 18, "bold"))
    title_label.pack(pady=15)

    tk.Label(app, text="Image Path", fg="white", bg="#2e003e", font=("Arial", 12, "bold")).pack(pady=(10, 2))
    entry_path = tk.Entry(app, width=60, font=("Arial", 10), bg="#fef6ff", fg="#2e003e")
    entry_path.pack()
    tk.Button(app, text="Browse", command=browse_image, bg="#ff6f61", fg="white", font=("Arial", 10, "bold"), activebackground="#ff3b2e").pack(pady=5)

    tk.Label(app, text="Message", fg="white", bg="#2e003e", font=("Arial", 12, "bold")).pack(pady=(10, 2))
    text_input = tk.Text(app, height=12, width=70, font=("Consolas", 10), wrap=tk.WORD, bg="#fef6ff", fg="#2e003e")
    text_input.pack(pady=5)

    tk.Button(app, text="Encode Message", command=encode_action, bg="#6a1b9a", fg="white", font=("Arial", 11, "bold"), activebackground="#8e24aa").pack(pady=10)
    tk.Button(app, text="Decode Message", command=decode_action, bg="#283593", fg="white", font=("Arial", 11, "bold"), activebackground="#3949ab").pack(pady=5)

    tk.Label(app, text="\u00a9 Your Project | Designed by Vedant Verma", fg="lightgray", bg="#2e003e", font=("Arial", 9)).pack(side="bottom", pady=10)

    app.mainloop()

if __name__ == "__main__":
    run_gui()
