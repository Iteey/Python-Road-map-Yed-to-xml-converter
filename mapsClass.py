from tkinter import *

backgroundColors = {
    'start':'#33cc33',
    'finish':'#0000ff',
    'normal':'#d7d2d2',
    'dropped':'#ff0000',
    'possible':'#ff6699',
    'selected':'#ffcc00',
    'visited':'#ff9933',
    'current':'#0099ff'
}
outlineColors = {
    'start':'#000000',
    'finish':'#000000',
    'normal':'#000000',
    'dropped':'#000000',
    'possible':'#14a10d',
    'selected':'#ffff99',
    'visited':'#000000',
    'current':'#000000'
}
fontColors = {
    'start':'#FFFFFF',
    'finish':'#FFFFFF',
    'normal':'#000000',
    'dropped':'#000000',
    'possible':'#14a10d',
    'selected':'#000000',
    'visited':'#000000',
    'current':'#000000'
}
pointNames = {
    'start':'Начало пути',
    'finish':'Конец пути',
    'normal':'Обычный узел',
    'dropped':'Исключенный узел',
    'possible':'Узел возможный для перехода',
    'selected':'Избранный узел',
    'visited':'Посещенный узел',
    'current':'Текущий узел'
}
routeColors = {
    'normal':'#000000',
    'visited':'#ff9933'
}
mapWidth = 1000
mapHeight = 1000
fontSize = 20
borderWidth = 2
routeWidth = 3
arrowForm = "25 32 22"

root = Tk()
moycanvas = Canvas(root, width=mapWidth, height=mapHeight)

class Point:
    def __init__(self, canvas:Canvas, posX, posY, text:str, textColor:str, fillColor:str, outlineColor:str):
        self.canvas = canvas
        self.x = posX
        self.y = posY
        self.text = text
        self.textColor = textColor
        self.fillColor = fillColor
        self.outlineColor = outlineColor
        self.diameter = fontSize + borderWidth * 2 + 10
        self.canvas.create_oval(
            self.x, self.y, self.x + self.diameter, self.y + self.diameter,
            fill = self.fillColor, outline=self.outlineColor, width=borderWidth,
            tags="point{}".format(text)
            )
        self.canvas.create_text(
            self.x + self.diameter/2, self.y + self.diameter/2, font=("LatoThin", fontSize),
            text=self.text, fill=self.textColor, tags="pointText{}".format(text)
        )
    def redraw(self, posX:int = None, posY:int = None, text:str = None, textColor:str = None, fillColor:str = None, outlineColor:str = None):
        self.canvas.delete("point{}".format(self.text))
        self.canvas.delete("pointText{}".format(self.text))

        if (posX != None):
            self.x = posX
        if (posY != None):
            self.y = posY
        if (text != None):
            self.text = text
        if (textColor != None):
            self.textColor = textColor
        if (fillColor != None):
            self.fillColor = fillColor
        if (outlineColor != None):
            self.outlineColor = outlineColor

        self.canvas.create_oval(
            self.x, self.y, self.x + self.diameter, self.y + self.diameter,
            fill = self.fillColor, outline=self.outlineColor, width=borderWidth,
            tags="point{}".format(self.text)
            )
        self.canvas.create_text(
            self.x + self.diameter/2, self.y + self.diameter/2, font=("LatoThin", fontSize),
            text=self.text, fill=self.textColor, tags="pointText{}".format(self.text)
        )
    def scale(self, minX, maxX, minY, maxY, mapWidth, mapHeight):
        width = maxX-minX
        height = maxY-minY
        
        mW = (mapWidth-100) / width
        mH = (mapHeight-100) / height
        # Множитель для масштабирования
        
        nX = self.x - minX
        nY = self.y - minY
        # Числа больше нуля
        
        x = nX * mW + 50
        y = nY * mH + 50
        # Новые координаты
        
        self.redraw(posX=x, posY=y)

