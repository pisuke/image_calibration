# Raw camera image calibration process using a Colour Checker Chart

## Tools

Argyll CMS
dcraw

Install the `numpy` and `colour-science` python libraries with the following command
```
pip install -r requirements.txt
```

## Procedure

1. Convert raw chart image to linear TIFF in the XYZ colour space (the -t flag can be changed to rotate the image)

```
dcraw -v -t 5 -T -o 5 -j -M -4 chart.nef
```

```
Loading Nikon D800 image from chart.nef ...
Scaling with darkness 0, saturation 4095, and
multipliers 2.261569 1.000000 1.181638 1.000000
AHD interpolation...
open .Converting to XYZ colorspace...
Writing data to chart.tiff ...
```


2. Create a ti3 file from the TIFF image of the chart

```
scanin -v -dipn chart.tiff SpyderChecker24.cht SpyderChecker24.cie
```

```
Input file 'chart.tiff': w=4924, h=7378, d = 3, bpp = 16
Data input file 'SpyderChecker24.cie'
Data output file 'chart.ti3'
Chart reference file 'SpyderChecker24.cht'
Creating diagnostic tiff file 'diag.tif'
About to allocate scanrd_ object
Verbosity = 2, flags = 0x42a01
About to read input tiff file and discover groups
adivval = 0.481716
About to calculate edge lines
6382 useful edges out of 124863
About to calculate rotation
Mean angle = 5.551539
Standard deviation = 19.471800
Robust mean angle = -0.582277 from 5454 lines
About to calculate feature information
About to read reference feature information
Read of chart reference file succeeded
About to match features
Checking xx
Checking yy
Checking xy
Checking yx
Checking xix
Checking yiy
Checking xiy
Checking yix
Axis matches for each possible orientation:
  0: xx  = 0.364762, yy  = 0.051372, xx.sc  = 0.145241, yy.sc  = 0.192654
 90: xiy = 0.069241, yx  = 0.353587, xiy.sc = 0.195243, yx.sc  = 0.193626
180: xix = 0.364762, yiy = 0.051372, xix.sc = 0.145241, yiy.sc = 0.192654
270: xy  = 0.069241, yix = 0.352210, xy.sc  = 0.195243, yix.sc = 0.194007
r0 = 0.277706, r90 = 0.357319, r180 = 0.277706, r270 = 0.356681
There are 4 candidate rotations:
cc = 0.277706, irot = -0.582277, xoff = 812.844097, yoff = 2588.940800, xscale = 6.885100, yscale = 5.190652
cc = 0.357319, irot = 89.417723, xoff = -4732.915532, yoff = 983.718436, xscale = 5.121834, yscale = 5.164599
cc = 0.277706, irot = 179.417723, xoff = -3680.488416, yoff = -5809.740115, xscale = 6.885100, yscale = 5.190652
cc = 0.356681, irot = 269.417723, xoff = 2599.671811, yoff = -4187.204718, xscale = 5.121834, yscale = 5.154443
About to compute match transform for rotation -0.582277 deg.
About to setup value scanrdg boxes
About to read raster values
About to compute expected value correlation
About to compute match transform for rotation 89.417723 deg.
About to setup value scanrdg boxes
About to read raster values
About to compute expected value correlation
About to compute match transform for rotation 179.417723 deg.
About to setup value scanrdg boxes
About to read raster values
About to compute expected value correlation
About to compute match transform for rotation 269.417723 deg.
About to setup value scanrdg boxes
About to read raster values
About to compute expected value correlation
Expected value distance values are:
0, rot -0.582277: 4219.046222
1, rot 89.417723: 3688.508849
2, rot 179.417723: 4331.774788
3, rot 269.417723: 4944.168545
Chosen rotation 89.417723 deg. as best
About to compute final match transform
Improve match
About to setup value scanrdg boxes
About to read raster values
About to write diag file
Writing output values to file 'chart.ti3'
```

