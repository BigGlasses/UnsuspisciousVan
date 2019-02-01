import pygame, mathtools,random
from pygame.locals import *
#Common Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
LAV = (150,100,80)
PINK = (255,100,200)
RED = (239,62,51)
ORANGE = (243,118,53)
YELLOW = (255,200,61)
GREEN = (52,203,150)
MUSHGREEN = (102,255,160)
LIGHTYELLOW = (250,200,150)
GOLD = (230,200,120)
BLUE = (0,146,206)
LIGHTBLUE = (0,100,255)
SKYBLUE = (142,195,255)
PURPLE = (161,0,255)
PINK2 = (255,100,125)
LIMEGREEN = (121,193,64)
SANDYELLOW = (247,222,113)
BEIGE = (200,150,100)
BEIGE2 = (210,140,90)
BROWN = (100,200,255)
GREY = (200,200,200)
GREY2 = (50,50,50)
DARKGREY = (73/2,87/2,91/2)
TRANS = (3,50,10)
TRANS2 = (2,2,2)
pygame.font.init()

def collideimage(image1,(x1,y1),image2,(x2,y2)):
    #Makes masks used to check collision
    mask1 = pygame.mask.from_surface(image1, 127)
    mask2 = pygame.mask.from_surface(image2, 127)
    
    xoffset = int(x2 - x1)
    yoffset = int(y2 - y1)
    if mask1.overlap(mask2,(xoffset,yoffset)):
        return True
    
def recolourLoad(path):
    icon = pygame.image.load(path).convert_alpha()
    #cols = [RED,BLUE,GREEN,GOLD,YELLOW,PURPLE]
    #col = random.choice(cols)
    #icon = tint(icon,col,0.25)
    return icon



def hpColor(currentHealth, maxHealth):
    perc = float(currentHealth)/maxHealth
    c = WHITE
    if perc < 0.33:
        c = ORANGE
    elif perc < 0.75:
        c = YELLOW
    else:
        c = LIMEGREEN
    return c

def ratioScale(image,ratio = 2.0):
    x = image.get_width()
    y = image.get_height()
    nx = int(x*ratio)
    ny = int(y*ratio)
    return pygame.transform.scale(image,(nx,ny))
def ratioScaleSmooth(image,ratio = 2.0):
    x = image.get_width()
    y = image.get_height()
    nx = int(x*ratio)
    ny = int(y*ratio)
    return pygame.transform.smoothscale(image,(nx,ny))

def monsterScale(monster):
    
    #===========================================================================
    # if icon.get_width() >= icon.get_height():
    #     ratio = float(icon.get_height())/icon.get_width()
    #     x = xn
    #     y = int(yn*ratio)
    # else:
    #     ratio = float(icon.get_width())/icon.get_height()
    #     y = yn
    #     x = int(xn*ratio)
    #return pygame.transform.scale(icon,(x,y))
    #===========================================================================
    return ratioScale(monster.icon,monster.scale)
def drawBetterCircle(surface,color,(x,y),radius,width = 0):
    #pygame.draw.circle(surface,color,(x,y),radius,width)
    #return None
    newSurf = pygame.Surface((radius*2,radius*2))
    c = TRANS
    if color == TRANS:
        c = TRANS2
    newSurf.fill(c)
    newSurf.set_colorkey(c)
    pygame.draw.circle(newSurf,color,(radius,radius),radius)
    if width > 0:
        drawBetterCircle(newSurf,TRANS,(radius,radius),radius - width)
    surface.blit(newSurf,(x-radius,y-radius))
    
def drawstar(surface,color,(x,y),starwidth,thickness): #Module to draw stars
    x -= starwidth
    starpoints = ((1.25*starwidth+x,0+y),(1.75*starwidth+x,starwidth+y),(2.75*starwidth+x,1.25*starwidth+y),(2*starwidth+x,2*starwidth+y),(2.25*starwidth+x,3*starwidth+y),(1.25*starwidth+x,2.5*starwidth+y),(0.25*starwidth+x,3*starwidth+y),(0.5*starwidth+x,2*starwidth+y),(-0.25*starwidth+x,1.25*starwidth+y),(0.75*starwidth+x,starwidth+y))#connects all of the points on the star
    pygame.draw.polygon(surface, color, starpoints, thickness)

