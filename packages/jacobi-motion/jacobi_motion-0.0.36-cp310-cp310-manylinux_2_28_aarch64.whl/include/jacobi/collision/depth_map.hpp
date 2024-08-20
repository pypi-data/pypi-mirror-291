#pragma once

#include <vector>


namespace jacobi {

//! A depth map collision object.
struct DepthMap {
    using Matrix = std::vector<std::vector<double>>;

    //! Matrix containing the depths at evenly spaced grid points
    Matrix depths;

    //! Size along the x-axis [m]
    float x;

    //! Size along the y-axis [m]
    float y;

    //! Maximum depth until to check collisions [m]
    float max_depth {1e2};

    //! Construct a height field with the given data.
    explicit DepthMap(const Matrix& depths, float x, float y): depths(depths), x(x), y(y) {}
    explicit DepthMap() {}
};

}
