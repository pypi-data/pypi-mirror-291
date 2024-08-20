#pragma once

#include <filesystem>
#include <functional>
#include <memory>
#include <optional>
#include <string>

#include <jacobi/collision/obstacle.hpp>
#include <jacobi/geometry/frame.hpp>
#include <jacobi/geometry/twist.hpp>
#include <jacobi/kinematics/result.hpp>
#include <jacobi/points/cartesian_waypoint.hpp>
#include <jacobi/utils/vector.hpp>
#include <jacobi/utils/vector_eigen.hpp>


namespace jacobi {

using Config = StandardVector<double, DynamicDOFs>;


namespace kinematics {
    class AnalyticIK;
    class NumericIK;
    class URAnalyticIK;
};


class RobotArm;


class Robot: public std::enable_shared_from_this<Robot> {
protected:
    //! Origin of the robot's base, relative to it's parent. Called base in Studio.
    Frame origin {Frame::Identity()};

public:
    constexpr static size_t DOFs {DynamicDOFs};
    using Config = StandardVector<double, DOFs>;

    //! ID of the robot obstacles
    size_t id {1024};

    //! The model name of the robot
    std::string model;

    //! The name (id) of the robot arm
    std::string name;

    virtual std::shared_ptr<Robot> clone() const = 0;
    virtual const std::shared_ptr<const RobotArm> get_next_arm(const std::shared_ptr<const RobotArm> arm = nullptr) const = 0;
    virtual const std::shared_ptr<RobotArm> get_next_arm(const std::shared_ptr<RobotArm> arm = nullptr) = 0;

    // Minimal interface for planning
    virtual std::optional<double> get_control_rate() const = 0;
    virtual size_t get_degrees_of_freedom() const = 0;
    virtual Config get_position() const = 0;
    virtual Config get_min_position() const = 0;
    virtual Config get_max_position() const = 0;
    virtual Config get_max_velocity() const = 0;
    virtual Config get_max_acceleration() const = 0;
    virtual Config get_max_jerk() const = 0;

    virtual void forward_position(const Config& q) = 0;
    virtual void forward_velocity(const Config& q, const Config& dq) = 0;
    virtual void forward_acceleration(const Config& q, const Config& dq, const Config& ddq) = 0;

    // Set origin / base
    virtual void set_base(const Frame& base, const Frame& parent = Frame::Identity());
    Frame base() const;

    // Helper methods
    virtual void set_speed(double speed) = 0;

    // Serialization
    virtual void to_json(nlohmann::json& j) const = 0;
    virtual void from_json(const nlohmann::json& j) = 0;

    static std::shared_ptr<Robot> from_model(const std::string& model);
    static std::shared_ptr<Robot> load_from_json(const nlohmann::json& data, const std::filesystem::path& base_path);
};

class RobotArm: public Robot {
public:
    enum class InverseKinematicsMethod {
        Analytic,
        Numeric,
        URAnalytic
    } inverse_kinematics_method;

    // Planning getters
    const std::shared_ptr<const RobotArm> get_next_arm(const std::shared_ptr<const RobotArm> arm = nullptr) const override { return !arm ? std::dynamic_pointer_cast<const RobotArm>(shared_from_this()) : nullptr; }
    const std::shared_ptr<RobotArm> get_next_arm(const std::shared_ptr<RobotArm> arm = nullptr) override { return !arm ? std::dynamic_pointer_cast<RobotArm>(shared_from_this()) : nullptr; }

    std::optional<double> get_control_rate() const override { return control_rate; }
    size_t get_degrees_of_freedom() const override { return degrees_of_freedom; }

    Config get_position() const override { return position; }
    Config get_min_position() const override { return min_position; }
    Config get_max_position() const override { return max_position; }
    Config get_max_velocity() const override { return max_velocity; }
    Config get_max_acceleration() const override { return max_acceleration; }
    Config get_max_jerk() const override { return max_jerk; }

