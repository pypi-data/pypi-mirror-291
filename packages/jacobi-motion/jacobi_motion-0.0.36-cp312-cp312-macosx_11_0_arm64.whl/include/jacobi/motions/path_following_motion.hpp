#pragma once

#include <json/json_fwd.hpp>

#include <iostream>
#include <jacobi/points/points.hpp>

namespace jacobi {

using Config = std::vector<double>;
using Path = std::vector<Config>;
using PathWaypoints = std::vector<Frame>;
using EigenConfig = EigenVector<double, DynamicDOFs>;

class PathType {
public:
    PathType() {};

    static Eigen::Vector3d plane_normal(const Frame& wp1, const Frame& wp2, const Frame& wp3);
    static Eigen::Matrix3d rotation_matrix(const Eigen::Vector3d& axis, const double angle);
    virtual PathWaypoints calculate_path(const double velocity, const double delta_time) = 0;
};

//! A path type for linear motion between two waypoints.
class LinearPath: public PathType {
public:
    //! The start pose of the linear path.
    Frame start;

    //! The goal pose of the linear path.
    Frame goal;

    LinearPath(const Frame& start, const Frame& goal): start(start), goal(goal) {};

    PathWaypoints calculate_path(const double velocity, const double delta_time) override;
};

//! A circular path type with a specified start pose, circle center, normal, and rotation angle, optionally maintaining tool-to-surface orientation.
class CircularPath: public PathType {
public:
    //! The start pose of the circular path.
    Frame start;

    //! The rotation angle of the circular path [rad].
    double theta;

    //! The center of the circle.
    std::vector<double> center;

    //! The normal of the plane in which to create a circular path.
    std::vector<double> normal;

    //! Whether to maintain the tool-to-surface orientation.
    bool keep_tool_to_surface_orientation;

    CircularPath(const Frame& start, const double theta, const std::vector<double>& center, const std::vector<double>& normal,
                 const bool keep_tool_to_surface_orientation = false)
        : start(start), theta(theta), center(center), normal(normal), keep_tool_to_surface_orientation(keep_tool_to_surface_orientation) {};
    CircularPath(const Frame& start, const Frame& goal, const std::vector<double>& center, const bool keep_tool_to_surface_orientation = false);

    PathWaypoints calculate_path(const double velocity, const double delta_time) override;
};

//! A path type for linear motion between waypoints with a circular blend to ensure motion continuity, optionally maintaining tool-to-surface orientation.
class BlendedPath: public PathType {
public:
    //! The path Cartesian waypoints.
    PathWaypoints waypoints;

    //! The blend radius for the circular blend.
    double blend_radius;

    //! Whether to maintain the tool-to-surface orientation.
    bool keep_tool_to_surface_orientation;

    BlendedPath(const PathWaypoints& waypoints, const double blend_radius, const bool keep_tool_to_surface_orientation = false)
        : waypoints(waypoints), blend_radius(blend_radius), keep_tool_to_surface_orientation(keep_tool_to_surface_orientation) {};
    BlendedPath(const PathWaypoints& waypoints, const bool keep_tool_to_surface_orientation = false);

    PathWaypoints calculate_path(const double velocity, const double delta_time) override;
};

//! A wrapper for a path with arbitrary user-provided waypoints.
class ArbitraryPath: public PathType {
public:
    //! The path Cartesian waypoints.
    PathWaypoints path;

    ArbitraryPath(const PathWaypoints& path): path(path) {};

    PathWaypoints calculate_path(const double velocity, const double delta_time) override {
        return path;
    }
};

//! Represents a request for a Cartesian-space motion to be followed by the end-effector.
class PathFollowingMotion {
public:
    //! The unique name of the motion.
    std::string name;

    //! The robot for the motion (e.g. defines the kinematics and the joint limits).
    std::shared_ptr<Robot> robot;

    //! \internal Pointer to the original robot for the motion, used for updating the position.
    std::shared_ptr<Robot> original_robot;

    //! The Cartesian path to follow.
    std::shared_ptr<PathType> path_type;

    //! The desired velocity of the end-effector [m/s].
    double velocity {50.0};

    //! If true, the planner will adjust path velocity until a solution until velocity limits are satisfied.
    bool soft_failure {true};

    //! The feasible velocity of the end-effector achieved after planning [m/s] (only used if soft_failure is true).
    double feasible_velocity {50.0};

    explicit PathFollowingMotion(std::shared_ptr<PathType> path_type, const double velocity = 50.0): PathFollowingMotion("", path_type, velocity) { }
    explicit PathFollowingMotion(const std::string& name, std::shared_ptr<PathType> path_type, const double velocity = 50.0)
        : name(name), path_type(path_type), velocity(velocity), feasible_velocity(velocity) { }
    explicit PathFollowingMotion(std::shared_ptr<Robot> robot, std::shared_ptr<PathType> path_type, const double velocity = 50.0)
        : PathFollowingMotion("", robot, path_type, velocity) { }
    explicit PathFollowingMotion(const std::string& name, std::shared_ptr<Robot> robot, std::shared_ptr<PathType> path_type, const double velocity = 50.0);
    explicit PathFollowingMotion() { }

    PathWaypoints calculate_path(const double delta_time) {
        return path_type->calculate_path(feasible_velocity, delta_time);
    }

    std::shared_ptr<RobotArm> robot_arm() const {
        return std::dynamic_pointer_cast<RobotArm>(robot);
    };
};

}
