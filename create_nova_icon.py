from PIL import Image, ImageDraw, ImageFont

SIZE = 1024

img = Image.new("RGBA", (SIZE, SIZE), (10, 15, 30, 255))
draw = ImageDraw.Draw(img)

# Outer circular background
draw.ellipse(
    (60, 60, SIZE - 60, SIZE - 60),
    fill=(20, 30, 55, 255),
    outline=(80, 180, 255, 255),
    width=18
)

# NOVA "N" symbol
points = [
    (300, 700),
    (300, 320),
    (390, 320),
    (650, 610),
    (650, 320),
    (740, 320),
    (740, 700),
    (650, 700),
    (390, 410),
    (390, 700),
]

draw.polygon(
    points,
    fill=(90, 200, 255, 255)
)

# Inner glow-style circle
draw.ellipse(
    (180, 180, 844, 844),
    outline=(40, 120, 200, 100),
    width=5
)

# Save PNG
img.save(
    r"C:\Users\sc\Desktop\NOVA\nova_icon.png"
)

# Save ICO with multiple resolutions
img.save(
    r"C:\Users\sc\Desktop\NOVA\nova_icon.ico",
    format="ICO",
    sizes=[
        (256, 256),
        (128, 128),
        (64, 64),
        (48, 48),
        (32, 32),
        (16, 16)
    ]
)

print("NOVA icon created successfully.")