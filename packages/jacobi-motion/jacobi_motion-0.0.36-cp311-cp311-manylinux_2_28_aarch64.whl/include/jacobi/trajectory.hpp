#pragma once

#include <filesystem>
#include <type_traits>
#include <vector>

#include <json/json_fwd.hpp>

#include <jacobi/utils/vector.hpp>


namespace jacobi {

//! The complete kinematic state of a robot along a trajectory
struct State {
    using Config = StandardVector<double, DynamicDOFs>;

    //! The unscaled time
    double time;

    //! Joint position [rad]
    Config position;

    //! Joint velocity [rad/s]
    Config velocity;

    //! Joint acceleration [rad/s^2]
    Config acceleration;

    //! Get the degrees of freedom of the joint space
    size_t size() const {
        return position.size();
    }

    void slice(size_t offset, size_t length) {
        position = std::vector<double>(position.begin() + offset, position.begin() + offset + length);
        velocity = std::vector<double>(velocity.begin() + offset, velocity.begin() + offset + length);
        acceleration = std::vector<double>(acceleration.begin() + offset, acceleration.begin() + offset + length);
    }
};


//! A robot's trajectory as a list of positions and velocities at specific times
class Trajectory {
    using Config = State::Config;

    Config get_filled_vector(double constant) const;

public:
    //! Field for identifying trajectories (for the user)
    std::string id;

    //! Name of the motion this trajectory was planned for
    std::string motion;

    //! The degrees of freedom (e.g. axis) of the trajectory
    size_t degrees_of_freedom;

    //! The total duration in [s]
    double duration {0.0};

    //! The exact time stamps for the position, velocity, and acceleration values. The times will usually be sampled at the delta_time distance of the Planner class, but might deviate at the final step.
    std::vector<double> times;

    //! The joint positions along the trajectory.
    std::vector<Config> positions;

    //! The joint velocities along the trajectory.
    std::vector<Config> velocities;

    //! The joint accelerations along the trajectory.
    std::vector<Config> accelerations;

    //! Create an empty trajectory with the given degrees of freedom
    explicit Trajectory(size_t dofs): degrees_of_freedom(dofs) { }
    explicit Trajectory() { }

    //! The number of time steps within the trajectory.
    size_t size() const { return times.size(); }

    //! Access the first state at t=0 of the trajectory
    State front() const;

    //! Access the last state at t=duration of the trajectory
    State back() const;

    //! Get the kinematic state at a given time. Make sure that the output arguments have enough memory.
    void at_time(double time, Config& new_position, Config& new_velocity, Config& new_acceleration) const;

    //! Get the minimum position along the trajectory for each degree of freedom individually
    Config get_min_position() const;

    //! Get the maximum position along the trajectory for each degree of freedom individually
    Config get_max_position() const;

    //! Get the minimum velocity along the trajectory for each degree of freedom individually
    Config get_min_velocity() const;

    //! Get the maximum velocity along the trajectory for each degree of freedom individually
    Config get_max_velocity() const;

    //! Get the minimum acceleration along the trajectory for each degree of freedom individually
    Config get_min_acceleration() const;

    //! Get the maximum acceleration along the trajectory for each degree of freedom individually
    Config get_max_acceleration() const;

    //! Update the first position of the trajectory
    void update_first_position(const Config& joint_position);

    //! Reverse the trajectory's start and goal
    Trajectory reverse() const;

    //! Appends another trajectory to the current one.
    void append(const Trajectory& other);
    Trajectory& operator+=(const Trajectory& other);

    //! Slice a trajectory starting from step start for a length of steps.
    Trajectory slice(size_t start, size_t steps) const;

    //! @brief Filter a path of sparse waypoints from the trajectory.
    //! The path has a maximum distance per degree of freedom between the linear
    //! interpolation of the sparse waypoints and the original trajectory.
    std::vector<Config> filter_path(const Config& max_distance) const;

    //! Loads a trajectory from a json string.
    static Trajectory from_json(const std::string& json);

    //! Loads a trajectory from a *.json file.
    static Trajectory from_json_file(const std::filesystem::path& file);

    //! Serializes a trajectory to a json string.
    std::string to_json() const;

    //! Saves a trajectory to a *.json file.
    void to_json_file(const std::filesystem::path& file) const;

    //! To pretty print the trajectory as a table of positions
    std::string as_table() const;

    friend void to_json(nlohmann::json& j, const Trajectory& value);
    friend void from_json(const nlohmann::json& j, Trajectory& value);
};

}
