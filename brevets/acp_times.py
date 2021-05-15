"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow



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

    speed_dic = {"0": 34, "200": 34, "400": 32, "600": 30, "1000": 28, "1300": 26}
    time_dic = {"0": 0, "200": 200 / 34, "400": 100 / 32, "600": 200 / 30, "1000": 400 / 28, "1300": 300 / 26}
    control_point = [0, 200, 400, 600, 1000, 1300]
    control_time = 0
    addition_time = 0
    total_time = 0

    # go to each pair in dictionary
    for i in range(len(time_dic)):
        if (control_point[i] <= brevet_dist_km):  # check whether the user input is the total distance of the brevet
            if (control_point[i] <= control_dist_km):  # check the key value of the pair
                control_time += time_dic[str(control_point[
                                                 i])]  # add the the value of that key to the total_time. #This method is quite redundent, since it have to loop in 5 brevet_dist_km every time.

            else:
                addition_time = (control_dist_km - control_point[i - 1]) / speed_dic[str(control_point[i])]
            total_time = control_time + addition_time
            total_second = total_time * 3600 + 30

            # end of adding time when reach the brevet_dist_km, as long as reach the brevet_dist_km, do nothing to the data.

    # take starttime, turn to the arrow object,
    open_t = arrow.get(brevet_start_time)
    control_open = open_t.shift(seconds=+total_second)

    return control_open.isoformat()




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
    # this is to account for the 0 value starting point where the original
    # calculator webpage adds an hour on for this part, so follow suit here
    speed_dic = {"0": 15, "200": 15, "300": 15, "400": 15, "600": 15, "1000": 11.428}
    time_dic = {"0": 0, "200": 200 / 15, "300": 100 / 15, "400": 100 / 15, "600": 200 / 15, "1000": 400 / 11.428}
    control_point = [0, 200, 300, 400, 600, 1000]
    fix_end = {"0.0": 1, "200.0": 13.5, "300.0": 20, "400.0": 27, "600.0": 40, "1000.0": 75}
    control_time = 0
    addition_time = 0
    total_time = 0

    if (control_dist_km == brevet_dist_km):
        total_time += fix_end[str(control_dist_km)]
    elif (control_dist_km == 0):
        total_time = 1

    else:
        # go to each pair in dictionary
        for i in range(len(time_dic)):
            if (control_point[i] <= brevet_dist_km):  # check whether the user input is the total distance of the brevet
                if (control_point[i] <= control_dist_km):  # check the key value of the pair
                    control_time += time_dic[str(control_point[
                                                     i])]  # add the the value of that key to the total_time. #This method is quite redundent, since it have to loop in 5 brevet_dist_km every time.

                else:
                    addition_time = (control_dist_km - control_point[i - 1]) / speed_dic[str(control_point[i])]
                total_time = control_time + addition_time
            # total_time = control_time + addition_time
            # print ("This is total time: "+ str(total_time))

            # end of adding time when reach the brevet_dist_km, as long as reach the brevet_dist_km, do nothing to the data.
    # take starttime, turn to the arrow object,
    close_t = arrow.get(brevet_start_time)
    control_close = close_t.shift(hours=+total_time)

    return control_close.isoformat()