# Path-finding Algorithm Webpage Design Document

## 1. UI Design

### 1.1 Grid Map

<img src="/Users/zhaoxiaofeng/Library/Application Support/typora-user-images/image-20241111124123442.png" alt="image-20241111124123442" style="zoom:33%;" />

#### 1.1.1 Attribute

- Size: 20 x 20

- Grid Status (Number, Name, Datatype, Color) 

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
      - Calculated by coordinate in front-end

    - 9, distanceToEnd, double
      - Calculated by coordinate in front-end

- **All grid status are represented as a number in the map array**

  

#### 1.1.2 Interaction

- Update map when:
  - New session established 
    - Session means the different communication windows established by each individual with the front-end server
  - Press any button
    - Button is for updating map, like emptyMap, regenerateMap, nextStep, chooseAlgorithm
- Every session is independent, which means everyone sees their own map (including grid status).



### 1.2 Buttons

### 1.2.1 emptyMap

- Totally Front-end
- Just set every grid status to be 0

### 1.2.2 regenerateMap ??who decide the obstacle

- Frond-end
  - A button, Post/Get to/from Back - End
    - request a new map and all infos (current path when traversing each node, shortest path)
    - Paras: Algoirthm
      - 0: Dijkstra
      - 1: A star
      - 2: Jump Point
- Back-end
  - Return a new 2darray when received request
    - generateMap function
    - Rest API
  - Return shortest path and all infos each step.

### 1.2.3 nextStep 

- Totally Front-end
  - Traverse path and show

### 1.2.4 chooseAlgorithm

- Totally Front-end
  - API request para When pressing regenerateMap button



## 2. Data Structure

#### 2.1 Grid Map

- 2d array

#### 2.2 Shortest Path

- An array of pair<int, int>
  - ex: {(0,0), (0,1), (1,1), (2,1)}

#### 2.3 Infos each step

- Array of pair of array of pair (or any other ordered mapping data structure)

  - Ex: { Key是isVisited的点，value是isNext

    ​	(0,0) : {(0,1),(1,0)},   

    ​	(0,1) : {(1,1), (0,2)},

    ​	(1,1) : {(1,2), (2,1)},

    ​	(2,1) : {(2,2), (3,1)}

    ​	}
  
## 3. Function and Structure
- with front end
  - getResult(selectedAlgorithm, 2darray()**with obstacle) -> 2darray()
  - generateMap() -> randomly generate different 20*20 2d array with obstacle
- with Algorithm
  - initialization(2darray,selectedAlgorithm) -> Shortest Path + Infos each step
    - star point and end point are default as（0，0）and （19，19）
    - 
## 4. Algorithm

### 4.1 Dijkstra

### 4.2 A Star

### 4.3 Jump Point Search
