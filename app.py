import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import datetime
import math
import io
import os


def create_certificate(image_file, name):
    # --- 字体设置 (最关键的一步) ---
    # 必须确保文件夹里有 simhei.ttf，否则云端会显示方框乱码
    font_path = "simhei.ttf"

    if not os.path.exists(font_path):
        st.error("❌ 错误：未找到字体文件 simhei.ttf，请确保该文件已上传！")
        return None

    # 如果找不到字体会报错，这里尝试加载
    try:
        title_font = ImageFont.truetype(font_path, 65)
        subtitle_font = ImageFont.truetype(font_path, 32)
        body_font = ImageFont.truetype(font_path, 28)
        slogan_font = ImageFont.truetype(font_path, 45)
        sign_font = ImageFont.truetype(font_path, 26)
        stamp_font = ImageFont.truetype(font_path, 20)
    except Exception as e:
        st.error(f"字体加载失败: {e}")
        return None

    # --- 以下是绘图逻辑 (和之前一样) ---
    WIDTH, HEIGHT = 800, 1130
    img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    RED, BLACK = (200, 20, 20), (0, 0, 0)

    # 绘制线条
    draw.line([(50, 110), (WIDTH - 50, 110)], fill=RED, width=5)
    draw.line([(50, 120), (WIDTH - 50, 120)], fill=RED, width=2)
    draw.line([(50, HEIGHT - 50), (WIDTH - 50, HEIGHT - 50)], fill=RED, width=3)

    # 标题
    title_text = "戒 色 公 证 办 事 处"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    draw.text(((WIDTH - (title_bbox[2] - title_bbox[0])) / 2, 30), title_text, font=title_font, fill=RED)

    # 副标题
    sub_text = "关于本人“戒导”的重要通知"
    sub_bbox = draw.textbbox((0, 0), sub_text, font=subtitle_font)
    draw.text(((WIDTH - (sub_bbox[2] - sub_bbox[0])) / 2, 160), sub_text, font=subtitle_font, fill=BLACK)

    # 正文
    margin, y_cursor = 80, 230
    draw.text((margin, y_cursor), "各位亲朋好友：", font=body_font, fill=BLACK)
    y_cursor += 50
    body_text = "        我承认我有色情成瘾的问题，自奖励以来，严重损害了我的身心健康，浪费了我的时间和精力，影响了我的学习和工作，今后，我将以此为戒，洗心革面，痛改前非，做到："

    line = ""
    for char in body_text:
        if draw.textlength(line + char, font=body_font) < (WIDTH - 2 * margin):
            line += char
        else:
            draw.text((margin, y_cursor), line, font=body_font, fill=BLACK)
            y_cursor += 45
            line = char
    draw.text((margin, y_cursor), line, font=body_font, fill=BLACK)

    # 照片处理
    try:
        photo = Image.open(image_file)
        target_w, target_h = 350, 450
        img_ratio = photo.width / photo.height
        target_ratio = target_w / target_h
        if img_ratio > target_ratio:
            scale_height = target_h
            scale_width = int(scale_height * img_ratio)
        else:
            scale_width = target_w
            scale_height = int(scale_width / img_ratio)
        photo = photo.resize((scale_width, scale_height), Image.Resampling.LANCZOS)
        left, top = (scale_width - target_w) / 2, (scale_height - target_h) / 2
        photo = photo.crop((left, top, left + target_w, top + target_h))
        img.paste(photo, (100, 480))
    except:
        draw.rectangle([100, 480, 450, 930], outline=BLACK, width=2)
        draw.text((150, 600), "图片加载失败", font=body_font, fill=BLACK)

    # 口号
    for i, t in enumerate(["严 于 律 己", "提 升 自 我", "奉 献 社 会"]):
        draw.text((480, 550 + i * 100), t, font=slogan_font, fill=BLACK)

    # 印章
    cx, cy = 630, 920
    draw.ellipse([cx - 90, cy - 90, cx + 90, cy + 90], outline=RED, width=4)
    points = []
    for i in range(5):
        angle = -90 + i * 72
        rad = math.radians(angle)
        points.append((cx + 25 * math.cos(rad), cy + 25 * math.sin(rad)))
        rad_in = math.radians(-90 + i * 72 + 36)
        points.append((cx + 10 * math.cos(rad_in), cy + 10 * math.sin(rad_in)))
    draw.polygon(points, fill=RED)
    draw.text((cx - 40, cy - 70), "公 证 办", font=stamp_font, fill=RED)
    draw.text((cx - 40, cy + 50), "业务专用章", font=stamp_font, fill=RED)

    # 签名日期
    draw.text((520, 880), f"戒导人：{name}", font=sign_font, fill=BLACK)
    dt = datetime.datetime.now()
    draw.text((520, 930), f"{dt.year} 年 {dt.month} 月 {dt.day} 日", font=sign_font, fill=BLACK)

    return img


def main():
    st.set_page_config(page_title="戒色通知书生成", page_icon="🈲")
    st.title("🈲 戒色公证生成器")
    st.write("上传照片，即刻生成")

    name = st.text_input("输入姓名", "高风亮节")
    uploaded_file = st.file_uploader("上传照片", type=['jpg', 'png', 'jpeg'])

    if uploaded_file and name:
        if st.button("生成图片", type="primary"):
            res = create_certificate(uploaded_file, name)
            if res:
                st.image(res, caption="长按保存图片", use_container_width=True)
                # 提供下载
                buf = io.BytesIO()
                res.save(buf, format="JPEG")
                st.download_button("下载图片", buf.getvalue(), "jiese.jpg", "image/jpeg")


if __name__ == "__main__":

    main()

