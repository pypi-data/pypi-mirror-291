"""
Next-Generation Motion Planning for Robots. Calculates highly time-optimized, collision-free, and jerk-constrained motions in less than 1ms.
"""
from __future__ import annotations
import os
import pybind11_stubgen.typing_ext
import typing
from . import drivers
from . import exceptions
from . import robots
__all__ = ['ArbitraryPath', 'BlendedPath', 'Box', 'Camera', 'CameraStream', 'Capsule', 'CartesianRegion', 'CartesianRegionBound', 'CartesianWaypoint', 'CircularPath', 'Color', 'Convex', 'Cylinder', 'Depth', 'DepthMap', 'Element', 'Environment', 'FileReference', 'Finished', 'Frame', 'GoalInCollisionError', 'Intrinsics', 'InvalidInputError', 'JacobiError', 'LinearMotion', 'LinearPath', 'LinearSection', 'LowLevelMotion', 'Motion', 'MultiRobotPoint', 'Obstacle', 'PathFollowingMotion', 'PathType', 'Planner', 'Region', 'Result', 'Robot', 'RobotArm', 'Sampler', 'Sphere', 'StartInCollisionError', 'State', 'Studio', 'Trainer', 'Trajectory', 'Twist', 'UnknownError', 'Waypoint', 'Working', 'activate_license', 'drivers', 'exceptions', 'robots', 'start_telemetry_daemon']
class ArbitraryPath(PathType):
    """
    A wrapper for a path with arbitrary user-provided waypoints.
    """
    def __init__(self, path: list[Frame]) -> None:
        ...
    def calculate_path(self, velocity: float, delta_time: float) -> list[Frame]:
        """
        Returns the provided waypoints as the path.
        """
    @property
    def path(self) -> list[Frame]:
        """
        The path Cartesian waypoints.
        """
    @path.setter
    def path(self, arg0: list[Frame]) -> None:
        ...
class BlendedPath(PathType):
    """
    A path type for linear motion between waypoints with a circular blend to ensure motion continuity, optionally maintaining tool-to-surface orientation.
    """
    @typing.overload
    def __init__(self, waypoints: list[Frame], blend_radius: float, keep_tool_to_surface_orientation: bool = False) -> None:
        ...
    @typing.overload
    def __init__(self, waypoints: list[Frame], keep_tool_to_surface_orientation: bool = False) -> None:
        ...
    def calculate_path(self, velocity: float, delta_time: float) -> list[Frame]:
        """
        Calculate the path waypoints given a velocity and time step.
        """
    @property
    def blend_radius(self) -> float:
        """
        The blend radius for the circular blend.
        """
    @blend_radius.setter
    def blend_radius(self, arg0: float) -> None:
        ...
    @property
    def keep_tool_to_surface_orientation(self) -> bool:
        """
        Whether to maintain the tool-to-surface orientation.
        """
    @keep_tool_to_surface_orientation.setter
    def keep_tool_to_surface_orientation(self, arg0: bool) -> None:
        ...
    @property
    def waypoints(self) -> list[Frame]:
        """
        The path Cartesian waypoints.
        """
    @waypoints.setter
    def waypoints(self, arg0: list[Frame]) -> None:
        ...
class Box:
    """
    A box collision object.
    """
    def __getstate__(self) -> tuple:
        ...
    def __init__(self, x: float, y: float, z: float) -> None:
        """
        Construct a box of size x, y, z along the respective axis,
        corresponding to the width, depth, height of the box.
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
    @property
    def x(self) -> float:
        """
        Dimensions of the box [m]
        """
    @property
    def y(self) -> float:
        """
        Dimensions of the box [m]
        """
    @property
    def z(self) -> float:
        """
        Dimensions of the box [m]
        """
class Camera(Element):
    intrinsics: Intrinsics
    model: str
    def __init__(self, model: str, name: str, origin: Frame, intrinsics: Intrinsics) -> None:
        ...
class CameraStream:
    """
    Possible streams of a camera
    
    Members:
    
      Color
    
      Depth
    """
    Color: typing.ClassVar[CameraStream]  # value = <CameraStream.Color: 0>
    Depth: typing.ClassVar[CameraStream]  # value = <CameraStream.Depth: 1>
    __members__: typing.ClassVar[dict[str, CameraStream]]  # value = {'Color': <CameraStream.Color: 0>, 'Depth': <CameraStream.Depth: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Capsule:
    """
    A capsule collision object.
    """
    def __getstate__(self) -> tuple:
        ...
    def __init__(self, radius: float, length: float) -> None:
        """
        Construct a capsule with the given radius and length. As a side note,
        a capsule is computationally efficient for collision checking.
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
    @property
    def length(self) -> float:
        """
        Length of the capsule along z-axis [m]
        """
    @property
    def radius(self) -> float:
        """
        Radius of the capsule [m]
        """
class CartesianRegion(Element):
    """
    A Cartesian-space region with possible minimum and maximum position,
    velocity, and/or acceleration values.
    """
    max_acceleration: CartesianRegionBound
    max_position: CartesianRegionBound
    max_velocity: CartesianRegionBound
    min_acceleration: CartesianRegionBound
    min_position: CartesianRegionBound
    min_velocity: CartesianRegionBound
    reference_config: list[float] | None
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, min_position: CartesianRegionBound, max_position: CartesianRegionBound, reference_config: list[float] | None = None) -> None:
        ...
    @typing.overload
    def __init__(self, min_position: CartesianRegionBound, max_position: CartesianRegionBound, min_velocity: CartesianRegionBound, max_velocity: CartesianRegionBound, reference_config: list[float] | None = None) -> None:
        ...
    @typing.overload
    def __init__(self, min_position: CartesianRegionBound, max_position: CartesianRegionBound, min_velocity: CartesianRegionBound, max_velocity: CartesianRegionBound, min_acceleration: CartesianRegionBound, max_acceleration: CartesianRegionBound, reference_config: list[float] | None = None) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class CartesianRegionBound:
    """
    The min or max boundary of a Cartesian region.
    """
    alpha: float
    gamma: float
    x: float
    y: float
    z: float
    def __init__(self, x: float, y: float, z: float, gamma: float = 0.0, alpha: float = 0.0) -> None:
        ...
