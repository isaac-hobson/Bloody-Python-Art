import pygame
from PIL import Image, ImageDraw, ImageFont
import random, math

pygame.init()

width, height = 800, 600
font_size = 20
columns = width // font_size
rows = height // font_size
drip_chars = "⸸†☠☯𖤐"
sigils = ["Ϟ", "Ѫ", "₪", "ૐ", "卍", "⸸", "⌖"]
drip_heights = [random.randint(0, rows) for _ in range(columns)]

try:
    font_path = "/system/fonts/DroidSansMono.ttf"
    font = ImageFont.truetype(font_path, font_size)
    t_font = ImageFont.truetype(font_path, 38)
    sig_font = ImageFont.truetype(font_path, 16)
except:
    font = ImageFont.load_default()
    t_font = font
    sig_font = font

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Blood Abyss Live")

clock = pygame.time.Clock()
running = True
f = 0

# ASCII-style skull drawings
def draw_skull(draw, x, y, scale=1.0):
    skull = [
        "   _____   ",
        "  /     \\  ",
        " | () () | ",
        "  \\  ^  /  ",
        "   |||||   ",
        "   |||||   ",
    ]
    for i, line in enumerate(skull):
        draw.text((x, y + i * int(font_size * scale)), line, font=font, fill=(255, 0, 0))

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    base = Image.new("RGB", (width, height), (10, 0, 0))
    draw = ImageDraw.Draw(base)
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    effects = ImageDraw.Draw(overlay)

    sway_x = int(3 * math.sin(f * 0.3))
    sway_y = int(2 * math.cos(f * 0.25))
    cx = width // 2 + sway_x
    cy = height // 2 + sway_y

    # Draw matrix drip characters
    for col in range(columns):
        y = drip_heights[col] * font_size
        for i in range(8):
            char = random.choice(drip_chars)
            yy = y - i * font_size
            if 0 <= yy < height:
                r = min(255, 80 + i * 20 + random.randint(-10, 10))
                draw.text((col * font_size + sway_x, yy + sway_y), char, font=font, fill=(r, 0, 0))
        drip_heights[col] = (drip_heights[col] + 1) % rows if random.random() > 0.05 else 0

    # Draw floating sigils
    for i in range(12):
        angle = math.radians(f * 8 + i * 30)
        r = 140 + 20 * math.sin(f * 0.1 + i)
        x = int(cx + r * math.cos(angle))
        y = int(cy + r * math.sin(angle))
        c = (random.randint(150, 255), 0, 0, random.randint(100, 160))
        s = random.choice(sigils)
        effects.text((x, y), s, font=font, fill=c)

    # Draw pulsating central circle
    for r in range(60, 0, -2):
        alpha = int(255 * (r / 60))
        red = int(100 + 155 * math.sin(f * 0.2))
        effects.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(red, 0, 0, alpha))

    intense = int(255 * abs(math.sin(f * 0.3)))
    effects.ellipse((cx - 35, cy - 15, cx - 15, cy + 5), fill=(intense, 0, 0, 255))
    effects.ellipse((cx + 15, cy - 15, cx + 35, cy + 5), fill=(intense, 0, 0, 255))

    # Title text
    pulse = 1 + 0.1 * math.sin(f * 0.3)
    title = "BLOOD ABYSS"
    tf = ImageFont.truetype(font_path, int(38 * pulse))
    bbox = tf.getbbox(title)
    tw = bbox[2] - bbox[0]
    effects.text((cx - tw // 2, cy + 100), title, font=tf, fill=(255, 0, 0, 255))

    # Footer signature
    sig = "rendered in curses"
    sop = int(100 + 100 * math.sin(f * 0.2))
    sb = sig_font.getbbox(sig)
    sw = sb[2] - sb[0]
    sh = sb[3] - sb[1]
    effects.text((width - sw - 10, height - sh - 5), sig, font=sig_font, fill=(255, 50, 50, sop))

    # Draw left and right skulls
    draw_skull(draw, 30, height // 2 - 60)
    draw_skull(draw, width - 150, height // 2 - 60)

    # Compose and render
    frame = Image.alpha_composite(base.convert("RGBA"), overlay)
    mode = frame.mode
    size = frame.size
    data = frame.tobytes()
    py_img = pygame.image.fromstring(data, size, mode)
    screen.blit(py_img, (0, 0))
    pygame.display.flip()

    clock.tick(15)
    f += 1

pygame.quit()
