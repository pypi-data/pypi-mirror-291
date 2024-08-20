#pragma once

#include <random>

#include <json/json_fwd.hpp>

#include <jacobi/element.hpp>
#include <jacobi/utils/vector.hpp>
#include <jacobi/points/waypoint.hpp>


namespace jacobi {

//! A joint-space region with possible position, velocity, and/or acceleration values.
class Region: public Element {
    using Config = StandardVector<double, DynamicDOFs>;

public:
    Config min_position, max_position;
    Config min_velocity, max_velocity;
    Config min_acceleration, max_acceleration;

    explicit Region();
    explicit Region(const Config& min_position, const Config& max_position);
    explicit Region(const Config& min_position, const Config& max_position, const Config& min_velocity, const Config& max_velocity);
    explicit Region(const Config& min_position, const Config& max_position, const Config& min_velocity, const Config& max_velocity, const Config& min_acceleration, const Config& max_acceleration);

    inline size_t size() const {
        return min_position.size();
    }

    bool is_within(const Waypoint& other) const;

    friend void to_json(nlohmann::json& j, const Region& value);
    friend void from_json(const nlohmann::json& j, Region& value);
};

}
