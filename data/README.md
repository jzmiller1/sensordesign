README HERE
===========

All data for Sensor Design app should be saved to this directory.
Data will be read and inserted into the database from this directory.
Additional Material datasets in ASCII format can be obtained from ftp directories at:

http://speclab.cr.usgs.gov/spectral-lib.html

Sample FTP directory (splib06)

ftp://ftpext.cr.usgs.gov/pub/cr/co/denver/speclab/pub/spectral.library/splib06.library/ASCII/

ASCII data must be saved as .txt and must conform to the USGS format.

The data reader is looking for the following specifications:

Line 1 contains source information
Line 15 contains material type
Line 17 first line of data (Full Tab    wavelenght    reflectance     standard deviation)

Example:


Line 1>   USGS Digital Spectral Library splib06a
          Clark and others 2007, USGS, Data Series 231.

          For further information on spectrsocopy, see: http://speclab.cr.usgs.gov

          ASCII Spectral Data file contents:
          metadata
          metadata
          metadata
          metadata

         (standard deviation of 0.000000 means not measured)
         (      -1.23e34  indicates a deleted number)
         ----------------------------------------------------
Line 15> Lawn_Grass GDS91 (Green)     W1R1Ba AREF
         copy of splib05a r 11208
Line 17>        0.205100      -1.23e34        0.000000