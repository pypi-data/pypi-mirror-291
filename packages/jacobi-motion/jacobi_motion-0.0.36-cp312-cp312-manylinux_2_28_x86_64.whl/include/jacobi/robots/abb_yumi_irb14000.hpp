#pragma once

#include <jacobi/geometry/frame.hpp>
#include <jacobi/robot.hpp>
#include <jacobi/robots/dual_arm.hpp>


namespace jacobi::robots {

class ABBYuMiIRB14000 : public DualArm {
    const static std::array<Obstacle, 8> default_link_obstacles;

public:
    class Arm : public RobotArm {
        std::shared_ptr<kinematics::NumericIK> ik;

    public:
        explicit Arm();
        using RobotArm::inverse_kinematics;

        std::shared_ptr<Robot> clone() const override;
        void forward_position(const Config& q) override;
        void forward_velocity(const Config& q, const Config& dq) override;
        void forward_acceleration(const Config& q, const Config& dq, const Config& ddq) override;
        Jacobian calculate_jacobian() const override;
        kinematics::Result _inverse_kinematics(const Frame& tcp, const Config& reference_config) override;
        kinematics::Result _inverse_kinematics(const Frame& tcp, const Config& reference_config, std::function<bool(const Config&, CollisionDetail&)> check) override;
    };

    explicit ABBYuMiIRB14000();
};

}
