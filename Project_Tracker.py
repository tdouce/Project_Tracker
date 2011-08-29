
import gdata,gdata.docs.service,gdata.spreadsheet.service, os, re, csv, datetime, sys
import pdb

class ProjectTracker:

    def __init__(self, email, password, spreadsheet_name ):

        """
        email - The gmail address 
        password - Password for gmail address
        spreadsheet_name - Name of the spreadsheet that you want to operate on.
        Has to be spelled exactly as it appears in google docs.
        """

        self.email = email
        self.password = password
        self.spreadsheet_name = spreadsheet_name

    def get_uri( self ):

        """
        Summary: Get uri number from google spreadsheets for the name of spreadsheet we
        passed in.
        """

        self.entry = ''

        gd_client = gdata.docs.service.DocsService(source="test")
        gd_client.ClientLogin( self.email, self.password)

        q = gdata.docs.service.DocumentQuery(categories=['spreadsheet'])
        feed = gd_client.Query(q.ToUri())

        if not feed.entry:
            print 'No entries in feed.'
        else:
            for entry in feed.entry:
                document_title = entry.title.text.encode('UTF-8')
                if document_title == self.spreadsheet_name:
                    self.entry = entry.resourceId.text


    def get_spreadsheet( self, csv_directory ):

        """
        Summary: Downnload spreadsheet and save it locally

        csv_directory - Path to the directory where the csv will be saved
        locally

        """

        self.file_path = os.path.join(csv_directory, self.spreadsheet_name + '.csv')

        # logging into google docs
        gd_client = gdata.docs.service.DocsService(source="test")
        gd_client.ClientLogin( self.email, self.password)

        print 'Retrieving CSV file'

        # Gets the spreadsheet objects
        spreadsheets_client = gdata.spreadsheet.service.SpreadsheetsService()
        spreadsheets_client.ClientLogin(self.email, self.password)

        # substitute the spreadsheets token into our gd_client
        docs_auth_token = gd_client.GetClientLoginToken()
        gd_client.SetClientLoginToken(spreadsheets_client.GetClientLoginToken())

        # export csv
        gd_client.Export(self.entry, self.file_path)

        # reset the DocList auth token
        gd_client.SetClientLoginToken(docs_auth_token)

        print 'Saving csv file'

    def parse_csv( self, yes_answer ):

        """
        Parse the csv file for 'completed' and 'not complted' sites

        'yes_answer' - The affirmative response as it appears in google docs spreadsheet that
        indicates a site has been completed.

        """

        self.forKml = []
        self.headers = []
        self.yes_answer = yes_answer 
        self.doneSites = 'doneSites'
        self.notDoneSites = 'notDoneSites'

        coordFileToList = [ line for line in csv.reader(open( self.file_path)) ]

        self.headers = coordFileToList[0]
        del coordFileToList[0]

        done = [ line for line in coordFileToList if self.yes_answer == line[1] ]
        done.insert( 0, [ self.doneSites ] )

        notDone = [ line for line in coordFileToList if self.yes_answer != line[1] ]
        notDone.insert( 0, [ self.notDoneSites ] )
        
        self.forKml = [done] + [notDone]

    def make_and_save_kml( self, outFolderKml, timestamp=None ):

        """
        Make and save the kml for 'completed sites' and 'not completed sites'

        'outFolderKml' - Location where you are going to save the kml

        'timestamp' - Optinal argument that will append a date stamp to the kml
        file name. If you want a timestamp appended to the file name then pass
        in:

            timestamp=True

        """

        print 'Generating KML'

        self.today = ''
        self.lat_holder = []
        self.long_holder = []
        self.number_done = []
        self.number_notdone = []

        self.today = datetime.datetime.now()

        for kml in self.forKml:
            
            fileName = kml[0][0]

            if timestamp == True:
                fileName = fileName + self.today.strftime("_%Y_%m_%d")
 
            
            output_kml_path = os.path.join( outFolderKml, fileName + '.kml' )
           
            f = open( output_kml_path ,'w')

            f.write(
"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<name>%s.kml</name>
<Style id="sn_red-circle">
        <IconStyle>
                <scale>1.1</scale>
                <Icon>
                        <href>http://maps.google.com/mapfiles/kml/paddle/red-circle.png</href>
                </Icon>
                <hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
        </IconStyle>
        <ListStyle>
                <ItemIcon>
                        <href>http://maps.google.com/mapfiles/kml/paddle/red-circle-lv.png</href>
                </ItemIcon>
        </ListStyle>
</Style>
<StyleMap id="msn_red-circle">
        <Pair>
                <key>normal</key>
                <styleUrl>#sn_red-circle</styleUrl>
        </Pair>
        <Pair>
                <key>highlight</key>
                <styleUrl>#sh_red-circle</styleUrl>
        </Pair>
</StyleMap>
<Style id="sh_red-circle">
        <IconStyle>
                <scale>1.3</scale>
                <Icon>
                        <href>http://maps.google.com/mapfiles/kml/paddle/red-circle.png</href>
                </Icon>
                <hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
        </IconStyle>
        <ListStyle>
                <ItemIcon>
                        <href>http://maps.google.com/mapfiles/kml/paddle/red-circle-lv.png</href>
                </ItemIcon>
        </ListStyle>
</Style>
<Style id="sn_blu-circle">
        <IconStyle>
                <scale>1.1</scale>
                <Icon>
                        <href>http://maps.google.com/mapfiles/kml/paddle/blu-circle.png</href>
                </Icon>
                <hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
        </IconStyle>
        <ListStyle>
                <ItemIcon>
                        <href>http://maps.google.com/mapfiles/kml/paddle/blu-circle-lv.png</href>
                </ItemIcon>
        </ListStyle>
</Style>
<StyleMap id="msn_blu-circle">
        <Pair>
                <key>normal</key>
                <styleUrl>#sn_blu-circle</styleUrl>
        </Pair>
        <Pair>
                <key>highlight</key>
                <styleUrl>#sh_blu-circle</styleUrl>
        </Pair>
</StyleMap>
<Style id="sh_blu-circle">
        <IconStyle>
                <scale>1.3</scale>
                <Icon>
                        <href>http://maps.google.com/mapfiles/kml/paddle/blu-circle.png</href>
                </Icon>
                <hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
        </IconStyle>
        <ListStyle>
                <ItemIcon>
                        <href>http://maps.google.com/mapfiles/kml/paddle/blu-circle-lv.png</href>
                </ItemIcon>
        </ListStyle>
</Style> """ % fileName )

            for index, mark in enumerate(kml):

                if index == 0:
                    continue
                    
                coords = mark[-2:]
                lat = coords[1]
                long = coords[0]


                f.write(
                '<Placemark>\n'
                '<name>id%s</name>\n' % (mark[0]) 
                )

                f.write('<description>')
                
                counter = 0
                for header in self.headers:
                    
                    f.write(
                        '<p> <b>%s</b> : %s </p>' % (self.headers[counter],mark[counter])
                        )
                        
                    counter += 1
                
                f.write('</description>')

                if mark[1] != self.yes_answer:
                    f.write('<styleUrl>#msn_red-circle</styleUrl> \n')
                    self.number_done.append( mark[1])
                else:
                    f.write('<styleUrl>#msn_blu-circle</styleUrl> \n')
                    self.number_notdone.append( mark[1])

                f.write(
                    '<Point>\n' + 
                            '<coordinates>%s,%s,0</coordinates>\n' % (lat,long) +
                    '</Point>\n'
                    '</Placemark>\n'
                    )


                self.lat_holder.append( lat )
                self.long_holder.append( long )


            f.write('</Document>\n'
                    '</kml>\n'
                    )
            
            f.close()



    def make_and_save_html( self, httpdownload, server_location, google_map_key, **kwargs  ):

        """
        httpdownload - Url location to the root directory on the server where the
        kml and html will be located. For example:

            httpdownload = 'http://somecompany.com/mappingProject/'


        server_location - File path to the root directory on the server where
        the kml and html file will be saved. For example:

            server_location = 'T:\Some\Location'

        google_map_key - The google map key for your site. For example:

            google_map_key = 'AlaksdflkjASDFGASSDFlkasdfoijqlkasdflkj@$#%$#SADFZ_4AQ'

        map_center - The latitude and longitude coordinate where your map will
        be centered.  You can pass in a latitude and logitude or you can pass
        in 'auto_generate' and the map's center will be automatically
        generated. For example:

            if you want to have the map center auto generated:

                map_center='auto_generate'

            if you want to pass in a specific map center

                map_center='-81.2345, 31.4325'

        map_zoom - The zoom level for the map.  If you do not include a
        map_zoom then the default zoom will be '9'. For example:

            map_zoom=6



        """

        print 'Making html'


        if kwargs.has_key('map_center') and kwargs['map_center'] == 'auto_generate':

            lat_integers = [ float(lat) for lat in self.lat_holder ]
            long_integers = [ float(long) for long in self.long_holder ]

            max_lat = max(lat_integers)
            min_lat = min(lat_integers)
            max_long = max(long_integers)
            min_long = min(long_integers)

            extent_lat = [ max(lat_integers), min(lat_integers), min(lat_integers), max(lat_integers)]
            extent_long = [ min(long_integers), min(long_integers), max(long_integers), max(long_integers) ]

            lat = sum( extent_lat )/ len(extent_lat)
            long = sum( extent_long )/len(extent_long)

            map_center = str(long) + ',' + str(lat)

        elif kwargs.has_key('map_center'):
            map_center = kwargs['map_center']

        else:

            print 'Please enter a map center'
            sys.exit(1)


        if kwargs.has_key('map_zoom'):
            map_zoom = kwargs['map_zoom']
        else:
            map_zoom = 9


        yourfile = open("%s\%s.html" % ( server_location, self.spreadsheet_name ),"w")

        self.spreadsheet_name = self.spreadsheet_name.replace('_',' ')

        yourfile.write("""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml">
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8"/>
<meta http-equiv="expires" content="Sat, 01 Jan 2011 1:00:00 GMT"/>
<title>%s</title>

<style type="text/css">
#map_canvas {width: 800px; height: 800px; float:left; border: 1px solid black;}
.status_box_number {width: 80px; text-align: center; }
#status_box {background:white; position:absolute; z-index: 100; top:790px; left: 10px;}
</style>
        
<!-- Working API code. You will have to get a unique Google API key for your site.  Get this at http://code.google.com/apis/maps/signup.html-->
<script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=%s" type="text/javascript"></script>
          
<script type="text/javascript">
var map;  // declare map variable
var notDoneKml; // declare notDoneKml variable
var PopulatedPlaces;  // declare PopulatedPlaces variable
var toggleStatedoneKml = 0;  // declare variable and Set toggle state
var toggleStatenotDoneKml = 0;  // declare variable and Set toggle state
        
    function initialize() {
      if (GBrowserIsCompatible()) {
        doneKml = new GGeoXml("%s"); // link to kml, converted from a shapefile 
        notDoneKml =  new GGeoXml("%s"); // link to kml, converted from a shapefile
 
        // Map Controls
        map = new GMap2(document.getElementById("map_canvas")); // Google API code: generates map canvas
        map.setCenter(new GLatLng(%s), %s); // Google API code: sets center of map and zoom in/out scale
        map.setUIToDefault();  // Google API code: generates the zoom in/out scale bar
        map.addControl(new GOverviewMapControl()); // Google API code: generates the setin map in lower right hand corner
        map.addOverlay(doneKml); // Google API code: tells the browser to have the doneKml layer displayed when page is rendered
        map.addOverlay(notDoneKml); // Google API code: tells the browser to have the doneKml layer displayed when page is rendered
      }
    }

    function toggledoneKml() {			// Toggle function for doneKml layer
      if (toggleStatedoneKml == 0) {
        map.removeOverlay(doneKml);
        toggleStatedoneKml = 1;
      } else {
        map.addOverlay(doneKml);
        toggleStatedoneKml = 0;
      }
    }
                
        function togglenotDoneKml() {			// Toggle function for notDoneKml layer
      if (toggleStatenotDoneKml == 0) {
        map.removeOverlay(notDoneKml);
        toggleStatenotDoneKml = 1;
      } else {
        map.addOverlay(notDoneKml);
        toggleStatenotDoneKml = 0;
      }
    }
                
</script>

</head>
<body onload="initialize()"> """  % ( self.spreadsheet_name,
                                      google_map_key,
                                      httpdownload + '/' + self.doneSites + '.kml',
                                      httpdownload + '/' + self.notDoneSites + '.kml',
                                      map_center, 
                                      str(map_zoom), 
                                    ))

        yourfile.write("""
<h1>%s</h1>
<p> Last Updated On: %s </p>
<div id="status_box">
<table border="1">
    <tr>
        <td><img src="http://maps.google.com/mapfiles/kml/paddle/red-circle.png" align="middle" width="32" height="32"/></td>
        <td><b>Sites NOT Completed</b></td>
        <td class="status_box_number" ><big><b>%s</b></big></td>
    </tr>
    <tr>
        <td><img src="http://maps.google.com/mapfiles/kml/paddle/blu-circle.png" align="middle" width="32" height="32"/></td>
        <td><b>Sites Completed</b></td>
        <td class="status_box_number"><big><b>%s</b></big></td>
    </tr>
</table>
</div>

<div id="map_canvas" ></div>
                <br clear="all"/>
                <br/>
                <input type="button" value="Sites that are completed" onClick="toggledoneKml();"/> <!-- Assign function call to button -->
                <input type="button" value="Site that are not completed" onClick="togglenotDoneKml();"/>  <!-- Assign function call to button -->
                <br/>
                <br/>
                <a href="%s.kml" target="_blank">Download Sites Completed KML file</a>
                <br/>
                <a href="%s.kml" target="_blank">Download Sites Not Completed KML file</a>
        </body>
        </html>	
""" %   (
        self.spreadsheet_name,
        self.today.strftime("%Y-%m-%d"),
        len(self.number_done), 
        len(self.number_notdone),
        httpdownload + self.doneSites,
        httpdownload + self.notDoneSites,
        ))


        yourfile.close()




