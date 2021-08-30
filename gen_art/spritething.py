# python spritething.py [SPRITE_DIMENSIONS] [NUMBER] [IMAGE_SIZE]


import PIL, random, sys, math
from PIL import Image, ImageDraw
import numpy as np

# = ( , , )

## Dynamic Slices #320
blu_acqua = (115 ,186 , 211)
giallo_ocra = (229 , 172, 59)
verde_acqua = ( 69, 156, 138)
rosso = ( 224, 48, 33)
arancione = ( 234, 137, 51)
palette_320 = [blu_acqua, giallo_ocra, verde_acqua, rosso, arancione]


## Dynamic Slices #287
rosa = ( 220,164 ,194 )
celeste = ( 199, 206, 224)
marroncino = ( 208, 166, 155)
blu = ( 120, 149, 207)

palette_287 = [rosa, celeste, marroncino, blu]


## Dynamic Slices rushmore
c1 = (106, 46, 90)
c2 = (219, 96, 82)
c3 = (163, 59, 92)

palette_rush = [c1, c2, c3]


# bluedark
d1 = (85,188,249)
d2 = (22,67,121)
d3 = (65,8,37)
d4 = (124,163,210)
palette_darkblue = [d1, d2, d3, d4]


palette_test1 = palette_287 + palette_320

palette = palette_287
#palette = palette_test1
black = (0,0,0)
white = (256,256,256)
gray = (128,128,128)

'''
 = ( , , )
 = ( , , )
 = ( , , )
 = ( , , )
 = ( , , )
 = ( , , )
 = ( , , )
 = ( , , )
 = ( , , )
 = ( , , )
'''




origDimension = 1500
r = lambda: random.randint(50,215)
rc = lambda: (r(), r(), r())

listSym = []

'''
def create_square(border, draw, randColor, element, size):
    #print(element,int(size/2))
    if (element == int(size/2)):
        draw.rectangle(border, randColor)
    elif (len(listSym) == element+1):
        draw.rectangle(border,listSym.pop())
    else:
        listSym.append(randColor)
        draw.rectangle(border, randColor)

def create_invader(border, draw, size):
    x0, y0, x1, y1 = border
    squareSize = (x1-x0)/size
    print(size)
    #randColors = [rc(), rc(), rc(), (0,0,0), (0,0,0), (0,0,0)]
    randColors = palette_320
    i = 1
    for y in range(0, size):
        i *= -1
        element = 0
        for x in range(0, size):
            topLeftX = x*squareSize + x0
            topLeftY = y*squareSize + y0
            botRightX = topLeftX + squareSize
            botRightY = topLeftY + squareSize

            create_square((topLeftX, topLeftY, botRightX, botRightY), draw, random.choice(randColors), element, size)
            if (element == int(size/2) or element == 0):
                i *= -1;
                element += i
'''

def fermat_spiral(dot):
    data=[]
    d=dot*0.1
    for i in range(dot):
        t = float(i) / d * math.pi
        print(t)
        x = (1. +  t) * math.cos(t)
        y = (1. +  t) * math.sin(t)
        print (x,y)
        data.append([x,y])
    narr = np.array(data)
    f_s = np.concatenate((narr,-narr))
    return f_s



def draw_circle(circle_border, r, draw, palette, lineColor, lineWidth):
    ## convert coordinates
    xc = random.uniform(circle_border[0]+r, circle_border[2]-r)
    yc = random.uniform(circle_border[1]+r, circle_border[3]-r)
    color = random.choice(palette)
    color_fill = color + (256,)
    #print(color_fill)

    #lineWidth=0
    #lineColor = random.choice([l0,l1])
    #lineColor = l1
    draw.ellipse((xc-r, yc-r, xc+r, yc+r), fill=color_fill, outline=lineColor, width=lineWidth )
    a = r/math.sqrt(2)
    #circle_border = (xc-a, yc-a, xc+a, yc+a)
    #circle_border = (xc-a, yc-a, xc+a, yc+a)
    return circle_border
    #draw.ellipse((xc-r, yc-r, xc+r, yc+r), color_fill)
    #palette.remove(color)

