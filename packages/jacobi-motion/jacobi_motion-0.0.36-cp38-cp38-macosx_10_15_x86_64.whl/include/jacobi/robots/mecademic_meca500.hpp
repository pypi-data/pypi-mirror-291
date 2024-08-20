#pragma once

#include <jacobi/robot.hpp>


namespace jacobi::robots {

class MecademicMeca500 : public RobotArm {
    const static std::array<Obstacle, 7> default_link_obstacles;
    std::shared_ptr<kinematics::AnalyticIK> ik;

public:
    explicit MecademicMeca500();
    using RobotArm::inverse_kinematics;

    std::shared_ptr<Robot> clone() const override;
    void forward_position(const Config& q) override;
    void forward_velocity(const Config& q, const Config& dq) override;
    void forward_acceleration(const Config& q, const Config& dq, const Config& ddq) override;
    Jacobian calculate_jacobian() const override;
    kinematics::Result _inverse_kinematics(const Frame& tcp, const Config& reference_config) override;
    kinematics::Result _inverse_kinematics(const Frame& tcp, const Config& reference_config, std::function<bool(const Config&, CollisionDetail&)> check) override;
};

}
