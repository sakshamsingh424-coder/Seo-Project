"""Offline demo pages so the dashboard can be shown without internet."""
GOOD = """<html lang='en'><head><title>Best Running Shoes for Beginners: 2026 Buying Guide</title>
<meta name='description' content='Learn how to choose running shoes as a beginner with our complete guide covering fit, cushioning, terrain and price.'>
<meta name='viewport' content='width=device-width, initial-scale=1'><link rel='canonical' href='https://demo.shop/guide'>
<meta property='og:title' content='Running Shoes Guide'><script type='application/ld+json'>{}</script></head>
<body><h1>Running Shoes for Beginners</h1><h2>Fit</h2><h2>Cushioning</h2><a href='/a'>a</a><a href='/b'>b</a><a href='/c'>c</a>
<img src='x.jpg' alt='Beginner running shoes'>""" + "<p>Choosing running shoes depends on fit, cushioning, terrain and budget for every beginner runner.</p>" * 40 + "</body></html>"
BAD = """<html><head><title>Home</title></head><body><h3>Welcome</h3><h1>Shop</h1><h1>Sale</h1><img src='a.jpg'><img src='b.jpg'>
<p>Buy shoes here.</p></body></html>"""
SAMPLES = {"Well-optimised page": GOOD, "Poorly-optimised page": BAD}


# ---- Before / After case study: the SAME website, before and after SEO fixes ----
BEFORE_HTML = """<html><head><title>Home</title></head><body>
<h1>Welcome</h1><h1>Shoes</h1><h4>Sale</h4>
<img src='s1.jpg'><img src='s2.jpg'><img src='s3.jpg'>
<p>We sell shoes. Buy shoes at our store. Good prices.</p></body></html>"""

AFTER_HTML = """<html lang='en'><head>
<title>Running Shoes for Beginners | Sharma Sports Store</title>
<meta name='description' content='Shop beginner running shoes with expert fitting advice. Compare cushioning, fit and price, with free delivery across India.'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<link rel='canonical' href='https://sharmasports.example/running-shoes'>
<meta property='og:title' content='Running Shoes for Beginners | Sharma Sports Store'>
<script type='application/ld+json'>{"@context":"https://schema.org","@type":"Store","name":"Sharma Sports Store"}</script>
</head><body>
<h1>Running Shoes for Beginners</h1>
<h2>How to choose the right fit</h2><h2>Cushioning and comfort</h2><h2>Prices and offers</h2>
<a href='/men'>Men</a><a href='/women'>Women</a><a href='/kids'>Kids</a><a href='/offers'>Offers</a>
<img src='s1.jpg' alt='Beginner running shoes with soft cushioning'>
<img src='s2.jpg' alt='Lightweight trail running shoes'>
<img src='s3.jpg' alt='Budget running shoes under 3000 rupees'>""" + \
"<p>Choosing running shoes depends on fit, cushioning, terrain and budget. Beginners should look for comfortable running shoes with good support.</p>" * 30 + "</body></html>"

CASE = {
    "site": "Sharma Sports Store (demo website)",
    "keyword": "running shoes",
    "before": dict(html=BEFORE_HTML, url="http://sharmasports.example/", load=2.8, robots=False, sitemap=False),
    "after": dict(html=AFTER_HTML, url="https://sharmasports.example/running-shoes", load=0.9, robots=True, sitemap=True),
}

FIXES = [
    ("Title tag", "Title was just 'Home'", "Keyword-rich 52-char title"),
    ("Meta description", "Missing", "Added 120-char description"),
    ("H1 heading", "Two H1 tags", "Exactly one H1"),
    ("Heading hierarchy", "H1 jumped to H4", "H1 then H2 sections"),
    ("Image alt text", "3 images without alt", "Descriptive alt on every image"),
    ("Content length", "About 10 words", "300+ words of useful content"),
    ("Internal links", "None", "4 navigation links"),
    ("Target keyword", "Keyword absent", "In title, H1 and description"),
    ("HTTPS", "Served over HTTP", "Moved to HTTPS"),
    ("Response time", "2.8 seconds", "0.9 seconds (compression, caching)"),
    ("Mobile viewport", "Missing", "Viewport meta added"),
    ("Technical tags", "No canonical, lang, Open Graph, JSON-LD", "All added"),
    ("robots.txt / sitemap.xml", "Missing", "Both published"),
]
