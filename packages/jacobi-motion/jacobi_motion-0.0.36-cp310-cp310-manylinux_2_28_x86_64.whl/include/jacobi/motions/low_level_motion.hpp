#pragma once

#include <json/json_fwd.hpp>

#include <jacobi/points/waypoint.hpp>
#include <jacobi/robot.hpp>


namespace jacobi {

//! @brief Represents a request for a low-level motion.
//! While low level motions are not checked for collisions, they are much faster to compute and allow for more
//! flexible constraints such as a minimum duration parameter.
class LowLevelMotion {
    bool operator<(const LowLevelMotion& other) const { return name < other.name; }

public:
    enum ControlInterface {
        Position,  ///< Position-control: Full control over the entire kinematic state (Default)
        Velocity,  ///< Velocity-control: Ignores the current position, target position, and velocity limits
    };

    enum Synchronization {
        Phase,  ///< Phase synchronize the DoFs when possible, else fallback to "Time" strategy (Default)
        Time,   ///< Always synchronize the DoFs to reach the target at the same time
        TimeIfNecessary,  ///< Synchronize only when necessary (e.g. for non-zero target velocity or acceleration)
        None,   ///< Calculate every DoF independently
    };

    enum DurationDiscretization {
        Continuous,  ///< Every trajectory synchronization duration is allowed (Default)
        Discrete,    ///< The trajectory synchronization duration must be a multiple of the control cycle
    };

    //! The unique name of the motion.
    std::string name;

    //! The robot for the motion (e.g. defines the kinematics and the joint limits).
    std::shared_ptr<Robot> robot;

    //! \internal Pointer to the original robot for the motion, used for updating the position.
    std::shared_ptr<Robot> original_robot;

    //! Start waypoint of the motion.
    Waypoint start;

    //! Goal waypoint of the motion.
    Waypoint goal;

    //! @brief List of intermediate positions.
    //! For a small number of waypoints (less than 16), the trajectory goes exactly through the intermediate waypoints.
    //! For a larger number of waypoints, first a filtering algorithm is used to keep the resulting trajectory close to the original waypoints.
    std::vector<Config> intermediate_positions;

    //! A minimum duration of the motion.
    std::optional<double> minimum_duration;

    //! The control interface for the motion.
    ControlInterface control_interface {ControlInterface::Position};

    //! The synchronization strategy for the motion.
    Synchronization synchronization {Synchronization::Phase};

    //! The duration discretization strategy for the motion.
    DurationDiscretization duration_discretization {DurationDiscretization::Continuous};

    explicit LowLevelMotion(const std::string& name, std::shared_ptr<Robot> robot);
    explicit LowLevelMotion(std::shared_ptr<Robot> robot): LowLevelMotion("", robot) { }
    explicit LowLevelMotion(const std::string& name): name(name) { }
    explicit LowLevelMotion() { }

    bool operator!=(const LowLevelMotion& rhs) const;
    std::shared_ptr<RobotArm> robot_arm() const { return std::dynamic_pointer_cast<RobotArm>(robot); };

    friend void to_json(nlohmann::json& j, const LowLevelMotion& value);
    friend void from_json(const nlohmann::json& j, LowLevelMotion& value);
};

}
