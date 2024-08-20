#pragma once

#include <optional>

#include <json/json_fwd.hpp>

#include <jacobi/geometry/frame.hpp>
#include <jacobi/points/points.hpp>


namespace jacobi {

//! Represents a linear Cartesian section for either the approach to the goal or the retraction from the start.
struct LinearSection {
    //! Relative linear cartesian offset from the reference pose.
    Frame offset;

    //! Speed of the sub-motion, relative to the overall motion’s speed.
    double speed {1.0};

    //! To approximate the Cartesian linear motion in joint space for singularity-free calculation.
    enum class Approximation {
        Never,
        // TODO NearSingularity,
        Always,
    } approximation {Approximation::Never};

    //! @brief Whether to use a smooth transition between this and the next or previous section.
    //! If false, the robot will come to a complete stop at the transition point.
    bool smooth_transition {true};

    friend void to_json(nlohmann::json& j, const LinearSection& value);
    friend void from_json(const nlohmann::json& j, LinearSection& value);
};


//! Represents a request for a collision-free point-to-point motion.
class Motion {
    bool operator<(const Motion& other) const { return name < other.name; }

public:
    //! The unique name of the motion.
    std::string name;

    //! Start point of the motion
    Point start;

    //! Goal point of the motion
    Point goal;

    //! The robot for the motion (e.g. defines the kinematics and the joint limits).
    std::shared_ptr<Robot> robot;

    //! \internal Pointer to the original robot for the motion, used for updating the position.
    std::shared_ptr<Robot> original_robot;

    //! Whether to ignore collisions
    bool ignore_collisions {false};

    //! @brief Intermediate waypoints that the motion passes through exactly.
    //! The list of waypoints is limited to less than four, otherwise please take a look at LowLevelMotion.
    std::vector<ExactPoint> waypoints;

    //! Optional relative linear cartesian motion for retracting from the start pose.
    std::optional<LinearSection> linear_retraction;

    //! Optional relative linear cartesian motion for approaching the goal pose.
    std::optional<LinearSection> linear_approach;

    //! @brief Enables soft collision checking at the start of the motion.
    //! Then, the item obstacle of the robot is allowed to be in collision at the start point. The trajectory will move the item out of collision, and won’t allow a collision thereafter.
    bool soft_collision_start {false};

    //! @brief Enables soft collision checking at the goal of the motion.
    //! Then, the item obstacle of the robot is allowed to be in collision at the goal point, but minimizes the time in collision and allows going into collision only once.
    bool soft_collision_goal {false};

    //! Weight of the loss minimizing the path length of the trajectory.
    double path_length_loss_weight {0.1};

    //! Weight of the loss minimizing the maximizing deviation of the end-effector orientation to the target value.
    double orientation_loss_weight {0.0};

    //! Target vector pointing in the direction of the end-effector (TCP) orientation in the global coordinate system.
    std::array<double, 3> orientation_target {{0.0, 0.0, 1.0}};

    //! Optional Cartesian TCP speed (translation-only) cutoff. This is a post-processing step.
    std::optional<double> cartesian_tcp_speed_cutoff;

    //! Optional initial waypoints to start the optimization with (don’t use with intermediate waypoints).
    std::optional<std::vector<ExactPoint>> initial_waypoints;

    explicit Motion(const Point& start, const Point& goal): Motion("", start, goal) { }
    explicit Motion(std::shared_ptr<Robot> robot, const Point& start, const Point& goal): Motion("", robot, start, goal) { }
    explicit Motion(const std::string& name, const Point& start, const Point& goal): name(name), start(start), goal(goal) { }
    explicit Motion(const std::string& name, std::shared_ptr<Robot> robot, const Point& start, const Point& goal);
    explicit Motion() { }

    bool operator!=(const Motion& rhs) const;
    std::shared_ptr<RobotArm> robot_arm() const { return std::dynamic_pointer_cast<RobotArm>(robot); };
    bool is_within(std::shared_ptr<Robot> robot, const Waypoint& start_test, const Waypoint& goal_test) const;

    friend void to_json(nlohmann::json& j, const Motion& value);
    friend void from_json(const nlohmann::json& j, Motion& value);
};

}
