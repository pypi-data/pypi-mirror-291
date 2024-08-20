#pragma once

#include <array>
#include <fstream>
#include <map>
#include <memory>
#include <optional>
#include <vector>

#include <jacobi/environment.hpp>
#include <jacobi/motions/motions.hpp>
#include <jacobi/result.hpp>
#include <jacobi/trajectory.hpp>


namespace jacobi::ruckig {
    struct Ruckig;
    class InputParameter;
    class Trajectory;
};

namespace jacobi {

using namespace jacobi::motions;


class Policy;
namespace telemetry { class PlanLogger; }


//! Planning motions for robots
class Planner {
public:
    //! The current environment to plan robot motions in
    std::shared_ptr<Environment> environment;

    //! The time step for sampling the trajectories in [s]. Usually, this should correspond to the control rate of the robot.
    double delta_time;

    //! Result of the last trajectory computation
    Result last_calculation_result {Result::Working};

    //! The calculation duration of the last full trajectory computation
    double last_calculation_duration {0.0}; // [ms]

    //! Resolution of the collision checking at the pre-planning stage
    double pre_collision_check_resolution {10e-2};

    //! Minimum number of samples in the pre-plannning stage
    size_t pre_minimum_samples {4096};

    //! Initial pertubation for the trajectory optimization
    double initial_pertubation_scale {0.04};

    //! Steps without improvement after which the pertubation scale is adapted
    size_t pertubation_change_steps {256};

    //! Change of the pertubation if no improvement could be found recently
    double pertubation_scale_change {1e-2};

    //! Maximum number of optimization steps
    size_t max_optimization_steps {5 * 1024};

    //! Max number of steps without improvement before early stopping
    size_t max_break_steps {1024};

    //! A meaningful relative improvement to avoid stopping
    double meaningful_loss_improvement {1e-2};

    //! The minimum compute budget (that the planner can use regardless)
    std::optional<float> min_calculation_duration; // [ms]

    //! The maximum compute budget (that won't be exceeded)
    std::optional<float> max_calculation_duration; // [ms]

    //! Last intermediate positions
    std::vector<Config> last_intermediate_positions;

private:
    //! The name of the project (e.g. for syncing with Studio)
    std::optional<std::string> project_name;

    //! Map of motions
    std::map<std::string, AnyMotion> motions;

    //! Map of policies for specific motions
    std::map<std::string, std::shared_ptr<Policy>> policies;

    //! Telemetry of the motion planning
    std::shared_ptr<telemetry::PlanLogger> logger;

    //! Random engine
    std::default_random_engine generator;

    //! Number of threads to use for parallelization. This can be set via the JACOBI_PARALLELIZATION environment variable.
    size_t parallelization;

    //! Load an encoded file
    static nlohmann::json load_encoded(const std::filesystem::path& file);

public:
    //! Create a planner with an environment and a specific delta time parameter.
    explicit Planner(std::shared_ptr<Environment> environment, double delta_time);

    //! Create a planner with the robot inside an empty environment and a specific delta time parameter.
    explicit Planner(std::shared_ptr<Robot> robot, double delta_time);

    //! Create a planner with an environment.
    explicit Planner(std::shared_ptr<Environment> environment);

    //! Create a planner with the robot inside an empty environment.
    explicit Planner(std::shared_ptr<Robot> robot);

    //! Set the seed of the planner's random number generator
    void set_seed(std::optional<unsigned int> seed);

    //! Add (or update when name already exists) a motion to the planner
    void add_motion(const Motion& motion);

    //! Get all loaded motions
    AnyMotion get_motion(const std::string& name) const;

    //! Load a *.jacobi-plan motion plan for accelerating the planning calculation.
    void load_motion_plan(const std::filesystem::path& file);

    // Helper methods to load planner from json
    static std::shared_ptr<Planner> load_from_json(const nlohmann::json& data, const std::filesystem::path& base_path);
    static std::shared_ptr<Planner> load_from_json_file(const std::filesystem::path& file, const std::filesystem::path& base_path);

    //! Loads a planner from a project file
    static std::shared_ptr<Planner> load_from_project_file(const std::filesystem::path& file);

    //! Loads a planner from a Studio project. Make sure to have the access token set as an environment variable.
    static std::shared_ptr<Planner> load_from_studio(const std::string& name);

private:
    std::optional<Trajectory> __plan(const Waypoint& start_, const Waypoint& goal_, std::shared_ptr<Robot> robot, const Motion& motion);
    std::optional<Trajectory> _plan(const Motion& motion, const std::optional<ExactPoint>& start_=std::nullopt, const std::optional<ExactPoint>& goal_=std::nullopt);
    std::optional<Trajectory> _plan(const LinearMotion& motion);
    std::optional<Trajectory> _plan(const LowLevelMotion& motion);
    std::optional<Trajectory> _plan(const std::string& name, const std::optional<ExactPoint>& start=std::nullopt, const std::optional<ExactPoint>& goal=std::nullopt);
    std::optional<Trajectory> _plan(const PathFollowingMotion& motion);
    std::optional<std::vector<Trajectory>> _plan(const std::vector<AnyMotion>& motions);

public:
    std::optional<Trajectory> plan(const Config& start, const Config& goal);

    //! Plans a time-optimized, collision-free, and jerk-limited motion from start to goal.
    std::optional<Trajectory> plan(const Point& start, const Point& goal);

    //! Plans a time-optimized, collision-free, and jerk-limited motion given the motion name. In case the motion was specified by a start or goal region, the respective exact start or goal positions needs to be passed.
    std::optional<Trajectory> plan(const std::string& name, const std::optional<ExactPoint>& start=std::nullopt, const std::optional<ExactPoint>& goal=std::nullopt);

    //! Plans a collision-free point-to-point motion.
    std::optional<Trajectory> plan(const Motion& motion, const std::optional<ExactPoint>& start=std::nullopt, const std::optional<ExactPoint>& goal=std::nullopt);

    //! Plans a linear motion.
    std::optional<Trajectory> plan(const LinearMotion& motion);

    //! Plans a low-level motion.
    std::optional<Trajectory> plan(const LowLevelMotion& motion);

    //! Plans a path-following motion.
    std::optional<Trajectory> plan(const PathFollowingMotion& motion);

    //! Plans a feasible sequence of motions.
    std::optional<std::vector<Trajectory>> plan(const std::vector<AnyMotion>& motions);
};

}