3. Create the icc profile from the ti3 file

```
colprof -v -D"Camera ICC Profile" -qm -am -u chart
```

```
No of test patches = 24
Find white & black points
Picked white patch 1 with dev = 0.27935100 0.28600980 0.24939010
       XYZ = 0.85000000 0.89310000 0.96330000, Lab = 95.709820 -2.083403 -18.008549
Picked black patch 21 with dev = 0.00959229 0.00984690 0.00852039
       XYZ = 0.02650000 0.02780000 0.03120000, Lab = 19.140364 -0.576381 -6.547829
Creating matrix...
 100%
Matrix = 3.706102 -0.144977 -0.054403
         0.079019 3.567243 -0.090599
         0.131569 -0.156201 3.411241
Matrix = 3.706102 -0.144977 -0.054403
         0.079019 3.567243 -0.090599
         0.131569 -0.156201 3.411241
Doing White point fine tune:
Before fine tune, rel WP = XYZ 0.98027074 1.01974611 0.84280877, Lab 100.758545 -0.507479 -0.128723
After fine tune, rel WP = XYZ 0.96420288 1.00000000 0.82490540, Lab 100.000000 -0.000000 0.000000
                 abs WP = XYZ 0.86432998 0.91083529 0.98419015, Lab 96.444428 -2.570642 -18.253553
Dev boundary white XYZ 3.02202924 3.18462964 3.44110639, scale WP by 3.496384, total WP scale 3.496384
Black point XYZ = 0.02966787 0.03136035 0.03361535, Lab = 20.580668 -0.996818 -5.754079
White point XYZ = 3.022029 3.184630 3.441106
Black point XYZ = 0.029668 0.031360 0.033615
Done gamma/shaper and matrix creation
Profile done
Profile check complete, peak err = 6.548814, avg err = 2.195294
```

4. Check quality of the icc file

```
profcheck -v2 -k chart.ti3 chart.icc
```

