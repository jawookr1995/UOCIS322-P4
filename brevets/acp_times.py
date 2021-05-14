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
minSpeedT = {200:15.0, 300:15.0, 400:15.0, 600:11.428, 1000:13.333}
maxSpeedT = {200:34.0, 300:32.0, 400:30.0, 600:28.0, 1000:26.0}

minSpeedOnly = [15.0, 15.0, 15.0, 11.428, 13.333]
maxSpeedOnly = [34.0, 32.0, 30.0, 28.0, 26.0]

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
    if (brevet_dist_km < control_dist_km):
        control_dist_km = brevet_dist_km

    rawTime = timeCalculator(control_dist_km)
    # when we know how much time we took, just add it to initial time.
    finalTime = timeAdder(rawTime, brevet_start_time)
    return finalTime

# Add time traveled to initial time
def timeAdder(rawTime, initialTime):

    # use arrow functions to add minutes from timeCalculator function.
    # and change it to formatted time
    toMinutes = ((rawTime * 60) + .5)
    int(totMinutes)

    finalTime = arrow.get(initialTime).shift(minutes =+ totMinutes).isoformat()
    return finalTime

def timeCalculator(kmGiven, speedTable):
    # initializers
    x = 0
    totTime = 0

    # intervals of 200k, as long as its greater than 200 we will keep cycle
    # through the main part.
    while kmGiven > 200:
        if x < 3:
            totTime = totTime + (200/speedTable[x])
            x += 1
            kmGiven = kmGiven - 200

    # this would be 200 or remiander for the final interval pass to evaluate
    totTime = totTime + (kmGiven / speedTable[x])

    return totTime
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
    if control_dist_km == 0:
        finalTime = timeAdder(1, brevet_start_time)
        return finalTime

    else:

        rawTime = timeCalculator(control_dist_km,minSpeedOnly)
        finalTime = timeAdder((rawTime),brevet_start_time)
    return finalTime
