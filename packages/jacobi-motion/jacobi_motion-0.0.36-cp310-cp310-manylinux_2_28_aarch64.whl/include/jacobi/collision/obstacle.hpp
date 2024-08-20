#pragma once

#include <variant>

#include <jacobi/collision/box.hpp>
#include <jacobi/collision/capsule.hpp>
#include <jacobi/collision/convex.hpp>
#include <jacobi/collision/cylinder.hpp>
#include <jacobi/collision/depth_map.hpp>
#include <jacobi/collision/sphere.hpp>
#include <jacobi/element.hpp>
#include <jacobi/geometry/frame.hpp>
#include <jacobi/utils/error.hpp>


namespace jacobi {

class Robot;

//! An environment obstacle.
class Obstacle: public Element {
public:
    using Color = std::string;
    using Geometry = std::variant<Box, Capsule, Convex, ConvexVector, Cylinder, DepthMap, Sphere>;

    //! The hex-string representation of the obstacle’s color, without the leading #.
    Color color;

    //! Optional reference to the visual file
    std::optional<FileReference> visual;

    //! The object for collision checking (and/or visualization).
    Geometry collision;

    //! Whether this obstacle is used for visualization.
    bool for_visual {true};

    //! Whether this obstacle is used for collision checking.
    bool for_collision {true};

    //! An additional obstacle-specific safety margin for collision checking (on top of the environment's global safety margin).
    float safety_margin {0.0};

    Robot* robot;

    explicit Obstacle();
    Obstacle(const Box& collision, const Frame& origin = Frame::Identity(), const Color& color = "000000", float safety_margin = 0.0);
    Obstacle(const Capsule& collision, const Frame& origin = Frame::Identity(), const Color& color = "000000", float safety_margin = 0.0);
    Obstacle(const Convex& collision, const Frame& origin = Frame::Identity(), const Color& color = "000000", float safety_margin = 0.0);
    Obstacle(const ConvexVector& collision, const Frame& origin = Frame::Identity(), const Color& color = "000000", float safety_margin = 0.0);
    Obstacle(const Cylinder& collision, const Frame& origin = Frame::Identity(), const Color& color = "000000", float safety_margin = 0.0);
    Obstacle(const DepthMap& collision, const Frame& origin = Frame::Identity(), const Color& color = "000000", float safety_margin = 0.0);
    Obstacle(const Sphere& collision, const Frame& origin = Frame::Identity(), const Color& color = "000000", float safety_margin = 0.0);
    Obstacle(const std::string& name, const Box& collision, const Frame& origin = Frame::Identity(), const Color& color = "000000", float safety_margin = 0.0);
    Obstacle(const std::string& name, const Capsule& collision, const Frame& origin = Frame::Identity(), const Color& color = "000000", float safety_margin = 0.0);
    Obstacle(const std::string& name, const Convex& collision, const Frame& origin = Frame::Identity(), const Color& color = "000000", float safety_margin = 0.0);
    Obstacle(const std::string& name, const ConvexVector& collision, const Frame& origin = Frame::Identity(), const Color& color = "000000", float safety_margin = 0.0);
    Obstacle(const std::string& name, const Cylinder& collision, const Frame& origin = Frame::Identity(), const Color& color = "000000", float safety_margin = 0.0);
    Obstacle(const std::string& name, const DepthMap& collision, const Frame& origin = Frame::Identity(), const Color& color = "000000", float safety_margin = 0.0);
    Obstacle(const std::string& name, const Sphere& collision, const Frame& origin = Frame::Identity(), const Color& color = "000000", float safety_margin = 0.0);

    //! Clone the current obstacle and set the new origin
    Obstacle with_origin(const Frame& origin) const;

    friend void to_json(nlohmann::json& j, const Obstacle& o);
    friend void from_json(const nlohmann::json& j, Obstacle& o);
};

}
