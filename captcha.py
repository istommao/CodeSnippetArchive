"""Python captcha."""
import random

from PIL import Image, ImageFont, ImageDraw, ImageFilter

FONT_TYPE = 'your font path'


def generate_captcha_image(size=(120, 32), bg_color=(255, 255, 255),
                           captcha_code='captcha'):
    img = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(img)
    width, height = size

    def create_lines():
        """绘制干扰线"""
        line_num = random.randint(2, 3)  # 干扰线条数
        for i in range(line_num):
            # 起始点a
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            # 结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points(point_chance=2):
        """绘制干扰点"""
        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs(text, fg_color=(0, 0, 255), font_size=20):
        """绘制验证码字符"""
        font = ImageFont.truetype(FONT_TYPE, font_size)
        font_width, font_height = font.getsize(text)
        draw.text(((width - font_width) / 3, (height - font_height) / 3),
                  text, font=font, fill=fg_color)

    create_lines()
    create_points()
    create_strs(captcha_code)

    params = [
        1 - float(random.randint(1, 2)) / 100,
        0,
        0,
        0,
        1 - float(random.randint(1, 10)) / 100,
        float(random.randint(1, 2)) / 500,
        0.001,
        float(random.randint(1, 2)) / 500
    ]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）
    return img
