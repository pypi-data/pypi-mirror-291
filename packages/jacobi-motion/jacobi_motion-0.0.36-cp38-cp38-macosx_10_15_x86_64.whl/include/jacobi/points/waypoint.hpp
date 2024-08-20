#pragma once

#include <json/json_fwd.hpp>

#include <jacobi/element.hpp>
#include <jacobi/utils/vector.hpp>


namespace jacobi {

//! A joint-space waypoint with possible position, velocity, and/or acceleration values.
class Waypoint: public Element {
    using Config = StandardVector<double, DynamicDOFs>;

    static constexpr double eps {1e-7};

public:
    //! The joint position at the waypoint.
    Config position;

    //! The joint velocity at the waypoint.
    Config velocity;

    //! The joint acceleration at the waypoint.
    Config acceleration;

    //! Construct a waypoint by position data.
    Waypoint(std::initializer_list<double> data);

    //! Construct a waypoint with given position and zero velocity and acceleration.
    Waypoint(const Config& position);

    //! Construct a waypoint with given position and velocity and zero acceleration.
    explicit Waypoint(const Config& position, const Config& velocity);

    //! Construct a waypoint with given position, velocity, and acceleration.
    explicit Waypoint(const Config& position, const Config& velocity, const Config& acceleration): position(position), velocity(velocity), acceleration(acceleration) { }

    //! Construct a zero-initialized waypoint with the given size.
    explicit Waypoint(size_t size) {
        position.resize(size);
        velocity.resize(size);
        acceleration.resize(size);
        std::fill(position.begin(), position.end(), 0.0);
        std::fill(velocity.begin(), velocity.end(), 0.0);
        std::fill(acceleration.begin(), acceleration.end(), 0.0);
    }

    //! Construct an empty waypoint
    explicit Waypoint(): Waypoint(0) { };

    //! Append another waypoint to this one
    void append(const Waypoint& other) {
        position.insert(position.end(), other.position.begin(), other.position.end());
        velocity.insert(velocity.end(), other.velocity.begin(), other.velocity.end());
        acceleration.insert(acceleration.end(), other.acceleration.begin(), other.acceleration.end());
    }

    //! The size (or degrees of freedom) of the waypoint
    inline size_t size() const {
        return position.size();
    }

    bool is_within(const Waypoint& other) const;

    friend void to_json(nlohmann::json& j, const Waypoint& value);
    friend void from_json(const nlohmann::json& j, Waypoint& value);
};

}