def create_patch(border, draw, size, palette, niter, lineColor, lineWidth):
    scale =  0.10
    x0, y0, x1, y1 = border
    #print(border)
    #print(palette, new_palette)

    size = (x1-x0)
    delta = (x1-x0)*scale

    background_color = random.choice(palette)
    background_color = white
    background_color = giallo_ocra
    draw.rectangle(border, background_color)

    draw_palette = list(palette)
    #draw_palette.remove(background_color)

    xb0 = x0+delta
    yb0 = y0+delta
    xb1 = x1-delta
    yb1 = y1-delta
    circle_border = (xb0, yb0, xb1, yb1)
    ## 1st circle


    size = circle_border[2] - circle_border[0]

    radii = []
    colors = []

    r = 0.5 * size
    for i in range(niter):
        radii.append(random.uniform(0, 1) * 0.5 * size)
        #rn = r * 0.75**i
        #radii.append(rn)

    radii.sort(reverse=True)

    for i in range(niter):
        r = radii[i]
        print(i, circle_border, r)
        circle_border = draw_circle(circle_border, r, draw, draw_palette, lineColor, lineWidth)
        #circle_border = (circle_border[0]+r, circle_border[1]+r, circle_border[2]-r, circle_border[3]-r)
        #rn = r/math.sqrt(2)
        #circle_border = (circle_border[0]+rn, circle_border[1]+rn, circle_border[2]-rn, circle_border[3]-rn)

def main_circles(size, number_of_figures, imgSize, params):
    origDimension = imgSize
    origImage = Image.new('RGB', (origDimension, origDimension))
    draw = ImageDraw.Draw(origImage, 'RGBA')
    figSize = origDimension/number_of_figures
    #padding = figSize/size
    padding = 0
    #print (figSize, padding)

    ## test spiral
    print(fermat_spiral(100))

    for x in range(0, number_of_figures):
        for y in range(0, number_of_figures):

            topLeftX = x*figSize + padding/2
            topLeftY = y*figSize + padding/2
            botRightX = topLeftX + figSize - padding
            botRightY = topLeftY + figSize - padding
            lineWidth = int(40/number_of_figures)


            ## randomly generate parameters for patch
            #niter = int(random.uniform(niter_max/4, niter_max))
            niter = random.choice(params[0])
            #patch_palette = random.sample(palette, 4)
            patch_palette = random.choice(params[1])
            patch_linecolor = random.choice(params[2])

            print(niter, patch_palette, patch_linecolor)
            create_patch((topLeftX, topLeftY, botRightX, botRightY), draw, size, patch_palette, niter, patch_linecolor, lineWidth)

    origImage.save("Examples/Circle-"+str(size)+"x"+str(size)+"-"+str(number_of_figures)+"-"+str(imgSize)+".jpg")


'''
def main(size, invaders, imgSize):
    origDimension = imgSize
    origImage = Image.new('RGB', (origDimension, origDimension))
    draw = ImageDraw.Draw(origImage)
    invaderSize = origDimension/invaders
    padding = invaderSize/size
    for x in range(0, invaders):
        for y in range(0, invaders):
            topLeftX = x*invaderSize + padding/2
            topLeftY = y*invaderSize + padding/2
            botRightX = topLeftX + invaderSize - padding
            botRightY = topLeftY + invaderSize - padding
            create_invader((topLeftX, topLeftY, botRightX, botRightY), draw, size)

    origImage.save("Examples/Example-"+str(size)+"x"+str(size)+"-"+str(invaders)+"-"+str(imgSize)+".jpg")
'''

niters = [80, 80, 80, 80, 80, 80, 80, 80, 80,
          40, 40, 40, 40,
          20, 20,
          10
          ]


#sniters = [5]


palettes = [palette_320, palette_320, palette_320, palette_320, palette_320, palette_320, palette_320, palette_320,
            palette_287, palette_287, palette_287, palette_287,
            palette_rush, palette_rush,
            palette_darkblue]

linecolors = [white, white, black]

params = [niters, palettes, linecolors]

if __name__ == "__main__":
    #main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    main_circles(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), params)
