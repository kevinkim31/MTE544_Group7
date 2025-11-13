from mapUtilities import *
from utilities import *
from numpy import cos, sin
import numpy as np


class particle:

    def __init__(self, pose, weight):
        self.pose = pose
        self.weight = weight

    def motion_model(self, v, w, dt):
        """
        v: linear velocity
        w: angular velocity
        dt: time step
        """
        # Get current orientation
        theta = self.pose[2]

        # Update position using the differential drive kinematic model
        self.pose[0] += v * cos(theta) * dt  # x position
        self.pose[1] += v * sin(theta) * dt  # y position
        self.pose[2] += w * dt                # orientation (theta)

    def calculateParticleWeight(self, scanOutput: LaserScan, mapManipulatorInstance: mapManipulator, laser_to_ego_transformation: np.array):
        """
        Calculate the weight (likelihood) of a particle based on how well the laser scan matches the map when viewed from the particle's pose
        Parameters:
        scanOutput : LaserScan = raw laser scan data containing ranges and angles
        mapManipulatorInstance : mapManipulator = object containing the map and pre-computed likelihood field
        laser_to_ego_transformation : np.array (3x3) = SE(2) transformation matrix from laser frame to robot base frame
        """

        # STEP 1: Compute transformation from laser frame to map frame
        T = np.matmul(self.__poseToTranslationMatrix(), laser_to_ego_transformation)

        # STEP 2: Convert laser scan to Cartesian coordinates and transform to map
        _, scanCartesianHomo = convertScanToCartesian(scanOutput)
        scanInMap = np.dot(T, scanCartesianHomo.T).T # Shape: (N, 3)

        # STEP 3: Get likelihood field and convert positions to grid cells
        likelihoodField = mapManipulatorInstance.getLikelihoodField()
        cellPositions = mapManipulatorInstance.position_2_cell( # continuous position to discrete grid cell indices
            scanInMap[:, 0:2])

        # STEP 4: Filter out scan points that fall outside the map boundaries
        lm_x, lm_y = likelihoodField.shape # map dimensions

        cellPositions = cellPositions[np.logical_and.reduce(
                (cellPositions[:, 0] > 0, -cellPositions[:, 1] > 0, cellPositions[:, 0] < lm_y,  -cellPositions[:, 1] < lm_x))]

         # STEP 5: Calculate particle weight from likelihood field
        log_weights = np.log( # give probability of observing a laser return if the particle's pose were correct
            likelihoodField[-cellPositions[:, 1], cellPositions[:, 0]])
        log_weight = np.sum(log_weights) 
        weight = np.exp(log_weight) # convert back from log-space 
        weight += 1e-10 # to prevent zero weights

        # STEP 6: Store the calculated weight
        self.setWeight(weight) # = how likely this particle's pose is

    def setWeight(self, weight):
        self.weight = weight

    def getWeight(self):
        return self.weight

    def setPose(self, pose):
        self.pose = pose

    def getPose(self):
        return self.pose[0], self.pose[1], self.pose[2]

    def __poseToTranslationMatrix(self):
        x, y, th = self.getPose()

        translation = np.array([[cos(th), -sin(th), x],
                                [sin(th), cos(th), y],
                                [0, 0, 1]])

        return translation