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
    """清洗文件名，去掉日期和语言后缀"""
    name = Path(name).stem
    parts = name.split("-")
    if parts[-1].lower() in ["en", "zh"]:
        parts = parts[:-1]
    # 移除日期部分
    parts = [p for p in parts if not re.match(r"\d{4}", p)]
    return " ".join(parts)

def extract_sections(md_text):
    """提取单文件中的英文和中文段落"""
    en_html = zh_html = None
    sections = re.split(r"^##\s+", md_text, flags=re.MULTILINE)
    for sec in sections:
        if sec.strip().lower().startswith("english"):
            en_md = "\n".join(sec.strip().splitlines()[1:])
            en_html = markdown.markdown(en_md, extensions=["fenced_code", "tables"])
        elif sec.strip().startswith("中文") or sec.strip().lower().startswith("chinese"):
            zh_md = "\n".join(sec.strip().splitlines()[1:])
            zh_html = markdown.markdown(zh_md, extensions=["fenced_code", "tables"])
    return en_html, zh_html

# 遍历文章文件
for file in ARTICLES_DIR.glob("*.md"):
    with open(file, encoding="utf-8") as f:
        raw_md = f.read()

    en_content, zh_content = extract_sections(raw_md)

    # 如果没有分段，使用文件名后缀判断
    if en_content is None and zh_content is None:
        stem = file.stem.lower()
        html_content = markdown.markdown(raw_md, extensions=["fenced_code", "tables"])
        if stem.endswith("-en"):
            en_content = html_content
        elif stem.endswith("-zh"):
            zh_content = html_content
        else:
            # 默认中文
            zh_content = html_content

    # 清洗标题，便于归类
    title_key = clean_title(file.stem)

    # 查找已有类似文章
    for key in list(articles.keys()):
        if similar(title_key, key):
            title_key = key
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
