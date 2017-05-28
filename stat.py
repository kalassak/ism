# http://www.darrinward.com/lat-long/?id=552821
# for plotting
 
# http://stackoverflow.com/questions/24978052/interpolation-over-regular-grid-in-python
# for scipy interpolation help
 
# https://knowledge.safe.com/articles/How_To/Calculating-accurate-length-in-meters-for-lat-long-coordinate-systems
# for lat/lon conversions to nautical miles
 
# http://matplotlib.org/basemap/users/examples.html
 
# create a 1 deg x 1 deg resolution grid for each month
# put storm absolute intensities, intensity change, and direction in them
# put SST data for each month
# put shear data?
 
#split SSTs by el nino and la nina and neutral
 
import math, sys
import numpy as np
import scipy.interpolate as interpolate
import matplotlib.pyplot as plt
 
class cycdat:
        def __init__(self, vx, vy, wind, pres, data):
                self.x = vx
                self.y = vy
                self.w = wind
                self.p = pres
                self.d = data #how many points of data are in this grid, so that velocities can be summed and averaged
                #self.t = temp
               
f = open('bst8089.txt', 'r+')
k = f.read()
 
lines = k.split('\n')
#ln1 = lines[1]
 
#make a grid or something
grid = []
for m in range(0, 12):
        temp2 = []
        for y in range(0, 50):
                temp = []
                for x in range(100, 180):
                        temp.append(cycdat(0, 0, 0, 0, 0))
                temp2.append(temp)
        grid.append(temp2)
       
#m-1, y, x-100
 
lastyear = None
 
for l in lines:
        sp = l.split(' ')
        sp = [y for y in sp if y != '']
       
        try:
                if sp[1] == '002':
                        #date
                        t1 = sp[0]
                        year1 = t1[:2]
                        month1 = int(t1[2:4])
                        day1 = t1[4:6]
         
                        #tropical or extratrop
                        if sp[2] == '6':
                                ex1 = False
                        else:
                                ex1 = True
               
                        #position
                        lat1 = int(sp[3])/10
                        lon1 = int(sp[4])/10
                 
                        #intensity
                        wind1 = int(sp[6])
                        pres1 = int(sp[5])
                       
                        if lastyear is not None and lastlon < 180.0 and lastlat < 50.0 and (t1[6:8] == "00" or t1[6:8] == "06" or t1[6:8] == "12" or t1[6:8] == "18"):
                                dlat = lat1 - lastlat
                                dlon = lon1 - lastlon
                                dwind = wind1 - lastwind
                                dpres = pres1 - lastpres
                               
                                grid[lastmonth - 1][math.floor(lastlat)][math.floor(lastlon) - 100].x += dlat
                                grid[lastmonth - 1][math.floor(lastlat)][math.floor(lastlon) - 100].y += dlon
                                grid[lastmonth - 1][math.floor(lastlat)][math.floor(lastlon) - 100].w += dwind
                                grid[lastmonth - 1][math.floor(lastlat)][math.floor(lastlon) - 100].p += dpres
                                grid[lastmonth - 1][math.floor(lastlat)][math.floor(lastlon) - 100].d += 1
                       
                        lastyear = year1
                        lastmonth = month1
                        lastday = day1
                        lastlat = lat1
                        lastlon = lon1
                        lastwind = wind1
                        lastpres = pres1
                if sp[0] == '66666': #reset all of the last things and bypass adding a point between storm end & start positions
                        lastyear = None
        except:
                print("end of file... probably")
 
for list in grid:
        for list2 in reversed(list):
                for x in list2:
                        if x.d != 0:
                                n = int(math.fabs(x.w/x.d))
                                if n > 9:
                                        n = chr(n + 55)
                                sys.stdout.write(str(n))
                                x.x = x.x/x.d
                                x.y = x.y/x.d
                                x.w = x.w/x.d
                                x.p = x.p/x.d
                        else:
                                sys.stdout.write(' ')
                sys.stdout.write('\n')
        sys.stdout.write('\n\n')
 
stormmonth = int(input('Initialization month: '))
stormlat = float(input('Initial latitude: '))
stormlon = float(input('Initial longitude: '))
stormwin = float(input('Initial wind speed (kt): '))
stormpre = float(input('Initial pressure (hPa): '))
stormsp = float(input('Initial speed (kt): ')) * 6 #6 hours of movement
stormdir = input('Initial direction (or STATIONARY): ')
#calculate nm/deg lon
rlat = stormlat * (math.pi/180)
hfactor = (111412.84 * math.cos(rlat) - 93.5 * math.cos(3*rlat))/1852
#calculate nm/deg lat
#calculate vector of speed/dir
if stormdir == "N":
    initv = stormsp / 60
    inith = 0
elif stormdir == "S":
    initv = -stormsp / 60
    inith = 0
elif stormdir == "W":
    inith = -stormsp / hfactor
    initv = 0
elif stormdir == "E":
    inith = stormsp / hfactor
    initv = 0
elif stormdir == "NE":
    inith = math.cos(math.pi/4) * stormsp / hfactor
    initv = math.sin(math.pi/4) * stormsp / 60
elif stormdir == "NW":
    inith = math.cos(3*math.pi/4) * stormsp / hfactor
    initv = math.sin(3*math.pi/4) * stormsp / 60
elif stormdir == "SW":
    inith = math.cos(5*math.pi/4) * stormsp / hfactor
    initv = math.sin(5*math.pi/4) * stormsp / 60
elif stormdir == "SE":
    inith = math.cos(7*math.pi/4) * stormsp / hfactor
    initv = math.sin(7*math.pi/4) * stormsp / 60