    // For use in collision checking
    virtual void for_link_obstacle(std::function<void(const RobotArm*, size_t, const Obstacle&, bool)> yield) const;
    virtual const Frame& get_link_frame(size_t offset) const;

public:
    using Jacobian = Eigen::Matrix<double, 6, EigenDynamicDOFs(DOFs)>;

protected:
    explicit RobotArm(size_t degrees_of_freedom, const Config& default_position);
    explicit RobotArm(size_t degrees_of_freedom, size_t number_joints, const Config& default_position);

    Frame flange_to_tcp_ {Frame::Identity()};

    // Default robot limits
    Config default_max_velocity;
    Config default_max_acceleration;
    Config default_max_jerk;

public:
    //! The degrees of freedom (or number of axis) of the robot.
    const size_t degrees_of_freedom;

    //! The number of joints with links in between.
    const size_t number_joints;

    //! The default robot position - used for initializing the current robot position.
    const Config default_position;

    //! The current (or last) position of the robot used for planning. Mostly relevant for multi-robot planning.
    Config position;

    //! The (optional) default control rate. [Hz]
    std::optional<double> control_rate;

    //! The obstacles for each robot link.
    StandardVector<Obstacle, DOFs, 1> link_obstacles;

    //! An (optional) obstacle attached to the robot’s flange.
    std::optional<Obstacle> end_effector_obstacle;

    //! An (optional) obstacle attached to the robot’s TCP.
    std::optional<Obstacle> item_obstacle;

    //! Minimum position for each joint. [rad]
    Config min_position;

    //! Maximum position for each joint. [rad]
    Config max_position;

    //! Maximum absolute velocity for each joint. [rad/s]
    Config max_velocity;

    //! Maximum absolute acceleration for each joint. [rad/s^2]
    Config max_acceleration;

    //! Maximum absolute jerk for each joint. [rad/s^3]
    Config max_jerk;

    //! Sets the velocity, acceleration, and jerk limits to a factor [0, 1] of their respective default (maximum) values.
    void set_speed(double speed) override;

    // Robot frames
    StandardVector<Frame, DOFs> joint_frames;
    StandardVector<Frame, DOFs, 3> link_frames;
    StandardVector<Twist, DOFs, 3> link_velocities;
    StandardVector<Twist, DOFs, 3> link_accelerations;

    void set_base(const Frame& base, const Frame& parent = Frame::Identity()) override;

    void set_flange_to_tcp(const Frame& flange_to_tcp) { flange_to_tcp_ = flange_to_tcp; }
    Frame flange_to_tcp() const { return flange_to_tcp_; }

    Frame world_base() const { return link_frames.front(); }
    virtual Frame flange() const { return *(link_frames.end() - 2); }
    Frame tcp() const { return tcp_position(); }
    virtual Frame tcp_position() const { return link_frames.back(); }
    virtual Twist tcp_velocity() const { return link_velocities.back(); }
    virtual Twist tcp_acceleration() const { return link_accelerations.back(); }

    //! Calculates the forward_kinematics and returns the frame of the robot’s TCP.
    Frame calculate_tcp(const Config& joint_position);

    //! Calculates the Cartesian speed (translation-only) of the TCP
    double calculate_tcp_speed(const Config& joint_position, const Config& joint_velocity);
    virtual Jacobian calculate_jacobian() const = 0;

    // Inverse kinematics
    std::optional<Config> inverse_kinematics(const CartesianWaypoint& waypoint);
    std::optional<Config> inverse_kinematics(const Frame& tcp, const Config& reference_config);
    std::optional<Config> inverse_kinematics(const Frame& tcp, const std::optional<Config>& reference_config = std::nullopt);
    virtual kinematics::Result _inverse_kinematics(const Frame& tcp, const Config& reference_config) = 0;
    virtual kinematics::Result _inverse_kinematics(const Frame& tcp, const Config& reference_config, std::function<bool(const Config&, CollisionDetail&)> check) = 0;

    // Serialization
    static std::shared_ptr<RobotArm> from_model(const std::string& model);
    void to_json(nlohmann::json& j) const override;
    void from_json(const nlohmann::json& j) override;
};

}
