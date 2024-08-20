#pragma once

#include <string>

#include <json/json_fwd.hpp>

#include <jacobi/element.hpp>
#include <jacobi/geometry/frame.hpp>


namespace jacobi {

//! Intrinsics of a camera
struct Intrinsics {
    //! The focal length along the x-axis in pixels
    double focal_length_x;

    //! The focal length along the y-axis in pixels
    double focal_length_y;

    //! The x-coordinate of the optical center
    double optical_center_x;

    //! The y-coordinate of the optical center
    double optical_center_y;

    //! The image width [px]
    int width;

    //! The image height [px]
    int height;

    //! @brief Return the intrinsics as a 3x3 matrix.
    //!
    //! The matrix is parameterized as:
    //! [f_x   0   c_x]
    //! [ 0   f_y  c_y]
    //! [ 0    0    1 ]
    Eigen::Matrix3d as_matrix() const;

    explicit Intrinsics();
    Intrinsics(double focal_length_x, double focal_length_y, double optical_center_x, double optical_center_y, int width, int height);

    // Serialization
    void to_json(nlohmann::json& j) const;
    void from_json(const nlohmann::json& j);
};


//! Camera element
class Camera: public Element {
public:
    //! The model name of the camera
    std::string model;

    //! The camera intrinsics
    Intrinsics intrinsics;

    explicit Camera();
    Camera(const std::string& model, const std::string& name, const Frame& origin, const Intrinsics& intrinsics);

    // Serialization
    friend void to_json(nlohmann::json& j, const Camera& c);
    friend void from_json(const nlohmann::json& j, Camera& c);
};

}