```
No of test patches = 24
[0.695511] A01: 0.27935100 0.28600980 0.24939010 -> 96.444460 -2.570318 -18.253946 should be 95.709820 -2.083403 -18.008549
[3.708374] B01: 0.04766215 0.06330266 0.10397870 -> 51.936976 -22.050236 -41.417990 should be 49.665474 -27.710625 -39.033197
[0.816741] C01: 0.11433590 0.08515763 0.01223388 -> 59.150234 31.938270 51.003335 should be 60.033014 31.507366 50.238780
[2.582117] D01: 0.10035170 0.13180050 0.11703470 -> 70.879154 -32.511222 -14.414676 should be 70.960456 -34.708567 -10.965818
[0.955407] A02: 0.17899430 0.18376710 0.15854150 -> 81.030912 -2.679262 -15.078656 should be 80.145835 -2.052533 -15.434911
[1.501749] B02: 0.09240834 0.06004796 0.07148322 -> 50.729916 47.894669 -26.090716 should be 49.905921 47.814842 -28.873484
[1.267740] C02: 0.03553294 0.03325528 0.08784781 -> 38.681169 12.854997 -56.198152 should be 39.698119 14.387480 -56.510599
[0.618846] D02: 0.07675619 0.07267465 0.10858220 -> 55.123824 9.820412 -38.674041 should be 55.123802 9.907428 -39.987720
[0.609172] A03: 0.10674880 0.10960690 0.09402302 -> 65.677879 -2.298207 -12.393951 should be 65.223667 -1.953779 -12.764540
[0.747580] B03: 0.18736080 0.18790390 0.02515252 -> 81.891034 -4.632931 73.056738 should be 82.384118 -4.237817 75.643946
[0.786461] C03: 0.09148488 0.05884175 0.03421373 -> 50.358665 46.429488 3.575845 should be 50.108930 45.125286 4.637681
[0.957118] D03: 0.03084334 0.03764189 0.01589858 -> 41.261256 -17.863206 15.039660 should be 42.015463 -17.283533 13.889525
[0.804681] A04: 0.05644580 0.05802685 0.04956443 -> 50.075241 -1.994348 -9.842960 should be 50.310700 -1.549318 -10.569142
[2.354877] B04: 0.07093429 0.03988989 0.01408457 -> 42.299980 53.861531 16.885270 should be 40.064674 52.481836 18.786999
[2.380736] C04: 0.02577725 0.01893710 0.03464128 -> 29.376105 25.088354 -32.328375 should be 31.647019 24.255374 -34.530906
[1.258738] D04: 0.05118002 0.05574878 0.08243329 -> 49.123820 -4.336481 -34.639283 should be 50.061275 -2.846856 -35.942037
[0.882221] A05: 0.02574579 0.02638895 0.02209193 -> 34.813893 -1.377530 -6.924907 should be 34.600020 -1.030339 -7.863544
[0.742719] B05: 0.04710186 0.07168459 0.02523323 -> 55.003903 -44.107048 25.943191 should be 54.438379 -42.705709 25.036105
[0.994880] C05: 0.10902940 0.13415970 0.02737630 -> 71.505633 -29.929837 52.680653 should be 72.074497 -29.110697 49.736048
[2.282542] D05: 0.12106930 0.10694700 0.06484298 -> 65.032114 14.709391 4.102927 should be 65.105195 12.797905 6.107326
[1.317799] A06: 0.00959229 0.00984690 0.00852039 -> 20.580679 -0.996712 -5.754206 should be 19.140364 -0.576381 -6.547829
[1.311532] B06: 0.01960350 0.01603082 0.06550115 -> 26.739965 22.555126 -62.907574 should be 27.709508 23.311589 -61.459356
[1.163927] C06: 0.14742550 0.12750980 0.01750432 -> 70.000667 15.671393 61.651685 should be 71.159530 16.385471 60.223000
[1.754958] D06: 0.03163249 0.02666194 0.01366246 -> 35.004529 12.685915 7.168514 should be 36.593244 11.541665 5.958297
Profile check complete, errors(CIEDE2000): max. = 3.708374, avg. = 1.354018, RMS = 1.555357
```

5. Convert tiff image using the ICC profile

```
cctiff -v -i a chart.icc chart.tiff chart_corrected.tiff
```

```
Possible Output Encodings for output colorspace XYZ are:
1: CIELab (Default)
2: ICCLab
Using default

Input raster file 'chart.tiff' is TIFF
Input TIFF file photometric is RGB
Input raster file ICC colorspace is RGB
Input raster file is 4924 x 7378 pixels
Input raster file description: ''

There are 1 profiles/calibrations in the sequence:

Profile 0 'chart.icc':
Header:
  size         = 3032 bytes
  CMM          = 'argl'
  Version      = 2.2.0
  Device Class = Input
  Color Space  = RGB
  Conn. Space  = XYZ
  Date, Time   = 8 May 2021, 16:37:30
  Platform     = Macintosh
  Flags        = Not Embedded Profile, Use anywhere
  Dev. Mnfctr. = 0x0
  Dev. Model   = 0x0
  Dev. Attrbts = Reflective, Glossy, Positive, Color
  Rndrng Intnt = Relative Colorimetric
  Illuminant   = 0.96420288, 1.00000000, 0.82490540    [Lab 100.000000, 0.000000, 0.000000]
  Creator      = 'argl'

Direction = Forward
Intent = Absolute Colorimetric
Algorithm = MatrixFwd
Input curves being post-converted to L*
Input space = RGB
Output space = XYZ
Output curves being pre-converted from L*
Output curves being combined

Output TIFF file 'chart_corrected.tiff'
Ouput raster file ICC colorspace is Lab
Output TIFF file photometric is CIELab

Using CLUT resolution 33
```
