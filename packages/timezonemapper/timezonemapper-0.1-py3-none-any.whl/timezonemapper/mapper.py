from pytz import timezone

# Dictionary mapping descriptive time zone names to their respective identifiers
TIME_ZONE_MAPPINGS = {
    "Indian Standard Time": "Asia/Kolkata",
    "Eastern Standard Time": "America/New_York",
    "Central European Time": "Europe/Berlin",
    "Pacific Standard Time": "America/Los_Angeles",
    # Add more mappings here as needed
}

class TimeZoneMapper:
    @staticmethod
    def get_timezone(description):
        tz_key = TIME_ZONE_MAPPINGS.get(description)
        if not tz_key:
            raise ValueError(f"Time zone description '{description}' is not recognized.")
        return timezone(tz_key)
