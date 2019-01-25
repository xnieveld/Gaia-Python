COLOR_R = []
COLOR_G = []
COLOR_B = []

def calculate_color(t):
    ''' Calculate an RGB colour from a given temperature '''
    ''' t = Temperature in Kelvin between 1000 and 40000 '''
    ''' returns: RGB Aproximate equivalent '''
    from numpy import log
    # color = [0, 0, 0]

    mCOLOR_R  = 0.0
    mCOLOR_G  = 0.0
    mCOLOR_B  = 0.0
    
    temperature_clamped = float(max(min(t, 40000), 1000))
    # max(min(my_value, max_value), min_value)

    temperature_clamped /= 100
    if temperature_clamped <= 66:
        mCOLOR_R += 255
        mCOLOR_G += float(max(min(float(99.4709025861) * log(temperature_clamped) - float(161.1195681661), 255), 0))
        if temperature_clamped > 19:
            mCOLOR_B = float(max(min(float(138.5177312231) * log(temperature_clamped - 10) - float(305.0447927307), 255), 0))
    else:
        mCOLOR_R += float(max(min(float(329.698727446) * (temperature_clamped - 60) ** float(-0.1332047592), 255), 0))
        mCOLOR_G += float(max(min(float(288.1221695283) * (temperature_clamped - 60) ** float(-0.0755148492), 255), 0))
        mCOLOR_B += 255

    mCOLOR_R /= 255
    mCOLOR_G /= 255
    mCOLOR_B /= 255
    print("COLOR_R: %s, COLOR_G: %s, COLOR_B: %s" % (mCOLOR_R, mCOLOR_G, mCOLOR_B))
    print("input: %s" % t)
    # print("COLOR_R: %s, COLOR_G: %s, COLOR_B: %s" % (len(COLOR_R), len(COLOR_G), len(COLOR_B)))
    COLOR_R.append(mCOLOR_R)
    COLOR_G.append(mCOLOR_G)
    COLOR_B.append(mCOLOR_B)
    # return color

print(calculate_color(1000.0))
print(calculate_color(1500.0))
print(calculate_color(6000.0))
print(calculate_color(4000.0))