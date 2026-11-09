#!/usr/bin/env python3
"""Applies the branding change to the web-apps tree of the pinned upstream image.

Only strings and logo files change. Every edit is an exact match with an
expected count, so a new upstream release fails the build instead of silently
shipping a half-branded or notice-less editor. No upstream notice, licence file
or source header is touched; check-notices.py verifies that afterwards.
"""
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(os.environ.get("DS_ROOT", "/var/www/onlyoffice/documentserver"))
APPS = ROOT / "web-apps/apps"
HERE = Path(__file__).resolve().parent
BRAND = os.environ.get("BRAND_NAME", "Memoris")
SITE = os.environ.get("BRAND_URL", "https://memorisclinical.com")
SOURCE_URL = os.environ["SOURCE_URL"]
LICENSE_URL = os.environ.get("LICENSE_URL", SOURCE_URL + "/blob/main/LICENSE")
MOD_DATE = os.environ["MODIFICATION_DATE"]
MODIFIER = os.environ.get("MODIFIER_NAME", "Memoris Clinical")

NOTICES = {
    "en": (f"This software is a modified version of ONLYOFFICE Docs, originally developed by Ascensio System SIA. "
           f"Modified by {MODIFIER} on {MOD_DATE}.", "License: GNU AGPL v3 and additional terms", "Source code"),
    "tr": (f"Bu yazılım, özgün geliştiricisi Ascensio System SIA olan ONLYOFFICE Docs'un değiştirilmiş bir sürümüdür. "
           f"Değiştiren: {MODIFIER}, {MOD_DATE}.", "Lisans: GNU AGPL v3 ve ek şartlar", "Kaynak kodu"),
    "de": (f"Diese Software ist eine geänderte Fassung von ONLYOFFICE Docs, ursprünglich entwickelt von Ascensio System SIA. "
           f"Geändert von {MODIFIER} am {MOD_DATE}.", "Lizenz: GNU AGPL v3 und Zusatzbedingungen", "Quellcode"),
}


def edit(rel, old, new, count=1):
    path = APPS / rel
    text = path.read_text(encoding="utf-8")
    found = text.count(old)
    if found != count:
        sys.exit(f"{rel}: expected {count} of {old[:60]!r}, found {found}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def about():
    rel = "common/main/lib/view/About.js"
    path = APPS / rel
    text = path.read_text(encoding="utf-8")
    table = re.compile(r"'<table id=\"id-about-licensor-info\".*?'</table>',\n", re.S)
    if len(table.findall(text)) != 1:
        sys.exit(f"{rel}: licensor table not found exactly once")
    block = """'<table id="id-about-licensor-info" cols="1" style="width: 100%;" class="margin-bottom">',
                    '<tr><td align="center" style="padding: 20px 8px 10px 8px; white-space: normal;"><label class="asc-about-desc"><%= notice %></label></td></tr>',
                    '<tr><td align="center" class="padding-small"><a href="<%= licenseurl %>" target="_blank" style="text-decoration: underline;"><%= licensetext %></a></td></tr>',
                    '<tr><td align="center" class="padding-small"><a href="<%= sourceurl %>" target="_blank" style="text-decoration: underline;"><%= sourcetext %></a></td></tr>',
                '</table>',
"""
    text = table.sub(lambda _: block, text)
    values = re.compile(r"publishername: 'Ascensio System SIA',.*?phonenum: '[^']*',\n", re.S)
    if len(values.findall(text)) != 1:
        sys.exit(f"{rel}: publisher values not found exactly once")
    import json
    notices = json.dumps(NOTICES, ensure_ascii=False)
    text = values.sub(lambda _: (
        f"publishername: 'Ascensio System SIA',\n"
        f"                    notice: ({notices}[(Common.Locale.getCurrentLanguage() || 'en').split('-')[0]] || {notices}.en)[0],\n"
        f"                    licensetext: ({notices}[(Common.Locale.getCurrentLanguage() || 'en').split('-')[0]] || {notices}.en)[1],\n"
        f"                    sourcetext: ({notices}[(Common.Locale.getCurrentLanguage() || 'en').split('-')[0]] || {notices}.en)[2],\n"
        f"                    licenseurl: '{LICENSE_URL}',\n"
        f"                    sourceurl: '{SOURCE_URL}',\n"
        f"                    publisherurl: '{SITE}',\n"), text)
    path.write_text(text, encoding="utf-8")


def logos():
    src = HERE / "logos"
    pairs = {
        "common/main/resources/img/header/header-logo_s.svg": "header-light.svg",
        "common/main/resources/img/header/dark-logo_s.svg": "header-dark.svg",
        "common/main/resources/img/about/logo_s.svg": "about-dark.svg",
        "common/main/resources/img/about/logo-white_s.svg": "about-white.svg",
        "common/embed/resources/img/logo.svg": "header-dark.svg",
    }
    for rel, name in pairs.items():
        if not (APPS / rel).is_file():
            sys.exit(f"missing logo {rel}")
        shutil.copyfile(src / name, APPS / rel)
    for editor in ("documenteditor", "pdfeditor", "presentationeditor", "spreadsheeteditor", "visioeditor"):
        for variant, name in (("about/logo_s.svg", "about-dark.svg"), ("about/logo-white_s.svg", "about-white.svg"),
                              ("about/logo-new.svg", "about-dark.svg"), ("about/logo-new-white.svg", "about-white.svg"),
                              ("header/header-logo-ios.svg", "header-dark.svg"), ("header/logo-ios.svg", "header-dark.svg"),
                              ("header/header-logo-android.svg", "header-light.svg"), ("header/logo-android.svg", "header-light.svg")):
            target = APPS / editor / "mobile/resources/img" / variant
            if target.is_file():
                shutil.copyfile(src / name, target)


def titles():
    pat = re.compile(r"<title>ONLYOFFICE ")
    n = 0
    for path in list(APPS.glob("*/*/index*.html*")) + list((APPS / "api/documents").glob("*.html")):
        text = path.read_text(encoding="utf-8")
        new, k = pat.subn(f"<title>{BRAND} ", text)
        if k:
            path.write_text(new, encoding="utf-8")
            n += k
    if n < 3:
        sys.exit(f"expected at least 3 titles, changed {n}")


def main():
    logos()
    titles()
    about()
    edit("common/main/lib/view/Header.js", "me.branding.logo.url : 'https://www.onlyoffice.com'",
         f"me.branding.logo.url : '{SITE}'")
    edit("documenteditor/main/app/view/LeftMenu.js", "window.open('https://support.onlyoffice.com')",
         f"window.open('{SITE}')")
    main_js = "documenteditor/main/app/controller/Main.js"
    edit(main_js, "me.defaultTitleText = 'ONLYOFFICE';", f"me.defaultTitleText = '{BRAND}';")
    edit(main_js, ".replace(/%1/g, 'ONLYOFFICE');", f".replace(/%1/g, '{BRAND}');", count=5)
    print("branding applied")


if __name__ == "__main__":
    main()