elif stormdir == "ENE":
    inith = math.cos(math.pi/8) * stormsp / hfactor
    initv = math.sin(math.pi/8) * stormsp / 60
elif stormdir == "NNE":
    inith = math.cos(3*math.pi/8) * stormsp / hfactor
    initv = math.sin(3*math.pi/8) * stormsp / 60
elif stormdir == "NNW":
    inith = math.cos(5*math.pi/8) * stormsp / hfactor
    initv = math.sin(5*math.pi/8) * stormsp / 60
elif stormdir == "WNW":
    inith = math.cos(7*math.pi/8) * stormsp / hfactor
    initv = math.sin(7*math.pi/8) * stormsp / 60
elif stormdir == "WSW":
    inith = math.cos(9*math.pi/8) * stormsp / hfactor
    initv = math.sin(9*math.pi/8) * stormsp / 60
elif stormdir == "SSW":
    inith = math.cos(11*math.pi/8) * stormsp / hfactor
    initv = math.sin(11*math.pi/8) * stormsp / 60
elif stormdir == "SSE":
    inith = math.cos(13*math.pi/8) * stormsp / hfactor
    initv = math.sin(13*math.pi/8) * stormsp / 60
elif stormdir == "ESE":
    inith = math.cos(15*math.pi/8) * stormsp / hfactor
    initv = math.sin(15*math.pi/8) * stormsp / 60
elif stormdir == "STATIONARY":
    inith = 0
    initv = 0
 
print('\n')
 
fi = open('output.txt', 'a')
fi2 = open('output_tcdn.txt', 'a')
 
hours = 0
print("[+" + str(hours) + "hr]\t+" + str(stormlat) + "\t" + str(-stormlon)  + "\t" + str(round(stormwin, 1)) + " kt\t" + str(round(stormpre, 1)) + " hPa")
fi.write(str(round(stormlat, 1)) + ", " + str(round(-stormlon, 1)) + "\n")
fi2.write("AL,00,0000000000,,,%sN,%sE,%i,%i,TS\n" % (round(stormlat, 1), round(stormlon, 1), stormwin, stormpre))
 
hgrid = [] #horizontal (W-E) motion
vgrid = [] #vertical (N-S) motion
wgrid = [] #wind
pgrid = [] #pressure
for list in grid:
    htemp = []
    vtemp = []
    wtemp = []
    ptemp = []
    for list2 in list:
        htemp2 = []
        vtemp2 = []
        wtemp2 = []
        ptemp2 = []
        for x in list2:
            htemp2.append(x.x)
            vtemp2.append(x.y)
            wtemp2.append(x.w)
            ptemp2.append(x.p)
        htemp.append(htemp2)
        vtemp.append(vtemp2)
        wtemp.append(wtemp2)
        ptemp.append(ptemp2)
    hgrid.append(htemp)
    vgrid.append(vtemp)
    wgrid.append(wtemp)
    pgrid.append(ptemp)
   
def interp(g):
    ar = np.array(g[stormmonth - 1])
    ar[ ar==0 ] = np.nan
    r = np.linspace(0, 1, ar.shape[1])
    c = np.linspace(0, 1, ar.shape[0])
     
    rr, cc = np.meshgrid(r, c)
    vals = ~np.isnan(ar)
    f = interpolate.Rbf(rr[vals], cc[vals], ar[vals], function='linear')
    return(f(rr, cc))
   
hi = interp(hgrid) #INTERPOLATE HORIZONTAL GRID
vi = interp(vgrid) #INTERPOLATE VERTICAL GRID
wi = interp(wgrid) #INTERPOLATE WIND SPEED GRID
pi = interp(pgrid) #INTERPOLATE PRESSURE GRID
 
#plt.imshow(wi)
#plt.show()
 
def simulate(slat, slon, g, g2, g3, g4):
        tlat = g[math.floor(slat)][math.floor(slon)-100]
        tlon = g2[math.floor(slat)][math.floor(slon)-100]
        twin = g3[math.floor(slat)][math.floor(slon)-100]
        tpre = g4[math.floor(slat)][math.floor(slon)-100]
        return (tlat, tlon, twin, tpre)
 
for x in range(0, 180, 6):
        templat, templon, tempwind, temppres = simulate(stormlat, stormlon, hi, vi, wi, pi)
        if hours < 36:
            frac = (1/1296) * (hours - 36)**2
            stormlat += frac * initv + (1-frac) * templat
            stormlon += frac * inith + (1-frac) * templon
        else:
            stormlat += templat
            stormlon += templon
        stormwin += tempwind
        stormpre += temppres
        if stormlat == lastlat and stormlon == lastlon:
                print("storm stalled")
                break
        if stormlat > 50.0 or stormlon > 180.0 or stormlat < 0.0 or stormlon < 100.0:
                print("storm left grid")
                break
        lastlat = stormlat
        lastlon = stormlon
        hours += 6
        print("[+" + str(hours).zfill(3) + "hr]\t+" + str(round(stormlat, 1)).zfill(4) + "\t+" + str(round(stormlon, 1)).zfill(5) + "\t" + str(round(stormwin, 1)).zfill(5) + " kt\t" + str(round(stormpre, 1)).zfill(5) + " hPa")
        fi.write(str(round(stormlat, 1)) + ", " + str(round(stormlon, 1)) + "\n")
        if stormwin < 25:
            stype = "DS"
        else:
            stype = "TS"
        fi2.write("AL,00,2016000000,,,%sN,%sE,%i,%i,%s\n" % (round(stormlat, 1), round(stormlon, 1), stormwin, stormpre, stype))
        if hours == 180:
                print("forecast end")
               
fi.close()
fi2.close()