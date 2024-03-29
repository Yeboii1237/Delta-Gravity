
import math
import matplotlib.pyplot as plt

# Helper functions

def to_thousands(num):
    '''Basically multiplies the number by a thousand then returns it.'''
    return num * 1000

def to_millions(num):
    '''Basically multiplies the number by a million then returns it.'''
    return num * 1000000

def to_billions(num):
    '''Basically multiplies the number by a billion then returns it.'''
    return num * 1000000000

def delta_r(r, h = 70000, c = 299792458):
    '''Calculates the amount of distance a galaxy / object will move by the
    time an object traveling at the speed of light reaches it.
    Uses meters for radius (r) but m/s per megaparsec for hubble constant (h)'''
    v = (h * r) / (3.086*(10**22))
    change_in_r = (v * r) / c
    return change_in_r

def light_years_to_meters(light_years):
    '''Multiplies the amount of light years by its conversion to meters'''
    return light_years * 9460730472580800

def newtonian_force_of_gravity(r, M = 1, m = 1, G = 6.67*(10**-11)):
    '''Stock standard newton's force of gravity.'''
    return (M * m * G) / (r ** 2)

def volume_of_sphere(r=1.0):
    '''Returns the volume of a sphere according to its radius.'''
    return (4/3) * math.pi * (r**3) # I probably use too many brackets lmao. Then again, I don't often deal with bugs to do with not enough so yyeeee

def true_distance(r=1, h=70000, c=299792458):
    '''Calculates the total amount of distance a galaxy / object will be at by the
    time an object traveling at the speed of light reaches it.
    Uses meters for radius (r) but m/s per megaparsec for hubble constant (h)'''
    return r + delta_r(r, h=h, c=c)

def volume_of_sphere_section(inner_radius, outer_radius):
    '''Returns the volume of a larger sphere minus the inner sphere's volume.
    Onions have layers, ogres have layers... -Shrek'''
    return volume_of_sphere(outer_radius) - volume_of_sphere(inner_radius)

def standard_force_from_sphere_section(inner_radius, outer_radius, density_of_universe):
    '''Calculates the amount of force a layer in a sphere will enact on its center with standard Newtonian physics.'''
    mass = volume_of_sphere_section(inner_radius, outer_radius) * density_of_universe
    return newtonian_force_of_gravity(outer_radius, mass)

def epow(num):
    '''Converts the number to a power of 10'''
    return 10 ** num

def extra_distance_with_velocity(distance = 1, v=1,c=299792458):
    '''Calculates the extra distance an object should travel.
    All units should be in meters.'''
    total = (v * distance / c)
    return total

def total_distance_with_velocity(distance = 1, v=1,c=299792458):
    '''Calculates the total extra distance an object should travel.
    All units should be in meters.'''
    return extra_distance_with_velocity(distance,v,c) + distance

def calc_forces(divisions=10000, distance=light_years_to_meters(to_billions(47)), density = 1, hubble_constant = 70000, return_force = False, return_list=False):
    '''Calculate the total gravitational force on a person in the center of a series of layers stacked on top of each other like an onion, as well as the force that
    would be felt when accounting for how far that mass would have moved in the time for gravity to travel.
    Distance is in meters, density is Kg/m^3, Hubble constant is m/s per mpc, output is N/kg'''
    # Calculating the distance for each segment to the center.
    segments = []
    for division in range(0, divisions + 1):
        segments.append(distance * division * (1 / divisions))

    # Finding the volume of each segment.
    volumes = [0.0]
    for segment in segments[1:]:
        volumes.append(volume_of_sphere(segment) - sum(volumes))

    # Finding the mass of each segment
    masses = []
    for volume in volumes:
        masses.append(density * volume)

    # Calculating the Newtonian force of gravity for each segment to the center and adding in the extra distance for delta forces.
    forces = []
    delta_forces = []
    for i in range(1, len(segments)):
        forces.append(newtonian_force_of_gravity(segments[i], masses[i]))
        delta_forces.append(newtonian_force_of_gravity(segments[i] + delta_r(segments[i], h=hubble_constant), masses[i]))

    # The amount of acceleration is the sum of the segments.
    force = sum(forces)
    delta_force = sum(delta_forces)

    # Plot of forces vs distance.
    plt.plot(range(len(delta_forces)), delta_forces)
    plt.plot(range(len(forces)), forces)
    # plt.show()
    if return_list == True:
        return [force, delta_force]
    if return_force == True:
        return force
    else:
        return delta_force


# Constants and other such numbers.

seconds_in_a_year = 3.15*(10**7)
density_of_universe = 9.9 * (10**-27)
meters_in_a_lightyear = 9.46 * (10**15)
meters_in_a_mpc = 3.086 * (10**22)
speed_of_light = 299792458
milkyway_mass = 1.15 * (10**12) * 2 * (10**30)
meters_in_a_glyr = meters_in_a_lightyear * to_billions(1)
time = to_billions(13) * seconds_in_a_year
radius_of_universe_in_meters = 4.4*(10**26)  # Meters

units_dict = {'mpc': meters_in_a_mpc, 'glyr': meters_in_a_glyr}
units_text = 'mpc'
units = units_dict[units_text]

# Calculations for [9/10]
distance = units * 14500
h = 70000
force, delta_force = calc_forces(10000, distance, density=density_of_universe * 1, return_list=True, hubble_constant=h)
extra_force = (force - delta_force) / 4  # Dividing by four since it should only the sum of the positive forces in a certain direction.

print('Calculating [9/10] (14500 mpc away with current assumptions)')
print(force, 'N/kg Normal, Newtonian force')
print(delta_force, 'N/kg Force with extra distance taken into account')
print(extra_force, 'N/kg Normal force minus Delta force aka the net/extra force.')
print(extra_force * (time ** 2) / units / 2, units_text + ' extra distance traveled. (In mpc by default)')

print('---------------------------------------------------------------')

# Calculations for [12]
distance = units * 7000
h = 70000
force, delta_force = calc_forces(10000, distance, density=density_of_universe * 1, return_list=True, hubble_constant=h)
extra_force = (force - delta_force) / 4  # Dividing by four since it should only the sum of the positive forces in a certain direction.

print('Calculating [12] (7000 mpc away with current assumptions)')
print(force, 'N/kg Normal, Newtonian force')
print(delta_force, 'N/kg Force with extra distance taken into account')
print(extra_force, 'N/kg Normal force minus Delta force aka the net/extra force.')
print(extra_force * (time ** 2) / units / 2, units_text + ' extra distance traveled. (In mpc by default)')

print('---------------------------------------------------------------')

# Calculations for [13]
distance = units * 3000
h = 70000
force, delta_force = calc_forces(10000, distance, density=density_of_universe * 1, return_list=True, hubble_constant=h)
extra_force = (force - delta_force) / 4  # Dividing by four since it should only the sum of the positive forces in a certain direction.

print('Calculating [13] (3000 mpc away with current assumptions)')
print(force, 'N/kg Normal, Newtonian force')
print(delta_force, 'N/kg Force with extra distance taken into account')
print(extra_force, 'N/kg Normal force minus Delta force aka the net/extra force.')
print(extra_force * (time ** 2) / units / 2, units_text + ' extra distance traveled. (In mpc by default)')

