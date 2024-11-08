#!/bin/sh
# FIXME: curl fails:
#  curl: (61) Unrecognized content encoding type. libcurl understands deflate, gzip, zstd content encodings.
wget -q -O- "https://curl.se/" 2>/dev/null |grep 'most recent stable version' |sed -e 's,.*<b>,,;s,</b>.*,,'
