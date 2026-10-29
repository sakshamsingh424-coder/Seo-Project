"""Rule-based on-page + technical SEO auditor (Milestone 1 engine)."""
import re, time
from collections import Counter
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "SEOAuditBot/1.0 (student mini-project)"}
STOP = set("the a an and or of to in is it for on with as at by this that from are be was your you we our can will not have has more all but".split())
SCORE = {"pass": 1.0, "warn": 0.5, "fail": 0.0}


def chk(cat, name, status, msg, fix="", w=1):
    return dict(category=cat, check=name, status=status, message=msg, fix=fix, weight=w)


def fetch(url, timeout=10):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    t = time.time()
    r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
    return r, time.time() - t


def file_exists(base, path):
    try:
        r = requests.get(urljoin(base, path), headers=HEADERS, timeout=6)
        return r.status_code == 200 and len(r.text.strip()) > 0
    except requests.RequestException:
        return False


def band(val, lo, hi, warn_lo=None, warn_hi=None):
    if lo <= val <= hi:
        return "pass"
    if (warn_lo is not None and warn_lo <= val < lo) or (warn_hi is not None and hi < val <= warn_hi):
        return "warn"
    return "fail"


def analyze(html, url, load_time=0.0, status_code=200, keyword="", has_robots=None, has_sitemap=None):
    soup = BeautifulSoup(html, "html.parser")
    host = urlparse(url).netloc
    C, O, T = [], "On-Page", "Technical"
    kw = keyword.strip().lower()

    # --- On-page: title
    title = (soup.title.string or "").strip() if soup.title else ""
    if not title:
        C.append(chk(O, "Title tag", "fail", "Missing <title>.", "Add a unique 30-60 char title.", 3))
    else:
        s = band(len(title), 30, 60, 15, 70)
        C.append(chk(O, "Title tag", s, f"{len(title)} chars: \"{title[:70]}\"",
                     "" if s == "pass" else "Aim for 30-60 characters.", 3))
    # meta description
    md = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    desc = (md.get("content") or "").strip() if md else ""
    if not desc:
        C.append(chk(O, "Meta description", "fail", "Missing meta description.", "Add a 70-160 char summary.", 2))
    else:
        s = band(len(desc), 70, 160, 40, 200)
        C.append(chk(O, "Meta description", s, f"{len(desc)} chars.", "" if s == "pass" else "Aim for 70-160 characters.", 2))
    # headings
    h1 = soup.find_all("h1")
    C.append(chk(O, "H1 heading", "pass" if len(h1) == 1 else "fail",
                 f"{len(h1)} H1 tag(s) found.", "" if len(h1) == 1 else "Use exactly one H1.", 3))
    levels = [int(h.name[1]) for h in soup.find_all(re.compile("^h[1-6]$"))]
    skips = any(b - a > 1 for a, b in zip(levels, levels[1:]))
    C.append(chk(O, "Heading hierarchy", "warn" if skips else "pass",
                 "Heading levels skip (e.g. H2 -> H4)." if skips else "Heading order is logical.",
                 "Do not skip heading levels." if skips else "", 1))
    # images
    imgs = soup.find_all("img")
    noalt = [i for i in imgs if not (i.get("alt") or "").strip()]
    if imgs:
        ratio = len(noalt) / len(imgs)
        s = "pass" if ratio == 0 else "warn" if ratio <= 0.3 else "fail"
        C.append(chk(O, "Image alt text", s, f"{len(noalt)} of {len(imgs)} images lack alt text.",
                     "" if s == "pass" else "Add descriptive alt text.", 2))
    # words
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    words = re.findall(r"[a-zA-Z']{2,}", soup.get_text(" "))
    s = "pass" if len(words) >= 300 else "warn" if len(words) >= 150 else "fail"
    C.append(chk(O, "Content length", s, f"{len(words)} words.", "" if s == "pass" else "Aim for 300+ words of useful content.", 2))
    # links
    links = [a.get("href") for a in soup.find_all("a", href=True)]
    internal = [l for l in links if l.startswith("/") or host in l]
    external = [l for l in links if l.startswith("http") and host not in l]
    C.append(chk(O, "Internal links", "pass" if len(internal) >= 3 else "warn",
                 f"{len(internal)} internal, {len(external)} external links.",
                 "" if len(internal) >= 3 else "Add more internal links.", 1))
    # keyword
    if kw:
        in_t, in_h, in_d = kw in title.lower(), any(kw in h.get_text().lower() for h in h1), kw in desc.lower()
        n = sum([in_t, in_h, in_d])
        C.append(chk(O, "Target keyword", "pass" if n == 3 else "warn" if n else "fail",
                     f"'{kw}' in title: {in_t}, H1: {in_h}, description: {in_d}.",
                     "" if n == 3 else "Use the keyword in title, H1 and meta description.", 3))

    # --- Technical
    C.append(chk(T, "HTTPS", "pass" if url.startswith("https") else "fail",
                 "Served over HTTPS." if url.startswith("https") else "Not using HTTPS.", "Install an SSL certificate.", 3))
    C.append(chk(T, "HTTP status", "pass" if status_code == 200 else "fail", f"Status {status_code}.", "", 2))
    s = "pass" if load_time < 1.5 else "warn" if load_time < 3 else "fail"
    C.append(chk(T, "Response time", s, f"{load_time:.2f}s.", "" if s == "pass" else "Use caching/compression/CDN.", 2))
    can = soup.find("link", rel="canonical")
    C.append(chk(T, "Canonical tag", "pass" if can else "warn", "Present." if can else "Missing canonical.",
                 "" if can else "Add <link rel='canonical'>.", 1))
    vp = soup.find("meta", attrs={"name": "viewport"})
    C.append(chk(T, "Mobile viewport", "pass" if vp else "fail", "Present." if vp else "Missing viewport meta.",
                 "" if vp else "Add width=device-width viewport tag.", 2))
    html_tag = soup.find("html")
    lang = bool(html_tag and html_tag.get("lang"))
    C.append(chk(T, "Language attribute", "pass" if lang else "warn", "Set." if lang else "Missing lang on <html>.", "", 1))
    rb = soup.find("meta", attrs={"name": "robots"})
    noindex = bool(rb and "noindex" in (rb.get("content") or "").lower())
    C.append(chk(T, "Indexability", "fail" if noindex else "pass", "Page is noindex." if noindex else "Page can be indexed.",
                 "Remove noindex." if noindex else "", 3))
    og = soup.find("meta", property="og:title")
    C.append(chk(T, "Open Graph tags", "pass" if og else "warn", "Present." if og else "Missing og:title.", "", 1))
    ld = soup.find("script", type="application/ld+json")
    C.append(chk(T, "Structured data", "pass" if ld else "warn", "JSON-LD found." if ld else "No JSON-LD.", "Add schema.org markup.", 1))
    if has_robots is not None:
        C.append(chk(T, "robots.txt", "pass" if has_robots else "warn", "Found." if has_robots else "Not found.", "", 1))
    if has_sitemap is not None:
        C.append(chk(T, "sitemap.xml", "pass" if has_sitemap else "warn", "Found." if has_sitemap else "Not found.", "", 1))

    # keywords
    freq = Counter(w.lower() for w in words if w.lower() not in STOP and len(w) > 3)
    top = [(w, c, round(100 * c / max(len(words), 1), 2)) for w, c in freq.most_common(10)]

    tot = sum(c["weight"] for c in C)
    score = round(100 * sum(SCORE[c["status"]] * c["weight"] for c in C) / tot) if tot else 0
    cats = {}
    for cat in (O, T):
        sub = [c for c in C if c["category"] == cat]
        w = sum(c["weight"] for c in sub)
        cats[cat] = round(100 * sum(SCORE[c["status"]] * c["weight"] for c in sub) / w) if w else 0
    return dict(url=url, score=score, category_scores=cats, checks=C, keywords=top, word_count=len(words))


def audit_url(url, keyword=""):
    r, t = fetch(url)
    base = f"{urlparse(r.url).scheme}://{urlparse(r.url).netloc}"
    return analyze(r.text, r.url, t, r.status_code, keyword,
                   file_exists(base, "/robots.txt"), file_exists(base, "/sitemap.xml"))


def compare(before, after):
    """Merge two audit results into a per-check before/after table."""
    b = {c["check"]: c for c in before["checks"]}
    rows = []
    for c in after["checks"]:
        old = b.get(c["check"], {})
        rows.append(dict(category=c["category"], check=c["check"],
                         before=old.get("status", "-"), after=c["status"],
                         before_msg=old.get("message", ""), after_msg=c["message"]))
    return rows