def drawRoundRect(surface,color,rect,width = 0):
    newSurf = pygame.Surface((rect.width,rect.height))
    c = TRANS
    if color == TRANS:
        c = TRANS2
    newSurf.fill(c)
    newSurf.set_colorkey(c)
    r = rect.height/2 +1
    centerRect = pygame.Rect(r,0,rect.width-r*2,rect.height)
    drawBetterCircle(newSurf,color,(r,r),r,width)
    drawBetterCircle(newSurf,color,(rect.width-r+1,r),r,width)
    pygame.draw.rect(newSurf,color,centerRect,width)
    if width > 0:
        pygame.draw.rect(newSurf,color,centerRect,width*2)
        smallRect = pygame.Rect(width,width, rect.width - width*2, rect.height - 2*width)
        print rect,smallRect
        drawRoundRect(newSurf,TRANS,smallRect)
    surface.blit(newSurf,(rect.left,rect.top))
    
        
    
        

def drawHeart(surface,color,(x,y),(width,height),thickness = 0):
    """
    Draws a heart
    """
    newSurf = pygame.Surface((width,height))
    newSurf.set_colorkey(TRANS)
    newSurf.fill(TRANS)
    if thickness == 0:
        newSurf.fill(TRANS2)
    r = width/4
    p1 = (0,r)
    p2 = (r*2,height)
    p3 = (width,r)
    pl = (p1,p2,p3)
    pygame.draw.polygon(newSurf,color,pl,0)
    
    """
    Draw 2 circles
    """
    r1 = pygame.Rect(0,0,r*2,r*2)
    r2 = pygame.Rect(r*2,0,r*2,r*2)
    rl = [r1,r2]
    for rec in rl:
        for i in range(-10,10):
            pygame.draw.arc(newSurf, color, rec,0+i/100.0,3.14, r)
            
    if thickness > 0:
        nx = thickness
        ny = thickness  
        nw = width - 2*thickness
        nh = height - 2*thickness
        drawHeart(newSurf,TRANS,(nx,ny),(nw,nh))
        newSurf.set_colorkey(TRANS)
    else:
        newSurf.set_colorkey(TRANS2)
        
    surface.blit(newSurf,(x,y))
    """
    done
    """
def drawfixcircle(surface,colour,(p1,p2),radius,thickness):
    tempcanvas = pygame.Surface((4*radius,4*radius))
    tempcanvas.set_colorkey(TRANS2)
    tempcanvas.fill(TRANS2)
    pygame.draw.circle(tempcanvas,colour,(2*radius,2*radius),radius,0)
    pygame.draw.circle(tempcanvas,TRANS2,(2*radius,2*radius),radius-thickness,0)
    surface.blit(tempcanvas,(p1-2*radius,p2-2*radius))

def makeorbmeter(METERR,percentage,colour):
    #Blood Meter
    tempcanvas = pygame.Surface((2*METERR,2*METERR))
    tempcanvas.set_colorkey(TRANS)
    tempcanvas.fill(TRANS)
    pygame.draw.rect(tempcanvas,colour,(0,2*METERR,2*METERR,-1*int(percentage*2*METERR)),0)
    drawfixcircle(tempcanvas,TRANS,(METERR,METERR),METERR + METERR/2,METERR/2)
    drawfixcircle(tempcanvas,WHITE,(METERR,METERR),METERR,10)
    drawfixcircle(tempcanvas,BLACK,(METERR,METERR),METERR,8)
    drawfixcircle(tempcanvas,WHITE,(METERR,METERR),METERR,2)
    return tempcanvas

def outline(icon,thickness,col = RED,firstPic= None):
    icon2 = pygame.Surface((icon.get_width()+2*thickness,icon.get_height()+2*thickness))
    icon2.fill(TRANS)
    icon2.set_colorkey(TRANS)
    if firstPic == None:
        blackPic = pygame.Surface(icon.get_size(),flags=SRCALPHA)
        blackPic.fill((0,0,0,0))
        blackPic.blit(icon,(0,0))
        
        firstPic = blackPic.convert_alpha()
        firstPic.blit(blackPic.convert(),(0,0),special_flags =BLEND_SUB)
        
    if col != BLACK:
        fake = pygame.Surface(firstPic.convert().get_size())
        fake.fill(col)
        firstPic.blit(fake,(0,0),special_flags =BLEND_ADD)
    
    for x in range(-thickness,thickness+1):
        for y in range(-thickness,thickness+1):
            icon2.blit(firstPic,(x+thickness,y+thickness))
    icon2.blit(icon,(thickness,thickness))
    return icon2


    
    

def darken((r,g,b)):
    newcol = (int(0.8*r),int(0.8*g),int(0.8*b))
    return newcol





