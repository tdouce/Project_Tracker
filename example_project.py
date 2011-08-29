
#############################################
## Variables

# gmail email address here
email = 'emailaddress@gmail.com' 

# password here
password = 'password' 

# Location of folder where the downloaded google spreadsheet (csv) will be saved to
csv_directory = r'C:\Path\to\googleDoc'

# Name of the google doc spreadsheet
spreadsheet_name = 'SpreadSheet_Name'

# The affirmative response in the google spreadsheet if a site has been checked
affirmative_answer = 'y'

# Path to directory where you want to save today's kml for archiving. You don't
# have to do this
outFolderKml = r'C:\Path\to\test_project\Archive'

# Path to root folder on server where the HTML and KML files will be saved to
server_location = r'T:\path\to\somewhere\onwerver\Test'

# URL to project root folder where the kml and shp files can be accessed
httpdownload = 'http://someurl.com/test_project/'

# Google map key
google_map_key = 'ABLKSADLKJASDLFKJvwueQkasdlkjdslfkjdsafljJ594klkdsalfkj8732498-TeELHIZ_4AQ'



###
Test_proj = ProjectTracker(  email, password, spreadsheet_name )

# Get the uri key from google docs
Test_proj.get_uri() 

# Download csv spreadsheet from google spreadsheets
Test_proj.get_spreadsheet( csv_directory ) 

# Parse the csv
Test_proj.parse_csv( affirmative_answer )

# Write kml to archive folder
Test_proj.make_and_save_kml( outFolderKml, timestamp=True )

# Write kml to server
Test_proj.make_and_save_kml( server_location )

# Write html to server 
Test_proj.make_and_save_html( httpdownload, server_location, google_map_key, map_center='auto_generate', map_zoom='9' )



