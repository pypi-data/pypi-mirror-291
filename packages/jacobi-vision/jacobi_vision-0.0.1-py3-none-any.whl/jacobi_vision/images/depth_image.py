import numpy as np
from numpy.typing import NDArray

from jacobi import Camera
from .image import Image


class DepthImage(Image):
    """Class for depth images."""
    def to_depth_map(self, camera: Camera, scale: int = 1) -> tuple[list, float, float]:
        """Convert the depth image to a depth map.

        Returns:
            list: the depth values
            int: Size along the x-axis [m]
            int: Size along the y-axis [m]
        """
        cloud = self.to_point_cloud(camera)
        cloud = cloud[:3, :]

        grid_x = self.data.shape[1] // scale
        grid_y = self.data.shape[0] // scale

        maxs = np.max(cloud, axis=1)
        mins = np.min(cloud, axis=1)
        depths = np.ones((grid_y, grid_x)) * maxs[2]
        # depths = np.zeros((grid_y, grid_x))
        counts = np.zeros((grid_y, grid_x))
        dim_x = maxs[0] - mins[0]
        dim_y = maxs[1] - mins[1]

        if cloud.shape[0] == 3:
            cloud = cloud.T

        for pt in cloud:
            x = (grid_x - 1) * ((pt[0] - mins[0]) / dim_x)
            y = (grid_y - 1) * ((pt[1] - mins[1]) / dim_y)
            x = int(np.floor(x))
            y = int(np.floor(y))
            # depths[y, x] += pt[2]
            counts[y, x] += 1
            if pt[2] > 0 and pt[2] < depths[y, x]:
                depths[y, x] = pt[2]

        # counts[counts == 0] = 1
        # depths /= counts
        depths[depths == 0] = maxs[2]

        return depths, dim_x, dim_y

    def to_point_cloud(self, camera: Camera) -> NDArray:
        """Convert the depth image to a point cloud in the camera frame.

        Args:
            camera (CameraDriver): A camera driver that provides the intrinsics.

        Returns:
            NDArray: An n x 3 array of points in the camera frame.
        """
        pixels = [[j, i, self.data[i, j]] for i in range(self.data.shape[0]) for j in range(self.data.shape[1])]
        pixels = np.array(pixels).T

        return self.deproject(pixels, camera)
