"""
file: lab1.py
description: CSCI 630, Lab 1, Summer Orienteering
language: Python
author: Abhishek Shah, as5553
"""

from PIL import Image
import sys
import math


class Node:
    """
    Each node in the Node class represents a pixel.
    """
    __slots__ = 'xCoordinate', 'yCoordinate', 'type', 'elevation', 'parent', 'score'

    def __init__(self, xCoordinate, yCoordinate):
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.type = None
        self.elevation = None
        self.parent = None
        self.score = float("inf")


def calculateG(node1, node2, axis, speed):
    """
    Calculating cost between two nodes.
    """
    # real world pixel size
    longitude = 10.29
    latitude = 7.55

    if axis == "xAxis":
        distance = math.sqrt((longitude ** 2) + (node2.elevation - node1.elevation) ** 2)
    else:
        distance = math.sqrt((latitude ** 2) + (node2.elevation - node1.elevation) ** 2)

    # time = distance/speed
    cost = distance / (speed[node1.type] + (node1.elevation - node2.elevation) / 40)
    return cost


def calculateH(node, destination, speed):
    """
    Calculating heuristic for node.
    """
    return math.sqrt(
        (node.xCoordinate - destination.xCoordinate) ** 2 + (node.yCoordinate - destination.yCoordinate) ** 2 \
        + (node.elevation - destination.elevation) ** 2) / 2


def calculateF(current, neighbour, destination, speed):
    """
    Calculating total f-score for node.
    """
    if neighbour.xCoordinate == current.xCoordinate:
        totalDistance = calculateG(current, neighbour, "xAxis", speed) + \
                        calculateH(neighbour, destination, speed)
    else:
        totalDistance = calculateG(current, neighbour, "yAxis", speed) + \
                        calculateH(neighbour, destination, speed)
    return totalDistance


