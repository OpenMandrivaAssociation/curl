#!/bin/sh
curl https://curl.se/ 2>/dev/null |grep 'most recent stable version' |sed -e 's,.*<b>,,;s,</b>.*,,'
