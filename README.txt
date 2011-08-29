This python script is meant to help project tracking  using Google Maps
as a visualization tool and using Google Docs (spreadsheet) as a quasi database
backend.

The script was built with the scientific community in mind, but I am sure other
applications exist.  

For example, imagine a group of scientists/orginazaions daily sampling 1000 sites
(individual locations) across a wide geographic area. The problem that arises
is the coordinating of efforts.  Each organization needs to know what sites
each other organization checked the previous day so that there is no duplication of effort
This script was written to help reduce duplication and smooth the process using
free tools.

A google spreadsheet is used a quasi 'database' backend.  All the sites that
need to be sampled are plugged into the google spreadsheet.  The google spreadsheet has to 
be formatted so that the a 'site_id' is the first column, the 'Completed or Not' 
column is the second column, Latitude coordinate column is the next to last
column and longitude coordinate column is the last column. The spelling of the 
column names do not matter, but in the index of the column DOES matter.  Other than 
these mentioned columns, there can be as many other columns as you wish.  For example:

stationid, Completed, Site Name, County, DateStart, DateEnd, Latitude, Longitude
1, y, somename , some county, somedate, somedate, 33.234, -83.4355
2, n, somename , some county, somedate, somedate, 33.334, -83.6355
3, y, somename , some county, somedate, somedate, 33.234, -83.9355
4, n, somename , some county, somedate, somedate, 33.634, -83.3355

The project flow would be as follows:
Each organization has access to the email address and password and 
at the end of each day, each organziation updates the column that holds the information 
on whether or  the site'has been completed' or 'has not been completed', i.e.
changing the 'y' to a 'n', or whatever convention is settled on. 
The script could be set as a scheduled task and run during the night. The
script would go to the google email address, login, download the spreadsheet as
a csv file, parse the columns on the 'completed or not column', generate a
'completed' kml and a 'not completed' kml.  Writes these kmls to a server and
write a basic html page that uses these kmls in the google map to display the
information.  Every column that is listed in the csv will be displayed in the 
'bubble' for each placemark in the google map. There is some javascript so you 
can toggle the 'completed' and 'not completed' sites.
