
---

## 📁 Project Structure
```
image-processor/
│
├── image_processor.py
├── requirements.txt
├── README.md
├── input/          (put your images here)
├── output/         (processed images go here)
└── watermark.png   (your watermark image)
```

---

## 📄 requirements.txt

```
Pillow
rembg
onnxruntime
```

---

## 📖 README.md

```markdown
# 🖼 Image Processor Bot

A powerful Python automation tool for bulk image processing.
Built with **Pillow** and **rembg**.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)
![Pillow](https://img.shields.io/badge/Pillow-latest-green?style=flat)
![rembg](https://img.shields.io/badge/rembg-latest-orange?style=flat)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔄 **Bulk Resize** | Resize hundreds of images at once |
| 💧 **Add Watermark** | Text or image watermarks with opacity control |
| 🔁 **Convert Format** | PNG → JPG → WEBP → BMP and more |
| ✂️ **Remove Background** | AI-powered background removal |
| 🚀 **All-in-One** | Run all steps with one command |

---

## 📁 Project Structure

```
image-processor/
│
├── image_processor.py   # Main script
├── requirements.txt     # Dependencies
├── README.md            # Documentation
├── input/               # 📥 Put your images here
├── output/              # 📤 Processed images saved here
│   ├── resized/
│   ├── watermarked/
│   ├── converted_jpg/
│   └── no_background/
└── watermark.png        # (Optional) Your watermark image
```

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/image-processor.git
cd image-processor
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Run the program
```bash
python image_processor.py
```

### You will see this menu
```
╔══════════════════════════════════════╗
║       🖼  IMAGE PROCESSOR BOT        ║
╠══════════════════════════════════════╣
║  1. Resize Images                    ║
║  2. Add Watermark (Text)             ║
║  3. Add Watermark (Image)            ║
║  4. Convert Format                   ║
║  5. Remove Background                ║
║  6. Run ALL Steps                    ║
║  7. Exit                             ║
╚══════════════════════════════════════╝
```

---

## 📖 Feature Guide

### 🔄 1. Resize Images
- Place images in the `input/` folder
- Choose option **1**
- Enter your desired **width** and **height** in pixels
- Resized images saved to `output/resized/`

```
Example:
Width  → 1920
Height → 1080
```

---

### 💧 2 & 3. Add Watermark
- Supports **text** or **image** watermarks
- Control **opacity** (0 = invisible, 255 = solid)
- Choose **position**:
  - `top-left`
  - `top-right`
  - `bottom-left`
  - `bottom-right`
  - `center`
- Watermarked images saved to `output/watermarked/`

---

### 🔁 4. Convert Format
Supported formats:

| Format | Extension |
|--------|-----------|
| JPEG   | `.jpg`    |
| PNG    | `.png`    |
| WebP   | `.webp`   |
| BMP    | `.bmp`    |
| GIF    | `.gif`    |

Converted images saved to `output/converted_[format]/`

---

### ✂️ 5. Remove Background
- Uses **AI** (rembg + onnxruntime) to remove backgrounds
- Works best with **people, products, animals**
- Output saved as **PNG** (to preserve transparency)
- Saved to `output/no_background/`

> ⚠️ First run will download the AI model (~170MB)

---

### 🚀 6. Run ALL Steps
Runs everything in sequence:
1. Resize
2. Add watermark
3. Convert format
4. Remove background

---

## 💡 Tips

- ✅ Works with: `.png` `.jpg` `.jpeg` `.bmp` `.gif` `.webp`
- ✅ For best background removal use clear product/portrait photos
- ✅ Use a virtual environment to avoid conflicts
- ✅ Watermark images should have a **transparent background** (PNG)

---

## 🛠 Requirements

- Python **3.8+**
- Pillow
- rembg
- onnxruntime

---

## 📦 Dependencies

```bash
pip install Pillow rembg onnxruntime
```

---

## 🐛 Common Issues

### ❌ `No images found in input folder`
→ Make sure you placed images inside the `input/` folder

### ❌ `Error removing background`
→ Make sure `onnxruntime` is installed:
```bash
pip install onnxruntime
```

### ❌ Font not found (watermark)
→ The script uses `arial.ttf` — falls back to default font automatically

### ❌ `rembg` slow on first run
→ It downloads the AI model (~170MB) on first use — this is normal!

---

## 🗺 Roadmap

- [ ] GUI with Tkinter
- [ ] Drag and drop support
- [ ] Progress bar for bulk processing
- [ ] Compress images
- [ ] Add filters (grayscale, blur, sharpen)
- [ ] Command line arguments support

---

## 📄 License

This project is licensed under the **MIT License**
Feel free to use, modify, and share!

---

## 🙋 Author

Made with ❤️ and Python

⭐ **Star this repo if you found it useful!**
```

---

## ▶️ Quick Start

```bash
# 1. Clone
git clone https://github.com/yourusername/image-processor.git

# 2. Install
pip install -r requirements.txt

# 3. Add images to input/ folder

# 4. Run
python image_processor.py
```

---

## 🗺 What Each Output Folder Contains

| Folder | Contents |
|---|---|
| `output/resized/` | Resized images |
| `output/watermarked/` | Watermarked images |
| `output/converted_jpg/` | Converted images |
| `output/no_background/` | Background removed |

---

Just ask! 👇
