from django.shortcuts import render

from .models import Hotel


def hotel_search(request):
    """
    Search for hotels based on the city that is passed in the query param.

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
