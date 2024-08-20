#pragma once

#include <jacobi/utils/vector_eigen.hpp> // Check for Eigen version before

#include <eigen3/Eigen/Dense>
#include <json/json_fwd.hpp>


namespace jacobi {

//! Represents a velocity in 3D Cartesian space.
struct Twist: public Eigen::Vector<double, 6> {
    Twist();
    Twist(double x, double y, double z, double rx, double ry, double rz);
    Twist(const std::array<double, 6>& twist);
    Twist(const Eigen::Vector<double, 6>& twist);

    Twist operator+(const Twist& other);

    Twist transform(const Eigen::Matrix3d& rotation, const Eigen::Vector3d& translation) const;
    Twist cross(const Twist& other) const;

    std::array<double, 6> to_array() const;

    friend void to_json(nlohmann::json& j, const Twist& value);
    friend void from_json(const nlohmann::json& j, Twist& value);
};

}
