import logging

from PIL import Image


def compress_image(input_path=None, output_path=None, img_quality=30, img_format="WEBP"):
    """
    轉換圖片格式並壓縮。

    Args:
        input_path (str): 輸入圖片的完整路徑。
        output_path (str): 輸出圖片的完整路徑。
        img_quality (int): 壓縮品質，範圍從0（最低品質）到100（最高品質），預設為30。
        img_format (str): 輸出的圖片格式，預設為WEBP。
    Returns:
        bool: 如果壓縮成功返回True，否則返回False。
    """
    try:
        with Image.open(input_path) as img:
            # 檢查圖片格式，如果不是RGB，則轉換
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(output_path, format=img_format, quality=img_quality, optimize=True)
        return True
    except FileNotFoundError:
        logging.error(f"🔴 錯誤：找不到檔案 '{input_path}'")
        raise
    except Exception as e:
        logging.error(f"🔴 壓縮圖片時發生非預期錯誤：{e}")
        raise


if __name__ == "__main__":
    pass
