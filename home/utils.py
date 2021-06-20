from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        try:
            if isinstance(response.data['detail'], list):
                response.data['detail'] = ",\n".join(response.data['detail'])
        except:
            pass

    return response
