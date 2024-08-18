import numpy as np
from PIL import Image
from ppocronnx.predict_system import TextSystem

文本系统 = TextSystem()


def 识别单行文本(图片: Image) -> str:
    ndarray = np.asarray(图片)
    文本, 可信度 = 文本系统.ocr_single_line(ndarray)
    return 文本


if __name__ == "__main__":
    pass
