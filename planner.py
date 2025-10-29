import numpy as np

# Type of planner
POINT_PLANNER=0; TRAJECTORY_PLANNER=1



class planner:
    def __init__(self, type_):

        self.type=type_

    
    def plan(self, goalPoint=[-1.0, -1.0]):
        
        if self.type==POINT_PLANNER:
            return self.point_planner(goalPoint)
        
        elif self.type==TRAJECTORY_PLANNER:
            return self.trajectory_planner()


    def point_planner(self, goalPoint):
        x = goalPoint[0]
        y = goalPoint[1]
        return (x, y)

    # TODO Part 6: Implement the trajectories here
    def trajectory_planner(self):
        # choose trajectory type: parabola or sigmoid
        trajectory_type = 'sigmoid'  # options: 'parabola', 'sigmoid'

        points = []
        if trajectory_type == 'parabola':
            # parabola: y=x^2, x ranging from 0 to 1.5
            x_vals = np.linspace(0, 1.5, 50)  # 50 points from 0 to 1.5
            for x in x_vals:
                y = x**2
                points.append([x, y])
        elif trajectory_type == 'sigmoid':
            # sigmoid: sigma = 2/(1+exp(-2x)) - 1, x ranging from 0 to 2.5
            x_vals = np.linspace(0, 2.5, 50)  # 50 points from 0 to 2.5
            for x in x_vals:
                sigma = 2 / (1 + np.exp(-2*x)) - 1
                points.append([x, sigma])

        # the return should be a list of trajectory points: [ [x1,y1], ..., [xn,yn]]
        return points 

