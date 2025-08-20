# LingoHub Project

LingoHub is a multilingual publishing pipeline designed for bloggers, educators, and learners.  
It automates **translation, summarization, key point extraction, audio generation, and publishing** to GitHub Pages, making content more accessible and engaging.

---

## ✨ Features

- **Incremental Workflow**: Only processes newly added or updated articles.
- **Multilingual Support**: Supports English 🇬🇧 and Chinese 🇨🇳 by default (easily extendable).
- **Auto Translation**: Uses LLMs to translate between languages while preserving formatting.
- **Smart Matching**: Treats similar article names as the same (e.g., typo tolerance in filenames).
- **Dual-Mode Articles**: Supports both single-file bilingual articles or separate files for each language.
- **Summaries & Key Points**: Auto-generated concise takeaways for each article.
- **Audio Narration**: Converts articles into high-quality speech using TTS.
- **Karaoke-Style Highlighting**: Synchronizes spoken words with highlighted text on the page.
- **Beautiful Pages**: Modern UI with reader-friendly layout and multilingual toggle.
- **GitHub Pages Deployment**: Fully automated via GitHub Actions.

---

## 📂 Project Structure

```bash
.
├── articles/                  # Input markdown articles
│   ├── 2025-08-21-ai-trends-en.md
│   ├── 2025-08-21-ai-trends-zh.md
│   └── 2025-08-21-ai-trends.md   # bilingual file also works
├── site/                      # Generated static site
│   └── index.html
├── scripts/                   # Processing scripts
│   ├── process_articles.py    # Core logic: parse, translate, build site
│   ├── translate_llm.py       # Handles LLM-based translation
│   ├── generate_audio.py      # Creates TTS audio + word timings
│   └── utils.py               # Helper functions (naming, parsing, etc.)
├── .github/workflows/         # GitHub Actions CI/CD
│   └── deploy.yml             # Build + deploy to GitHub Pages
└── README.md                  # Project documentation
```

---

## 🚀 Workflow

1. **Write Article**  
   Add markdown files to `articles/` in either English, Chinese, or bilingual format.

2. **Run Workflow**  
   GitHub Actions detects new or updated articles:
   - Translate missing versions with LLM.
   - Generate summary & key points.
   - Create audio narration with timestamps.
   - Build static pages with modern UI.

3. **Deploy**  
   The updated site is automatically published on **GitHub Pages**.

---

## 🔧 Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-username/lingohub.git
cd lingohub
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
- Add your **LLM API key** (e.g., OpenAI) to repository secrets.
- Add your **TTS API key** (Azure, Google, or OpenAI Whisper) if needed.

### 4. Enable GitHub Pages
- Go to **Settings > Pages** and enable Pages from the `gh-pages` branch.

---

## 📖 Usage

### Local Build
```bash
python scripts/process_articles.py
```

### Deploy Manually
```bash
mkdocs build
mkdocs gh-deploy
```

### Auto Deploy (CI/CD)
Every push to `main` triggers:
- Incremental processing
- Translation & audio generation
- Static site rebuild
- GitHub Pages deployment

---

## 📝 TODOS

- [ ] Add support for **more languages** (Spanish, French, etc.).
- [ ] Improve typo-tolerant filename matching (use fuzzy matching).
- [ ] Enhance UI with **dark/light theme** toggle.
- [ ] Add **search and filter** for articles.
- [ ] Support **podcast feed (RSS)** from generated audio.
- [ ] Integrate **interactive quizzes** for language learning.

---

## 🤖 Powered By

- **OpenAI / Anthropic** for LLM-based translation & summarization.
- **Azure / Google / OpenAI TTS** for natural-sounding speech synthesis.
- **Python + MkDocs** for static site generation.
- **GitHub Actions** for CI/CD automation.

---

## ❤️ Contributing

Contributions are welcome!  
Feel free to open issues, submit PRs, or suggest features.

---

## 📜 License

MIT License © 2025  
You are free to use, modify, and distribute this project.
