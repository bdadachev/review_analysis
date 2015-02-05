from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

import json
import geopy.distance
import operator

import datawrapper

#############
# Home page #
#############
def home(request):
    return render(request, "review_analyzer/index.html")

@csrf_exempt
def validate_coordinates(request):
    """
    Function ensuring that the coordinates the user wants to display on the map
    are nearby known restaurants (i.e., restaurants from the dataset).
    """
    try:
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        
        latitude = float(latitude)
        assert(-180. <= latitude <= 180.)
        longitude = float(longitude)
        assert(-180. <= longitude <= 180.)       
    except:
        return HttpResponseServerError("Incorrect or illegal arguments.") 
    # OLD - fyi, the cities in the dataset are:
    #availableCities = [
    #    ("Phoenix", ("33.4500", "-112.0667")),
    #    ("Las Vegas", ("36.1215", "-115.1739")),
    #    ("Madison", ("43.0667", "-89.4000")),
    #    ("Waterloo", ("43.4667", "-80.5167")),
    #    ("Edimburgh", ("55.9531", "-3.1889")),
    #]
    maxDistance = 20 # in miles
    acceptLocation = datawrapper.find_restaurant_in_radius(latitude, longitude, maxDistance)
    response = {"acceptLocation": acceptLocation, "maxDistance": maxDistance}
    return HttpResponse(json.dumps(response))



##############
# About page #
##############
def about(request):
    return render(request, "review_analyzer/about.html")



###################
# Restaurant page #
###################
def restaurant_by_hash(request, hash):
    def clean_address(address):
        import re
        # replace all but last '\n' by a comma, to make sure the address fits on two lines
        return re.sub(r"\n(?=.*\n)", ", ", address)
    def get_short_address(address):
        # returns city, post code and state
        return address.split('\n')[-1]
    #print "RECEIVED HASH", hash
    if not datawrapper.is_valid_restaurant(hash):
        return render(request, "review_analyzer/404.html") # to do properly
    info = datawrapper.get_restaurant_information(hash)
    trendValues = {0: "stable", -1: "decreasing", 1: "increasing"}
    trend = "Ratings are {} over the last {} months.".format(trendValues[info["rating_trend"]["trend"]], info["rating_trend"]["months"])
    topics = sorted(info["predicted_topics"].items(), key=operator.itemgetter(1), reverse=True)
    topicIndices = zip(*topics)[0]
    topicLabels = datawrapper.get_topic_labels(topicIndices[:5]) # keep top 5? keep 50% of cumulated proba?
    print info["mean_rating"], type(info["mean_rating"])
    statsRadius = 5
    statsNbRestaurants, stats = datawrapper.compute_restaurant_statistics(hash, statsRadius)
    roundedRating = round(info["mean_rating"] * 2) / 2
    nbFullStars = int(roundedRating)
    nbHalfStars = int(nbFullStars != roundedRating)
    nbEmptyStars = 5 - nbFullStars - nbHalfStars
    timeLabels, trendData = datawrapper.get_restaurant_ratings(hash)
    context = {
            "id": hash,
            "name": info["name"],
            "city": info["city"],
            "state": info["state"],
            "categories": info["categories"],
            "predicted_categories": info["predicted_categories"],
            "avg_rating": round(info["mean_rating"], 1),
            "nb_ratings": info["review_count"],
            "address": clean_address(info["full_address"]),
            "short_address": get_short_address(info["full_address"]),
            "latitude": info["longlat_location"][1], #info["latitude"],
            "longitude": info["longlat_location"][0], #info["longitude"],
            "trend": trend,
            "topics": topicLabels,
            "stats": stats,
            "stats_nb_restaurants": statsNbRestaurants,
            "stats_radius": statsRadius,
            "nbFullStars": nbFullStars,
            "nbHalfStars": nbHalfStars,
            "nbEmptyStars": nbEmptyStars,
            "time_labels": timeLabels,
            "trend_data": json.dumps(trendData),
        }
    return render(request, "review_analyzer/restaurant.html", context)

@csrf_exempt
def regional_statistics(request):
    try:
        hash = request.POST.get('hash')
        radius = float(request.POST.get('radius'))
    except:
        return HttpResponseServerError("Incorrect or illegal arguments.")
    if not datawrapper.is_valid_restaurant(hash):
        return HttpResponseServerError("Incorrect or illegal arguments.")

    stats = datawrapper.compute_restaurant_statistics(hash, radius)
    return HttpResponse(json.dumps(stats))

