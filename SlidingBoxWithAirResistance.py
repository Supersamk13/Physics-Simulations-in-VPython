from vpython import *
#Web VPython 3.2
from visual import *

#Set up window 
display (width=1400, height=475)


#Get important parameters from the user

#Get initial speed from the user
initialSpeed=float(input("Enter the initial speed of the box in m/s :"))

'''The user is inputting the coefficient of kinetic (sliding) friction between the block which can be experimentally determined or estimated
by knowing the materials of the block and the surface as well as the shared cross setional area between the block and the surface'''
friction=float(input("Enter the coefficient of friction between the box and the surface: "))

#These determine the size parameters of the box
#The depth and height parameters determine the cross-sectional area for the box in relation to air resistance
depth=float(input("Enter the depth of the box in meters: "))
height=float(input("Enter the height of the box in meters: "))
width=float(input("Enter the width of the box in meters: "))

#Conversion of size parameters to centimeters 
cmDepth=depth * 100.0
cmHeight=height * 100.0 
cmWidth=width * 100.0

#The user inputs the mass of the box
mass = float(input("Enter the mass of the block in kg: "))

#The user inputs the temperature in Fahrenheit of the room
temperature=float(input("Enter the temperature in Fahrenheit: "))
#Converts the temperature to more useful temperature units
kelvinTemperature= ((5/9) * (temperature-32)) + 273.15
celsiusTemperature=kelvinTemperature - 273.15

#The user inputs the air pressure of the room gethered by using a Barometer
kPascalPressure=float(input("Enter the absolute pressure in kiloPascals: "))
#Converts the air pressure to more useful units
pascalPressure=kPascalPressure * 1000.0

#The user inputs the relative humidity percentage of the room as gathered by a Hygrometer
relativeHumidity=float(input("Enter the relative humidity in %: "))

#Set up box position, size, and color
myBox=box(pos=vector(-150, -48, 0), size=vector(cmWidth, cmHeight, cmDepth), color=color.purple)

#Set up important variables that are going to be used in the model

#Gives the box its initial velocity
myBox.velocity=vector(initialSpeed,0,0)

#Sets the time interval between each calculation/time point in the model
dt=.01

#Sets up the initial time for the timer
time=0

#Force of air resistace is 1/2 * air density * drag coefficient * cross secional area

#Sets the cross sectional area of the box in relation to air resistance
crossSectionArea= height * depth

#The drag coefficient is unitless and can only truly be experimentally found but for rectangular prisms it is about 2.1
dragCoefficient=2.1


#This calculation (Tetens' Equation) gets the maximum humidity (vaporPressure at 100% relative humidity) at a specific temperature in Celsius
saturationVaporPressurehPa= 6.108 * 10**((7.5 * celsiusTemperature)/(celsiusTemperature + 237.3))
#Converts hpa to pA (correct units)
saturationVaporPressurePa=saturationVaporPressurehPa * 100
#The vapor pressure is the maximum huminity at a specific temperature multiplied by the relative humidity (the humidity percentage relative to the maximum humidity)
vaporPressure = saturationVaporPressurePa * (relativeHumidity/100)

#By Dalton's Law of Partial Pressured, when two fluids (gases or liquids) take up a space, the total pressure is the combined pressures of each of the fluids
dryPressure = pascalPressure - vaporPressure
'''This equations gets the air density my multiplying the air pressure due to dry air multiplied by the molar mass of dry air (thus getting the total mass of dry air )
multiplied by the air pressure due to water vapor multiplied by the molar mass of water (thus getting the total mass of the water vapor)
this is then divided by (the temperature in kelvin multiplied by the universal gas constant (R))
this means that you get the total mass of the humid air the block is hitting/dragging divided by the volume that the aforementioned humid air is taking up
Hotter air is less dense than cooler air
Air density is mass/volume
Ideal Gas Law PV=mRT
P=mRT/V 
P/RT=m/V=air density
airDensity = P/RT''' 
#Molar mass converts from moles of a gas to kilograms
airDensity= (((dryPressure * .029) + (vaporPressure * .018))/ (kelvinTemperature * 8.31446))
airResistanceCoefficient=1/2 * airDensity * dragCoefficient * crossSectionArea
#air resistance coefficient = 1/2 x drag coefficient x P/RT x HxD
#Calculate acceleration due to friction (constant)
#Depends on the shared cross-sectional area between the block and the surface as well as the materials of the block and the material of the surface
#We may not be able to see it, but every object is somewhat rough and has litte ridges that collide against each other when the surfaces slide relative to each other
frictionAcceleration = -1 * 9.8 * friction

#Run until the box stops
while(myBox.velocity.x >=0):
    
    #Calculate/Update acceleration due to air resistance
    #Reynold's number is high so we multply by velocity twice
    #As the box goes faster, it is dragging more mass of air and is giving each air particle more mass (conservation of momentum/collision)
    airAcceleration=((-1 * airResistanceCoefficient * myBox.velocity.x * myBox.velocity.x) / mass)
    
    #Calculate/Update total acceleration from the addition of the accelerations from the two respective horizontal forces
    myAcceleration=myBox.acceleration=vector((airAcceleration + frictionAcceleration),0,0)
    
    #Calculate/Update velocity
    #Change in velocity = acceleration * time is very close to the actual change in celocity as the final acceleration is very close to the average acceleration
    #On this interval even though acceleration is changing
    #For very small time intervals it is similar to instantaneous rate of change (derivatives)
    myBox.velocity=myBox.velocity + (myAcceleration * dt)
    
    #Calculate/update position
    #Change in position = velocity * time is very close to the actual change in position as the final velocity is very close to the average velocity on this interval
    #For very small time intervals it is similar to instantaneous rate of change (derivatives) even though velocity is changing
    myBox.pos = myBox.pos + (myBox.velocity * dt)
    
    #Calculate/Update time
    #final time = initla time + change in time
    time=time + dt
    
    #Output current acceleration, velocity, position, time
    print((myBox.pos.x + 150), myBox.velocity.x, myBox.acceleration.x, time)
    
    #Delays the program the interval I calculated to be most similar to real life
    sleep(dt/100)
    
#Output out results
print ("The box traveled", (myBox.pos.x) +150, "meters on the surface in", time, "seconds!") 