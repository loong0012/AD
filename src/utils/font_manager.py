"""
统一字体管理器 - 跨平台中文字体解决方案
所有模块通过此模块获取中文字体，避免重复的字体检测逻辑
"""

import os
import sys
import glob
import logging

logger = logging.getLogger('alzheimer-diagnostic')


class FontManager:
    """统一字体管理器，单例模式"""

    _instance = None
    _initialized = False

    # 中文字体关键词
    _CN_KEYWORDS = [
        'yahei', 'simhei', 'simsun', 'simkai', 'simfang',
        'noto', 'cjk', 'chinese', 'han', 'ming', 'hei', 'kai', 'song', 'fang',
        'wqy', 'wenquan', 'droid', 'pingfang', 'heiti', 'stheit',
        'msmincho', 'yugoth', 'malgun', 'gulim',
    ]

    # 字体搜索路径（按优先级）
    _FONT_SEARCH_PATHS = [
        # 项目内置字体
        'static/fonts/NotoSansCJKsc-Regular.otf',
        'static/fonts/NotoSansCJKsc-Regular.ttf',
        'static/fonts/NotoSansSC-Regular.otf',
        'static/fonts/wqy-microhei.ttc',
        # Linux 系统字体
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttf',
        '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
        '/usr/share/fonts/truetype/arphic/uming.ttc',
        '/usr/share/fonts/truetype/arphic/ukai.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf',
        # Windows 系统字体
        'C:\\Windows\\Fonts\\msyh.ttc',
        'C:\\Windows\\Fonts\\msyh.ttf',
        'C:\\Windows\\Fonts\\simhei.ttf',
        'C:\\Windows\\Fonts\\simsun.ttc',
        'C:\\Windows\\Fonts\\simkai.ttf',
        'C:\\Windows\\Fonts\\simfang.ttf',
        # macOS 系统字体
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/Library/Fonts/Arial Unicode.ttf',
    ]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if FontManager._initialized:
            return
        FontManager._initialized = True
        self._mpl_font_name = None
        self._mpl_font_path = None
        self._pdf_font_path = None
        self._pdf_font_name = None
        self._init_fonts()

    def _init_fonts(self):
        """初始化字体配置"""
        self._find_and_register_fonts()

    def _find_and_register_fonts(self):
        """查找并注册中文字体"""
        # 1. 先尝试已知路径
        project_root = self._get_project_root()
        for path in self._FONT_SEARCH_PATHS:
            abs_path = os.path.join(project_root, path) if not os.path.isabs(path) else path
            abs_path = os.path.abspath(abs_path)
            if os.path.exists(abs_path) and os.path.getsize(abs_path) > 1000:
                if self._register_font(abs_path):
                    return

        # 2. 扫描项目 fonts 目录
        fonts_dir = os.path.join(project_root, 'static', 'fonts')
        if os.path.isdir(fonts_dir):
            for f in os.listdir(fonts_dir):
                fpath = os.path.join(fonts_dir, f)
                if os.path.isfile(fpath) and f.lower().endswith(('.ttf', '.ttc', '.otf')):
                    if self._register_font(fpath):
                        return

        # 3. 扫描系统字体目录
        if os.name == 'nt':
            self._scan_windows_fonts()
        else:
            self._scan_linux_fonts()

        if self._mpl_font_path:
            return

        # 4. 使用 matplotlib 的 findSystemFonts
        try:
            import matplotlib.font_manager as fm
            for fpath in fm.findSystemFonts():
                fname = os.path.basename(fpath).lower()
                if any(kw in fname for kw in self._CN_KEYWORDS):
                    if self._register_font(fpath):
                        return
        except Exception:
            pass

        # 5. 按名称查找已注册的字体
        try:
            import matplotlib.font_manager as fm
            for font in fm.fontManager.ttflist:
                if any(k in font.name for k in ['SimHei', 'YaHei', 'SimSun', 'KaiTi', 'FangSong',
                                                  'Noto', 'CJK', 'WenQuanYi', 'PingFang',
                                                  'Heiti', 'AR PL', 'STSong', 'Droid']):
                    self._mpl_font_path = font.fname
                    self._mpl_font_name = font.name
                    self._pdf_font_path = font.fname
                    self._pdf_font_name = font.name
                    logger.info(f"FontManager: 使用已注册字体 {font.name}")
                    return
        except Exception:
            pass

        # 6. 运行时下载字体（兜底方案）
        if self._runtime_download_font():
            return

        logger.warning("FontManager: 未找到任何中文字体，中文可能显示为乱码")

    def _register_font(self, font_path):
        """注册一个字体文件"""
        try:
            import matplotlib.font_manager as fm
            import matplotlib.pyplot as plt

            fm.fontManager.addfont(font_path)
            font_prop = fm.FontProperties(fname=font_path)
            font_name = font_prop.get_name()

            self._mpl_font_path = font_path
            self._mpl_font_name = font_name
            self._pdf_font_path = font_path
            self._pdf_font_name = os.path.splitext(os.path.basename(font_path))[0]

            plt.rcParams['font.sans-serif'] = [font_name, 'SimHei', 'Microsoft YaHei', 'sans-serif']
            plt.rcParams['axes.unicode_minus'] = False

            logger.info(f"FontManager: 注册字体 {font_name} ({font_path})")
            return True
        except Exception as e:
            logger.debug(f"FontManager: 注册字体失败 {font_path}: {e}")
            return False

    def _scan_windows_fonts(self):
        """扫描 Windows 字体目录"""
        fonts_dir = 'C:\\Windows\\Fonts'
        if not os.path.exists(fonts_dir):
            return
        try:
            for entry in os.scandir(fonts_dir):
                if entry.is_file() and entry.name.lower().endswith(('.ttf', '.ttc', '.otf')):
                    if any(kw in entry.name.lower() for kw in self._CN_KEYWORDS):
                        if self._register_font(entry.path):
                            return
        except Exception:
            pass

    def _scan_linux_fonts(self):
        """扫描 Linux 字体目录"""
        linux_font_dirs = [
            '/usr/share/fonts',
            '/usr/local/share/fonts',
            '/home/*/.fonts',
        ]
        for base_dir in linux_font_dirs:
            for root, _, files in os.walk(base_dir):
                for f in files:
                    if f.lower().endswith(('.ttf', '.ttc', '.otf')):
                        if any(kw in f.lower() for kw in self._CN_KEYWORDS):
                            fpath = os.path.join(root, f)
                            if self._register_font(fpath):
                                return

    def _get_project_root(self):
        """获取项目根目录"""
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def _runtime_download_font(self):
        """运行时下载字体兜底方案"""
        project_root = self._get_project_root()
        fonts_dir = os.path.join(project_root, 'static', 'fonts')
        os.makedirs(fonts_dir, exist_ok=True)
        font_path = os.path.join(fonts_dir, 'NotoSansCJKsc-Regular.otf')

        if os.path.exists(font_path) and os.path.getsize(font_path) > 500000:
            return self._register_font(font_path)

        urls = [
            'https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf',
            'https://cdn.jsdelivr.net/gh/notofonts/noto-cjk@main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf',
            'https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf',
            'https://mirrors.aliyun.com/noto-cjk/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf',
        ]

        for url in urls:
            try:
                logger.info(f"FontManager: 运行时下载字体 {url[:80]}...")
                import urllib.request
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = resp.read()
                if len(data) > 500000:
                    with open(font_path, 'wb') as f:
                        f.write(data)
                    logger.info(f"FontManager: 运行时字体下载成功 ({len(data)} bytes)")
                    return self._register_font(font_path)
                logger.warning(f"FontManager: 下载文件太小 ({len(data)} bytes)")
            except Exception as e:
                logger.warning(f"FontManager: 运行时下载失败 ({url[:60]}): {str(e)[:80]}")

        logger.warning("FontManager: 所有运行时下载源均失败")
        return False

    @property
    def mpl_font_name(self):
        """获取 matplotlib 字体名称"""
        if not self._mpl_font_name:
            self._find_and_register_fonts()
        return self._mpl_font_name or 'sans-serif'

    @property
    def mpl_font_path(self):
        """获取 matplotlib 字体文件路径"""
        if not self._mpl_font_path:
            self._find_and_register_fonts()
        return self._mpl_font_path

    @property
    def pdf_font_path(self):
        """获取 PDF 字体文件路径"""
        if not self._pdf_font_path:
            self._find_and_register_fonts()
        return self._pdf_font_path

    @property
    def pdf_font_name(self):
        """获取 PDF 字体名称"""
        if not self._pdf_font_name:
            self._find_and_register_fonts()
        return self._pdf_font_name or 'Helvetica'

    def setup_matplotlib(self):
        """配置 matplotlib 使用中文字体"""
        try:
            import matplotlib.pyplot as plt
            name = self.mpl_font_name
            if name and name != 'sans-serif':
                plt.rcParams['font.sans-serif'] = [name, 'SimHei', 'Microsoft YaHei', 'DejaVu Sans', 'sans-serif']
                plt.rcParams['axes.unicode_minus'] = False
                return True
        except Exception:
            pass
        return False

    def setup_reportlab(self):
        """注册 reportlab 中文字体，返回 (font_name, font_path)"""
        try:
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            from reportlab.lib.fonts import addMapping

            CHINESE_FONT_REGISTERED_NAME = 'ChineseFont'

            path = self.pdf_font_path
            if not path or not os.path.exists(path):
                for test_path in [
                    'C:/Windows/Fonts/msyh.ttc',
                    'C:/Windows/Fonts/msyh.ttf',
                    'C:/Windows/Fonts/simhei.ttf',
                    'C:/Windows/Fonts/simsun.ttc',
                    'C:/Windows/Fonts/simkai.ttf',
                    'C:/Windows/Fonts/simfang.ttf',
                ]:
                    if os.path.exists(test_path) and os.path.getsize(test_path) > 1000:
                        path = test_path
                        break

            if not path or not os.path.exists(path):
                project_root = self._get_project_root()
                fonts_dir = os.path.join(project_root, 'static', 'fonts')
                for fname in os.listdir(fonts_dir) if os.path.isdir(fonts_dir) else []:
                    if fname.lower().endswith(('.ttf', '.ttc', '.otf')):
                        fpath = os.path.join(fonts_dir, fname)
                        if os.path.getsize(fpath) > 1000:
                            path = fpath
                            break

            if path and os.path.exists(path):
                try:
                    if path.lower().endswith('.ttc'):
                        pdfmetrics.registerFont(TTFont(CHINESE_FONT_REGISTERED_NAME, path, subfontIndex=0))
                    else:
                        pdfmetrics.registerFont(TTFont(CHINESE_FONT_REGISTERED_NAME, path))

                    addMapping(CHINESE_FONT_REGISTERED_NAME, 0, 0, CHINESE_FONT_REGISTERED_NAME)
                    addMapping(CHINESE_FONT_REGISTERED_NAME, 0, 1, CHINESE_FONT_REGISTERED_NAME)
                    addMapping(CHINESE_FONT_REGISTERED_NAME, 1, 0, CHINESE_FONT_REGISTERED_NAME)
                    addMapping(CHINESE_FONT_REGISTERED_NAME, 1, 1, CHINESE_FONT_REGISTERED_NAME)

                    self._pdf_font_path = path
                    self._pdf_font_name = CHINESE_FONT_REGISTERED_NAME

                    logger.info(f"FontManager: reportlab 注册中文字体 {CHINESE_FONT_REGISTERED_NAME} ({path})")
                    return CHINESE_FONT_REGISTERED_NAME, path
                except Exception as e:
                    logger.warning(f"FontManager: reportlab TTFont注册失败: {e}")

            logger.warning("FontManager: 未找到PDF中文字体文件，尝试使用CID字体")
            try:
                pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
                logger.info("FontManager: reportlab 注册CID字体 STSong-Light")
                return 'STSong-Light', None
            except Exception:
                logger.warning("FontManager: CID字体注册也失败，中文将显示为乱码")
                return 'Helvetica', None
        except ImportError:
            return 'Helvetica', None

    def has_chinese_font(self):
        """检查是否有可用的中文字体"""
        return self._mpl_font_path is not None


# 全局单例
font_manager = FontManager()