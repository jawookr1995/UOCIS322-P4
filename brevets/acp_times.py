"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#
Max_ctrl = 1.20
B_TABLE = [(200,15,34),(400,15,32),(600,15,30),(1000,11.428,28),(1300,13.333,26)]

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  A date object (arrow)
    Returns:
       A date object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    # Initialize arrow object for manipulation.
    new_date = arrow.get(brevet_start_time)

    # Catch values zeros or below.
    if control_dist_km <= 0:
        return new_date.isoformat()

    # Skip processing if Control is too large.
    if control_dist_km > brevet_dist_km * Max_ctrl:
        return None

    # Scale Control to brevet length, if oversizes.
    if brevet_dist_km < control_dist_km <= brevet_dist_km * Max_ctrl:
        control_dist_km = brevet_dist_km

    # Initialize a control's opening time.
    opening_time = 0
    for key, value in sorted(B_TABLE.items()):
        if control_dist_km <= key:
            opening_time += control_dist_km / value[1]
            break
        elif control_dist_km > key:
            opening_time += 200 / value[1]
        control_dist_km = control_dist_km - 200

    to_hour = math.floor(opening_time)
    to_min = round((opening_time - to_hour) * 60)
    return new_date.shift(hours=+to_hour, minutes=+to_min).isoformat()

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  A date object (arrow)
    Returns:
       A date object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    new_date = arrow.get(brevet_start_time)

    if control_dist_km <= 0:
        return new_date.shift(hours=+1).isoformat()

    if control_dist_km > brevet_dist_km * Max_ctrl:
        return None

    if brevet_dist_km < control_dist_km <= brevet_dist_km * Max_ctrl:
        control_dist_km = brevet_dist_km

    temp_control = control_dist_km
    opening_time = 0  # Initialize a control's opening time.
    for key, value in sorted(B_TABLE.items()):
        if temp_control <= key:
            opening_time += temp_control / value[0]
            break
        elif temp_control > key:
            opening_time += 200 / value[0]
        temp_control = temp_control - 200

    to_hour = math.floor(opening_time)
    to_min = round((opening_time - to_hour) * 60)
    if control_dist_km == 200:
        to_min += 10.0
    return new_date.shift(hours=+to_hour, minutes=+to_min).isoformat()