def tint(icon = None,color = WHITE,perc = 1, firstPic = None):
    blackPic = pygame.Surface(icon.get_size(),flags=SRCALPHA)
    blackPic.fill((0,0,0,0))
    blackPic.blit(icon,(0,0))
    if firstPic == None:
         
        firstPic = blackPic.convert_alpha()
        firstPic.blit(blackPic.convert(),(0,0),special_flags =BLEND_SUB)
        
    firstLayer = pygame.Surface(icon.get_size())
    firstLayer.fill(TRANS)
    firstLayer.set_colorkey(BLACK)
    firstLayer.blit(firstPic,(0,0))
    
    icon = blackPic
    surf = pygame.Surface(icon.get_size())
    surf.fill(color)
    if perc > 1:
        perc = 1
    alpha = (256 * perc) 
    surf.set_alpha(alpha)
    icon.blit(surf,(0,0))
    
    icon.blit(firstLayer,(0,0))  
    icon = icon.convert()
    icon.set_colorkey(TRANS)
    icon.set_colorkey(icon.get_at([0,0]))
    #icon.set_colorkey((0, 48, 0))
        
    return icon
    
def shadow(icon = None,r = 1, firstPic = None):
    if firstPic == None:
        blackPic = pygame.Surface(icon.get_size(),flags=SRCALPHA)
        blackPic.fill((0,0,0,0))
        blackPic.blit(icon,(0,0))
        firstPic = blackPic.convert_alpha()
        firstPic.blit(blackPic.convert(),(0,0),special_flags =BLEND_SUB)
        #firstPic.fill(GREEN)
    firstPic = pygame.transform.scale(firstPic,(firstPic.get_width(),firstPic.get_height()/r))
    r = 2
    warp = 1
    
    h = int(firstPic.get_height()) #this is root 2
    w = int(firstPic.get_width()*1.41)
    ws = (h/float(w))
    stretch = pygame.Surface((w*warp,h))
    stretch.fill(TRANS)
    stretch.set_colorkey(TRANS)
    div = 4
    for i in range(h/div):
        cropRect = (0,i*div,w,div)
        x = int(i*ws*warp)
        y = i*div
        stretch.blit(firstPic,(x,y),cropRect)
        #print x
    
    #firstPic = tint(firstPic,WHITE,0.1)
    #firstPic.set_colorkey(WHITE)
    return stretch

def scaleSize(icon,x = 1, y = 1):
    if x != 1 or y != 1:
        nx = int(icon.get_width()*x)
        ny = int(icon.get_height()*y)
        icon = pygame.transform.scale(icon,(nx,ny))
    return icon

def centerRectBlit(screen,icon,center):
    x = center[0] - icon.get_width()/2
    y = center[1] - icon.get_height()/2
    screen.blit(icon,(x,y))
def bottomRectBlit(screen,icon,center):
    x = center[0] - icon.get_width()/2
    y = center[1] - icon.get_height()
    screen.blit(icon,(x,y))

def outlineText(text,font,col,col2,thickness,aa = False):
    name = font.render(text,aa,col)
    namebad = font.render(text,aa,col2)
    namesurface = pygame.Surface((name.get_width()+2*thickness,name.get_height()+2*thickness))
    namesurface.fill(TRANS)
    namesurface.set_colorkey(TRANS)
    """for x in range(0,3*thickness,thickness):
        for y in range(0,3*thickness,thickness):
            namesurface.blit(namebad,(x,y))"""
    for x in range(-thickness,thickness+1):
        for y in range(-thickness,thickness+1):
            namesurface.blit(namebad,(x+thickness,y+thickness))
    namesurface.blit(name,(thickness,thickness))
    return namesurface
    
def mountain(y = 40):
    points = [(0,540),(960,540)]
    h = 0.5
    p = []
    for loops in range(10):
        #Get lines
        for p in points[:]:
            #print p
            c = points.index(p)
            if c != len(points)-1:
                ep = points[c + 1]
                mp = list(mathtools.findMidpoint(p,ep))
                mp [1] += random.uniform(-y,0)
                points.insert(c+1,mp)
        y *= 2**(-h)
        #if y < 1:
            #y = 2
    return points
        
def roundP (pointList, times = 5):
    points = pointList[:]
    for loops in range(times):
        originals = points [:]
        for p in points[:]:
                c = points.index(p)
                if c != len(points)-1:
                    ep = points[c + 1]
                else:
                    ep = points[0]
                    
                mp = list(mathtools.findMidpoint(p,ep))
                mp1 = list(mathtools.findMidpoint(mp,p))
                mp2 = list(mathtools.findMidpoint(mp,ep))
                points.insert(c+1,mp1)
                points.insert(c+2,mp2)
        for o in originals:
            points.remove(o)
    return points