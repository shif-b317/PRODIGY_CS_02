from tkinter import *
from tkinter import filedialog
from PIL import Image
import os

file_path = ""

def browse_file():
    global file_path

    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
    )

    if file_path:
        # Show ONLY file name in text box
        file_entry.config(state="normal")
        file_entry.delete(0, END)
        file_entry.insert(0, os.path.basename(file_path))
        file_entry.config(state="readonly")

        status_label.config(text=" Image loaded", fg="green")


def encrypt_image():
    if not file_path:
        status_label.config(text=" Please select an image first!", fg="red")
        return

    try:
        key = int(entry.get())
        if key < 0 or key > 255:
            raise ValueError
    except:
        status_label.config(text=" Enter valid key (0-255)", fg="red")
        return

    img = Image.open(file_path)
    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pixels[i, j]
            pixels[i, j] = (
                (r + key) % 256,
                (g + key) % 256,
                (b + key) % 256
            )

    folder = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    output_path = os.path.join(folder, f"encrypted_{filename}")
    img.save(output_path)

    img.save("encrypted_image.jpg")

    status_label.config(text=" Encrypted saved", fg="green")


def decrypt_image():
    if not file_path:
        status_label.config(text=" Please select an image first!", fg="red")
        return

    try:
        key = int(entry.get())
        if key < 0 or key > 255:
            raise ValueError
    except:
        status_label.config(text=" Enter valid key (0-255)", fg="red")
        return

    img = Image.open(file_path)
    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pixels[i, j]
            pixels[i, j] = (
                (r - key) % 256,
                (g - key) % 256,
                (b - key) % 256
            )

    img.save("decrypted_image.jpg")

    status_label.config(text=" Decrypted saved", fg="green")


# GUI
root = Tk()
root.title(" Image Encryption Tool")
root.geometry("420x320")

Button(root, text="Browse Image", command=browse_file).pack(pady=10)

file_entry = Entry(root, width=45)
file_entry.pack(pady=5)
file_entry.insert(0, "No file selected")
file_entry.config(state="readonly")

Label(root, text="Enter Key (0-255):").pack(pady=5)
entry = Entry(root)
entry.pack()

Button(root, text="Encrypt", command=encrypt_image).pack(pady=5)
Button(root, text="Decrypt", command=decrypt_image).pack(pady=5)

Button(root, text="Exit", command=root.destroy, bg="red", fg="white").pack(pady=10)

status_label = Label(root, text="")
status_label.pack(pady=5)

root.mainloop()