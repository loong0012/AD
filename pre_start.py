"""
Render启动前脚本 - 注册字体并验证
v3.4.0 - 适配统一字体名ChineseFont
"""
import os
import sys
import matplotlib.font_manager as fm

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)


def main():
    print("=" * 60)
    print("Pre-start: 字体验证")
    print("=" * 60)

    font_path = 'static/fonts/NotoSansCJKsc-Regular.otf'

    if os.path.exists(font_path):
        try:
            fm.fontManager.addfont(font_path)
            prop = fm.FontProperties(fname=font_path)
            print(f'[OK] matplotlib 字体验证: {prop.get_name()}')
        except Exception as e:
            print(f'[WARN] matplotlib 字体注册失败: {e}')

    try:
        fm._load_fontmanager(try_read_cache=False)
    except Exception:
        pass

    cn_fonts = [f.name for f in fm.fontManager.ttflist if any(
        k in f.name.lower() for k in
        ['yahei', 'simhei', 'wqy', 'noto', 'cjk', 'hei', 'song', 'kai', 'ming']
    )]
    if cn_fonts:
        print(f'[OK] 可用中文字体: {cn_fonts[:8]}')
    else:
        print('[WARN] 未找到中文字体，matplotlib图表中文可能显示为方框')

    print()
    print("=" * 60)
    print("Pre-start: ReportLab PDF字体验证")
    print("=" * 60)
    try:
        from src.utils.font_manager import font_manager
        font_name, font_path_out = font_manager.setup_reportlab()
        if font_name and font_name != 'Helvetica':
            print(f'[OK] ReportLab字体: {font_name} ({font_path_out})')
        else:
            print('[WARN] ReportLab字体注册失败，PDF中文将显示为乱码')
    except Exception as e:
        print(f'[ERROR] ReportLab字体注册异常: {e}')

    print()
    print("=" * 60)
    print("Pre-start: 目录结构验证")
    print("=" * 60)
    required_dirs = [
        'data', 'results', 'reports', 'uploaded_img',
        'demodata', 'logs', 'static/fonts'
    ]
    for d in required_dirs:
        if os.path.isdir(d):
            print(f'[OK] {d}/')
        else:
            print(f'[WARN] {d}/ 不存在')

    print()
    print("=" * 60)
    print("Pre-start: 完成")
    print("=" * 60)


if __name__ == '__main__':
    main()