#pragma once

#include <optional>

#include <jacobi/collision/detail.hpp>
#include <jacobi/utils/vector.hpp>


namespace jacobi::kinematics {

//! An IK solution is returned as soon as it is precise, but might still be in collision.
struct Solution {
    using Config = StandardVector<double, DynamicDOFs>;

    //! The actual position
    Config joint_position;

    //! Is the solution collision free?
    bool collision_free {false};

    //! Possible details about the collision
    CollisionDetail collision_detail;
};

//! Result of the internal inverse kinematics (IK)
struct Result {
    //! The IK result contains a solution as soon as it is precise.
    std::optional<Solution> solution;

    //! A vector of all feasible solutions, empty if no solution was found.
    std::vector<Solution> feasible_solutions;

    //! Whether the calculation did reset to a random state and therefore ignored the reference config,
    //! currently only for numerical IK.
    bool did_reset {false};
};

}
