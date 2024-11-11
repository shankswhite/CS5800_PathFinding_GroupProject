# Path-finding Algorithm Webpage Design Document

## 1. UI Design

### 1.1 Grid Map

<img src="/Users/zhaoxiaofeng/Library/Application Support/typora-user-images/image-20241111124123442.png" alt="image-20241111124123442" style="zoom:33%;" />

#### 1.1.1 Attribute

- Size: 20 x 20

- Grid Status (Number, Name, Datatype, Color) :

  - 0, Empty

  - 1, Start Point, bool, Red

  - 2, End Point, bool, Green

  - 3, isVisited, bool, Orange

    - Nodes already traversed when traversing to the current position

  - 4, isNext, bool, Blue

    - The next set of nodes to be traversed immediately upon traversing to the current position

  - 5, isFinalPath, bool, Yellow

    - Used to determine whether showing the shortest path

  - 6, isObstacle, bool, Gray

  - 7, isBlock, bool, Black

    - isVisited == True && isObstacle == True

  - Auxiliary Status

    - 8, distanceToStart, double
      - Calculated by coordinate

    - 9, distanceToEnd, double
      - Calculated by coordinate

- All grid status are represented as a number in the map array

  

#### 1.1.2 Interaction

- Update map when:
  - New session established 
    - Session means the different communication windows established by each individual with the front-end server
  - Press any button
    - Button is for updating map, like emptyMap, regenerateMap, nextStep, chooseAlgorithm
- Every session is independent, which means everyone sees the map (including grid status) differently.



### 1.2 Buttons

### 1.2.1 emptyMap

- Totally front-end
- Just set every grid status to be 0

### 1.2.2 regenerateMap

- 





## 2. Algorithm

### 2.1 Dijkstra

### 2.2 A Star

### 2.3 Jump Point Search

