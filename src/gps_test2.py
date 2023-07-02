from math import sin, cos, sqrt, atan, atan2, radians, tan, pi
import pandas as pd

def findSpeed(df, time_interval=5):  
    df.sort_values(by='timestamp', inplace=True)
    df.reset_index(drop=True, inplace=True)
    computeDistance(df)
    df['offset'] = getTimeOffsets(df)
    df['dspan'] = df['tspan'] = df['cspeed'] = df['diff'] = df['cheating'] = None

    for N in range(len(df)):
        if N == 0:
            continue
        backi = N
        totOffset = df.at[N, 'offset']
        while totOffset <= time_interval:  # Compare to time_interval (now in seconds)
            backi -= 1
            if backi > 0:
                totOffset += (df.at[backi, 'timestamp'] - df.at[backi-1, 'timestamp']).total_seconds()
            if backi == 0:
                break

        tspan = df.at[N, 'timestamp'] - df.at[backi, 'timestamp']
        df.at[N, 'tspan'] = tspan.total_seconds()
        distance = df.at[N, 'll_dist_traveled'] - df.at[backi, 'll_dist_traveled']
        df.at[N, 'dspan'] = round(distance, 3)
        if tspan.total_seconds() == 0:
            df.at[N, 'cspeed'] = 0
            continue
        else:
            speed = round(distance / tspan.total_seconds(), 2)
            df.at[N, 'cspeed'] = speed
        speed_diff = round(df.at[N, 'speed'] - speed, 2)
        df.at[N, 'diff'] = speed_diff

        # Check for cheating
        if speed >= 25 or abs(speed_diff) >= 5:  # Changed conditions to 'greater than or equal to'
            df.at[N, 'cheating'] = True
        else:
            df.at[N, 'cheating'] = False

    return df


def vincenty_distance(lat1, lon1, lat2, lon2):
    a = 6378137.0
    f = 1 / 298.257223563
    b = (1 - f) * a

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    L = lon2 - lon1
    U1 = atan((1 - f) * tan(lat1))
    U2 = atan((1 - f) * tan(lat2))

    sin_U1, cos_U1 = sin(U1), cos(U1)
    sin_U2, cos_U2 = sin(U2), cos(U2)

    lambda_ = L
    for i in range(1000):
        sin_lambda, cos_lambda = sin(lambda_), cos(lambda_)
        sin_sigma = sqrt((cos_U2*sin_lambda)**2 + (cos_U1*sin_U2-sin_U1*cos_U2*cos_lambda)**2)
        cos_sigma = sin_U1*sin_U2 + cos_U1*cos_U2*cos_lambda
        sigma = atan2(sin_sigma, cos_sigma)
        sin_alpha = cos_U1 * cos_U2 * sin_lambda / sin_sigma
        cos2_alpha = 1 - sin_alpha**2
        cos2_sigma_m = cos_sigma - 2*sin_U1*sin_U2/cos2_alpha
        C = f/16*cos2_alpha*(4+f*(4-3*cos2_alpha))
        lambda_prev = lambda_
        lambda_ = L + (1-C) * f * sin_alpha * (sigma + C*sin_sigma*(cos2_sigma_m+C*cos_sigma*(-1+2*cos2_sigma_m**2)))

        if abs(lambda_ - lambda_prev) < 1e-12:
            break
    else:
        raise ValueError("Vincenty's formula failed to converge!")

    u2 = cos2_alpha * (a**2 - b**2) / b**2
    A = 1 + u2/16384*(4096+u2*(-768+u2*(320-175*u2)))
    B = u2/1024 * (256+u2*(-128+u2*(74-47*u2)))
    delta_sigma = B*sin_sigma*(cos2_sigma_m+0.25*B*(cos_sigma*(-1+2*cos2_sigma_m**2) - B/6*cos2_sigma_m*(-3+4*sin_sigma**2)*(-3+4*cos2_sigma_m**2)))

    distance = b*A*(sigma-delta_sigma)

    return round(distance, 6)

def computeDistance(df):
    prevLat = prevLon = 0
    total_dist = 0
    for N in range(len(df)):
        lat = float(df.at[N, 'latitude'])
        lon = float(df.at[N, 'longitude'])
        if N == 0:
            df.at[N, 'll_dist'] = 0
        else:
            df.at[N, 'll_dist'] = vincenty_distance(prevLat, prevLon, lat, lon)
        total_dist += df.at[N, 'll_dist']
        df.at[N, 'll_dist_traveled'] = round(total_dist, 6)
        prevLat = lat
        prevLon = lon

    return round(total_dist, 6)


def getTimeOffsets(df, timestamp_col='timestamp'):
    df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    timeOffsets = (df[timestamp_col] - df[timestamp_col].shift()).fillna(pd.Timedelta(seconds=0))
    return timeOffsets.dt.total_seconds().astype(int)



data = [
    {"timestamp": "2023-05-27 08:00:00", "latitude": 45.0703, "longitude": 7.6869, "speed": 0},
    {"timestamp": "2023-05-27 08:00:05", "latitude": 45.0704, "longitude": 7.6870, "speed": 7},
    {"timestamp": "2023-05-27 08:00:10", "latitude": 45.0705, "longitude": 7.6871, "speed": 10},
    {"timestamp": "2023-05-27 08:00:15", "latitude": 45.0706, "longitude": 7.6872, "speed": 15},
    {"timestamp": "2023-05-27 08:00:20", "latitude": 45.0707, "longitude": 7.6873, "speed": 13},
    {"timestamp": "2023-05-27 08:00:25", "latitude": 45.0708, "longitude": 7.6874, "speed": 7},
    {"timestamp": "2023-05-27 08:00:30", "latitude": 45.0709, "longitude": 7.6875, "speed": 0},
    {"timestamp": "2023-05-27 08:00:35", "latitude": 45.0710, "longitude": 7.6876, "speed": 5},
    {"timestamp": "2023-05-27 08:00:40", "latitude": 45.0711, "longitude": 7.6877, "speed": 10},
    {"timestamp": "2023-05-27 08:00:45", "latitude": 45.0712, "longitude": 7.6878, "speed": 15},
    {"timestamp": "2023-05-27 08:00:50", "latitude": 45.0713, "longitude": 7.6879, "speed": 12},
    {"timestamp": "2023-05-27 08:00:55", "latitude": 45.0714, "longitude": 7.6880, "speed": 8},
    {"timestamp": "2023-05-27 08:01:00", "latitude": 45.0715, "longitude": 7.6881, "speed": 5},
    {"timestamp": "2023-05-27 08:01:05", "latitude": 45.0716, "longitude": 7.6882, "speed": 0},
]



df = pd.DataFrame(data)

result_df = findSpeed(df)

print(result_df[['timestamp', 'latitude', 'longitude', 'speed', 'cspeed', 'diff', 'cheating']])