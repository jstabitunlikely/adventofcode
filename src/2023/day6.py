# Time:        61     67     75     71
# Distance:   430   1036   1307   1150

time = [61,67,75,71]
distance = [430,1036,1307,1150]
ways = 1
for t_race, record in zip(time, distance):
    ways *= len([t_charge for t_charge in range(0,t_race+1) if (t_race*t_charge - t_charge**2) > record])
print(ways)

time = [61677571]
distance = [430103613071150]
ways = 1
for t_race, record in zip(time, distance):
    ways *= len([t_charge for t_charge in range(0,t_race+1) if (t_charge*(t_race - t_charge)) > record])
print(ways)
