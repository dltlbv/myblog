from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.utils.functional import SimpleLazyObject
from user_agents import parse
from .models import BrowserStats
from django.core.cache import cache
from django.http import HttpResponseTooManyRequests

from django.conf import settings


class BrowserStatsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        user_agent_data = parse(user_agent)
        browser_name = user_agent_data.browser.family

        stats, created = BrowserStats.objects.get_or_create(browser_name=browser_name)
        if not created:
            stats.visit_count += 1
            stats.save()


class RateLimitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = request.META.get("REMOTE_ADDR")
        cache_key = f"rate_limit_{ip}"
        request_count = cache.get(cache_key, 0)

        if request_count >= 100:
            return HttpResponseTooManyRequests(
                "Слишком много запросов. Попробуйте позже."
            )

        cache.set(cache_key, request_count + 1, timeout=60)


class UnsupportedBrowserMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        user_agent_data = parse(user_agent)
        browser_name = user_agent_data.browser.family

        if browser_name in settings.UNSUPPORTED_BROWSERS:
            response.context_data["browser_warning"] = (
                f"Ваш браузер {browser_name} не поддерживается."
            )

        return response
