#pragma once

#include <optional>

#include <json/json_fwd.hpp>

#include <jacobi/element.hpp>
#include <jacobi/geometry/frame.hpp>
#include <jacobi/utils/vector.hpp>
#include <jacobi/points/cartesian_waypoint.hpp>


namespace jacobi {

class RobotArm;


//! The min or max boundary of a Cartesian region.
struct CartesianRegionBound {
    double x {0.0}, y {0.0}, z {0.0};
    double gamma {0.0};
    double alpha {0.0};

    explicit CartesianRegionBound() {}
    explicit CartesianRegionBound(double x, double y, double z, double gamma=0.0, double alpha=0.0): x(x), y(y), z(z), gamma(gamma), alpha(alpha) {}
};


//! A Cartesian-space region with possible minimum and maximum position, velocity, and/or acceleration values.
class CartesianRegion: public Element {
    using Config = StandardVector<double, DynamicDOFs>;

public:
    CartesianRegionBound min_position, max_position;
    CartesianRegionBound min_velocity, max_velocity;
    CartesianRegionBound min_acceleration, max_acceleration;

    std::optional<Config> reference_config;

    explicit CartesianRegion();
    explicit CartesianRegion(const Frame& origin);
    explicit CartesianRegion(const CartesianRegionBound& min_position, const CartesianRegionBound& max_position, const std::optional<Config>& reference_config=std::nullopt);
    explicit CartesianRegion(const CartesianRegionBound& min_position, const CartesianRegionBound& max_position, const CartesianRegionBound& min_velocity, const CartesianRegionBound& max_velocity, const std::optional<Config>& reference_config=std::nullopt);
    explicit CartesianRegion(const CartesianRegionBound& min_position, const CartesianRegionBound& max_position, const CartesianRegionBound& min_velocity, const CartesianRegionBound& max_velocity, const CartesianRegionBound& min_acceleration, const CartesianRegionBound& max_acceleration, const std::optional<Config>& reference_config=std::nullopt);

    bool is_within(const CartesianWaypoint& other) const;
    bool is_within(const Waypoint& other, std::shared_ptr<RobotArm> robot) const;

    friend void to_json(nlohmann::json& j, const CartesianRegion& value);
    friend void from_json(const nlohmann::json& j, CartesianRegion& value);
};

}
