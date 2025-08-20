import os
import shutil
from pathlib import Path
import markdown
from difflib import SequenceMatcher
import re

# 文章目录
ARTICLES_DIR = Path("articles")
SITE_DIR = Path("site")
TEMPLATE_DIR = Path("templates")

# 清空旧站点内容
if SITE_DIR.exists():
    shutil.rmtree(SITE_DIR)
SITE_DIR.mkdir(exist_ok=True)

# 加载模板
article_template = (TEMPLATE_DIR / "article_template.html").read_text(encoding="utf-8")
index_template = (TEMPLATE_DIR / "index_template.html").read_text(encoding="utf-8")

# 文章索引
articles = {}

def similar(a, b):
    """简单相似度检测，返回True表示两个名字类似"""
    return SequenceMatcher(None, a, b).ratio() > 0.85

def clean_title(name):
    """移除日期和语言后缀"""
    # 去掉文件扩展名
    name = Path(name).stem
    # 去掉日期和语言标记
    parts = name.split("-")
    if parts[-1] in ["en", "zh"]:
        parts = parts[:-1]
    # 去掉日期格式部分
    parts = [p for p in parts if not re.match(r"\d{4}", p)]
    return "-".join(parts)

def extract_sections(md_text):
    """如果文件中同时有英文和中文，用## English / ## 中文分段"""
    en_html = zh_html = None
    sections = re.split(r"^##\s+", md_text, flags=re.MULTILINE)
    for sec in sections:
        if sec.strip().startswith("English"):
            en_md = "\n".join(sec.strip().splitlines()[1:])
            en_html = markdown.markdown(en_md, extensions=["fenced_code", "tables"])
        elif sec.strip().startswith("中文") or sec.strip().startswith("Chinese"):
            zh_md = "\n".join(sec.strip().splitlines()[1:])
            zh_html = markdown.markdown(zh_md, extensions=["fenced_code", "tables"])
    return en_html, zh_html

# 遍历文章文件
for file in ARTICLES_DIR.glob("*.md"):
    with open(file, encoding="utf-8") as f:
        raw_md = f.read()

    # 先尝试提取分段
    en_content, zh_content = extract_sections(raw_md)

    # 如果没有分段，用语言后缀判断
    if not en_content and not zh_content:
        stem = file.stem.lower()
        if stem.endswith("-en"):
            en_content = markdown.markdown(raw_md, extensions=["fenced_code", "tables"])
        elif stem.endswith("-zh"):
            zh_content = markdown.markdown(raw_md, extensions=["fenced_code", "tables"])
        else:
            # 默认中文
            zh_content = markdown.markdown(raw_md, extensions=["fenced_code", "tables"])

    # 标题清洗，用于归类类似名字
    title_key = clean_title(file.stem)

    # 查找已有类似文章
    found = False
    for key in articles.keys():
        if similar(title_key, key):
            title_key = key
            found = True
            break

    if title_key not in articles:
        articles[title_key] = {"title": title_key, "en": None, "zh": None}

    # 合并内容
    if en_content:
        articles[title_key]["en"] = en_content
    if zh_content:
        articles[title_key]["zh"] = zh_content

# 生成文章页面
for key, meta in articles.items():
    slug = key.replace(" ", "-")
    output_file = SITE_DIR / f"{slug}.html"

    en_content = meta.get("en") or "<p><i>No English version available.</i></p>"
    zh_content = meta.get("zh") or "<p><i>暂无中文翻译。</i></p>"

    html = article_template.replace("{{title}}", meta["title"])
    html = html.replace("{{en}}", en_content)
    html = html.replace("{{zh}}", zh_content)

    output_file.write_text(html, encoding="utf-8")

# 生成首页
items_html = ""
for key, meta in sorted(articles.items()):
    slug = key.replace(" ", "-")
    items_html += f'<li><a class="text-blue-600 underline" href="{slug}.html">{meta["title"]}</a></li>\n'

index_html = index_template.replace("{{articles}}", items_html)
(SITE_DIR / "index.html").write_text(index_html, encoding="utf-8")

print("✅ Site built successfully. Check site/index.html")
