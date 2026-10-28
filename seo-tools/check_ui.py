#!/usr/bin/env python3 -I
"""Interactive acceptance checks with Playwright (Chromium) against the dev server.

    python3 -I seo-tools/check_ui.py [http://localhost:8000]

Checks: skip link is the first focusable element and moves focus to <main>; header dropdowns open and close
by keyboard (Tab/Enter/Esc) and by touch tap; the mobile menu opens, traps Escape, and does not cover the
content once closed; sticky bars do not overlap the last section; the lightbox and booking widget work.
"""
import sys
from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000").rstrip("/")
fails = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


with sync_playwright() as p:
    b = p.chromium.launch()
    # ---------------- desktop keyboard
    pg = b.new_page(viewport={"width": 1366, "height": 900})
    pg.goto(BASE + "/yachts/48-isabella", wait_until="networkidle")
    pg.keyboard.press("Tab")
    first = pg.evaluate("() => document.activeElement.className")
    check(first == "myc-skip", f"skip link is the first focusable element ({first})")
    pg.keyboard.press("Enter")
    pg.wait_for_timeout(200)
    check(pg.evaluate("() => location.hash") == "#main", "skip link jumps to #main")
    pg.evaluate("() => document.querySelector('.myc-nav-toggle').focus()")
    pg.keyboard.press("Enter")
    pg.wait_for_timeout(250)
    check(pg.evaluate("() => document.querySelector('.myc-nav-toggle').getAttribute('aria-expanded')") == "true", "Enter opens the Yachts dropdown")
    pg.keyboard.press("ArrowDown")
    pg.wait_for_timeout(100)
    check(pg.evaluate("() => document.activeElement.closest('.myc-menu') !== null"), "ArrowDown moves focus into the menu")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(250)
    check(pg.evaluate("() => document.querySelector('.myc-nav-toggle').getAttribute('aria-expanded')") == "false", "Escape closes the dropdown")
    check(pg.evaluate("() => document.activeElement.classList.contains('myc-nav-toggle')"), "Escape returns focus to the toggle")
    # Tab through: toggle -> next toggle (menu closed means its links are skipped?) -> open with Enter, Tab into links
    pg.keyboard.press("Enter"); pg.wait_for_timeout(200)
    pg.keyboard.press("Tab"); pg.wait_for_timeout(100)
    check(pg.evaluate("() => document.activeElement.closest('#myc-menu-yachts') !== null"), "Tab after Enter reaches the first menu link")
    # hover opens, leave closes
    pg.mouse.move(5, 5); pg.wait_for_timeout(300)
    pg.hover(".myc-has-menu:nth-child(2) .myc-nav-toggle"); pg.wait_for_timeout(250)
    check(pg.evaluate("() => document.querySelectorAll('.myc-has-menu')[1].classList.contains('is-open')"), "hover opens the Experiences dropdown")
    pg.mouse.move(700, 600); pg.wait_for_timeout(400)
    check(not pg.evaluate("() => document.querySelectorAll('.myc-has-menu')[1].classList.contains('is-open')"), "leaving closes the dropdown")
    # lightbox
    pg.click("[data-lightbox-open]"); pg.wait_for_timeout(300)
    check(pg.evaluate("() => { const d = document.querySelector('dialog.myc-lightbox'); return !!d && d.open }"), "View all photos opens the lightbox")
    pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(100)
    check(pg.evaluate("() => document.querySelector('.myc-lb-count').textContent.startsWith('2 /')"), "ArrowRight advances the lightbox")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
    check(not pg.evaluate("() => document.querySelector('dialog.myc-lightbox').open"), "Escape closes the lightbox")
    # booking widget builds a WhatsApp URL
    pg.fill("#w-date", "2026-12-20"); pg.fill("#w-guests", "8")
    with pg.expect_popup() as pop:
        pg.click(".myc-widget form button[type=submit]")
    url = pop.value.url  # wa.me redirects to api.whatsapp.com/send/?phone=...&text=... (spaces become '+')
    from urllib.parse import urlsplit, parse_qs, unquote_plus
    q = parse_qs(urlsplit(url).query)
    text = unquote_plus(q.get("text", [""])[0])
    phone_ok = "17876645040" in url
    check(phone_ok and "Isabella" in text and "8 guests" in text and "Dec 20" in text, f"booking widget opens WhatsApp with the details ({text[:80]})")
    pop.value.close()
    pg.close()

    # ---------------- phone touch
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
    pg = ctx.new_page()
    pg.goto(BASE + "/experiences/birthday-yacht-party-miami", wait_until="networkidle")
    pg.tap(".myc-burger"); pg.wait_for_timeout(300)
    check(pg.evaluate("() => !document.getElementById('myc-mobile').hidden"), "tap on the hamburger opens the mobile menu")
    check(pg.evaluate("() => document.documentElement.classList.contains('myc-menu-open')"), "page scroll is locked behind the menu")
    pg.tap(".myc-m-toggle"); pg.wait_for_timeout(200)
    check(pg.evaluate("() => !document.getElementById('myc-m-yachts').hidden"), "tap on Yachts expands the accordion")
    check(pg.evaluate("() => { const a = document.querySelector('#myc-m-yachts a'); const r = a.getBoundingClientRect(); return r.top > 60 && r.bottom < 844 }"), "accordion links are on screen")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
    check(pg.evaluate("() => document.getElementById('myc-mobile').hidden"), "Escape closes the mobile menu")
    # sticky bar must not cover the footer's last line
    pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)"); pg.wait_for_timeout(400)
    overlap = pg.evaluate("""() => { const bar = document.querySelector('.myc-sticky-cta').getBoundingClientRect();
        const last = document.querySelector('.myc-footer-bottom').getBoundingClientRect(); return last.bottom > bar.top }""")
    check(not overlap, "sticky bar does not cover the footer bottom bar when scrolled to the end")
    hs = pg.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth")
    check(not hs, "no horizontal scroll on a phone")
    pg.close(); ctx.close()
    b.close()

print(f"\n{len(fails)} failures" if fails else "\nALL UI CHECKS PASSED")
sys.exit(1 if fails else 0)
