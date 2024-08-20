#pragma once

#include <functional>
#include <map>
#include <variant>

#include <jacobi/collision/detail.hpp>
#include <jacobi/points/waypoint.hpp>
#include <jacobi/points/cartesian_waypoint.hpp>
#include <jacobi/points/region.hpp>
#include <jacobi/points/cartesian_region.hpp>


namespace jacobi {

class Robot;


using Config = StandardVector<double, DynamicDOFs>;

namespace points {

template<class... T>
struct RobotMap: public std::map<std::string, std::variant<T...>> {
    using SharedRobotMap = const std::map<std::shared_ptr<Robot>, std::variant<T...>>;

    RobotMap() {}
    RobotMap(const SharedRobotMap& map) {
        for (const auto& [key, value]: map) {
            this->try_emplace(key->name, value);
        }
    }
};

}

using MultiRobotPoint = points::RobotMap<Config, Waypoint, CartesianWaypoint>;
using Point = std::variant<Config, Waypoint, CartesianWaypoint, MultiRobotPoint, Region, CartesianRegion>;
using ExactPoint = std::variant<Config, Waypoint, CartesianWaypoint, MultiRobotPoint>;
using RegionPoint = std::variant<Region, CartesianRegion>;


void to_json(nlohmann::json& j, const ExactPoint& value);
void from_json(const nlohmann::json& j, ExactPoint& value);

void to_json(nlohmann::json& j, const Point& value);
void from_json(const nlohmann::json& j, Point& value);


struct PointImpl {
    using CollisionCheckCallback = std::function<bool(const std::shared_ptr<Robot>&, const Config&, CollisionDetail&)>;

    static bool is_equal(const Point& a, const Point& b);
    static bool is_equal(const ExactPoint& a, const ExactPoint& b);
    static bool is_config_within(const std::shared_ptr<Robot>& robot, const Point& point, const ExactPoint& test);

    static std::optional<ExactPoint> get_state(const std::shared_ptr<Robot>& robot, const Point& point, const std::optional<ExactPoint>& test);

    // For multi-robot waypoints, return as a single concatenated joint waypoint
    static bool get_waypoint_in_joint_space(const ExactPoint& point, const std::shared_ptr<Robot>& robot, const Config& reference_config, Waypoint& result);

    // For multi-robot waypoints, return as a single concatenated joint waypoint
    static void get_start_goal_waypoints(const ExactPoint& start, const ExactPoint& goal, Waypoint& result_start, Waypoint& result_goal, const std::shared_ptr<Robot>& robot, CollisionCheckCallback collision_check_start, CollisionCheckCallback collision_check_goal);
};

}
