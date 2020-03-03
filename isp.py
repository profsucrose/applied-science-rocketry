## Dan's ISP plotter refactored to Python using matplotlib

import matplotlib.pylab as plt
import matplotlib.patches as mpatches
import math
import numpy as np

ENGINE_ISP = 282

def deltaVSimple(sImpulseSpecific):
    # Calculates and plots deltaV over range of fuelmass
    # Utilizes Merlin LOX engine, 282 Isp, Sea Level

    color_legends = {
        'deltaV': 'orange',
        'mRocket': 'green',
        'mFuel': 'blue',
        'nEfficiency': 'red',
        'greaterThanTotalDeltaV': 'pink'
    }

    g = 9.8070 # m/s^2
    mRocket0 = 2000 #Baseline rocket mass, kgs, dry-weight
    mFuel = 0 
    i = 0 # Incrementer to order plot entries
    muEarth = 3.986004418 * 10**(14) #m^3/s^2, GM, or Grav. Constant, Earth
    muMoon = 4.9048695 * 10**(12) #m^3/s^2, GM, or Grav. Constant, Moon
    vEarthSurface = 460 #m/s
    sRadii_earth = 6378000 #m
    sRadii_iss = sRadii_earth + 400000 #m
    dV1 = math.sqrt(muEarth/sRadii_earth)*(math.sqrt(2*sRadii_iss/(sRadii_earth+sRadii_iss)-1)) 
    dV2 = math.sqrt(muEarth/sRadii_iss)*(1-math.sqrt(2*sRadii_earth/(sRadii_earth+sRadii_iss))) 
    sAxisSemiMajor = (sRadii_earth + sRadii_iss)/2 
    vInit = math.sqrt(muEarth/sRadii_earth) #Theoretical orbital velocity at earth surface
    vFinal = math.sqrt(muEarth/sRadii_iss) #Orbital velocity of ISS 400km up
    vTransferA = math.sqrt(muEarth*(2/sRadii_earth - 1/sAxisSemiMajor)) #Velocity at Initial Orbit A
    vTransferB = math.sqrt(muEarth*(2/sRadii_iss - 1/sAxisSemiMajor)) #Velocity at Initial Orbit B
    dVA = vTransferA-vInit #Initial velocity change, m/s
    dVB = vTransferB-vFinal #Final Velocity change, m/s
    dVT = dVA + dVB #Total deltaV

    deltaVList = []
    mRocketList = []
    mFuelList = []
    nEfficiencyFuelList = []
    greaterThanTotalDeltaVList = []

    while mFuel <= 10000:
        i = i + 1 
        mFuel = mFuel + 100 #Add 10 kgs per loop
        mRocket = mFuel + mRocket0 
        deltaV = sImpulseSpecific*g*np.log(mRocket/mRocket0) 
        nEfficiencyFuel = deltaV/mFuel # deltaV/kgOfFuel

        greaterThanTotalDeltaV = 0
        if (deltaV >= dVT):
            greaterThanTotalDeltaV = 1

        deltaVList.append(deltaV)
        mRocketList.append(mRocket)
        mFuelList.append(mFuel)
        nEfficiencyFuelList.append(nEfficiencyFuel)
        greaterThanTotalDeltaVList.append(greaterThanTotalDeltaV)

    plt.plot(deltaVList, color=color_legends['deltaV'])
    plt.plot(mRocketList, color=color_legends['mRocket'])
    plt.plot(mFuelList, color=color_legends['mFuel'])
    plt.plot(nEfficiencyFuel, color=color_legends['nEfficiency'])
    plt.plot(greaterThanTotalDeltaVList, color=color_legends['greaterThanTotalDeltaV'])

    plt.legend(handles=[
        mpatches.Patch(color=color_legends['deltaV'], label='Delta V'),
        mpatches.Patch(color=color_legends['mRocket'], label='Rocket Mass'),
        mpatches.Patch(color=color_legends['mFuel'], label='Fuel Mass'),
        mpatches.Patch(color=color_legends['nEfficiency'], label='Fuel Efficiency'),
        mpatches.Patch(color=color_legends['greaterThanTotalDeltaV'], label='Greater than Total Delta V')
    ])

    # Configure plot

    plt.title('ISP Graph')
    plt.xlabel('Fuel Mass')
    plt.ylabel('Rocket Mass')

    plt.show() # display chart via localhost

deltaVSimple(ENGINE_ISP)