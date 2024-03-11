def calculate_operational_time(energy_capacity_wh, power_consumption_w):
    """
    Calculate the operational time based on the battery's energy capacity and power consumption.

    :param energy_capacity_wh: Total energy capacity of the battery in Watt-hours
    :param power_consumption_w: Power consumption in Watts
    :return: Operational time in hours
    """
    if power_consumption_w == 0:
        return 0  # Return zero operational time when power consumption is zero
    else:
        return energy_capacity_wh / power_consumption_w


def calculate_range_km(operational_time_h, speed_m_per_s):
    """
    Calculate the range in kilometers based on the operational time and speed.

    :param operational_time_h: Operational time in hours
    :param speed_m_per_s: Speed in meters per second
    :return: Range in kilometers
    """
    if operational_time_h == 0:
        return 0  # Return zero range when operational time is zero
    else:
        speed_km_per_h = speed_m_per_s * 3.6  # Convert m/s to km/h
        return speed_km_per_h * operational_time_h
