"""LLM Wiki 與簡報的檢查節點。

用法：
  python3 pipeline/check.py wiki      # Lint Wiki
  python3 pipeline/check.py outline   # 檢查簡報大綱（產生 HTML 前）
  python3 pipeline/check.py slides    # 檢查簡報內容
"""
import re, sys, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
SLIDES = ROOT.parent / "slides" / "korea-exchange" / "index.html"
META_PAGES = {"index.md", "log.md", "sources.md", "conflicts.md"}
CITE = re.compile(r"\[(S\d+)\]")
NUM = re.compile(r"\d[\d,./–-]*\d|\d")
VISA = re.compile(r"[A-Z]-\d(?:-\d)?")  # 簽證代碼不算數字

def load_sources():
    tiers = {}
    for line in (WIKI / "sources.md").read_text().splitlines():
        m = re.match(r"\|\s*(S\d+)\s*\|.*\|\s*(official|secondary)\s*\|", line)
        if m:
            tiers[m.group(1)] = m.group(2)
    return tiers

def lint_wiki():
    tiers = load_sources()
    errors = []
    for page in sorted(WIKI.glob("*.md")):
        if page.name in META_PAGES:
            continue
        for n, line in enumerate(page.read_text().splitlines(), 1):
            s = line.strip()
            if not s.startswith("- "):
                continue
            cites = CITE.findall(s)
            where = f"{page.name}:{n}"
            if not cites and "待確認" in s:
                continue  # 規則允許：查不到的資訊寫「待確認」
            if not cites:
                errors.append(f"[無來源] {where}  {s[:50]}")
                continue
            for c in cites:
                if c not in tiers:
                    errors.append(f"[來源不存在] {where}  {c}")
            body = VISA.sub("", CITE.sub("", s))
            only_secondary = all(tiers.get(c) == "secondary" for c in cites)
            if only_secondary and NUM.search(body):
                errors.append(f"[二手來源撐數字] {where}  {s[:50]}")
    return errors

def wiki_text():
    return "\n".join(p.read_text() for p in WIKI.glob("*.md"))

def check_slides():
    tiers = load_sources()
    corpus = wiki_text()
    doc = SLIDES.read_text()
    errors = []
    slides = re.findall(r'<section class="slide"[^>]*>(.*?)</section>', doc, re.S)
    if not 10 <= len(slides) <= 16:
        errors.append(f"[張數] 共 {len(slides)} 張，建議 10–16 張")
    facts = re.findall(r'<(?:li|p|td)[^>]*class="fact"[^>]*data-src="([^"]*)"[^>]*>(.*?)</(?:li|p|td)>', doc, re.S)
    if not facts:
        errors.append("[找不到事實句] 沒有 class=fact 的元素")
    for src, body in facts:
        text = html.unescape(re.sub(r"<[^>]+>", "", body)).strip()
        ids = src.split()
        if not ids:
            errors.append(f"[無來源] {text[:40]}")
        gaps = set(re.findall(r"\|\s*(G\d+)\s*\|", (WIKI / "conflicts.md").read_text()))
        for i in ids:
            if i in gaps:
                continue  # 缺口編號：代表「待確認」，要能在 conflicts.md 找到
            if i not in tiers:
                errors.append(f"[來源不存在] {i}  {text[:40]}")
        if ids and all(tiers.get(i) == "secondary" for i in ids) and NUM.search(VISA.sub("", text)):
            errors.append(f"[二手來源撐數字] {text[:40]}")
        for num in NUM.findall(VISA.sub("", text)):
            if num not in corpus:
                errors.append(f"[數字不在 Wiki] {num}  ←  {text[:40]}")
    # 給初學者：術語第一次出現時要有白話說明（後面緊接全形括號）
    plain = html.unescape(re.sub(r"<[^>]+>", " ", doc))
    for term in ["D-2-6", "ARC", "NHIS", "K-ETA", "CoA"]:
        i = plain.find(term)
        if i == -1:
            continue
        after = plain[i + len(term): i + len(term) + 3]
        if "（" not in after and "(" not in after:
            errors.append(f"[術語沒解釋] {term} 第一次出現時沒有說明")
    for k, s in enumerate(slides, 1):
        t = re.sub(r"<[^>]+>", "", s)
        t = re.sub(r"\s+", "", html.unescape(t))
        if len(t) > 260:
            errors.append(f"[字太多] 第 {k} 張約 {len(t)} 字（上限 260）")
    return errors

def check_outline():
    tiers = load_sources()
    corpus = wiki_text()
    text = (ROOT / "pipeline" / "outline.md").read_text()
    gaps = set(re.findall(r"\|\s*(G\d+)\s*\|", (WIKI / "conflicts.md").read_text()))
    errors = []
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s.startswith("- "):
            continue
        cites = re.findall(r"\[((?:S|G)\d+)\]", s)
        if not cites:
            errors.append(f"[無來源] outline.md:{n}  {s[:40]}")
        for c in cites:
            if c not in tiers and c not in gaps:
                errors.append(f"[來源不存在] outline.md:{n}  {c}")
        for num in NUM.findall(VISA.sub("", re.sub(r"\[(?:S|G)\d+\]|C\d", "", s))):
            if num not in corpus:
                errors.append(f"[數字不在 Wiki] outline.md:{n}  {num}")
    terms = set(re.findall(r"([A-Z][A-Za-z0-9-]+)＝", text))
    for term in ["D-2-6", "ARC", "NHIS", "K-ETA", "CoA"]:
        if term in text and term not in terms:
            errors.append(f"[術語沒列入術語欄] {term}")
    return errors

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "wiki"
    errs = {"wiki": lint_wiki, "outline": check_outline, "slides": check_slides}[mode]()
    print(f"== check {mode}: {len(errs)} 個問題")
    for e in errs:
        print(" ", e)
    sys.exit(1 if errs else 0)
