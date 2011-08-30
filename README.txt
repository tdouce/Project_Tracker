This python script is meant to help project tracking using Google Maps
as a visualization tool and using Google Docs (spreadsheet) as a quasi database
backend.  The script was built with the scientific community in mind, but I am sure other
applications exist.  

Prequisites:
You will need to download and install the Google Data Python Libraray
http://code.google.com/apis/gdata/articles/python_client_lib.html

Context:
For example, imagine a group of scientists/orginazations sampling 1000 sites
(individual locations) across a wide geographic area during the same time period. 
A problem with the coordination of efforts arises.  Each organization needs to know what sites
each other organization checked the previous day so there is no duplication of
effort and sampling.  This script was written to help reduce duplication and 
smooth the collaboration process using open source tools.

How it works:
A google spreadsheet is used a quasi 'database' backend.  All the sites that are
to be sampled are plugged into the google spreadsheet.  The google spreadsheet HAS to 
be formatted so that the a 'site_id' is the first column, the 'Completed or Not' 
column is the second column, 'Latitude Coordinates' column is the next to last
column and 'Longitude Coordinates' column is the last column. The spelling of the 
column names do not matter, but the index of the columns DO matter.  Other than 
these mentioned columns, there can be as many other columns as you wish. The script 
goes to the google email address, logs in and downloads the spreadsheet as
a csv file. It then parses the columns on the 'completed or not column', and
generates a 'completed' kml and a 'not completed' kml.  It then writes these kmls 
to a server and writes a basic html page that uses these kmls in a google map to display the
information.  The 'completed sites' have a blue pin and the 'sites not
completed' have a red pin. Every column that is listed in the csv will be displayed in the 
'bubble' for each placemark in the google map. There is some javascript on the
html page for toggling the 'completed' and 'not completed' sites.  The google spreadsheet 
should be formated like:

stationid, Completed, Site Name, County, DateStart, DateEnd, Latitude, Longitude
1, y, somename , some county, somedate, somedate, 33.234, -83.4355
2, n, somename , some county, somedate, somedate, 33.334, -83.6355
3, y, somename , some county, somedate, somedate, 33.234, -83.9355
4, n, somename , some county, somedate, somedate, 33.634, -83.3355


The project flow would be as follows:
All the sampling sites are written to the google spreadsheet. All organization
begin sampling. Each organization has access to the gmail email address and password. 
At the end of each day, each organziation updates the column that holds the information 
on whether about whether or not the site'has been completed' or 'has not been completed', i.e.
changing the 'y' to a 'n' (or whatever convention is settled on by all organizations).  
The script should be set to run as a scheduled task on a computer that has writing access 
to the server.  I suggest running the script during the night.  The following
morning an updated and accurate google map is generated, displaying sites that
'have been sampled' and sites that 'have not been sampled'.
