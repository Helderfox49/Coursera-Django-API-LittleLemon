from rest_framework.throttling import UserRateThrottle

class TenCallsPerMinute(UserRateThrottle):
    scope = 'ten_calls_per_minute'
    rate = '10/days'