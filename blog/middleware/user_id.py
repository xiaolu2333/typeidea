import uuid

USER_KEY = "uid"
TEN_YEARS = 60 * 60 * 24 * 365 * 10


class UserIDMiddleware:
    def __init__(self, get_response):
        """One-time configuration and initialization."""
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        """Code to be executed for each request before the view (and later middleware) are called."""
        uid = self.generate_uid(request)
        request.uid = uid
        response = self.get_response(request)
        response.set_cookie(USER_KEY, uid, max_age=TEN_YEARS, httponly=True)
        return response

    def generate_uid(self, request):
        try:
            # print(request.COOKIES)
            uid = request.COOKIES[USER_KEY]
            # print('已存在的uid:', uid)
        except KeyError:
            uid = uuid.uuid4().hex
        return uid
