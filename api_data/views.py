from django.http import JsonResponse
from django.shortcuts import render

from .models import Hotel, City


def get_cities(request):
    """
    API endpoint to get all cities

    Args:
        request: The HTTP request object

    Returns:
        JsonResponse: a JSON with all the potential cities
    """

    cities =City.objects.all().values_list('name', flat=True).order_by('name')

    return JsonResponse(list(cities), safe=False)


def hotel_search(request):
    """
    API endpoint to get all hotels for a certain city. The city is passed in the query param.

    Args:
        request: The HTTP request object, including the query param

    Returns:
        HttpResponse: An HTTP response object that renders the 'api_data/hotel_search.html' template,
        that includes a list of hotels that was found for the city
    """

    # Get the city from the query param and remove possible trailing spaces
    query = request.GET.get('city', '').strip()

    # If no city was sent (it is an empty string), return no hotels
    if not query:
        context = {
            'query': query,
            'hotels_in_city': [],
        }

    else:
        # Filter the Hotels based on the city that was passed.
        # Search for an exact match but case-insensitive (hence the iexact filter)
        hotels_in_city = Hotel.objects.filter(city__name__iexact=query).select_related('city')

        # Filter in the template using the query
        context = {
            'query': query,
            'hotels_in_city': hotels_in_city,
        }

    return render(request, 'api_data/hotel_search.html', context)
