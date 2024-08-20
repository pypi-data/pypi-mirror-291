#pragma once

#include <array>
#include <iomanip>
#include <sstream>
#include <vector>


namespace jacobi {

//! STL-based vector type
constexpr static size_t DynamicDOFs {0};
template<class T, size_t DOFs, size_t Plus = 0> using StandardVector = typename std::conditional<DOFs >= 1, std::array<T, DOFs + Plus>, std::vector<T>>::type;


//! Element-wise vector comparison
template<class T>
bool is_within(const std::vector<T>& vector, const std::vector<T>& lower, const std::vector<T>& upper) {
    for (size_t dof = 0; dof < vector.size(); ++dof) {
        if (vector[dof] < lower[dof] || vector[dof] > upper[dof]) {
            return false;
        }
    }
    return true;
}


//! Joint vector to string
template<class T>
std::string join(const std::vector<T>& vector, size_t precision = 4) {
    std::ostringstream s;
    s << std::setprecision(precision);
    for (const auto& i: vector) {
        if (&i != &vector[0]) {
            s << ", ";
        }
        s << i;
    }
    return s.str();
}

}