def possibleNeighbors(node, terrain, speed):
    """
    Searching and storing all possible neigbors
    that can be reached from the current node.
    """
    validNeighbors = []
    xCoordinate = node.xCoordinate
    yCoordinate = node.yCoordinate

    # checking all the edge cases
    if xCoordinate == 0 and yCoordinate == 0:
        if speed[terrain[xCoordinate][yCoordinate + 1].type] != 0:
            validNeighbors.append(terrain[xCoordinate][yCoordinate + 1])
        if speed[terrain[xCoordinate+1][yCoordinate].type] != 0:
            validNeighbors.append(terrain[xCoordinate + 1][yCoordinate])

    elif xCoordinate == 0 and yCoordinate == 394:
        if speed[terrain[xCoordinate][yCoordinate - 1].type] != 0:
            validNeighbors.append(terrain[xCoordinate][yCoordinate - 1])
        if speed[terrain[xCoordinate + 1][yCoordinate].type] != 0:
            validNeighbors.append(terrain[xCoordinate + 1][yCoordinate])

    elif xCoordinate == 499 and yCoordinate == 0:
        if speed[terrain[xCoordinate][yCoordinate + 1].type] != 0:
            validNeighbors.append(terrain[xCoordinate][yCoordinate + 1])
        if speed[terrain[xCoordinate - 1][yCoordinate].type] != 0:
            validNeighbors.append(terrain[xCoordinate - 1][yCoordinate])

    elif xCoordinate == 499 and yCoordinate == 394:
        if speed[terrain[xCoordinate][yCoordinate - 1].type] != 0:
            validNeighbors.append(terrain[xCoordinate][yCoordinate - 1])
        if speed[terrain[xCoordinate - 1][yCoordinate].type] != 0:
            validNeighbors.append(terrain[xCoordinate - 1][yCoordinate])

    elif xCoordinate == 0 and (0 < yCoordinate < 394):
        if speed[terrain[xCoordinate][yCoordinate - 1].type] != 0:
            validNeighbors.append(terrain[xCoordinate][yCoordinate - 1])
        if speed[terrain[xCoordinate][yCoordinate + 1].type] != 0:
            validNeighbors.append(terrain[xCoordinate][yCoordinate + 1])
        if speed[terrain[xCoordinate + 1][yCoordinate].type] != 0:
            validNeighbors.append(terrain[xCoordinate + 1][yCoordinate])

    elif xCoordinate == 499 and (0 < yCoordinate < 394):
        if speed[terrain[xCoordinate][yCoordinate - 1].type] != 0:
            validNeighbors.append(terrain[xCoordinate][yCoordinate - 1])
        if speed[terrain[xCoordinate][yCoordinate + 1].type] != 0:
            validNeighbors.append(terrain[xCoordinate][yCoordinate + 1])
        if speed[terrain[xCoordinate - 1][yCoordinate].type] != 0:
            validNeighbors.append(terrain[xCoordinate - 1][yCoordinate])

    elif yCoordinate == 0 and (0 < xCoordinate < 499):
        if speed[terrain[xCoordinate + 1][yCoordinate].type] != 0:
            validNeighbors.append(terrain[xCoordinate + 1][yCoordinate])
        if speed[terrain[xCoordinate][yCoordinate + 1].type] != 0:
            validNeighbors.append(terrain[xCoordinate][yCoordinate + 1])
        if speed[terrain[xCoordinate - 1][yCoordinate].type] != 0:
            validNeighbors.append(terrain[xCoordinate - 1][yCoordinate])

    elif yCoordinate == 394 and (0 < xCoordinate < 499):
        if speed[terrain[xCoordinate + 1][yCoordinate].type] != 0:
            validNeighbors.append(terrain[xCoordinate + 1][yCoordinate])
        if speed[terrain[xCoordinate][yCoordinate - 1].type] != 0:
            validNeighbors.append(terrain[xCoordinate][yCoordinate - 1])
        if speed[terrain[xCoordinate - 1][yCoordinate].type] != 0:
            validNeighbors.append(terrain[xCoordinate - 1][yCoordinate])

    else:
        if speed[terrain[xCoordinate + 1][yCoordinate].type] != 0:
            validNeighbors.append(terrain[xCoordinate + 1][yCoordinate])
        if speed[terrain[xCoordinate][yCoordinate - 1].type] != 0:
            validNeighbors.append(terrain[xCoordinate][yCoordinate - 1])
        if speed[terrain[xCoordinate - 1][yCoordinate].type] != 0:
            validNeighbors.append(terrain[xCoordinate - 1][yCoordinate])
        if speed[terrain[xCoordinate][yCoordinate + 1].type] != 0:
            validNeighbors.append(terrain[xCoordinate][yCoordinate + 1])

    return validNeighbors


def nodeWithMinScore(nodesNotVisited):
    """
    Returning the pixel with the lowest score
    """
    cheapestNode = None
    minScore = float("inf")
    for node in nodesNotVisited:
        if node.score < minScore:
            minScore = node.score
            cheapestNode = node

    return cheapestNode


def aStarSearch(startNode, destinationNode, terrain, speed):
    """
    Performing A* search
    """
    if speed[startNode.type] == 0 or speed[destinationNode.type] == 0:
        print("Invalid Node")
        return

    visitedNodes = []
    nodesNotVisited = []
    startNode.score = 0
    currentNode = startNode
    nodesNotVisited.append(currentNode)

    while len(nodesNotVisited) != 0:
        currentNode = nodeWithMinScore(nodesNotVisited)
        # if path is established
        if currentNode == destinationNode:
            while currentNode.parent:
                # keeping up with the path
                point = [currentNode.xCoordinate, currentNode.yCoordinate]
                finalPath.append(point)
                currentNode = currentNode.parent

            point = [currentNode.xCoordinate, currentNode.yCoordinate]
            finalPath.append(point)
            return finalPath

        nodesNotVisited.remove(currentNode)
        visitedNodes.append(currentNode)
        neighbours = possibleNeighbors(currentNode, terrain, speed)
        for neighbour in neighbours:
            if neighbour not in visitedNodes:
                if neighbour in nodesNotVisited:
                    # if the node has seen before
                    score = calculateF(currentNode, neighbour, destinationNode, speed)
                    if score < neighbour.score:
                        neighbour.score = score
                        neighbour.parent = currentNode
                else:
                    # if the node has never seen before
                    neighbour.score = calculateF(currentNode, neighbour, destinationNode, speed)
                    neighbour.parent = currentNode
                    nodesNotVisited.append(neighbour)

    # if no path is found
    print("No path!")


