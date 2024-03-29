def simple(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        print("middle", request.META["HTTP_ORIGIN"])
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
