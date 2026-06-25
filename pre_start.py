"""
Render启动前脚本 - 注册字体并验证
"""
import os
import matplotlib.font_manager as fm


def main():
    font_path = 'static/fonts/NotoSansCJKsc-Regular.otf'
    if os.path.exists(font_path):
        try:
            fm.fontManager.addfont(font_path)
            prop = fm.FontProperties(fname=font_path)
            print(f'字体验证成功: {prop.get_name()}')
        except Exception as e:
            print(f'字体注册失败: {e}')

    try:
        fm._load_fontmanager(try_read_cache=False)
    except Exception:
        pass

    cn_fonts = [f.name for f in fm.fontManager.ttflist if any(
        k in f.name.lower() for k in
        ['yahei', 'simhei', 'wqy', 'noto', 'cjk', 'hei', 'song', 'kai', 'ming']
    )]
    print(f'可用中文字体: {cn_fonts[:8]}')


if __name__ == '__main__':
    main()