class Route:
    def __init__(self, canvas:Canvas, point1:Point, point2:Point, color):
        self.canvas = canvas
        self.point1 = point1
        self.point2 = point2
        self.lineColor = color
        self.x1 = point1.x + point1.diameter / 2
        self.y1 = point1.y + point1.diameter / 2
        self.x2 = point2.x + point2.diameter / 2
        self.y2 = point2.y + point2.diameter / 2

        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=color, width=routeWidth, arrow=LAST, arrowshape=arrowForm, tags="route{}{}".format(point1.text, point2.text))
        self.point1.redraw()
        self.point2.redraw()

    def redraw(self, color = None, x1 = None, y1 = None, x2 = None, y2 = None):
        self.canvas.delete("route{}{}".format(self.point1.text, self.point2.text))

        if (color != None):
            self.lineColor = color
        if (x1 != None):
            self.x1 = x1 + self.point1.diameter / 2
        if (y1 != None):
            self.y1 = y1 + self.point1.diameter / 2
        if (x2 != None):
            self.x2 = x2 + self.point2.diameter / 2
        if (y2 != None):
            self.y2 = y2 + self.point2.diameter / 2

        self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.lineColor, width=routeWidth, arrow=LAST, arrowshape=arrowForm, tags="route{}{}".format(self.point1.text, self.point2.text))
        
        self.point1.redraw()
        self.point2.redraw()

    def scale(self, minX, maxX, minY, maxY, mapWidth, mapHeight):
        width = maxX-minX
        height = maxY-minY
        
        mW = (mapWidth-100) / width
        mH = (mapHeight-100) / height
        # Множитель для масштабирования
        
        nX1 = (self.x1 - self.point1.diameter / 2) - minX
        nY1 = (self.y1 - self.point1.diameter / 2) - minY
        nX2 = (self.x2 - self.point2.diameter / 2 ) - minX
        nY2 = (self.y2 - self.point2.diameter / 2) - minY
        # Числа больше нуля
        
        x1 = nX1 * mW + 50
        y1 = nY1 * mH + 50
        x2 = nX2 * mW + 50
        y2 = nY2 * mH + 50
        # Новые координаты
        
        self.redraw(None, x1, y1, x2, y2)

pointLines = []
routeLines = []

points = []
routes = []

file = open("newMap.xml")

for line in file:
    if (line.find("<point ") > -1):
        pointLines.append(line)
    if (line.find("<route ")> -1):
        routeLines.append(line)

file.close()

x = y = id = m = 0
minX = minY = None
maxX = maxY = None

for line in pointLines:
    if (line.find('x="') > -1):
        l = line[line.find('x="'):]
        l = l[l.find('"')+1:]
        l = l[:l.find('"')]
        x = int(l)
    if (line.find('y="') > -1):
        l = line[line.find('y="'):]
        l = l[l.find('"')+1:]
        l = l[:l.find('"')]
        y = int(l)
    if (line.find('id="') > -1):
        l = line[line.find('id="'):]
        l = l[l.find('"')+1:]
        l = l[:l.find('"')]
        id = int(l)
    if (line.find('m="') > -1):
        l = line[line.find('m="'):]
        l = l[l.find('"')+1:]
        l = l[:l.find('"')]
        m = int(l)

    x = int(x)
    y = int(y)
    if (minX == None):
        minX = x
    if (maxX == None):
        maxX = x
    if (minY == None):
        minY = y
    if (maxY == None):
        maxY = y

    if (minX > x):
        minX = x
    if (maxX < x):
        maxX = x
    if (minY > y):
        minY = y
    if (maxY < y):
        maxY = y
    
    tochka = Point(moycanvas, x, y, str(id), fontColors['normal'], backgroundColors['visited'], outlineColors['normal'])
    points.append(tochka)

for line in routeLines:
    if (line.find('from="') > -1):
        l = line[line.find('from="'):]
        l = l[l.find('"')+1:]
        l = l[:l.find('"')]
        routeFrom = str(l)
    if (line.find('to="') > -1):
        l = line[line.find('to="'):]
        l = l[l.find('"')+1:]
        l = l[:l.find('"')]
        routeTo = str(l)

    point1 = point2 = None
    
    for i in range(0, len(points)):
        if (points[i].text == routeFrom):
            point1 = points[i]
        elif (points[i].text == routeTo):
            point2 = points[i]
    strelka = Route(moycanvas, point1, point2, routeColors['normal'])
    routes.append(strelka)

for point in points:
    point.scale(minX, maxX, minY, maxY, mapWidth, mapHeight)

for route in routes:
    route.scale(minX, maxX, minY, maxY, mapWidth, mapHeight)

moycanvas.pack()
root.mainloop()