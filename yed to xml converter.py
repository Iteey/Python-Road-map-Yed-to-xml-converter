import xml.etree.ElementTree as XMLmap
tree = XMLmap.parse("map.xgml")
root = tree.getroot()
newMap=open('newMap.xml',"w")
routeN=0
newMap.write("<map>\r\n<points>\r\n")
pointNames={}
for child in root[2]:
    if child.tag=="section" and child.attrib['name']=="node":
        label=child[1].text
        x=str(round(float(child[2] [0].text)))
        y=str(round(float(child[2] [1].text)))
        newMap.write('<point x="'+x+'" y="'+y+'" id="'+label+'" m="10" />\r')
        pointNames[child[0].text]=child[1].text
newMap.write("</points>\r</map>\r")
for child in root[2]:
    if (child.tag=="section" and child.attrib['name']=="edge"):
        nodeFrom=pointNames[child[0].text]
        nodeTO=pointNames[child[1].text]
        newMap.write('<route from="'+nodeFrom+'" to="'+nodeTO+'" v="50" id="'+str(routeN)+'"/>\r')
        routeN=routeN+1
        newMap.write('</routes>\r</map>\r')
newMap.close()