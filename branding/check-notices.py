#!/usr/bin/env python3
"""Fails the image build if a required notice or licence file is missing.

Required text comes from the upstream LICENSE additional terms; see NOTICE.md.
"""
import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get("DS_ROOT", "/var/www/onlyoffice/documentserver"))
errors = []
lic = ROOT / "LICENSE.txt"
text = lic.read_text(encoding="utf-8") if lic.is_file() else ""
for needle in ("GNU AFFERO GENERAL PUBLIC LICENSE", "Retention of Notices and Attribution",
               "identify ONLYOFFICE as the original developer", "No Trademark License"):
    if needle not in text:
        errors.append(f"LICENSE.txt lacks {needle!r}")
if not (ROOT / "3rd-Party.txt").is_file():
    errors.append("3rd-Party.txt missing")
if not any((ROOT / "license").glob("*")):
    errors.append("license/ directory empty")
about = (ROOT / "web-apps/apps/common/main/lib/view/About.js").read_text(encoding="utf-8")
for needle in ("Copyright (C) Ascensio System SIA", "ONLYOFFICE Docs", "Ascensio System SIA", "licenseurl", "sourceurl"):
    if needle not in about:
        errors.append(f"About.js lacks {needle!r}")
if errors:
    sys.exit("\n".join(errors))
print("notices present")
