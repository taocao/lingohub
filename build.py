import os, datetime
from pathlib import Path
import markdown

ARTICLES_DIR = Path("articles")
DIST_DIR = Path("dist")
TEMPLATE_DIR = Path("templates")

DIST_DIR.mkdir(exist_ok=True)

# 加载模板
article_template = (TEMPLATE_DIR / "article_template.html").read_text(encoding="utf-8")
index_template = (TEMPLATE_DIR / "index_template.html").read_text(encoding="utf-8")

# 文章索引
articles = {}

for file in ARTICLES_DIR.glob("*.md"):
    parts = file.stem.split("-")
    date = "-".join(parts[:3])          # 文件名前三段当日期 (YYYY-MM-DD)
    title = " ".join(parts[3:-1])       # 中间部分当标题
    lang = parts[-1]                    # 最后一段是语言 (en / zh)

    with open(file, encoding="utf-8") as f:
        raw_md = f.read()
        html_content = markdown.markdown(raw_md, extensions=["fenced_code", "tables"])

    key = f"{date}-{title}"
    if key not in articles:
        articles[key] = {"date": date, "title": title, "en": None, "zh": None}

    articles[key][lang] = html_content

# 生成文章页面
for key, meta in articles.items():
    slug = key.replace(" ", "-")
    output_file = DIST_DIR / f"{slug}.html"

    en_content = meta.get("en", "<p><i>No English version available.</i></p>")
    zh_content = meta.get("zh", "<p><i>暂无中文翻译。</i></p>")

    html = article_template.replace("{{title}}", meta["title"])
    html = html.replace("{{date}}", meta["date"])
    html = html.replace("{{en}}", en_content)
    html = html.replace("{{zh}}", zh_content)

    output_file.write_text(html, encoding="utf-8")

# 生成首页
items_html = ""
for key, meta in sorted(articles.items(), reverse=True):
    slug = key.replace(" ", "-")
    items_html += f'<li><a class="text-blue-600 underline" href="{slug}.html">{meta["date"]} - {meta["title"]}</a></li>\n'

index_html = index_template.replace("{{articles}}", items_html)
(DIST_DIR / "index.html").write_text(index_html, encoding="utf-8")

print("✅ Site built successfully. Check dist/index.html")
