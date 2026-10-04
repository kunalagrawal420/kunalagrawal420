import sys
import numpy as np
import cv2
from PIL import Image
from rembg import remove

src = sys.argv[1]
img = Image.open(src).convert("RGB")

# 1) Remove the background so only you gets converted (busy backgrounds become noise).
cut = remove(img)                      # RGBA: alpha channel = "is this you?"
alpha = np.array(cut)[:, :, 3]

# 2) Composite onto pure black: black maps to the blank end of the ASCII ramp.
bg = Image.new("RGBA", cut.size, (0, 0, 0, 255))
bg.alpha_composite(cut)
gray = np.array(bg.convert("L"))

# 3) CLAHE = local contrast boost. Flat lighting turns into a dark blob without it.
gray = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)
gray[alpha < 10] = 0                   # CLAHE can lift the background slightly: re-blank it

# 4) Crop tightly to the subject so the portrait fills the frame.
ys, xs = np.where(alpha > 10)
m = int(0.04 * max(gray.shape))
y0, y1 = max(ys.min() - m, 0), min(ys.max() + m, gray.shape[0])
x0, x1 = max(xs.min() - m, 0), min(xs.max() + m, gray.shape[1])
Image.fromarray(gray[y0:y1, x0:x1]).save("source-prepped.png")
print("wrote source-prepped.png")