@csrf_exempt
def ratings(request):
    try:
        hash = request.POST.get('hash')
        time = request.POST.get('time')
    except:
        return HttpResponseServerError("Incorrect or illegal arguments.")
    if not datawrapper.is_valid_restaurant(hash):
        return HttpResponseServerError("Incorrect or illegal arguments.")

    ratings = datawrapper.get_restaurant_ratings_for_time(hash, time)
    return HttpResponse(json.dumps(ratings))



###################
# Restaurant page #
###################
def location(request, address):
    try:
        latitude = request.GET.get('lat')
        longitude = request.GET.get('lng')
    except:
        return HttpResponseServerError("Incorrect or illegal arguments.")

    #print "lat/lng: {}/{}".format(latitude, longitude)

    # here, we should check the values of lat/lng are valid coordinates
    if latitude is None or longitude is None:
        return HttpResponseServerError("Incorrect or illegal arguments.")
    # ..more checks to do...
    
    context = {
        "address": address,
        "latitude": latitude,
        "longitude": longitude,
    }
    return render(request, "review_analyzer/location.html", context)

@csrf_exempt
def get_restaurants_on_map(request):
    try:
        # get arguments and check their validity
        northEastLatitude = request.POST.get("northEastLatitude")
	northEastLongitude = request.POST.get("northEastLongitude")
        southWestLatitude = request.POST.get("southWestLatitude")
	southWestLongitude = request.POST.get("southWestLongitude")
        #
        northEastLatitude = float(northEastLatitude)
        northEastLongitude = float(northEastLongitude)
        southWestLatitude = float(southWestLatitude)
        southWestLongitude = float(southWestLongitude)
        #
        assert(-180. <= northEastLatitude <= 180.)
        assert(-180. <= northEastLongitude <= 180.)
        assert(-180. <= southWestLatitude <= 180.)
        assert(-180. <= southWestLongitude <= 180.)
        # check relation between the 4 variables?

	# nb:	
	# selectedCategories == ["Barbeque", ...]: search only BBQ, ... restaurants
	# selectedCategories == None: search all categories
	selectedCategories = json.loads(request.POST.get("categoryFilters"))
	print "selectedCategories", selectedCategories
    except:
        return HttpResponseServerError("Incorrect or illegal arguments.")

    print "Get rest on maps: {}/{}, {}/{}".format(
        northEastLatitude, northEastLongitude, southWestLatitude, southWestLongitude
    )

    # shrinking box to avoid displaying restaurants near the sides of the map
    deltaLatitude = abs(northEastLatitude - southWestLatitude)
    deltaLongitude = abs(northEastLongitude - southWestLongitude)
    # remove 10% on all four sides - to check: might this break somehow?
    if northEastLatitude > southWestLatitude:
        northEastLatitude -= deltaLatitude / 10.
        southWestLatitude += deltaLatitude / 10.
    else:
        southWestLatitude -= deltaLatitude / 10.
        northEastLatitude += deltaLatitude / 10.
    if northEastLongitude > southWestLongitude:
        northEastLongitude -= deltaLongitude / 10.
        southWestLongitude += deltaLongitude / 10.
    else:
        southWestLongitude -= deltaLongitude / 10.
        northEastLongitude += deltaLongitude / 10.    

    #print "Get rest on maps, after shrinking: {}/{}, {}/{}".format(
    #    northEastLatitude, northEastLongitude, southWestLatitude, southWestLongitude
    #)    

    restaurants, nbRestAfterFilter = datawrapper.get_restaurants_in_box(
        northEastLatitude, northEastLongitude, 
	southWestLatitude, southWestLongitude,
	selectedCategories
    )  
    #print "Found {} restaurants inside box".format(len(restaurants))
  
    return HttpResponse(json.dumps([restaurants, nbRestAfterFilter], ensure_ascii=False).encode("utf8"))

###############
# Error pages #
###############
def error404(request):
    context = {
        "error_message": "<h2>404: Page not found</h2> Sorry, the page you are looking for does not exist. Please check the URL and try again!",
    }
    return render(request, 'review_analyzer/error.html', context, status=404)
def error500(request):
    context = {
        "error_message": "<h2>500: Mayday, mayday!</h2> Sorry, we have had a problem, we have been notified and are working hard to fix this!",
    }
    return render(request, 'review_analyzer/error.html', context, status=500)
