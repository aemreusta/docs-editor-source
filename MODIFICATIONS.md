# Modifications

Every change to the upstream program. Newest first.

## 2026-11-09, based on upstream 10.0.0 (build 169)

Applied by `branding/apply.py` to the web-apps files of the upstream image.

| File under `web-apps/apps/` | Change |
|---|---|
| `common/main/resources/img/header/header-logo_s.svg`, `dark-logo_s.svg`, `about/logo_s.svg`, `about/logo-white_s.svg`, `common/embed/resources/img/logo.svg` | Logo file replaced |
| `*/mobile/resources/img/about/*`, `*/mobile/resources/img/header/*` (SVG) | Logo file replaced |
| `*/*/index*.html`, `api/documents/*.html` | Page title name replaced |
| `common/main/lib/view/About.js` | Vendor address, e-mail, telephone and web link replaced by a notice naming the original developer and this modification, plus licence and source links |
| `common/main/lib/view/Header.js` | Logo link target |
| `documenteditor/main/app/view/LeftMenu.js` | Support link target |
| `documenteditor/main/app/controller/Main.js` | Window title name; product name in licence warning text |

Added: `modified-version/` in the image, holding this file, `NOTICE.md`, `LICENSE` and `UPSTREAM.md`.

Not changed: server, converter, sdkjs, locale files, licence files, source file headers, help content, mobile
application bundles.