class CartesianWaypoint(Element):
    """
    A Cartesian-space waypoint with possible position, velocity, and/or
    acceleration values.
    """
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, position: Frame, reference_config: list[float] | None = None) -> None:
        """
        Construct a Cartesian waypoint with given position and zero velocity
        and acceleration.
        """
    @typing.overload
    def __init__(self, position: Frame, velocity: Frame, reference_config: list[float] | None = None) -> None:
        """
        Construct a Cartesian waypoint with given position and velocity and
        zero acceleration.
        """
    @typing.overload
    def __init__(self, position: Frame, velocity: Frame, acceleration: Frame, reference_config: list[float] | None = None) -> None:
        """
        Construct a Cartesian waypoint with given position, velocity, and
        acceleration.
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
    @property
    def acceleration(self) -> Frame:
        """
        Frame of the acceleration.
        """
    @acceleration.setter
    def acceleration(self, arg0: Frame) -> None:
        ...
    @property
    def position(self) -> Frame:
        """
        Frame of the position.
        """
    @position.setter
    def position(self, arg0: Frame) -> None:
        ...
    @property
    def reference_config(self) -> list[float] | None:
        """
        An optional joint position that is used as a reference for inverse
        kinematics.
        """
    @reference_config.setter
    def reference_config(self, arg0: list[float] | None) -> None:
        ...
    @property
    def velocity(self) -> Frame:
        """
        Frame of the velocity.
        """
    @velocity.setter
    def velocity(self, arg0: Frame) -> None:
        ...
class CircularPath(PathType):
    """
    A circular path type with a specified start pose, circle center, normal, and rotation angle, optionally maintaining tool-to-surface orientation.
    """
    @typing.overload
    def __init__(self, start: Frame, theta: float, center: list[float], normal: list[float], keep_tool_to_surface_orientation: bool = False) -> None:
        ...
    @typing.overload
    def __init__(self, start: Frame, goal: Frame, center: list[float], keep_tool_to_surface_orientation: bool = False) -> None:
        ...
    def calculate_path(self, velocity: float, delta_time: float) -> list[Frame]:
        """
        Calculate the path waypoints given a velocity and time step.
        """
    @property
    def center(self) -> list[float]:
        """
        The center of the circle.
        """
    @center.setter
    def center(self, arg0: list[float]) -> None:
        ...
    @property
    def keep_tool_to_surface_orientation(self) -> bool:
        """
        Whether to maintain the tool-to-surface orientation.
        """
    @keep_tool_to_surface_orientation.setter
    def keep_tool_to_surface_orientation(self, arg0: bool) -> None:
        ...
    @property
    def normal(self) -> list[float]:
        """
        The normal of the plane in which to create a circular path.
        """
    @normal.setter
    def normal(self, arg0: list[float]) -> None:
        ...
    @property
    def start(self) -> Frame:
        """
        The start pose of the circular path.
        """
    @start.setter
    def start(self, arg0: Frame) -> None:
        ...
    @property
    def theta(self) -> float:
        """
        The rotation angle of the circular path [rad].
        """
    @theta.setter
    def theta(self, arg0: float) -> None:
        ...
class Convex:
    """
    A convex mesh collision object.
    """
    @staticmethod
    def load_from_file(path: os.PathLike, scale: float | None = None) -> list[Convex]:
        """
        Load *.obj or *.stl from file
        """
    @staticmethod
    def reference_studio_file(path: os.PathLike, scale: float | None = None) -> Convex:
        """
        Reference Studio file
        """
    def __init__(self, vertices: list[typing_extensions.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(3)]], triangles: list[typing_extensions.Annotated[list[int], pybind11_stubgen.typing_ext.FixedSize(3)]]) -> None:
        ...
    @property
    def bounding_box_maximum(self) -> typing_extensions.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(3)]:
        """
        Get vector of maximum position
        """
    @property
    def bounding_box_minimum(self) -> typing_extensions.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(3)]:
        """
        Get vector of minimum position
        """
    @property
    def file_reference(self) -> FileReference | None:
        """
        Path of the object (if loaded from file)
        """
    @file_reference.setter
    def file_reference(self, arg0: FileReference | None) -> None:
        ...
    @property
    def triangles(self) -> list[...]:
        ...
    @property
    def vertices(self) -> list[..., 3, 1, 0, 3, ...]:
        ...
class Cylinder:
    """
    A cylinder collision object.
    """
    def __getstate__(self) -> tuple:
        ...
    def __init__(self, radius: float, length: float) -> None:
        """
        Construct a cylinder with the given radius and length.
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
    @property
    def length(self) -> float:
        """
        Length of the cylinder along z-axis [m]
        """
    @property
    def radius(self) -> float:
        """
        Radius of the cylinder [m]
        """
