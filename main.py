import os
import time
from pathlib import Path

from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

star = (
    Image.open(Path(__file__).parent.joinpath("star.png"))
    .convert("RGBA")
    .resize((80, 80))
)
garin = (
    Image.open(Path(__file__).parent.joinpath("grain.png"))
    .convert("RGBA")
    .resize((128, 96))
)
base_offset = 110
draw_text = ImageDraw.Draw(garin)

font_path = f"{os.path.dirname(__file__)}\\HYWenHei 85W.ttf"
content_size = (730, 96)
content = Image.new("RGB", content_size, "rgb(235, 226, 215)")  # 中间部分
frame_size = (734, 100)
frame = Image.new("RGB", frame_size, "rgb(224, 214, 203)")  # 边框


class Achievement(BaseModel):
    achieve_time: str
    name: str
    description: str
    keep_time: str


def get_time() -> str:
    """获取格式化后的当前时间"""
    return time.strftime("%Y/%m/%d/ %p%I:%M:%S", time.localtime())


def cut_text(
    font: FreeTypeFont,
    origin: str,
    chars_per_line: int,
):
    """将单行超过指定长度的文本切割成多行
    https://github.com/Redlnn/signin-image-generator/blob/master/util.py
    Args:
        font (FreeTypeFont): 字体
        origin (str): 原始文本
        chars_per_line (int): 每行字符数（按全角字符算）
    """
    target = ""
    start_symbol = "[{<(【《（〈〖［〔“‘『「〝"
    end_symbol = ",.!?;:]}>)%~…，。！？；：】》）〉〗］〕”’～』」〞"
    line_width = chars_per_line * font.getlength("一")
    for i in origin.splitlines(False):
        if i == "":
            target += "\n"
            continue
        j = 0
        for ind, elem in enumerate(i):
            if i[j : ind + 1] == i[j:]:
                target += i[j : ind + 1] + "\n"
                continue
            elif font.getlength(i[j : ind + 1]) <= line_width:
                continue
            elif ind - j > 3:
                if i[ind] in end_symbol and i[ind - 1] != i[ind]:
                    target += i[j : ind + 1] + "\n"
                    j = ind + 1
                    continue
                elif i[ind] in start_symbol and i[ind - 1] != i[ind]:
                    target += i[j:ind] + "\n"
                    continue
            target += i[j:ind] + "\n"
            j = ind
    return target.rstrip()


def font(size: int):
    return ImageFont.truetype(font_path, size)


def generate_img(achievement_list: list[Achievement]):
    total_size = (750, len(achievement_list) * 110 + 5)
    canvas = Image.new("RGB", total_size, "rgb(240, 234, 226)")
    i = 0
    for achievement in achievement_list:
        text_format = cut_text(font(16), achievement.description, 28)
        off = 1 if len(text_format.splitlines()) > 1 else 0
        content_size = (730, 96)
        content = Image.new("RGB", content_size, "rgb(235, 226, 215)")  # 中间部分
        draw = ImageDraw.Draw(content)
        draw.text(
            (120, 22 - off * 10),
            achievement.name,
            font=font(24),
            fill="rgb(88, 87, 87)",
        )

        draw.text(
            (120, 61 - off * 15),
            text_format,
            font=ImageFont.truetype(font_path, 16),
            fill="rgb(152, 139, 129)",
            spacing=7,
        )

        garin_get = garin.copy()  # 右边花纹
        draw_text = ImageDraw.Draw(garin_get)
        w, h = draw_text.textsize(
            achievement.keep_time, font=ImageFont.truetype(font_path, 20)
        )
        draw_text.text(
            ((128 - w) / 2, (96 - h) / 2),
            achievement.keep_time,
            font=ImageFont.truetype(font_path, 20),
            fill="rgb(152, 139, 129)",
            align="center",
        )
        w, h = draw.textsize(
            achievement.achieve_time, font=ImageFont.truetype(font_path, 15)
        )
        draw_text.text(
            ((128 - w) / 2, 81 - h / 2),
            achievement.achieve_time,
            font=ImageFont.truetype(font_path, 15),
            fill="rgb(152, 139, 129)",
            align="right",
        )
        offset = base_offset * i
        canvas.paste(frame, (8, 6 + offset))
        canvas.paste(content, (10, 8 + offset))
        canvas.paste(star, (24, 16 + offset))
        canvas.paste(garin_get, (600, 8 + offset))
        i = i + 1
    return canvas


if __name__ == "__main__":
    achieve1 = Achievement(
        achieve_time="2021/05/18",
        keep_time="42 天5 时",
        name="「专家仓鼠」",
        description="从2021/09/21到2021/11/02没有使用「纠缠之缘」进行抽卡。作为仓鼠，你就是专家!",
    )

    achieve2 = Achievement(
        achieve_time="2021/05/18",
        keep_time="83",
        name="「原来非酋竟是我自己」",
        description="抽了 83 次才最终抽到了「宵宫」",
    )
    achieve3 = Achievement(
        achieve_time="2022/11/18",
        keep_time="6",
        name="「单抽出奇迹？」",
        description="在 40 抽内获取 5 星共计 6 次，其中通过单抽获取的数目为 4，通过十连获取的数目为 2",
    )
    # achieve4 = Achievement(
    #     achieve_time="小保底歪的概率",
    #     keep_time="1/8",
    #     name="「晴时总比雨时多」",
    #     description="在「角色活动祈愿」中，小保底偏向于抽中当期Up角色",
    # )
    img = generate_img([achieve1, achieve2, achieve3])
    img.save("test2.png")
    img.show()
