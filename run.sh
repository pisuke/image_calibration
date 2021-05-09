#!/bin/bash

dcraw -v -t 5 -T -o 5 -j -M -4 chart.nef
scanin -v -dipn chart.tiff SpyderChecker24.cht SpyderChecker24.cie
colprof -v -D"Camera ICC Profile" -qm -am -u chart
profcheck -v2 -k chart.ti3 chart.icc
cctiff -v -i a chart.icc chart.tiff chart_corrected.tiff


