"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


def _min_max_time(control_dist_km, is_max):
    dist_list = [0, 200, 400, 600, 1000]
    min_speed_list = [15, 15, 15, 11.428, 13.333]
    max_speed_list = [34, 32, 30, 28, 26]

    for i in range(5):
        if dist_list[i] > control_dist_km:
            break

    ret = 0
    for j in range(i + 1):
        if j != 0:
            prev_dist = dist_list[j - 1]
            if is_max:
                speed = min_speed_list[j - 1]
            else:
                speed = max_speed_list[j - 1]
        else:
            prev_dist = 0
            if is_max:
                speed = min_speed_list[0]
            else:
                speed = max_speed_list[0]
        if j < i:
            if is_max:
                ret += (dist_list[j] - prev_dist) / speed
            else:
                ret += (dist_list[j] - prev_dist) / speed
        else:
            if is_max:
                ret += (control_dist_km - prev_dist) / speed
            else:
                ret += (control_dist_km - prev_dist) / speed

    return ret


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

    dt = arrow.get(brevet_start_time)
    total_time = _min_max_time(control_dist_km, False)
    dt = dt.shift(hours=total_time)
    return dt.isoformat()


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
    dt = arrow.get(brevet_start_time)
    total_time = _min_max_time(control_dist_km, True)
    dt = dt.shift(hours=total_time)
    return dt.isoformat()
