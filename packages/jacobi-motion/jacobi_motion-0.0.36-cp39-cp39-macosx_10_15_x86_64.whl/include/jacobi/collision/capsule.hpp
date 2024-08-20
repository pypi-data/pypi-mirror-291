#pragma once


namespace jacobi {

//! A capsule collision object.
struct Capsule {
    //! Radius of the capsule [m]
    float radius;

    //! Length of the capsule along z-axis [m]
    float length;

    //! Construct a capsule with the given radius and length. As a side note, a capsule is computationally efficient for collision checking.
    explicit Capsule(float radius, float length): radius(radius), length(length) {}
    explicit Capsule() {}
};

}
