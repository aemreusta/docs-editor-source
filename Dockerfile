# Upstream ONLYOFFICE Docs 10.0.0 image, digest-pinned. Multi-arch: pin matches compose.
FROM onlyoffice/documentserver@sha256:ca17889f10b11141cc6441836aebdd2835cf3e1b49681b2fd6e155c94b7850b3

ARG SOURCE_URL
ARG MODIFICATION_DATE
COPY branding/ /tmp/branding/
COPY LICENSE NOTICE.md MODIFICATIONS.md UPSTREAM.md /var/www/onlyoffice/documentserver/modified-version/
RUN test -n "$SOURCE_URL" && test -n "$MODIFICATION_DATE" \
 && SOURCE_URL="$SOURCE_URL" MODIFICATION_DATE="$MODIFICATION_DATE" python3 /tmp/branding/apply.py \
 && python3 /tmp/branding/check-notices.py \
 && rm -rf /tmp/branding
