#pragma once

#include <memory>
#include <optional>

#include <jacobi/geometry/frame.hpp>
#include <jacobi/robot.hpp>


namespace jacobi::robots {

class DualArm : public Robot {
public:
    //! The left arm of the robot
    std::shared_ptr<RobotArm> left;

    //! The right arm of the robot
    std::shared_ptr<RobotArm> right;

    explicit DualArm(std::shared_ptr<RobotArm> left, std::shared_ptr<RobotArm> right);

    std::shared_ptr<Robot> clone() const override;
    const std::shared_ptr<const RobotArm> get_next_arm(const std::shared_ptr<const RobotArm> arm) const override;
    const std::shared_ptr<RobotArm> get_next_arm(const std::shared_ptr<RobotArm> arm) override;

    std::optional<double> get_control_rate() const override;
    size_t get_degrees_of_freedom() const override;
    Config get_position() const override;
    Config get_min_position() const override;
    Config get_max_position() const override;
    Config get_max_velocity() const override;
    Config get_max_acceleration() const override;
    Config get_max_jerk() const override;

    void forward_position(const Config& q) override;
    void forward_velocity(const Config& q, const Config& dq) override;
    void forward_acceleration(const Config& q, const Config& dq, const Config& ddq) override;

    //! Helper methods
    void set_base(const Frame& base, const Frame& parent = Frame::Identity()) override;
    void set_speed(double speed) override;

    //! Serialization
    void to_json(nlohmann::json& j) const override;
    void from_json(const nlohmann::json& j) override;
};

}