class DepthMap:
    """
    A depth map collision object.
    """
    def __getstate__(self) -> tuple:
        ...
    def __init__(self, depths: list[list[float]], x: float, y: float) -> None:
        """
        Construct a height field with the given data.
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
    @property
    def depths(self) -> list[list[float]]:
        """
        Matrix containing the depths at evenly spaced grid points
        """
    @depths.setter
    def depths(self, arg0: list[list[float]]) -> None:
        ...
    @property
    def max_depth(self) -> float:
        """
        Maximum depth until to check collisions [m]
        """
    @property
    def x(self) -> float:
        """
        Size along the x-axis [m]
        """
    @property
    def y(self) -> float:
        """
        Size along the y-axis [m]
        """
class Element:
    """
    The base element of a scene
    """
    def get_parameter(self, tag: str) -> str | None:
        """
        Reads the value of a tag parameter `param=value`. Tags are case-
        insensitive.
        """
    def has_tag(self, tag: str) -> bool:
        """
        Checks whether a tag is present on the element. Tags are case-
        insensitive.
        """
    @property
    def name(self) -> str:
        """
        The unique name of the element, for display and identification.
        """
    @name.setter
    def name(self, arg0: str) -> None:
        ...
    @property
    def origin(self) -> Frame:
        """
        Pose of the element, relative to the parent. Is called "base" for
        robots in Studio.
        """
    @origin.setter
    def origin(self, arg0: Frame) -> None:
        ...
    @property
    def tags(self) -> list[str]:
        """
        Given tags of the element, might be with a parameter `param=value`.
        """
    @tags.setter
    def tags(self, arg0: list[str]) -> None:
        ...
class Environment:
    @typing.overload
    def __init__(self, robot: Robot, safety_margin: float = 0.0) -> None:
        ...
    @typing.overload
    def __init__(self, robots: set[Robot], safety_margin: float = 0.0) -> None:
        ...
    @typing.overload
    def add_obstacle(self, obstacle: Obstacle) -> Obstacle:
        ...
    @typing.overload
    def add_obstacle(self, object: Box, origin: Frame = ..., name: str = '000000', safety_margin: float = 0.0) -> Obstacle:
        ...
    @typing.overload
    def add_obstacle(self, object: Capsule, origin: Frame = ..., name: str = '000000', safety_margin: float = 0.0) -> Obstacle:
        ...
    @typing.overload
    def add_obstacle(self, object: Convex, origin: Frame = ..., name: str = '000000', safety_margin: float = 0.0) -> Obstacle:
        ...
    @typing.overload
    def add_obstacle(self, object: list[Convex], origin: Frame = ..., name: str = '000000', safety_margin: float = 0.0) -> Obstacle:
        ...
    @typing.overload
    def add_obstacle(self, object: Cylinder, origin: Frame = ..., name: str = '000000', safety_margin: float = 0.0) -> Obstacle:
        ...
    @typing.overload
    def add_obstacle(self, object: DepthMap, origin: Frame = ..., name: str = '000000', safety_margin: float = 0.0) -> Obstacle:
        ...
    @typing.overload
    def add_obstacle(self, object: Sphere, origin: Frame = ..., name: str = '000000', safety_margin: float = 0.0) -> Obstacle:
        ...
    @typing.overload
    def add_obstacle(self, name: str, object: Box, origin: Frame = ..., name: str = '000000', safety_margin: float = 0.0) -> Obstacle:
        ...
    @typing.overload
    def add_obstacle(self, name: str, object: Capsule, origin: Frame = ..., name: str = '000000', safety_margin: float = 0.0) -> Obstacle:
        ...
    @typing.overload
    def add_obstacle(self, name: str, object: Convex, origin: Frame = ..., name: str = '000000', safety_margin: float = 0.0) -> Obstacle:
        ...
    @typing.overload
    def add_obstacle(self, name: str, object: list[Convex], origin: Frame = ..., name: str = '000000', safety_margin: float = 0.0) -> Obstacle:
        ...
    @typing.overload
    def add_obstacle(self, name: str, object: Cylinder, origin: Frame = ..., name: str = '000000', safety_margin: float = 0.0) -> Obstacle:
        ...
    @typing.overload
    def add_obstacle(self, name: str, object: DepthMap, origin: Frame = ..., name: str = '000000', safety_margin: float = 0.0) -> Obstacle:
        ...
    @typing.overload
    def add_obstacle(self, name: str, object: Sphere, origin: Frame = ..., name: str = '000000', safety_margin: float = 0.0) -> Obstacle:
        ...
    @typing.overload
    def check_collision(self, robot: Robot, joint_position: list[float]) -> bool:
        ...
    @typing.overload
    def check_collision(self, joint_position: list[float]) -> bool:
        ...
    @typing.overload
    def check_collision(self, robot: Robot, waypoint: CartesianWaypoint) -> bool:
        ...
    @typing.overload
    def check_collision(self, robot: Robot, tcp: Frame, reference_config: list[float] | None = None) -> bool:
        ...
    @typing.overload
    def check_collision(self, tcp: Frame, reference_config: list[float] | None = None) -> bool:
        ...
    @typing.overload
    def check_collision(self, waypoint: CartesianWaypoint) -> bool:
        ...
    def get_camera(self, name: str = '') -> Camera:
        """
        Get a camera from the environment
        """
    def get_collision_free_joint_position_nearby(self, joint_position: list[float], robot: Robot = None) -> list[float] | None:
        ...
    def get_obstacle(self, name: str) -> Obstacle:
        """
        Get the obstacle with the given name from the environment. Throws an
        error if no obstacle with the name exists.
        """
    def get_obstacles(self) -> list[Obstacle]:
        """
        Get all obstacles within the environment
        """
    def get_obstacles_by_tag(self, tag: str) -> list[Obstacle]:
        """
        Get all obstacles within the environment that carry the given tag.
        """
    def get_robot(self, name: str = '') -> Robot:
        """
        Get the robot with the given name from the environment. In case there
        is only a single robot in the environment, the default empty name
        argument will return this robot. Otherwise throws an error if no robot
        with the name exists.
        """
    def get_robots(self) -> list[Robot]:
        """
        Get all robots within the environment
        """
    def get_waypoint(self, name: str) -> list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion:
        """
        Get the waypoint with the given name from the environment. Throws an
        error if no waypoint with the name exists.
        """
    def get_waypoint_by_tag(self, tag: str) -> list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion | None:
        """
        Get a waypoint within the environment given a tag. If multiple
        waypoints have the same tag, the first one to be found is returned.
        """
    def get_waypoints(self) -> list[list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion]:
        """
        Get all waypoints within the environment
        """
    def get_waypoints_by_tag(self, tag: str) -> list[list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion]:
        """
        Get all waypoints within the environment given a tag.
        """
    def remove_obstacle(self, obstacle: Obstacle) -> None:
        """
        Removes the given obstacles from the environment and from all
        collision checking.
        """
    def update_depth_map(self, obstacle: Obstacle) -> None:
        """
        Updates the depths matrix of a given depth map obstacle for the
        internal collision checking.
        """
    def update_fixed_obstacles(self) -> None:
        """
        Updates all fixed obstacles for the internal collision checking. This
        should be called after changing e.g. the position or size of an
        obstacle.
        """
    def update_joint_position(self, robot: Robot, joint_position: list[float]) -> None:
        """
        Updates the joint position of the given robot for the internal
        collision checking.
        """
    @property
    def default_robot(self) -> Robot:
        ...
    @property
    def safety_margin(self) -> float:
        """
        Environment's global safety margin for collision checking [m]
        """
class FileReference:
    """
    """
    @property
    def path(self) -> os.PathLike:
        """
        Path of the object (if loaded from file)
        """
    @path.setter
    def path(self, arg0: os.PathLike) -> None:
        ...
    @property
    def scale(self) -> float | None:
        """
        Scale for loading from file
        """
    @scale.setter
    def scale(self, arg0: float | None) -> None:
        ...
class Frame:
    """
    Represents a transformation or pose in 3D Cartesian space.
    """
    @staticmethod
    def Identity() -> Frame:
        ...
    @staticmethod
    def from_euler(x: float, y: float, z: float, a: float, b: float, c: float) -> Frame:
        """
        The angles a, b, c are using the extrinsic XYZ convention.
        """
    @staticmethod
    def from_matrix(data: typing_extensions.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(16)]) -> Frame:
        ...
    @staticmethod
    def from_quaternion(x: float, y: float, z: float, qw: float, qx: float, qy: float, qz: float) -> Frame:
        ...
    @staticmethod
    def from_translation(x: float, y: float, z: float) -> Frame:
        ...
    def __getstate__(self) -> tuple:
        ...
    def __init__(self, *, x: float = 0.0, y: float = 0.0, z: float = 0.0, a: float = 0.0, b: float = 0.0, c: float = 0.0, qw: float = 1.0, qx: float = 0.0, qy: float = 0.0, qz: float = 0.0) -> None:
        ...
    def __mul__(self, arg0: Frame) -> Frame:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def angular_distance(self, other: Frame) -> float:
        """
        Calculates the angle of the rotational difference.
        """
    def interpolate(self, t: float, other: Frame) -> Frame:
        """
        Calculates a spherical linear interpolation between this and the other
        frame at the interpolation parameter t.
        """
    def inverse(self) -> Frame:
        ...
    def translational_distance(self, other: Frame) -> float:
        """
        Calculates the Euclidian norm of the position difference.
        """
    @property
    def euler(self) -> typing_extensions.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(6)]:
        """
        The angles a, b, c are using the extrinsic XYZ convention.
        """
    @property
    def matrix(self) -> typing_extensions.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(16)]:
        ...
    @property
    def quaternion(self) -> typing_extensions.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(4)]:
        ...
    @property
    def rotation(self) -> Frame:
        ...
    @property
    def translation(self) -> typing_extensions.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(3)]:
        ...
class Intrinsics:
    focal_length_x: float
    focal_length_y: float
    height: int
    optical_center_x: float
    optical_center_y: float
    width: int
    def __init__(self, focal_length_x: float, focal_length_y: float, optical_center_x: float, optical_center_y: float, width: int, height: int) -> None:
        ...
    def as_matrix(self) -> numpy.ndarray[numpy.float64]:
        ...
class JacobiError(Exception):
    pass
class LinearMotion:
    """
    Represents a request for a linear Cartesian-space motion.
    """
    @typing.overload
    def __init__(self, start: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint, goal: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint) -> None:
        ...
    @typing.overload
    def __init__(self, robot: Robot, start: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint, goal: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint) -> None:
        ...
    @typing.overload
    def __init__(self, name: str, start: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint, goal: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint) -> None:
        ...
    @typing.overload
    def __init__(self, name: str, robot: Robot, start: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint, goal: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint) -> None:
        ...
    @property
    def goal(self) -> list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint:
        """
        Goal point of the motion.
        """
    @goal.setter
    def goal(self, arg0: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint) -> None:
        ...
    @property
    def ignore_collisions(self) -> bool:
        """
        Whether to ignore collisions
        """
    @ignore_collisions.setter
    def ignore_collisions(self, arg0: bool) -> None:
        ...
    @property
    def name(self) -> str:
        """
        The unique name of the motion.
        """
    @name.setter
    def name(self, arg0: str) -> None:
        ...
    @property
    def robot(self) -> Robot:
        """
        The robot for the motion (e.g. defines the kinematics and the joint
        limits).
        """
    @property
    def start(self) -> list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint:
        """
        Start point of the motion
        """
    @start.setter
    def start(self, arg0: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint) -> None:
        ...
class LinearPath(PathType):
    """
    A path type for linear motion between two waypoints.
    """
    def __init__(self, start: Frame, goal: Frame) -> None:
        """
        Constructor for a linear path between the start and goal poses.
        """
    def calculate_path(self, velocity: float, delta_time: float) -> list[Frame]:
        """
        Calculate the path waypoints given a velocity and time step.
        """
    @property
    def goal(self) -> Frame:
        """
        The goal pose of the linear path.
        """
    @goal.setter
    def goal(self, arg0: Frame) -> None:
        ...
    @property
    def start(self) -> Frame:
        """
        The start pose of the linear path.
        """
    @start.setter
    def start(self, arg0: Frame) -> None:
        ...
class LinearSection:
    """
    Represents a linear Cartesian section for either the approach to the
    goal or the retraction from the start.
    """
    class Approximation:
        """
        To approximate the Cartesian linear motion in joint space for
        singularity-free calculation.
        
        Members:
        
          Always
        
          Never
        """
        Always: typing.ClassVar[LinearSection.Approximation]  # value = <Approximation.Always: 1>
        Never: typing.ClassVar[LinearSection.Approximation]  # value = <Approximation.Never: 0>
        __members__: typing.ClassVar[dict[str, LinearSection.Approximation]]  # value = {'Always': <Approximation.Always: 1>, 'Never': <Approximation.Never: 0>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Always: typing.ClassVar[LinearSection.Approximation]  # value = <Approximation.Always: 1>
    Never: typing.ClassVar[LinearSection.Approximation]  # value = <Approximation.Never: 0>
    approximation: LinearSection.Approximation
    def __init__(self, offset: Frame, speed: float = 1.0, approximation: LinearSection.Approximation = ..., smooth_transition: bool = True) -> None:
        ...
    @property
    def offset(self) -> Frame:
        """
        Relative linear cartesian offset from the reference pose.
        """
    @offset.setter
    def offset(self, arg0: Frame) -> None:
        ...
    @property
    def smooth_transition(self) -> bool:
        """
        Whether to use a smooth transition between this and the next or
        previous section. If false, the robot will come to a complete stop at
        the transition point.
        """
    @smooth_transition.setter
    def smooth_transition(self, arg0: bool) -> None:
        ...
    @property
    def speed(self) -> float:
        """
        Speed of the sub-motion, relative to the overall motion’s speed.
        """
    @speed.setter
    def speed(self, arg0: float) -> None:
        ...
class LowLevelMotion:
    """
    Represents a request for a low-level motion. While low level motions
    are not checked for collisions, they are much faster to compute and
    allow for more flexible constraints such as a minimum duration
    parameter.
    """
    class ControlInterface:
        """
        Members:
        
          Position
        
          Velocity
        """
        Position: typing.ClassVar[LowLevelMotion.ControlInterface]  # value = <ControlInterface.Position: 0>
        Velocity: typing.ClassVar[LowLevelMotion.ControlInterface]  # value = <ControlInterface.Velocity: 1>
        __members__: typing.ClassVar[dict[str, LowLevelMotion.ControlInterface]]  # value = {'Position': <ControlInterface.Position: 0>, 'Velocity': <ControlInterface.Velocity: 1>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    class DurationDiscretization:
        """
        Members:
        
          Continuous
        
          Discrete
        """
        Continuous: typing.ClassVar[LowLevelMotion.DurationDiscretization]  # value = <DurationDiscretization.Continuous: 0>
        Discrete: typing.ClassVar[LowLevelMotion.DurationDiscretization]  # value = <DurationDiscretization.Discrete: 1>
        __members__: typing.ClassVar[dict[str, LowLevelMotion.DurationDiscretization]]  # value = {'Continuous': <DurationDiscretization.Continuous: 0>, 'Discrete': <DurationDiscretization.Discrete: 1>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    class Synchronization:
        """
        Members:
        
          Phase
        
          Time
        
          TimeIfNecessary
        
          None
        """
        None: typing.ClassVar[LowLevelMotion.Synchronization]  # value = <Synchronization.None: 3>
        Phase: typing.ClassVar[LowLevelMotion.Synchronization]  # value = <Synchronization.Phase: 0>
        Time: typing.ClassVar[LowLevelMotion.Synchronization]  # value = <Synchronization.Time: 1>
        TimeIfNecessary: typing.ClassVar[LowLevelMotion.Synchronization]  # value = <Synchronization.TimeIfNecessary: 2>
        __members__: typing.ClassVar[dict[str, LowLevelMotion.Synchronization]]  # value = {'Phase': <Synchronization.Phase: 0>, 'Time': <Synchronization.Time: 1>, 'TimeIfNecessary': <Synchronization.TimeIfNecessary: 2>, 'None': <Synchronization.None: 3>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Continuous: typing.ClassVar[LowLevelMotion.DurationDiscretization]  # value = <DurationDiscretization.Continuous: 0>
    Discrete: typing.ClassVar[LowLevelMotion.DurationDiscretization]  # value = <DurationDiscretization.Discrete: 1>
    None: typing.ClassVar[LowLevelMotion.Synchronization]  # value = <Synchronization.None: 3>
    Phase: typing.ClassVar[LowLevelMotion.Synchronization]  # value = <Synchronization.Phase: 0>
    Position: typing.ClassVar[LowLevelMotion.ControlInterface]  # value = <ControlInterface.Position: 0>
    Time: typing.ClassVar[LowLevelMotion.Synchronization]  # value = <Synchronization.Time: 1>
    TimeIfNecessary: typing.ClassVar[LowLevelMotion.Synchronization]  # value = <Synchronization.TimeIfNecessary: 2>
    Velocity: typing.ClassVar[LowLevelMotion.ControlInterface]  # value = <ControlInterface.Velocity: 1>
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, robot: Robot) -> None:
        ...
    @typing.overload
    def __init__(self, name: str) -> None:
        ...
    @typing.overload
    def __init__(self, name: str, robot: Robot) -> None:
        ...
    @property
    def control_interface(self) -> LowLevelMotion.ControlInterface:
        """
        The control interface for the motion.
        """
    @control_interface.setter
    def control_interface(self, arg0: LowLevelMotion.ControlInterface) -> None:
        ...
    @property
    def duration_discretization(self) -> LowLevelMotion.DurationDiscretization:
        """
        The duration discretization strategy for the motion.
        """
    @duration_discretization.setter
    def duration_discretization(self, arg0: LowLevelMotion.DurationDiscretization) -> None:
        ...
    @property
    def goal(self) -> Waypoint:
        """
        Goal waypoint of the motion.
        """
    @goal.setter
    def goal(self, arg0: Waypoint) -> None:
        ...
    @property
    def intermediate_positions(self) -> list[list[float]]:
        """
        List of intermediate positions. For a small number of waypoints (less
        than 16), the trajectory goes exactly through the intermediate
        waypoints. For a larger number of waypoints, first a filtering
        algorithm is used to keep the resulting trajectory close to the
        original waypoints.
        """
    @intermediate_positions.setter
    def intermediate_positions(self, arg0: list[list[float]]) -> None:
        ...
    @property
    def minimum_duration(self) -> float | None:
        """
        A minimum duration of the motion.
        """
    @minimum_duration.setter
    def minimum_duration(self, arg0: float | None) -> None:
        ...
    @property
    def name(self) -> str:
        """
        The unique name of the motion.
        """
    @name.setter
    def name(self, arg0: str) -> None:
        ...
    @property
    def robot(self) -> Robot:
        """
        The robot for the motion (e.g. defines the kinematics and the joint
        limits).
        """
    @property
    def start(self) -> Waypoint:
        """
        Start waypoint of the motion.
        """
    @start.setter
    def start(self, arg0: Waypoint) -> None:
        ...
    @property
    def synchronization(self) -> LowLevelMotion.Synchronization:
        """
        The synchronization strategy for the motion.
        """
    @synchronization.setter
    def synchronization(self, arg0: LowLevelMotion.Synchronization) -> None:
        ...
class Motion:
    """
    Represents a request for a collision-free point-to-point motion.
    """
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, start: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion, goal: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion) -> None:
        ...
    @typing.overload
    def __init__(self, robot: Robot, start: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion, goal: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion) -> None:
        ...
    @typing.overload
    def __init__(self, name: str, start: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion, goal: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion) -> None:
        ...
    @typing.overload
    def __init__(self, name: str, robot: Robot, start: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion, goal: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
    @property
    def cartesian_tcp_speed_cutoff(self) -> float | None:
        """
        Optional Cartesian TCP speed (translation-only) cutoff. This is a
        post-processing step.
        """
    @cartesian_tcp_speed_cutoff.setter
    def cartesian_tcp_speed_cutoff(self, arg0: float | None) -> None:
        ...
    @property
    def goal(self) -> list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion:
        """
        Goal point of the motion
        """
    @goal.setter
    def goal(self, arg0: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion) -> None:
        ...
    @property
    def ignore_collisions(self) -> bool:
        """
        Whether to ignore collisions
        """
    @ignore_collisions.setter
    def ignore_collisions(self, arg0: bool) -> None:
        ...
    @property
    def initial_waypoints(self) -> list[list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint] | None:
        """
        Optional initial waypoints to start the optimization with (don’t use
        with intermediate waypoints).
        """
    @initial_waypoints.setter
    def initial_waypoints(self, arg0: list[list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint] | None) -> None:
        ...
    @property
    def linear_approach(self) -> LinearSection | None:
        """
        Optional relative linear cartesian motion for approaching the goal
        pose.
        """
    @linear_approach.setter
    def linear_approach(self, arg0: LinearSection | None) -> None:
        ...
    @property
    def linear_retraction(self) -> LinearSection | None:
        """
        Optional relative linear cartesian motion for retracting from the
        start pose.
        """
    @linear_retraction.setter
    def linear_retraction(self, arg0: LinearSection | None) -> None:
        ...
    @property
    def name(self) -> str:
        """
        The unique name of the motion.
        """
    @name.setter
    def name(self, arg0: str) -> None:
        ...
    @property
    def orientation_loss_weight(self) -> float:
        """
        Weight of the loss minimizing the maximizing deviation of the end-
        effector orientation to the target value.
        """
    @orientation_loss_weight.setter
    def orientation_loss_weight(self, arg0: float) -> None:
        ...
    @property
    def orientation_target(self) -> typing_extensions.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(3)]:
        """
        Target vector pointing in the direction of the end-effector (TCP)
        orientation in the global coordinate system.
        """
    @orientation_target.setter
    def orientation_target(self, arg0: typing_extensions.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(3)]) -> None:
        ...
    @property
    def path_length_loss_weight(self) -> float:
        """
        Weight of the loss minimizing the path length of the trajectory.
        """
    @path_length_loss_weight.setter
    def path_length_loss_weight(self, arg0: float) -> None:
        ...
    @property
    def robot(self) -> Robot:
        """
        The robot for the motion (e.g. defines the kinematics and the joint
        limits).
        """
    @property
    def soft_collision_goal(self) -> bool:
        """
        Enables soft collision checking at the goal of the motion. Then, the
        item obstacle of the robot is allowed to be in collision at the goal
        point, but minimizes the time in collision and allows going into
        collision only once.
        """
    @soft_collision_goal.setter
    def soft_collision_goal(self, arg0: bool) -> None:
        ...
    @property
    def soft_collision_start(self) -> bool:
        """
        Enables soft collision checking at the start of the motion. Then, the
        item obstacle of the robot is allowed to be in collision at the start
        point. The trajectory will move the item out of collision, and won’t
        allow a collision thereafter.
        """
    @soft_collision_start.setter
    def soft_collision_start(self, arg0: bool) -> None:
        ...
    @property
    def start(self) -> list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion:
        """
        Start point of the motion
        """
    @start.setter
    def start(self, arg0: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion) -> None:
        ...
    @property
    def waypoints(self) -> list[list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint]:
        """
        Intermediate waypoints that the motion passes through exactly. The
        list of waypoints is limited to less than four, otherwise please take
        a look at LowLevelMotion.
        """
    @waypoints.setter
    def waypoints(self, arg0: list[list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint]) -> None:
        ...
class MultiRobotPoint:
    def __init__(self, map: dict[..., list[float] | Waypoint | CartesianWaypoint]) -> None:
        ...
class Obstacle(Element):
    """
    """
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, collision: Box, origin: Frame = ..., color: str = '000000', safety_margin: float = 0.0) -> None:
        ...
    @typing.overload
    def __init__(self, collision: Capsule, origin: Frame = ..., color: str = '000000', safety_margin: float = 0.0) -> None:
        ...
    @typing.overload
    def __init__(self, collision: Convex, origin: Frame = ..., color: str = '000000', safety_margin: float = 0.0) -> None:
        ...
    @typing.overload
    def __init__(self, collision: list[Convex], origin: Frame = ..., color: str = '000000', safety_margin: float = 0.0) -> None:
        ...
    @typing.overload
    def __init__(self, collision: Cylinder, origin: Frame = ..., color: str = '000000', safety_margin: float = 0.0) -> None:
        ...
    @typing.overload
    def __init__(self, collision: DepthMap, origin: Frame = ..., color: str = '000000', safety_margin: float = 0.0) -> None:
        ...
    @typing.overload
    def __init__(self, collision: Sphere, origin: Frame = ..., color: str = '000000', safety_margin: float = 0.0) -> None:
        ...
    @typing.overload
    def __init__(self, name: str, collision: Box, origin: Frame = ..., color: str = '000000', safety_margin: float = 0.0) -> None:
        ...
    @typing.overload
    def __init__(self, name: str, collision: Capsule, origin: Frame = ..., color: str = '000000', safety_margin: float = 0.0) -> None:
        ...
    @typing.overload
    def __init__(self, name: str, collision: Convex, origin: Frame = ..., color: str = '000000', safety_margin: float = 0.0) -> None:
        ...
    @typing.overload
    def __init__(self, name: str, collision: list[Convex], origin: Frame = ..., color: str = '000000', safety_margin: float = 0.0) -> None:
        ...
    @typing.overload
    def __init__(self, name: str, collision: Cylinder, origin: Frame = ..., color: str = '000000', safety_margin: float = 0.0) -> None:
        ...
    @typing.overload
    def __init__(self, name: str, collision: DepthMap, origin: Frame = ..., color: str = '000000', safety_margin: float = 0.0) -> None:
        ...
    @typing.overload
    def __init__(self, name: str, collision: Sphere, origin: Frame = ..., color: str = '000000', safety_margin: float = 0.0) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def with_origin(self, origin: Frame) -> Obstacle:
        ...
    @property
    def collision(self) -> Box | Capsule | Convex | list[Convex] | Cylinder | DepthMap | Sphere:
        """
        The object for collision checking (and/or visualization).
        """
    @collision.setter
    def collision(self, arg0: Box | Capsule | Convex | list[Convex] | Cylinder | DepthMap | Sphere) -> None:
        ...
    @property
    def color(self) -> str:
        """
        The hex-string representation of the obstacle’s color, without the
        leading #.
        """
    @color.setter
    def color(self, arg0: str) -> None:
        ...
    @property
    def for_collision(self) -> bool:
        """
        Whether this obstacle is used for collision checking.
        """
    @property
    def for_visual(self) -> bool:
        """
        Whether this obstacle is used for visualization.
        """
    @property
    def robot(self) -> ...:
        ...
    @property
    def safety_margin(self) -> float:
        """
        An additional obstacle-specific safety margin for collision checking
        (on top of the environment's global safety margin).
        """
    @safety_margin.setter
    def safety_margin(self, arg0: float) -> None:
        ...
class PathFollowingMotion:
    """
    Represents a request for a Cartesian-space motion to be followed by the end-effector.
    """
    @typing.overload
    def __init__(self, path_type: PathType, velocity: float = 50.0) -> None:
        ...
    @typing.overload
    def __init__(self, name: str, path_type: PathType, velocity: float = 50.0) -> None:
        ...
    @typing.overload
    def __init__(self, robot: Robot, path_type: PathType, velocity: float = 50.0) -> None:
        ...
    @typing.overload
    def __init__(self, name: str, robot: Robot, path_type: PathType, velocity: float = 50.0) -> None:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    def calculate_path(self, delta_time: float) -> list[Frame]:
        """
        Calculate the path waypoints given the delta time, based on the feasible velocity.
        """
    def robot_arm(self) -> RobotArm:
        """
        Returns the robot arm associated with the motion, if available.
        """
    @property
    def feasible_velocity(self) -> float:
        """
        The feasible velocity of the end-effector achieved after planning [m/s] (only used if soft_failure is true).
        """
    @feasible_velocity.setter
    def feasible_velocity(self, arg0: float) -> None:
        ...
    @property
    def name(self) -> str:
        """
        The unique name of the motion.
        """
    @name.setter
    def name(self, arg0: str) -> None:
        ...
    @property
    def path_type(self) -> PathType:
        """
        The Cartesian path to follow.
        """
    @path_type.setter
    def path_type(self, arg0: PathType) -> None:
        ...
    @property
    def robot(self) -> Robot:
        """
        The robot for the motion (e.g. defines the kinematics and the joint limits).
        """
    @robot.setter
    def robot(self, arg0: Robot) -> None:
        ...
    @property
    def soft_failure(self) -> bool:
        """
        If true, the planner will adjust path velocity until a solution until velocity limits are satisfied.
        """
    @soft_failure.setter
    def soft_failure(self, arg0: bool) -> None:
        ...
    @property
    def velocity(self) -> float:
        """
        The desired velocity of the end-effector [m/s].
        """
    @velocity.setter
    def velocity(self, arg0: float) -> None:
        ...
class PathType:
    def calculate_path(self, velocity: float, delta_time: float) -> list[Frame]:
        ...
class Planner:
    """
    """
    initial_pertubation_scale: float
    max_break_steps: int
    max_calculation_duration: float | None
    max_optimization_steps: int
    meaningful_loss_improvement: float
    min_calculation_duration: float | None
    pertubation_change_steps: int
    pertubation_scale_change: float
    pre_collision_check_resolution: float
    pre_minimum_samples: int
    @staticmethod
    def load_from_json_file(file: os.PathLike, base_path: os.PathLike) -> Planner:
        ...
    @staticmethod
    def load_from_project_file(file: os.PathLike) -> Planner:
        """
        Loads a planner from a project file
        """
    @staticmethod
    def load_from_studio(name: str) -> Planner:
        """
        Loads a planner from a Studio project. Make sure to have the access
        token set as an environment variable.
        """
    @typing.overload
    def __init__(self, environment: Environment, delta_time: float) -> None:
        """
        Create a planner with an environment and a specific delta time
        parameter.
        """
    @typing.overload
    def __init__(self, robot: Robot, delta_time: float) -> None:
        """
        Create a planner with the robot inside an empty environment and a
        specific delta time parameter.
        """
    @typing.overload
    def __init__(self, environment: Environment) -> None:
        """
        Create a planner with an environment.
        """
    @typing.overload
    def __init__(self, robot: Robot) -> None:
        """
        Create a planner with the robot inside an empty environment.
        """
    def add_motion(self, motion: Motion) -> None:
        """
        Add (or update when name already exists) a motion to the planner
        """
    def get_motion(self, name: str) -> Motion | LinearMotion | LowLevelMotion | PathFollowingMotion:
        """
        Get all loaded motions
        """
    def load_motion_plan(self, file: os.PathLike) -> None:
        """
        Load a *.jacobi-plan motion plan for accelerating the planning
        calculation.
        """
    @typing.overload
    def plan(self, start: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion, goal: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion) -> Trajectory | None:
        ...
    @typing.overload
    def plan(self, motion: Motion, start: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | None = None, goal: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | None = None) -> Trajectory | None:
        ...
    @typing.overload
    def plan(self, motion: LinearMotion) -> Trajectory | None:
        ...
    @typing.overload
    def plan(self, motion: LowLevelMotion) -> Trajectory | None:
        ...
    @typing.overload
    def plan(self, motion: PathFollowingMotion) -> Trajectory | None:
        ...
    @typing.overload
    def plan(self, name: str, start: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | None = None, goal: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | None = None) -> Trajectory | None:
        ...
    @typing.overload
    def plan(self, motions: list[Motion | LinearMotion | LowLevelMotion | PathFollowingMotion]) -> list[Trajectory] | None:
        ...
    def set_seed(self, seed: int | None) -> None:
        ...
    @property
    def delta_time(self) -> float:
        """
        The time step for sampling the trajectories in [s]. Usually, this
        should correspond to the control rate of the robot.
        """
    @property
    def environment(self) -> Environment:
        """
        The current environment to plan robot motions in
        """
    @environment.setter
    def environment(self, arg0: Environment) -> None:
        ...
    @property
    def last_calculation_duration(self) -> float:
        ...
    @property
    def last_calculation_result(self) -> Result:
        ...
    @property
    def last_intermediate_positions(self) -> list[list[float]]:
        ...
class Region(Element):
    """
    A joint-space region with possible position, velocity, and/or
    acceleration values.
    """
    max_acceleration: list[float]
    max_position: list[float]
    max_velocity: list[float]
    min_acceleration: list[float]
    min_position: list[float]
    min_velocity: list[float]
    def __getstate__(self) -> tuple:
        ...
    def __init__(self, min_position: list[float], max_position: list[float]) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def is_within(self, other: Waypoint) -> bool:
        ...
class Result:
    """
    Members:
    
      Working
    
      Finished
    
      UnknownError
    
      InvalidInputError
    
      StartInCollisionError
    
      GoalInCollisionError
    """
    Finished: typing.ClassVar[Result]  # value = <Result.Finished: 1>
    GoalInCollisionError: typing.ClassVar[Result]  # value = <Result.GoalInCollisionError: -102>
    InvalidInputError: typing.ClassVar[Result]  # value = <Result.InvalidInputError: -100>
    StartInCollisionError: typing.ClassVar[Result]  # value = <Result.StartInCollisionError: -101>
    UnknownError: typing.ClassVar[Result]  # value = <Result.UnknownError: -1>
    Working: typing.ClassVar[Result]  # value = <Result.Working: 0>
    __members__: typing.ClassVar[dict[str, Result]]  # value = {'Working': <Result.Working: 0>, 'Finished': <Result.Finished: 1>, 'UnknownError': <Result.UnknownError: -1>, 'InvalidInputError': <Result.InvalidInputError: -100>, 'StartInCollisionError': <Result.StartInCollisionError: -101>, 'GoalInCollisionError': <Result.GoalInCollisionError: -102>}
    def __and__(self, other: typing.Any) -> typing.Any:
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __ge__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __gt__(self, other: typing.Any) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __invert__(self) -> typing.Any:
        ...
    def __le__(self, other: typing.Any) -> bool:
        ...
    def __lt__(self, other: typing.Any) -> bool:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __or__(self, other: typing.Any) -> typing.Any:
        ...
    def __rand__(self, other: typing.Any) -> typing.Any:
        ...
    def __repr__(self) -> str:
        ...
    def __ror__(self, other: typing.Any) -> typing.Any:
        ...
    def __rxor__(self, other: typing.Any) -> typing.Any:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    def __xor__(self, other: typing.Any) -> typing.Any:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Robot:
    """
    """
    base: Frame
    @staticmethod
    def from_model(model: str) -> Robot:
        ...
    def __repr__(self) -> str:
        ...
    def set_speed(self, speed: float) -> None:
        ...
    @property
    def control_rate(self) -> float | None:
        ...
    @property
    def id(self) -> int:
        ...
    @property
    def max_acceleration(self) -> list[float]:
        ...
    @property
    def max_jerk(self) -> list[float]:
        ...
    @property
    def max_position(self) -> list[float]:
        ...
    @property
    def max_velocity(self) -> list[float]:
        ...
    @property
    def min_position(self) -> list[float]:
        ...
    @property
    def model(self) -> str:
        """
        The model name of the robot
        """
    @model.setter
    def model(self, arg0: str) -> None:
        ...
    @property
    def name(self) -> str:
        """
        The name (id) of the robot arm
        """
    @name.setter
    def name(self, arg0: str) -> None:
        ...
class RobotArm(Robot):
    """
    """
    flange_to_tcp: Frame
    link_obstacles: list[Obstacle]
    def calculate_tcp(self, joint_position: list[float]) -> Frame:
        """
        Calculates the forward_kinematics and returns the frame of the robot’s
        TCP.
        """
    def calculate_tcp_speed(self, joint_position: list[float], joint_velocity: list[float]) -> float:
        """
        Calculates the Cartesian speed (translation-only) of the TCP
        """
    @typing.overload
    def inverse_kinematics(self, waypoint: CartesianWaypoint) -> list[float] | None:
        ...
    @typing.overload
    def inverse_kinematics(self, tcp: Frame, reference_config: list[float] | None = None) -> list[float] | None:
        ...
    def set_speed(self, speed: float) -> None:
        """
        Sets the velocity, acceleration, and jerk limits to a factor [0, 1] of
        their respective default (maximum) values.
        """
    @property
    def default_position(self) -> list[float]:
        """
        The default robot position - used for initializing the current robot
        position.
        """
    @property
    def degrees_of_freedom(self) -> int:
        """
        The degrees of freedom (or number of axis) of the robot.
        """
    @property
    def end_effector_obstacle(self) -> Obstacle | None:
        """
        An (optional) obstacle attached to the robot’s flange.
        """
    @end_effector_obstacle.setter
    def end_effector_obstacle(self, arg0: Obstacle | None) -> None:
        ...
    @property
    def item_obstacle(self) -> Obstacle | None:
        """
        An (optional) obstacle attached to the robot’s TCP.
        """
    @item_obstacle.setter
    def item_obstacle(self, arg0: Obstacle | None) -> None:
        ...
    @property
    def max_acceleration(self) -> list[float]:
        """
        Maximum absolute acceleration for each joint. [rad/s^2]
        """
    @max_acceleration.setter
    def max_acceleration(self, arg0: list[float]) -> None:
        ...
    @property
    def max_jerk(self) -> list[float]:
        """
        Maximum absolute jerk for each joint. [rad/s^3]
        """
    @max_jerk.setter
    def max_jerk(self, arg0: list[float]) -> None:
        ...
    @property
    def max_position(self) -> list[float]:
        """
        Maximum position for each joint. [rad]
        """
    @max_position.setter
    def max_position(self, arg0: list[float]) -> None:
        ...
    @property
    def max_velocity(self) -> list[float]:
        """
        Maximum absolute velocity for each joint. [rad/s]
        """
    @max_velocity.setter
    def max_velocity(self, arg0: list[float]) -> None:
        ...
    @property
    def min_position(self) -> list[float]:
        """
        Minimum position for each joint. [rad]
        """
    @min_position.setter
    def min_position(self, arg0: list[float]) -> None:
        ...
    @property
    def number_joints(self) -> int:
        ...
    @property
    def tcp(self) -> Frame:
        ...
    @property
    def tcp_acceleration(self) -> Twist:
        ...
    @property
    def tcp_position(self) -> Frame:
        ...
    @property
    def tcp_velocity(self) -> Twist:
        ...
class Sampler:
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, seed: int) -> None:
        ...
    @typing.overload
    def sample(self, region: Region) -> Waypoint:
        ...
    @typing.overload
    def sample(self, cartesian_region: CartesianRegion) -> CartesianWaypoint:
        ...
class Sphere:
    """
    A sphere collision object.
    """
    def __getstate__(self) -> tuple:
        ...
    def __init__(self, radius: float) -> None:
        """
        Construct a sphere with the given radius.
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
    @property
    def radius(self) -> float:
        """
        Radius of the sphere [m]
        """
class State:
    """
    The complete kinematic state of a robot along a trajectory
    """
    def __init__(self) -> None:
        ...
    def __len__(self) -> int:
        """
        Get the degrees of freedom of the joint space
        """
    def __repr__(self) -> str:
        ...
    @property
    def acceleration(self) -> list[float]:
        """
        Joint acceleration [rad/s^2]
        """
    @acceleration.setter
    def acceleration(self, arg0: list[float]) -> None:
        ...
    @property
    def position(self) -> list[float]:
        """
        Joint position [rad]
        """
    @position.setter
    def position(self, arg0: list[float]) -> None:
        ...
    @property
    def time(self) -> float:
        """
        The unscaled time
        """
    @time.setter
    def time(self, arg0: float) -> None:
        ...
    @property
    def velocity(self) -> list[float]:
        """
        Joint velocity [rad/s]
        """
    @velocity.setter
    def velocity(self, arg0: list[float]) -> None:
        ...
class Studio:
    """
    Helper class to connect and visualize trajectories and events in
    Jacobi Studio.
    """
    class Action:
        """
        An action that can be performed in Jacobi Studio, e.g. setting a robot
        to a specific joint position or adding an obstacle to the environment.
        """
    class Events:
        """
        A container that maps a specific timing to one or multiple actions.
        The static methods of this class do not change the visualization in
        Jacobi Studio immediately, but only return an action that can be
        executed later (e.g. alongside a trajectory).
        """
        @staticmethod
        def add_camera(camera: Camera) -> Studio.Action:
            """
            Returns an action that adds a camera.
            """
        @staticmethod
        def add_obstacle(obstacle: Obstacle) -> Studio.Action:
            """
            Returns an action that adds the given obstacle to the environment.
            """
        @staticmethod
        def add_robot(robot: Robot) -> Studio.Action:
            """
            Returns an action that adds the given robot to the environment.
            """
        @staticmethod
        def add_waypoint(point: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion) -> Studio.Action:
            """
            Returns an action that adds the given Cartesian waypoint to the
            environment.
            """
        @staticmethod
        def remove_camera(camera: Camera) -> Studio.Action:
            """
            Returns an action that removes a camera.
            """
        @staticmethod
        def remove_obstacle(obstacle: Obstacle) -> Studio.Action:
            """
            Returns an action that removes the given obstacle (by name) from the
            environment.
            """
        @staticmethod
        def set_camera_depth_map(depths: list[list[float]], x: float, y: float, camera: Camera = None) -> Studio.Action:
            """
            Returns an action that sets the depth map visualization of a camera.
            """
        @staticmethod
        def set_camera_image_encoded(image: str, camera: Camera) -> Studio.Action:
            """
            Returns an action that sets an image for a camera encoded as a string.
            """
        @staticmethod
        def set_io_signal(name: str, value: int | float, robot: Robot = None) -> Studio.Action:
            """
            Returns an action that sets an I/O signal of the given robot, or the
            last active robot instead.
            """
        @staticmethod
        def set_item(obstacle: Obstacle | None, robot: Robot = None) -> Studio.Action:
            """
            Returns an action that sets the item obstacle of the given robot, or
            the last active robot instead.
            """
        @staticmethod
        def set_joint_position(joint_position: list[float], robot: Robot = None) -> Studio.Action:
            """
            Returns an action that sets the joint position of the given robot, or
            the last active robot instead.
            """
        @staticmethod
        def set_material(material: str, robot: Robot = None) -> Studio.Action:
            """
            Returns an action that sets the material of the given robot, or the
            last active robot instead.
            """
        @staticmethod
        def update_camera(camera: Camera) -> Studio.Action:
            """
            Returns an action that updates a camera with the same name.
            """
        @staticmethod
        def update_obstacle(obstacle: Obstacle) -> Studio.Action:
            """
            Returns an action that updates the obstacle with the same name.
            """
        def __init__(self) -> None:
            """
            A container that maps a specific timing to one or multiple actions.
            The static methods of this class do not change the visualization in
            Jacobi Studio immediately, but only return an action that can be
            executed later (e.g. alongside a trajectory).
            """
        def __setitem__(self, arg0: float, arg1: Studio.Action) -> None:
            ...
    def __init__(self, auto_connect: bool = True, timeout: float = 3.0) -> None:
        """
        Interface Jacobi Studio via code. Connects to Jacobi Studio
        automatically - please make sure to enable the Studio Live feature in
        the Jacobi Studio settings.
        """
    def add_camera(self, camera: Camera) -> None:
        """
        Adds a camera in Jacobi Studio.
        """
    def add_obstacle(self, obstacle: Obstacle) -> None:
        """
        Adds the given obstacle to the environment.
        """
    def add_robot(self, robot: Robot) -> None:
        """
        Adds the given robot to the environment.
        """
    def add_waypoint(self, point: list[float] | Waypoint | CartesianWaypoint | MultiRobotPoint | Region | CartesianRegion) -> None:
        """
        Adds the given Cartesian waypoint to the environment.
        """
    def get_camera_image_encoded(self, stream: CameraStream, camera: Camera) -> str:
        """
        Get an image from a camera encoded as a string.
        """
    def get_joint_position(self, robot: Robot = None) -> list[float]:
        """
        Get the joint position of a robot.
        """
    def reconnect(self, timeout: float = 3.0) -> bool:
        """
        Reconnect to Studio Live
        """
    def remove_camera(self, camera: Camera) -> None:
        """
        Removes a camera in Jacobi Studio.
        """
    def remove_obstacle(self, obstacle: Obstacle) -> None:
        """
        Removes the given obstacle (by name) from the environment.
        """
    def reset(self) -> None:
        """
        Resets the environment to the state before a trajectory or events were
        run. In particular, it removes all obstacles there were added
        dynamically.
        """
    def run_action(self, action: Studio.Action) -> None:
        """
        Run the given action in Jacobi Studio.
        """
    def run_events(self, events: Studio.Events) -> None:
        """
        Run the events at the specified timings in Jacobi Studio.
        """
    def run_trajectory(self, trajectory: Trajectory, events: Studio.Events = ..., loop_forever: bool = False, robot: Robot = None) -> None:
        """
        Runs a trajectory for the given robot (or the last active robot) in
        Jacobi Studio, alongside the events at the specified timings.
        Optionally, the visualization can be looped.
        """
    def set_camera_depth_map(self, depths: list[list[float]], x: float, y: float, camera: Camera = None) -> None:
        """
        Sets the depth map visualization of a camera.
        """
    def set_camera_image_encoded(self, image: str, camera: Camera) -> None:
        """
        Sets an image for a camera encoded as a string.
        """
    def set_camera_point_cloud(self, points: list[float], camera: Camera = None) -> None:
        """
        Sets the point cloud visualization of a camera.
        """
    def set_io_signal(self, name: str, value: int | float, robot: Robot = None) -> None:
        """
        Sets an I/O signal of the given robot, or the last active robot
        instead.
        """
    def set_item(self, obstacle: Obstacle | None, robot: Robot = None) -> None:
        """
        Sets the item obstacle of the given robot, or the last active robot
        instead.
        """
    def set_joint_position(self, joint_position: list[float], robot: Robot = None) -> None:
        """
        Sets the joint position of the given robot, or the last active robot
        instead.
        """
    def set_material(self, material: str, robot: Robot = None) -> None:
        """
        Sets the material of the given robot, or the last active robot
        instead.
        """
    def update_camera(self, camera: Camera) -> None:
        """
        Updates the camera with the same name in Jacobi Studio.
        """
    def update_obstacle(self, obstacle: Obstacle) -> None:
        """
        Updates the obstacle with the same name.
        """
    @property
    def is_connected(self) -> bool:
        """
        Whether the library is connected to Studio Live
        """
    @property
    def port(self) -> int:
        """
        Port of the websocket connection
        """
    @port.setter
    def port(self, arg0: int) -> None:
        ...
    @property
    def speedup(self) -> float:
        """
        A factor to speed up or slow down running trajectories or events.
        """
    @speedup.setter
    def speedup(self, arg0: float) -> None:
        ...
class Trainer:
    class Result:
        @property
        def duration(self) -> float:
            ...
        @property
        def is_valid(self) -> bool:
            ...
        @property
        def loss(self) -> float:
            ...
    def __init__(self, environment: Environment, motion: Motion, max_number_waypoints: int) -> None:
        ...
    def calculate_motion_with_waypoints(self, start: Waypoint, goal: Waypoint, intermediate_positions: list[list[float]]) -> Trainer.Result:
        ...
    def is_direct_motion_valid(self, start: Waypoint, goal: Waypoint) -> bool:
        ...
    @property
    def max_number_waypoints(self) -> int:
        ...
class Trajectory:
    """
    A robot's trajectory as a list of positions and velocities at specific
    times
    """
    @staticmethod
    def from_json(json: str) -> Trajectory:
        """
        Loads a trajectory from a json string.
        """
    @staticmethod
    def from_json_file(file: os.PathLike) -> Trajectory:
        """
        Loads a trajectory from a *.json file.
        """
    def __getstate__(self) -> tuple:
        ...
    def __iadd__(self, arg0: Trajectory) -> Trajectory:
        ...
    def __init__(self, degrees_of_freedom: int) -> None:
        """
        Create an empty trajectory with the given degrees of freedom
        """
    def __len__(self) -> int:
        """
        The number of time steps within the trajectory.
        """
    def __repr__(self) -> str:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def append(self, other: Trajectory) -> None:
        """
        Appends another trajectory to the current one.
        """
    def as_table(self) -> str:
        """
        To pretty print the trajectory as a table of positions
        """
    def at_time(self, time: float) -> tuple:
        ...
    def back(self) -> State:
        """
        Access the last state at t=duration of the trajectory
        """
    def filter_path(self, max_distance: list[float]) -> list[list[float]]:
        """
        Filter a path of sparse waypoints from the trajectory. The path has a
        maximum distance per degree of freedom between the linear
        interpolation of the sparse waypoints and the original trajectory.
        """
    def front(self) -> State:
        """
        Access the first state at t=0 of the trajectory
        """
    def reverse(self) -> Trajectory:
        """
        Reverse the trajectory's start and goal
        """
    def slice(self, start: int, steps: int) -> Trajectory:
        """
        Slice a trajectory starting from step start for a length of steps.
        """
    def to_json(self) -> str:
        """
        Serializes a trajectory to a json string.
        """
    def to_json_file(self, file: os.PathLike) -> None:
        """
        Saves a trajectory to a *.json file.
        """
    def update_first_position(self, joint_position: list[float]) -> None:
        ...
    @property
    def accelerations(self) -> list[list[float]]:
        """
        The joint accelerations along the trajectory.
        """
    @property
    def duration(self) -> float:
        """
        The total duration in [s]
        """
    @property
    def id(self) -> str:
        """
        Field for identifying trajectories (for the user)
        """
    @id.setter
    def id(self, arg0: str) -> None:
        ...
    @property
    def motion(self) -> str:
        """
        Name of the motion this trajectory was planned for
        """
    @motion.setter
    def motion(self, arg0: str) -> None:
        ...
    @property
    def positions(self) -> list[list[float]]:
        """
        The joint positions along the trajectory.
        """
    @property
    def times(self) -> list[float]:
        """
        The exact time stamps for the position, velocity, and acceleration
        values. The times will usually be sampled at the delta_time distance
        of the Planner class, but might deviate at the final step.
        """
    @property
    def velocities(self) -> list[list[float]]:
        """
        The joint velocities along the trajectory.
        """
class Twist:
    """
    Represents a velocity in 3D Cartesian space.
    """
    def __init__(self, x: float, y: float, z: float, rx: float, ry: float, rz: float) -> None:
        ...
class Waypoint(Element):
    """
    A joint-space waypoint with possible position, velocity, and/or
    acceleration values.
    """
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, position: list[float]) -> None:
        """
        Construct a waypoint by position data.
        """
    @typing.overload
    def __init__(self, position: list[float], velocity: list[float]) -> None:
        """
        Construct a waypoint with given position and zero velocity and
        acceleration.
        """
    @typing.overload
    def __init__(self, position: list[float], velocity: list[float], acceleration: list[float]) -> None:
        """
        Construct a waypoint with given position and velocity and zero
        acceleration.
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def is_within(self, other: Waypoint) -> bool:
        ...
    @property
    def acceleration(self) -> list[float]:
        """
        The joint acceleration at the waypoint.
        """
    @acceleration.setter
    def acceleration(self, arg0: list[float]) -> None:
        ...
    @property
    def position(self) -> list[float]:
        """
        The joint position at the waypoint.
        """
    @position.setter
    def position(self, arg0: list[float]) -> None:
        ...
    @property
    def velocity(self) -> list[float]:
        """
        The joint velocity at the waypoint.
        """
    @velocity.setter
    def velocity(self, arg0: list[float]) -> None:
        ...
def activate_license() -> None:
    ...
def start_telemetry_daemon() -> int:
    ...
Color: CameraStream  # value = <CameraStream.Color: 0>
Depth: CameraStream  # value = <CameraStream.Depth: 1>
Finished: Result  # value = <Result.Finished: 1>
GoalInCollisionError: Result  # value = <Result.GoalInCollisionError: -102>
InvalidInputError: Result  # value = <Result.InvalidInputError: -100>
StartInCollisionError: Result  # value = <Result.StartInCollisionError: -101>
UnknownError: Result  # value = <Result.UnknownError: -1>
Working: Result  # value = <Result.Working: 0>
__version__: str = '0.0.37'
