"""
class 识别区域类

def 切换到mumu()

def 点击(
    坐标: pag.Point,
    点击前延时: float = 0,
    点击后延时: float = 0,
    点击次数: int = 1,
    移动时间: float = 0.8,
)

def 获取图片坐标(
    图片路径: str, 识别区域: 识别区域类 = None, 图片相似度: float = 0.85
) -> pag.Point | None

def 等待图片出现(
    图片路径: str,
    识别区域: 识别区域类 = None,
    图片相似度: float = 0.85,
    超时时间: float = 5,
) -> tuple[bool, pag.Point]

def 点击图片(
    图片路径: str,
    点击前延时: float = 0,
    点击后延时: float = 0,
    识别区域: 识别区域类 = None,
    移动时间: float = 0.8,
    图片相似度: float = 0.85,
    超时时间: float = 5,
) -> pag.Point | None
"""

import random
from dataclasses import astuple, dataclass
from pathlib import Path

import pyautogui as pag
import win32con
import win32gui
from PIL import Image

from qfpy.log import logger


@dataclass
class 识别区域类:
    左: int
    上: int
    宽: int
    高: int


def 切换到mumu():
    hwnd = win32gui.FindWindow(None, "MuMu模拟器12")

    win32gui.SetForegroundWindow(hwnd)
    # 缩小：SW_RESTORE
    # 放大：SW_MAXIMIZE
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    pag.sleep(0.5)


def 点击(
    坐标: pag.Point,
    点击前延时: float = 0,
    点击后延时: float = 0,
    点击次数: int = 1,
    移动时间: float = 0.8,
):
    x, y = 坐标

    pag.moveTo(x, y, 移动时间)

    if 点击前延时 == 0:
        点击前延时 = random.uniform(0.3, 0.6)
    pag.sleep(点击前延时)

    多次点击间隔 = random.uniform(0.1, 0.2)
    pag.click(x, y, 点击次数, 多次点击间隔)

    pag.sleep(点击后延时)


def 获取图片坐标(
    图片路径: str, 识别区域: 识别区域类 = None, 图片相似度: float = 0.85
) -> pag.Point | None:
    """获取图片坐标"""
    try:
        图片 = Image.open(图片路径)

        识别区域 = astuple(识别区域) if 识别区域 else None

        坐标 = pag.locateCenterOnScreen(图片, confidence=图片相似度, region=识别区域)
        图片.close()
        return 坐标
    except pag.ImageNotFoundException:
        return None


def 等待图片出现(
    图片路径: str,
    识别区域: 识别区域类 = None,
    图片相似度: float = 0.85,
    超时时间: float = 5,
) -> tuple[bool, pag.Point]:
    """
    图片出现后返回 (True, 坐标)；否则返回 (False, None)
    """
    while True:
        if 超时时间 <= 0:
            logger.error("等待图片超时：" + Path(图片路径).stem)
            return (False, None)

        xy = 获取图片坐标(图片路径, 识别区域, 图片相似度)
        if xy:
            return (True, pag.Point(*xy))

        pag.sleep(0.3)
        超时时间 -= 0.3


def 点击图片(
    图片路径: str,
    点击前延时: float = 0,
    点击后延时: float = 0,
    识别区域: 识别区域类 = None,
    移动时间: float = 0.8,
    图片相似度: float = 0.85,
    超时时间: float = 5,
) -> pag.Point | None:
    """点击图片

    默认一直等待图片出现，5 秒超时

    成功点击图片，返回坐标；失败返回 None
    """
    flag, xy = 等待图片出现(图片路径, 识别区域, 图片相似度, 超时时间)
    if not flag:
        return None

    # 随机偏移坐标
    xy = (
        xy[0] + random.randint(-5, 5),
        xy[1] + random.randint(-5, 5),
    )

    点击(
        xy,
        点击前延时=点击前延时,
        点击后延时=点击后延时,
        移动时间=移动时间,
    )
    logger.info(f"点击图片：{Path(图片路径).stem} {xy}")
    return xy


if __name__ == "__main__":
    pass
