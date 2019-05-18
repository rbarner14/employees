# -*- coding: utf-8 -*-
import json 
# import httplib2 # Imported to make HTTP requests.
import requests

# Imported to enable non-ascii characters (non-English language) to render 
# properly in code.
# import sys
# import codecs
# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)

import os

# API Keys
foursquare_client_id = os.environ.get('FORSQUARE_CLIENT_ID')
foursquare_client_secret = os.environ.get('FORSQUARE_CLIENT_SECRET')
google_api_key = os.environ.get('GOOLE_API_KEY')

# Geocode location (return coordinates of a location) by passing in search 
# string and creating a Google API GET request.
def getGeocodeLocation(inputString):
    #Replace spaces in argument passed in as search string with '+' in URL.
    locationString = inputString.replace(" ", "+")
    # Google URL (Uniform Resource Locator); web address, web resource.
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'% (locationString, google_api_key))
    # print(url) 
    # Create Http Class instance and name this object 'h'. 
    # h = httplib2.Http()
    # h.request(url,'GET') is a get request on the URL passed in.  The response
    # is a list of 2 items: the first, the status code & message, the 2nd, is
    # the requested info.  This is then jsonified with the loads method imported
    # from the json library and stored as the variable "result".
    # result = json.loads(h.request(url,'GET')[1])

    # or with: 
    result = requests.get(url).json()

    # The json result is parsed for the data we need: lat & lng.
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    # print(latitude,longitude) 
    # Latitude and longitude are returned as a tuple.
    return (latitude,longitude) 

# This function takes in a string representation of a location and cuisine type, 
# geocodes the location, and then passes in the latitude and longitude 
# coordinates to a string that becomes the Foursquare API GET request.
def findAVenue(features, location):

    # Parse tuple resulting from the return value of the getGeocodeLocation
    # function with the location of search passed into it called.  Bind 
    # latitude to the first item in tuple and longitude to the 2nd.
    latitude, longitude = getGeocodeLocation(location)
    # Create URL with latitude, longitude, API keys and features.
    url = (f'https://api.foursquare.com/v2/venues/search?client_id={foursquare_client_id}&client_secret={foursquare_client_secret}&v=20190513&ll={latitude},{longitude}&features={features}')
    # h = httplib2.Http()
    # result = json.loads(h.request(url, 'GET')[1])

    result = requests.get(url).json()

    # Return restaurant info diction if a restaurant that matches search exists;
    # return "No Restaraunts Found" otherwise.
    if result['response']['venues']:
        # Grab the first venue, its id, name and address.
        venue = result['response']['venues'][0]
        venue_id = venue['id']
        venue_name = venue['name']
        venue_address = venue['location']['formattedAddress']
        # Format the Venue Address into one string.
        address = ""

        for i in venue_address:
            address += i + " "

        venue_address = address
        
        # Get a  300x300 picture of the venue using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
        url = (f'https://api.foursquare.com/v2/venues/{venue_id}/photos?client_id={foursquare_client_id}&v=20190513&client_secret={foursquare_client_secret}')
        # result = json.loads(h.request(url, 'GET')[1])

        result = requests.get(url).json()
        
        # Grab the first image.
        # If no image available, insert default image url.
        if result['response']['photos']['items']:
            firstpic = result['response']['photos']['items'][0]
            prefix = firstpic['prefix']
            suffix = firstpic['suffix']
            imageURL = prefix + "300x300" + suffix
        else:
            imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"

        venueInfo = {'name': venue_name,
                     'address': venue_address,
                     'image': imageURL}
        # print "Venue Name: %s " % venueInfo['name']
        # print "Venue Address: %s " % venueInfo['address']
        # print "Image: %s \n " % venueInfo['image']
        print(venueInfo)
        return venueInfo
    else:
        # print "No Restaurants Found for %s" % location
        return "No Restaurants Found"


###############################################################################
# Enable running at command line.
if __name__ == '__main__':
    findAVenue('13', "Tokyo, Japan")
    findAVenue('13', "San Francisco, CA")
    findAVenue('13', "Los Angeles, CA")
    findAVenue('13', "Seattle, WA")
    findAVenue('13', "San Juan, Puerto Rico")




