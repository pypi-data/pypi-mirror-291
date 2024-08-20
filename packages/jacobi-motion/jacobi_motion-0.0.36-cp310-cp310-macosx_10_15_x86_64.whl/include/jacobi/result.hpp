#pragma once


namespace jacobi {

enum Result {
    Working = 0, ///< The trajectory is calculated normally
    Finished = 1, ///< Trajectory has reached its final position
    UnknownError = -1, ///< Unclassified error
    InvalidInputError = -100, ///< Input is invalid
    StartInCollisionError = -101, ///< Start state is in collision
    GoalInCollisionError = -102, ///< Goal state is in collision
};

}
