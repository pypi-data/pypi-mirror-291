#pragma once

#include <forward_list>
#include <map>
#include <memory>
#include <optional>
#include <set>

#include <jacobi/camera.hpp>
#include <jacobi/collision/obstacle.hpp>
#include <jacobi/collision/detail.hpp>
#include <jacobi/geometry/frame.hpp>
#include <jacobi/points/points.hpp>
#include <jacobi/robot.hpp>
#include <jacobi/utils/error.hpp>


namespace jacobi {

class Collision;
class Planner;
class Trainer;

//! The environment a robot lives in
class Environment {
    friend class Planner;
    friend class Trainer;

public:
    // The collision model of the environment
    std::shared_ptr<Collision> collision;

    //! All robots used for collision checking with default parameters
    std::map<std::string, std::shared_ptr<Robot>> robots;

    //! All robots used for collision checking with default parameters
    std::map<std::string, Point> waypoints;

    //! All static obstacles in the environment, owning the data
    std::vector<std::shared_ptr<Obstacle>> obstacles;

    //! All cameras in the environment
    std::map<std::string, std::shared_ptr<Camera>> cameras;

    //! Create an environment with a controllable robot
    explicit Environment(std::shared_ptr<Robot> robot, float safety_margin = 0.0);
    explicit Environment(const std::set<std::shared_ptr<Robot>>& robots, float safety_margin = 0.0);

    //! Environment's global safety margin for collision checking [m]
    float get_safety_margin() const;

    //! @brief Get the robot with the given name from the environment.
    //! In case there is only a single robot in the environment, the default empty name argument will return this robot.
    //! Otherwise throws an error if no robot with the name exists.
    std::shared_ptr<Robot> get_robot(const std::string& name = "") const;

    //! Get all robots within the environment
    std::vector<std::shared_ptr<Robot>> get_robots() const;

    //! Get the waypoint with the given name from the environment. Throws an error if no waypoint with the name exists.
    Point get_waypoint(const std::string& name) const;

    //! Get a waypoint within the environment given a tag. If multiple waypoints have the same tag, the first one to be found is returned.
    std::optional<Point> get_waypoint_by_tag(const std::string& tag) const;

    //! Get all waypoints within the environment given a tag.
    std::vector<Point> get_waypoints_by_tag(const std::string& tag) const;

    //! Get all waypoints within the environment
    std::vector<Point> get_waypoints() const;

    //! Get the obstacle with the given name from the environment. Throws an error if no obstacle with the name exists.
    std::shared_ptr<Obstacle> get_obstacle(const std::string& name) const;

    //! Get all obstacles within the environment that carry the given tag.
    std::vector<std::shared_ptr<Obstacle>> get_obstacles_by_tag(const std::string& tag) const;

    //! Get all obstacles within the environment
    std::vector<std::shared_ptr<Obstacle>> get_obstacles() const;

    //! Get a camera from the environment
    std::shared_ptr<Camera> get_camera(const std::string& name = "") const;

    //! Add an obstacle to the environment (and returns the pointer to it)
    std::shared_ptr<Obstacle> add_obstacle(const Obstacle& obstacle);
    std::shared_ptr<Obstacle> add_obstacle(const Box& object, const Frame& origin = Frame::Identity(), const Obstacle::Color& color = "000000", float safety_margin=0.0);
    std::shared_ptr<Obstacle> add_obstacle(const Capsule& object, const Frame& origin = Frame::Identity(), const Obstacle::Color& color = "000000", float safety_margin=0.0);
    std::shared_ptr<Obstacle> add_obstacle(const Convex& object, const Frame& origin = Frame::Identity(), const Obstacle::Color& color = "000000", float safety_margin=0.0);
    std::shared_ptr<Obstacle> add_obstacle(const ConvexVector& object, const Frame& origin = Frame::Identity(), const Obstacle::Color& color = "000000", float safety_margin=0.0);
    std::shared_ptr<Obstacle> add_obstacle(const Cylinder& object, const Frame& origin = Frame::Identity(), const Obstacle::Color& color = "000000", float safety_margin=0.0);
    std::shared_ptr<Obstacle> add_obstacle(const DepthMap& object, const Frame& origin = Frame::Identity(), const Obstacle::Color& color = "000000", float safety_margin=0.0);
    std::shared_ptr<Obstacle> add_obstacle(const Sphere& object, const Frame& origin = Frame::Identity(), const Obstacle::Color& color = "000000", float safety_margin=0.0);
    std::shared_ptr<Obstacle> add_obstacle(const std::string& name, const Box& object, const Frame& origin = Frame::Identity(), const Obstacle::Color& color = "000000", float safety_margin=0.0);
    std::shared_ptr<Obstacle> add_obstacle(const std::string& name, const Capsule& object, const Frame& origin = Frame::Identity(), const Obstacle::Color& color = "000000", float safety_margin=0.0);
    std::shared_ptr<Obstacle> add_obstacle(const std::string& name, const Convex& object, const Frame& origin = Frame::Identity(), const Obstacle::Color& color = "000000", float safety_margin=0.0);
    std::shared_ptr<Obstacle> add_obstacle(const std::string& name, const ConvexVector& object, const Frame& origin = Frame::Identity(), const Obstacle::Color& color = "000000", float safety_margin=0.0);
    std::shared_ptr<Obstacle> add_obstacle(const std::string& name, const Cylinder& object, const Frame& origin = Frame::Identity(), const Obstacle::Color& color = "000000", float safety_margin=0.0);
    std::shared_ptr<Obstacle> add_obstacle(const std::string& name, const DepthMap& object, const Frame& origin = Frame::Identity(), const Obstacle::Color& color = "000000", float safety_margin=0.0);
    std::shared_ptr<Obstacle> add_obstacle(const std::string& name, const Sphere& object, const Frame& origin = Frame::Identity(), const Obstacle::Color& color = "000000", float safety_margin=0.0);

    //! Removes the given obstacles from the environment and from all collision checking.
    void remove_obstacle(const std::shared_ptr<Obstacle>& obstacle);

    //! Updates all fixed obstacles for the internal collision checking. This should be called after changing e.g. the position or size of an obstacle.
    void update_fixed_obstacles();

    //! Updates the depths matrix of a given depth map obstacle for the internal collision checking.
    void update_depth_map(const std::shared_ptr<Obstacle>& obstacle);

    //! Updates the joint position of the given robot for the internal collision checking.
    void update_joint_position(const std::shared_ptr<Robot>& robot, const Config& joint_position);

    //! Check if a joint position is in collision
    bool check_collision(const std::shared_ptr<Robot>& robot, const Config& joint_position, CollisionDetail& detail);
    bool check_collision(const std::shared_ptr<Robot>& robot, const Config& joint_position);
    bool check_collision(const Config& joint_position);

    //! Check if there exists a collision-free inverse kinematics for the Cartesian position
    bool check_collision(const std::shared_ptr<Robot>& robot, const CartesianWaypoint& waypoint);
    bool check_collision(const std::shared_ptr<Robot>& robot, const Frame& tcp, const std::optional<Config>& reference_config = std::nullopt);
    bool check_collision(const CartesianWaypoint& waypoint);
    bool check_collision(const Frame& tcp, const std::optional<Config>& reference_config = std::nullopt);

    //! Calculate a collision free joint position close to the reference position.
    std::optional<Config> get_collision_free_joint_position_nearby(const Config& joint_position, const std::shared_ptr<Robot>& robot = nullptr);

    // Serialization helpers
    nlohmann::json obstacles_to_json() const;
    void add_obstacles(const nlohmann::json& data);
};

}
