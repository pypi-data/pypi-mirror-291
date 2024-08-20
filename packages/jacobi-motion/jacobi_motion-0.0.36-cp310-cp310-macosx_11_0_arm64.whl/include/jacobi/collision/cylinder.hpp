#pragma once


namespace jacobi {

//! A cylinder collision object.
struct Cylinder {
    //! Radius of the cylinder [m]
    float radius;

    //! Length of the cylinder along z-axis [m]
    float length;

    //! Construct a cylinder with the given radius and length.
    explicit Cylinder(float radius, float length): radius(radius), length(length) {}
    explicit Cylinder() {}
};

}
