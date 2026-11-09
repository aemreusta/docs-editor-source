# docs-editor-source

Corresponding source for the document editor image used by Memoris Clinical.

The image is a modified version of [ONLYOFFICE Docs](https://github.com/ONLYOFFICE/DocumentServer),
originally developed by Ascensio System SIA. It is licensed under the GNU AGPL v3 with additional
terms; see [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md). This project is not affiliated with or
endorsed by Ascensio System SIA. The licence grants no trademark rights.

## What changes

Only the editor's name, logo files and its About panel. See [MODIFICATIONS.md](MODIFICATIONS.md).
The server, conversion engine and editing code are the unmodified upstream build.

## Build

```bash
docker build --build-arg SOURCE_URL=<this repository URL> --build-arg MODIFICATION_DATE=<YYYY-MM-DD> -t docs-editor .
```

The Dockerfile starts from the upstream image pinned by digest in [UPSTREAM.md](UPSTREAM.md), then
`branding/apply.py` applies each change as an exact match with an expected count. If upstream moved
the text, the build fails instead of shipping a partial change. `branding/check-notices.py` then fails
the build if a required licence file or notice is missing.

The upstream source for the pinned build is at the tags listed in [UPSTREAM.md](UPSTREAM.md).
