def accept_routing_middleware(get_response):
    def middleware(request):
        if request.META['HTTP_ACCEPT'] in ['application/activity+json', 'application/ld+json; profile="https://www.w3.org/ns/activitystreams"']:
            request.urlconf = 'misaca_federation.routes.activitypub_urls'

        response = get_response(request)
        return response
    return middleware