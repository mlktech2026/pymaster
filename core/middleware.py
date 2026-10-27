from django.utils import timezone

class PageViewMiddleware:
    """
    Middleware that silently records visitor page views for visual analytics.
    Excludes static assets, media files, and internal background endpoints.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        path = request.path
        # Exclude static files, media uploads, internal API run polling, favicon, and admin assets
        ignored_prefixes = (
            '/static/',
            '/media/',
            '/favicon.ico',
            '/robots.txt',
            '/practice/run/',
        )
        
        if not any(path.startswith(prefix) for prefix in ignored_prefixes) and response.status_code == 200:
            try:
                from core.models import PageView
                
                user = request.user if request.user.is_authenticated else None
                ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
                if ip:
                    ip = ip.split(',')[0].strip()
                ua = request.META.get('HTTP_USER_AGENT', '')[:250]
                referer = request.META.get('HTTP_REFERER', '')[:290]
                session_key = request.session.session_key or ''

                PageView.objects.create(
                    path=path[:250],
                    user=user,
                    ip_address=ip if ip else None,
                    user_agent=ua,
                    referer=referer,
                    session_key=session_key
                )
            except Exception:
                # Middleware should never disrupt request execution
                pass

        return response
