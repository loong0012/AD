"""
Render构建脚本 - 下载中文字体并清除matplotlib缓存
"""
import os
import urllib.request
import glob
import subprocess
import sys


def main():
    os.makedirs('static/fonts', exist_ok=True)
    font_path = 'static/fonts/NotoSansCJKsc-Regular.otf'

    if os.path.exists(font_path) and os.path.getsize(font_path) > 500000:
        print(f'[build_font] 字体已存在: {font_path} ({os.path.getsize(font_path)} bytes)')
        return

    if os.path.exists(font_path):
        os.remove(font_path)

    urls = [
        'https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf',
        'https://cdn.jsdelivr.net/gh/notofonts/noto-cjk@main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf',
        'https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf',
        'https://mirrors.aliyun.com/noto-cjk/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf',
    ]

    for url in urls:
        try:
            print(f'[build_font] 下载字体: {url[:80]}...')
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            if len(data) > 500000:
                with open(font_path, 'wb') as f:
                    f.write(data)
                print(f'[build_font] 字体下载成功: {len(data)} bytes')
                break
            print(f'[build_font] 文件太小: {len(data)} bytes')
        except Exception as e:
            print(f'[build_font] 下载失败: {str(e)[:120]}')

    if not os.path.exists(font_path):
        print('[build_font] 所有URL下载失败，尝试安装系统字体包...')
        subprocess.run(['apt-get', 'update', '-qq'], check=False, timeout=120)
        subprocess.run(['apt-get', 'install', '-y', '-qq', 'fonts-wqy-microhei'], check=False, timeout=120)
        # 安装后检查
        for test_path in [
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        ]:
            if os.path.exists(test_path):
                print(f'[build_font] 系统字体已安装: {test_path}')
                break

    # 清除matplotlib缓存
    try:
        import matplotlib
        cache_dir = matplotlib.get_cachedir()
        for f in glob.glob(os.path.join(cache_dir, 'fontlist*.json')):
            try:
                os.remove(f)
                print(f'[build_font] 已清除缓存: {os.path.basename(f)}')
            except Exception:
                pass
    except Exception as e:
        print(f'[build_font] 清除缓存失败: {e}')

    print('[build_font] 构建完成')


if __name__ == '__main__':
    main()