def terrainData(terrainArray, elevations):
    """
    This function uses the terrain data from image, the elevations data
    and combines both the data into a single data structure
    """
    terrain = []
    for rows in range(500):
        line = []
        for columns in range(395):
            temp = Node(rows, columns)
            temp.type = terrainTypes[terrainArray[rows][columns][:3]]
            temp.elevation = elevations[rows][columns]
            line.append(temp)
        terrain.append(line)

    return terrain


# different types of terrains available
terrainTypes = {
    (248, 148, 18): "openLand",  # F89412
    (255, 192, 0): "roughMeadow",  # FFC000
    (255, 255, 255): "easyMovementForest",  # FFFFFF
    (2, 208, 60): "slowRunForest",  # 02D03C
    (2, 136, 40): "walkForest",  # 028828
    (5, 73, 24): "impassibleVegetation",  # 054918
    (0, 0, 255): "lakeSwampMarsh",  # 0000FF
    (71, 51, 3): "pavedRoad",  # 473303
    (0, 0, 0): "footpath",  # 000000
    (205, 0, 101): "outOfBounds"  # CD0065
}

# speedMap for each type of terrain
# 6 being fastest and 0 being the slowest
speedMap = {
    "openLand": 2.0,
    "roughMeadow": 0.25,
    "easyMovementForest": 1.25,
    "slowRunForest": 1,
    "walkForest": 0.75,
    "impassibleVegetation": 0,
    "lakeSwampMarsh": 0,
    "pavedRoad": 2,
    "footpath": 2,
    "outOfBounds": 0
}

finalPath = []  # list that stores the final path


def main():
    """
    The main function
    """
    # taking inputs from user
    inputImageName = sys.argv[1]
    elevationMap = sys.argv[2]
    courseFile = sys.argv[3]
    outputImageName = sys.argv[4]
    speed = speedMap

    # reading and storing elevations data
    elevations = []
    with open(elevationMap) as f:
        for line in f:
            line = line.strip()
            temp = line.split()[:-5]
            for i in range(len(temp)):
                temp[i] = float(temp[i])
            elevations.append(temp)

    # loading input image
    img = Image.open(inputImageName)
    imageData = list(img.getdata())
    imageDataArray = []
    columns = 0
    rows = []

    # storing image data as an array
    for pixel in imageData:
        rows.append(pixel)
        columns += 1
        if columns == 395:
            columns = 0
            imageDataArray.append(rows)
            rows = []

    # array fo course points
    controlPoints = []
    with open(courseFile) as f:
        for line in f:
            courseData = []
            line = line.strip()
            temp = line.split()
            courseData.append(int(temp[1]))
            courseData.append(int(temp[0]))
            controlPoints.append(courseData)

    # running the A* algorithm for all [x,y] coordinates of control points
    for j in range(len(controlPoints) - 1):
        terrain = terrainData(imageDataArray, elevations)
        start = controlPoints[j]
        destination = controlPoints[j + 1]
        aStarSearch(terrain[start[0]][start[1]], terrain[destination[0]][destination[1]], terrain, speed)

    # drawing the path
    for coordinates in finalPath:
        img.putpixel((coordinates[1], coordinates[0]), (255, 0, 0))

    # saving the output image with path
    img.save(outputImageName)
    print("Length of final path: ", len(finalPath))


if __name__ == "__main__":
    main()
