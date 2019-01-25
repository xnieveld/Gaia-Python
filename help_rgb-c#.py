def color_temperature(t):
    ''' Calculate an RBG colour from a given temperature '''
    ''' t = Temperature in Kelvin between 1000 and 40000 '''
    ''' returns: RGB Aproximate equivalent '''
    from numpy import log
    color = [0, 0, 0]

    temperature_clamped = float(max(min(t, 40000), 1000))
    # max(min(my_value, max_value), min_value)

    temperature_clamped /= 100
    if temperature_clamped <= 66:
        color[0] += 255
        color[1] = float(max(min(float(99.4709025861) * log(temperature_clamped) - float(161.1195681661), 0), 255))
        if temperature_clamped > 19:
            color[2] = float(max(min(float(138.5177312231) * log(temperature_clamped - 10) - float(305.0447927307), 255), 0))
    else:
        color[0] += float(max(min(float(329.698727446) * (temperature_clamped - 60) ** float(-0.1332047592), 255), 0))
        color[1] += float(max(min(float(288.1221695283) * (temperature_clamped - 60) ** float(-0.0755148492), 255), 0))
        color[2] += 255

    color[0] /= 255
    color[1] /= 255
    color[2] /= 255

    return color
