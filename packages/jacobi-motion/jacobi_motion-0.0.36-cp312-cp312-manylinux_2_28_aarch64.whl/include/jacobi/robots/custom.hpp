#pragma once

#include <filesystem>
#include <optional>

#include <jacobi/robot.hpp>
#include <jacobi/utils/error.hpp>


namespace jacobi::robots {

//! A custom robot arm that can be loaded from a URDF file
class CustomRobot : public RobotArm {
    struct URDFDetails {
        std::filesystem::path file_path;

        std::string base_link_name;
        std::string end_link_name {""};
    };

    std::optional<URDFDetails> urdf_details;
    std::shared_ptr<kinematics::NumericIK> ik;

    Config filter_relevant_config(const Config& config) const;

    template<class T>
    static T concat(const T& a, const T& b) {
        auto result = a;
        result.insert(result.end(), b.begin(), b.end());
        return result;
    }

public:
    explicit CustomRobot(size_t degrees_of_freedom);
    explicit CustomRobot(size_t degrees_of_freedom, size_t number_joints);
    using RobotArm::inverse_kinematics;

    //! Possible child robot
    std::shared_ptr<RobotArm> child;

    enum class JointType {
        Revolute,
        Continuous,
        Prismatic,
        Fixed,
    };

    StandardVector<Frame, DOFs> link_translations;
    StandardVector<std::array<double, 3>, DOFs> joint_axes;
    StandardVector<JointType, DOFs> joint_types;
    StandardVector<std::string, DOFs> joint_names;

    //! The names of the joints corresponding to a joint configuration
    StandardVector<std::string, DOFs> config_joint_names;

    //! Maps joints to dofs and vice versa
    StandardVector<int, DOFs> map_joints_to_dofs;
    StandardVector<int, DOFs> map_dofs_to_joints;

    //! Load the robot from a URDF file
    static std::shared_ptr<CustomRobot> load_from_urdf_file(const std::filesystem::path& file, const std::string& base_link="base_link", const std::string& end_link="flange");

    std::shared_ptr<Robot> clone() const override;
    void forward_position(const Config& q) override;
    void forward_velocity(const Config& q, const Config& dq) override;
    void forward_acceleration(const Config& q, const Config& dq, const Config& ddq) override;
    Jacobian calculate_jacobian() const override;
    kinematics::Result _inverse_kinematics(const Frame& tcp, const Config& reference_config) override;
    kinematics::Result _inverse_kinematics(const Frame& tcp, const Config& reference_config, std::function<bool(const Config&, CollisionDetail&)> check) override;

    void for_link_obstacle(std::function<void(const RobotArm*, size_t, const Obstacle&, bool)> yield) const override;
    const Frame& get_link_frame(size_t offset) const override;

    size_t get_degrees_of_freedom() const override { return degrees_of_freedom + (child ? child->get_degrees_of_freedom() : 0.0); }
    Config get_position() const override { return child ? concat(position, child->get_position()) : position; }
    Config get_min_position() const override { return child ? concat(min_position, child->get_min_position()) : min_position; }
    Config get_max_position() const override { return child ? concat(max_position, child->get_max_position()) : max_position; }
    Config get_max_velocity() const override { return child ? concat(max_velocity, child->get_max_velocity()) : max_velocity; }
    Config get_max_acceleration() const override { return child ? concat(max_acceleration, child->get_max_acceleration()) : max_acceleration; }
    Config get_max_jerk() const override { return child ? concat(max_jerk, child->get_max_jerk()) : max_jerk; }

    Frame tcp_position() const override { return child ? child->tcp_position() : link_frames.back(); }
    Twist tcp_velocity() const override { return child ? child->tcp_velocity() : link_velocities.back(); }
    Twist tcp_acceleration() const override { return child ? child->tcp_acceleration() : link_accelerations.back(); }
};

}
