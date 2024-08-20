#pragma once

#include <future>
#include <optional>
#include <string>
#include <thread>
#include <variant>

#include <json/json.hpp>

#include <jacobi/collision/obstacle.hpp>
#include <jacobi/points/points.hpp>
#include <jacobi/trajectory.hpp>


namespace jacobi {

struct WebSocket;
class Camera;
class Robot;

//! Possible streams of a camera
enum class CameraStream {
    Color,
    Depth
};

//! Helper class to connect and visualize trajectories and events in Jacobi Studio.
class Studio {
    //! Websocket connection
    std::shared_ptr<WebSocket> websocket;

    std::promise<bool> is_connected_promise;
    std::thread server_thread;

    // Read data from websocket
    std::string expected_key;
    std::promise<nlohmann::json> expected_data;

    // Time step to send run trajectory updates
    double delta_time {0.01667};  // 60 [Hz]

    void setup_ctrl_c();
    void serve();

public:
    //! An action that can be performed in Jacobi Studio, e.g. setting a robot to a specific joint position or adding an obstacle to the environment.
    class Action {
        struct Command {
            std::optional<nlohmann::json> value;
            std::optional<std::string> element;  // Name of the element
        };

    public:
        std::string key;

        //! One action can have multiple commands, e.g. when setting joint positions of a dual arm robot
        std::vector<Command> commands;

        explicit Action(const std::string& key): key(key) {}
        explicit Action(const std::string& key, const nlohmann::json& value): key(key), commands({{ value, std::nullopt }}) {}

        Action& add(const std::optional<nlohmann::json>& value, const std::shared_ptr<Robot>& robot = nullptr, const std::shared_ptr<Camera>& camera = nullptr);
    };

    //! A container that maps a specific timing to one or multiple actions. The static methods of this class do not change the visualization in Jacobi Studio immediately, but only return an action that can be executed later (e.g. alongside a trajectory).
    struct Events: public std::multimap<double, Action> {
        //! Returns an action that sets the joint position of the given robot, or the last active robot instead.
        static Action set_joint_position(const Config& joint_position, const std::shared_ptr<Robot> robot = nullptr);

        //! Returns an action that sets the item obstacle of the given robot, or the last active robot instead.
        static Action set_item(const std::optional<Obstacle>& obstacle, const std::shared_ptr<Robot> robot = nullptr);

        //! Returns an action that sets the material of the given robot, or the last active robot instead.
        static Action set_material(const std::string& material, const std::shared_ptr<Robot> robot = nullptr);

        //! Returns an action that adds the given robot to the environment.
        static Action add_robot(const std::shared_ptr<Robot>& robot);

        //! Returns an action that adds the given obstacle to the environment.
        static Action add_obstacle(const Obstacle& obstacle);

        //! Returns an action that adds the given Cartesian waypoint to the environment.
        static Action add_waypoint(const Point& point);

        //! Returns an action that updates the obstacle with the same name.
        static Action update_obstacle(const Obstacle& obstacle);

        //! Returns an action that removes the given obstacle (by name) from the environment.
        static Action remove_obstacle(const Obstacle& obstacle);

        //! Returns an action that sets an I/O signal of the given robot, or the last active robot instead.
        static Action set_io_signal(const std::string& name, std::variant<int, float> value, const std::shared_ptr<Robot> robot = nullptr);

        //! Returns an action that sets an image for a camera encoded as a string.
        static Action set_camera_image_encoded(const std::string& image, const std::shared_ptr<Camera> camera = nullptr);

        //! Returns an action that sets the depth map visualization of a camera.
        static Action set_camera_depth_map(const std::vector<std::vector<double>>& depths, float x, float y, const std::shared_ptr<Camera> camera = nullptr);

        //! Returns an action that sets the point cloud visualization of a camera.
        static Action set_camera_point_cloud(const std::vector<double>& points, const std::shared_ptr<Camera> camera = nullptr);

        //! Returns an action that adds a camera.
        static Action add_camera(const std::shared_ptr<Camera> camera);

