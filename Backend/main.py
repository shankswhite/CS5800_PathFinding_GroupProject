from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import asyncio
from models import MapRequest, Algorithm
from session_manager import SessionManager
from pathfinding import PathFinder

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_manager = SessionManager()

def create_grid(size: Tuple[int, int], obstacle_count: int) -> np.ndarray:
    rows, cols = size
    grid = np.zeros((rows, cols), dtype=int)
    
    # Keep start and end points clear
    available_positions = [(i, j) for i in range(rows) for j in range(cols)
                         if (i, j) != (0, 0) and (i, j) != (rows-1, cols-1)]
    
    # Place obstacles randomly
    obstacle_positions = np.random.choice(
        len(available_positions), 
        size=min(obstacle_count, len(available_positions)), 
        replace=False
    )
    
    for pos_idx in obstacle_positions:
        x, y = available_positions[pos_idx]
        grid[x, y] = 1
        
        # Check if path exists (you'll need to implement this)
        pathfinder = PathFinder(grid)
        if not pathfinder.has_valid_path():
            grid[x, y] = 0
            
    return grid

@app.post("/generate-map")
async def generate_map(request: MapRequest):
    grid = create_grid(request.grid_size, request.obstacle_count)
    pathfinder = PathFinder(grid)
    
    # Calculate all steps based on selected algorithm
    if request.algorithm == Algorithm.DIJKSTRA:
        steps = pathfinder.dijkstra()
    elif request.algorithm == Algorithm.ASTAR:
        steps = pathfinder.astar()  # To be implemented
    else:
        steps = pathfinder.jump_point()  # To be implemented
    
    session_data = {
        "grid": grid,
        "algorithm": request.algorithm,
        "steps": steps,
        "current_step": 0
    }
    
    session_manager.add_session(request.session_id, session_data)
    
    return {
        "grid": grid.tolist(),
        "start": (0, 0),
        "end": (request.grid_size[0]-1, request.grid_size[1]-1)
    }

@app.post("/next-step")
async def get_next_step(session_id: str):
    session_data = session_manager.get_session(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session_data["current_step"] >= len(session_data["steps"]):
        return {"completed": True}
    
    step = session_data["steps"][session_data["current_step"]]
    session_data["current_step"] += 1
    
    return {
        "current_node": step.current_node,
        "visited_nodes": step.visited_nodes,
        "next_nodes": step.next_nodes,
        "path_so_far": step.path_so_far,
        "completed": False
    }

# Start session cleanup task
@app.on_event("startup")
async def startup_event():
    async def cleanup_task():
        while True:
            session_manager.cleanup_sessions()
            await asyncio.sleep(60)  # Check every minute
            
    asyncio.create_task(cleanup_task()) 