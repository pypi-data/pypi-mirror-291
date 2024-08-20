#pragma once


namespace jacobi {

//! A sphere collision object.
struct Sphere {
    //! Radius of the sphere [m]
    float radius;

    //! Construct a sphere with the given radius.
    explicit Sphere(float radius): radius(radius) {}
    explicit Sphere() {}
};

}
