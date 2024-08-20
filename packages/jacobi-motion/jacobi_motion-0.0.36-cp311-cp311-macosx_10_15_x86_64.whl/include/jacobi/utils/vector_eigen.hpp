#pragma once

#include <eigen3/Eigen/Core>

// Check for Eigen version
#if !EIGEN_VERSION_AT_LEAST(3,4,0)
#error "Please provide an Eigen version of at least 3.4.0."
#endif


namespace jacobi {

//! Eigen-based vector type
constexpr static int EigenDynamicDOFs(size_t DOFs) { return DOFs >= 1 ? static_cast<int>(DOFs) : Eigen::Dynamic ; }
template<class T, size_t DOFs> using EigenVector = typename std::conditional<DOFs >= 1, Eigen::Vector<T, DOFs>, Eigen::Vector<T, Eigen::Dynamic>>::type;

}
