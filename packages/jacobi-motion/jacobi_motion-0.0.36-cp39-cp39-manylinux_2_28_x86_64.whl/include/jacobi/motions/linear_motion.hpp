#pragma once

#include <json/json_fwd.hpp>

#include <jacobi/points/points.hpp>


namespace jacobi {

//! Represents a request for a linear Cartesian-space motion.
class LinearMotion {
    bool operator<(const LinearMotion& other) const { return name < other.name; }

public:
    //! The unique name of the motion.
    std::string name;

    //! Start point of the motion
    ExactPoint start;

    //! Goal point of the motion.
    ExactPoint goal;

    //! The robot for the motion (e.g. defines the kinematics and the joint limits).
    std::shared_ptr<Robot> robot;

    //! \internal Pointer to the original robot for the motion, used for updating the position.
    std::shared_ptr<Robot> original_robot;

    //! Whether to ignore collisions
    bool ignore_collisions {true};

    explicit LinearMotion(const ExactPoint& start, const ExactPoint& goal): LinearMotion("", start, goal) { }
    explicit LinearMotion(std::shared_ptr<Robot> robot, const ExactPoint& start, const ExactPoint& goal): LinearMotion("", robot, start, goal) { }
    explicit LinearMotion(const std::string& name, const ExactPoint& start, const ExactPoint& goal): name(name), start(start), goal(goal) { }
    explicit LinearMotion(const std::string& name, std::shared_ptr<Robot> robot, const ExactPoint& start, const ExactPoint& goal);
    explicit LinearMotion() { }

    bool operator!=(const LinearMotion& rhs) const;
    std::shared_ptr<RobotArm> robot_arm() const { return std::dynamic_pointer_cast<RobotArm>(robot); };

    friend void to_json(nlohmann::json& j, const LinearMotion& value);
    friend void from_json(const nlohmann::json& j, LinearMotion& value);
};

}