        //! Returns an action that updates a camera with the same name.
        static Action update_camera(const std::shared_ptr<Camera> camera);

        //! Returns an action that removes a camera.
        static Action remove_camera(const std::shared_ptr<Camera> camera);
    };

    //! Port of the websocket connection
    int port {8768};

    //! A factor to speed up or slow down running trajectories or events.
    double speedup {1.0};

    //! Interface Jacobi Studio via code. Connects to Jacobi Studio automatically - please make sure to enable the Studio Live feature in the Jacobi Studio settings.
    explicit Studio(bool auto_connect=true, double timeout=5.0);  // [s]
    ~Studio();

    //! Reconnect to Studio Live
    bool reconnect(double timeout=5.0);  // [s]

    //! Whether the library is connected to Studio Live
    bool is_connected() const;

    //! Sets the joint position of the given robot, or the last active robot instead.
    void set_joint_position(const Config& joint_position, const std::shared_ptr<Robot> robot = nullptr) const;

    //! Sets the item obstacle of the given robot, or the last active robot instead.
    void set_item(const std::optional<Obstacle>& obstacle, const std::shared_ptr<Robot> robot = nullptr) const;

    //! Sets the material of the given robot, or the last active robot instead.
    void set_material(const std::string& material, const std::shared_ptr<Robot> robot = nullptr) const;

    //! Adds the given robot to the environment.
    void add_robot(const std::shared_ptr<Robot>& robot) const;

    //! Adds the given obstacle to the environment.
    void add_obstacle(const Obstacle& obstacle) const;

    //! Adds the given Cartesian waypoint to the environment.
    void add_waypoint(const Point& obstacle) const;

    //! Updates the obstacle with the same name.
    void update_obstacle(const Obstacle& obstacle) const;

    //! Removes the given obstacle (by name) from the environment.
    void remove_obstacle(const Obstacle& obstacle) const;

    //! Sets an I/O signal of the given robot, or the last active robot instead.
    void set_io_signal(const std::string& name, std::variant<int, float> value, const std::shared_ptr<Robot> robot = nullptr) const;

    //! Sets an image for a camera encoded as a string.
    void set_camera_image_encoded(const std::string& image, const std::shared_ptr<Camera> camera = nullptr) const;

    //! Sets the depth map visualization of a camera.
    void set_camera_depth_map(const std::vector<std::vector<double>>& depths, float x, float y, const std::shared_ptr<Camera> camera = nullptr) const;

    //! Sets the point cloud visualization of a camera.
    void set_camera_point_cloud(const std::vector<double>& points, const std::shared_ptr<Camera> camera = nullptr) const;

    //! Adds a camera in Jacobi Studio.
    void add_camera(const std::shared_ptr<Camera> camera) const;

    //! Updates the camera with the same name in Jacobi Studio.
    void update_camera(const std::shared_ptr<Camera> camera) const;

    //! Removes a camera in Jacobi Studio.
    void remove_camera(const std::shared_ptr<Camera> camera) const;

    //! Run the given action in Jacobi Studio.
    void run_action(const Action& action) const;

    //! Runs a trajectory for the given robot (or the last active robot) in Jacobi Studio, alongside the events at the specified timings. Optionally, the visualization can be looped.
    void run_trajectory(const Trajectory& trajectory, const Events& events = {}, bool loop_forever = false, const std::shared_ptr<Robot> robot = nullptr) const;

    //! Run the events at the specified timings in Jacobi Studio.
    void run_events(const Events& events) const;

    //! Get the joint position of a robot.
    Config get_joint_position(const std::shared_ptr<Robot> robot = nullptr);

    //! Get an image from a camera encoded as a string.
    std::string get_camera_image_encoded(CameraStream stream, const std::shared_ptr<Camera> camera = nullptr);

    //! Resets the environment to the state before a trajectory or events were run. In particular, it removes all obstacles there were added dynamically.
    void reset() const;

private:
    void check_status(std::future_status status);
};

}
