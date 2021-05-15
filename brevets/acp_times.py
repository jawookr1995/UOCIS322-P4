"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
import math

ACP_METRICS = {200: [15, 34],
               300: [15, 32],
               400: [15, 30],
               600: [11.428, 28],
               1000: [13.333, 26]}

LEEWAY = 1.20


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    new_date = arrow.get(brevet_start_time)     # Initialize arrow object for manipulation.

    if control_dist_km <= 0:                    # Catch values zeros or below.
        return new_date.isoformat()

    if control_dist_km > brevet_dist_km*LEEWAY:  # Skip processing if Control is too large.
        return None

    if brevet_dist_km < control_dist_km <= brevet_dist_km*LEEWAY:
        control_dist_km = brevet_dist_km        # Scale Control to brevet length, if oversizes.

    opening_time = 0    # Initialize a control's opening time.
    for key, value in sorted(ACP_METRICS.items()):
        if control_dist_km <= key:
            opening_time += control_dist_km/value[1]
            break
        elif control_dist_km > key:
            opening_time += 200/value[1]
        control_dist_km = control_dist_km - 200

    to_hour = math.floor(opening_time)
    to_min = round((opening_time - to_hour) * 60)
    return new_date.shift(hours=+to_hour, minutes=+to_min).isoformat()


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
        control_dist_km:  number, the control distance in kilometers
        brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
        brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    new_date = arrow.get(brevet_start_time)

    if control_dist_km <= 0:
        return new_date.shift(hours=+1).isoformat()

    if control_dist_km > brevet_dist_km * LEEWAY:
        return None

    if brevet_dist_km < control_dist_km <= brevet_dist_km * LEEWAY:
        control_dist_km = brevet_dist_km

    temp_control = control_dist_km
    opening_time = 0  # Initialize a control's opening time.
    for key, value in sorted(ACP_METRICS.items()):
        if temp_control <= key:
            opening_time += temp_control/value[0]
            break
        elif temp_control > key:
            opening_time += 200/value[0]
        temp_control = temp_control - 200

    to_hour = math.floor(opening_time)
    to_min = round((opening_time - to_hour) * 60)
    if control_dist_km == 200:
        to_min += 10.0
    return new_date.shift(hours=+to_hour, minutes=+to_min).isoformat()