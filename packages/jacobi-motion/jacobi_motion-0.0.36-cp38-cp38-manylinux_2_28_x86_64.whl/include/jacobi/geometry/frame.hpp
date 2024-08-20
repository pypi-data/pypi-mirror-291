#pragma once

#include <jacobi/utils/vector_eigen.hpp> // Check for Eigen version before

#include <eigen3/Eigen/Geometry>
#include <eigen3/unsupported/Eigen/EulerAngles>
#include <json/json_fwd.hpp>


namespace jacobi {

//! Represents a transformation or pose in 3D Cartesian space.
struct Frame: public Eigen::Isometry3d {
    using Translation = Eigen::Translation3d;
    using EulerAngles = Eigen::EulerAngles<double, Eigen::EulerSystemXYZ>;
    using EulerParameter = std::array<double, 6>;
    using QuaternionParameter = std::array<double, 7>;

    Frame();
    Frame(const Eigen::Isometry3d& frame);

    static Frame Identity();

    static Frame from_matrix(const std::array<double, 16>& data);
    static Frame from_translation(double x, double y, double z);
    static Frame from_quaternion(double x, double y, double z, double qw, double qx, double qy, double qz);

    //! The angles a, b, c are using the extrinsic XYZ convention.
    static Frame from_euler(double x, double y, double z, double a, double b, double c);

    //! Calculates the Euclidian norm of the position difference.
    double translational_distance(const Frame& other) const;

    //! Calculates the angle of the rotational difference.
    double angular_distance(const Frame& other) const;

    //! Calculates a spherical linear interpolation between this and the other frame at the interpolation parameter t.
    Frame interpolate(double t, const Frame& other) const;

    std::array<double, 16> to_matrix() const;

    //! The angles a, b, c are using the extrinsic XYZ convention.
    std::array<double, 6> to_euler() const;

    static Frame x(double x);
    static Frame y(double y);
    static Frame z(double z);

    static Frame Rx(double c, double s);
    static Frame Ry(double c, double s);
    static Frame Rz(double c, double s);
    static Frame Rx(double a);
    static Frame Ry(double a);
    static Frame Rz(double a);

    friend void to_json(nlohmann::json& j, const Frame& value);
    friend void from_json(const nlohmann::json& j, Frame& value);
};

}
