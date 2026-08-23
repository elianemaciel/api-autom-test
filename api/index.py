from urllib.parse import parse_qs

from run import app as flask_app


# Vercel's Python runtime looks for a WSGI-compatible variable.
class VercelPathMiddleware:
    def __init__(self, wrapped_app):
        self.wrapped_app = wrapped_app

    def __call__(self, environ, start_response):
        query_params = parse_qs(environ.get('QUERY_STRING', ''))
        rewritten_path = query_params.get('path', [None])[0]

        if rewritten_path:
            environ['PATH_INFO'] = rewritten_path

        return self.wrapped_app(environ, start_response)


app = VercelPathMiddleware(flask_app)
handler = app
