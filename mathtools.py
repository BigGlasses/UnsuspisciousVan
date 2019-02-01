import math,pygame

def findMidpoint((x1,y1),(x2,y2)):
    x = (x1 + x2)/2.0
    y = (y1 + y2)/2.0
    return (x,y)
def findMidpoint2(pl):
    x = 0
    y = 0
    for p in pl:
        x += p[0]
        y += p[1]
    x /= len(pl)
    y /= len(pl)
    return [x,y]

def findTrueAngle((x1,y1),(x2,y2),degrees = False):
    x = x2-x1
    y = y2-y1
    
    angle = math.atan2(y, x)
    if degrees:
        angle = math.degrees(angle)
    return angle

def finddistance(p1,p2):
    d12 = ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5
    return d12
def fixAngle(a):
    while a < 0:
        a += 3.1415*2
    while a > 3.1415*2:
        a -= 3.1415*2
    return a

def findxyratio((x1,y1),(x2,y2)): #Used to find the angle ratio between two objects
    x = x2-x1
    y = y2-y1
    z = float(x**2 + y**2)**0.5
    
    if x == 0:
        xratio = 0
    else:
        xratio = x/z
    if y == 0:
        yratio = 0
    else:
        yratio = y/z
        
    return [xratio,yratio]
def collideimage(image1,(x1,y1),image2,(x2,y2)):
    #Makes masks used to check collision
    mask1 = pygame.mask.from_surface(image1, 127)
    mask2 = pygame.mask.from_surface(image2, 127)
    
    xoffset = x2 - x1
    yoffset = y2 - y1
    if mask1.overlap(mask2,(xoffset,yoffset)):
        return True