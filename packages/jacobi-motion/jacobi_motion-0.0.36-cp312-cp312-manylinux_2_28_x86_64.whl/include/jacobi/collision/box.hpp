#pragma once


namespace jacobi {

//! A box collision object.
struct Box {
    //! Dimensions of the box [m]
    float x, y, z;

    //! Construct a box of size x, y, z along the respective axis, corresponding to the width, depth, height of the box.
    explicit Box(float x, float y, float z): x(x), y(y), z(z) {}
    explicit Box() {}
};

}
