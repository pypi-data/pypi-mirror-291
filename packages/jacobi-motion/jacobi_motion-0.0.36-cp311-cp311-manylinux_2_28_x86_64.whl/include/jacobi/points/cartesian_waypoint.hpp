#pragma once

#include <optional>

#include <json/json_fwd.hpp>

#include <jacobi/element.hpp>
#include <jacobi/geometry/frame.hpp>
#include <jacobi/points/waypoint.hpp>
#include <jacobi/utils/vector.hpp>


namespace jacobi {

class RobotArm;


//! A Cartesian-space waypoint with possible position, velocity, and/or acceleration values.
class CartesianWaypoint: public Element {
    using Config = StandardVector<double, DynamicDOFs>;

    static constexpr double translational_eps {1e-4}; // [m]
    static constexpr double angular_eps {1e-4}; // [rad]

public:
    //! Frame of the position.
    Frame position {Frame::Identity()};

    //! Frame of the velocity.
    Frame velocity {Frame::Identity()};

    //! Frame of the acceleration.
    Frame acceleration {Frame::Identity()};

    //! An optional joint position that is used as a reference for inverse kinematics.
    std::optional<Config> reference_config;

    //! Construct a Cartesian waypoint with given position and zero velocity and acceleration.
    CartesianWaypoint(const Frame& position, const std::optional<Config>& reference_config=std::nullopt);

    //! Construct a Cartesian waypoint with given position and velocity and zero acceleration.
    explicit CartesianWaypoint(const Frame& position, const Frame& velocity, const std::optional<Config>& reference_config=std::nullopt);

    //! Construct a Cartesian waypoint with given position, velocity, and acceleration.
    explicit CartesianWaypoint(const Frame& position, const Frame& velocity, const Frame& acceleration, const std::optional<Config>& reference_config=std::nullopt);

    explicit CartesianWaypoint();

    bool is_within(const CartesianWaypoint& other) const;
    bool is_within(const Waypoint& other, std::shared_ptr<RobotArm> robot) const;

    friend void to_json(nlohmann::json& j, const CartesianWaypoint& value);
    friend void from_json(const nlohmann::json& j, CartesianWaypoint& value);
};

}
