#!/usr/bin/env python3
"""Build the static RemoteTaskPortal deployment artifact."""
from __future__ import annotations
import html
import json
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"
BASE = "https://remotetaskportal.site"
NAV = """<a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="container header-inner"><a class="brand" href="/" aria-label="RemoteTaskPortal home"><span class="brand-mark" aria-hidden="true">R</span><span>RemoteTask<span class="brand-accent">Portal</span></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="primary-nav" aria-label="Open navigation"><span></span><span></span><span></span></button><nav id="primary-nav" class="nav-links" aria-label="Main navigation"><a href="/tasks/">Browse tasks</a><a href="/how-it-works/">How it works</a><a href="/about/">About</a><a href="/faq/">FAQ</a><a class="nav-cta" href="/tasks/">Explore offers</a></nav></div></header>"""
FOOTER = """<footer class="site-footer"><div class="container footer-grid"><div><a class="brand footer-brand" href="/"><span class="brand-mark" aria-hidden="true">R</span><span>RemoteTask<span class="brand-accent">Portal</span></span></a><p class="footer-note">A directory of third-party online offers. Clear information, direct links, and no earnings promises.</p></div><div><h2>Explore</h2><a href="/tasks/">Browse offers</a><a href="/how-it-works/">How it works</a><a href="/about/">About us</a><a href="/faq/">FAQ</a></div><div><h2>Information</h2><a href="/contact/">Contact</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a></div></div><div class="container footer-bottom"><span>© <span data-year>2026</span> RemoteTaskPortal</span><span>Independent directory · Third-party offers</span></div></footer><script src="/assets/js/app.js" defer></script>"""
def shell(title: str, description: str, path: str, content: str, *, noindex: bool = False) -> str:
    robots = 'noindex,follow' if noindex else 'index,follow'
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(description, quote=True)}">
<meta name="robots" content="{robots}"><link rel="canonical" href="{BASE}{path}"><link rel="icon" href="data:,"><link rel="stylesheet" href="/assets/css/style.css"></head>
<body>{NAV}<main id="main">{content}</main>{FOOTER}</body></html>
'''
def main() -> None:
    offers_doc = json.loads((ROOT / "data/offers.json").read_text(encoding="utf-8"))
    offers = offers_doc.get("offers", [])
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    for name in ("index.html", "404.html", "tasks", "how-it-works", "faq", "about", "contact", "privacy", "terms", "assets"):
        src = ROOT / name
        if src.is_dir():
            shutil.copytree(src, OUT / name)
        elif src.is_file():
            shutil.copy2(src, OUT / name)
    (OUT / "data").mkdir(exist_ok=True)
    shutil.copy2(ROOT / "data/offers.json", OUT / "data/offers.json")
    # Keep every slug stable. Draft details are noindex; inactive and draft entries
    # never receive an outbound CTA. The public directory lists active offers only.
    for offer in offers:
        slug = str(offer.get("slug", "")).strip()
        if not slug or any(part in slug for part in ("/", "\\", "..")):
            raise ValueError(f"Unsafe or missing offer slug: {slug!r}")
        status = offer.get("status", "draft")
        if status not in {"active", "inactive", "draft"}:
            raise ValueError(f"Invalid status for {slug}: {status}")
        path = f"/tasks/{slug}/"
        title = html.escape(str(offer.get("title", "Online offer")))
        desc = html.escape(str(offer.get("description", "")), quote=True)
        countries = ", ".join(html.escape(str(c)) for c in offer.get("countries", []))
        active = status == "active"
        link = str(offer.get("getlink", ""))
        configured = active and link.startswith("https://") and "example.com/replace-with-adbluemedia-getlink" not in link
        button = (f'<a class="button button-primary provider-action" href="{html.escape(link, quote=True)}" target="_blank" rel="sponsored noopener noreferrer">Continue to provider <span aria-hidden="true">↗</span></a>'
                  if configured else f'<span class="button provider-action" aria-disabled="true">{ "GetLink not configured" if active else ("Offer unavailable" if status == "inactive" else "Offer not published")}</span>')
        requirements = "".join(f"<li>{html.escape(str(item))}</li>" for item in offer.get("requirements", []))
        status_note = "" if active else f'<div class="notice">{ "This offer is currently inactive." if status == "inactive" else "This offer is a draft and is not available to visitors."}</div>'
        body = f'''<section class="page-hero page-hero-compact"><div class="container"><p class="eyebrow">Offer details · {countries}</p><h1>{title}</h1><p class="page-lede">{desc}</p></div></section>
<section class="section section-reading"><div class="container content-grid"><article class="prose offer-detail"><h2>Before you continue</h2><p>{desc}</p><ul>{requirements}</ul><p><strong>Reward information:</strong> {html.escape(str(offer.get("reward", "See provider terms")))}. Eligibility, availability, and any reward are determined by the provider.</p><div class="disclosure">This is a third-party offer. RemoteTaskPortal does not operate the activity or verify completion. Review the provider’s terms and privacy information before participating. Rewards are not guaranteed.</div>{status_note}{button}</article><aside class="side-card"><span class="side-icon">↗</span><h2>Third-party provider</h2><p>The provider controls sign-up, eligibility, activity, terms, any reward, and support. Contact it directly with participation questions.</p><a class="text-link" href="/how-it-works/">How offers work →</a></aside></div></section>'''
        (OUT / "tasks" / slug).mkdir(parents=True, exist_ok=True)
        (OUT / "tasks" / slug / "index.html").write_text(shell(f"{title} | RemoteTaskPortal", desc, path, body, noindex=status == "draft"), encoding="utf-8")
    today = date.today().isoformat()
    urls = ["/", "/tasks/", "/how-it-works/", "/faq/", "/about/", "/contact/", "/privacy/", "/terms/"]
    urls += [f"/tasks/{o['slug']}/" for o in offers if o.get("status") == "active" and o.get("slug")]
    entries = "".join(f"<url><loc>{BASE}{html.escape(path)}</loc></url>" for path in urls)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{entries}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    (OUT / "CNAME").write_text("remotetaskportal.site\n", encoding="utf-8")
    print(f"Built {len(offers)} offer detail page(s) into {OUT} on {today}.")
if __name__ == "__main__":
    main()
