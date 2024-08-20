#pragma once

#include <optional>
#include <string>
#include <vector>

#include <json/json_fwd.hpp>

#include <jacobi/geometry/frame.hpp>


namespace jacobi {

//! The base element of a scene
struct Element {
    //! The unique name of the element, for display and identification.
    std::string name;

    //! Pose of the element, relative to the parent. Is called "base" for robots in Studio.
    Frame origin {Frame::Identity()};

    //! Given tags of the element, might be with a parameter `param=value`.
    std::vector<std::string> tags;

    Element() {}
    explicit Element(const std::string& name): name(name) {}
    explicit Element(const std::string& name, const Frame& origin): name(name), origin(origin) {}

    //! Checks whether a tag is present on the element. Tags are case-insensitive.
    bool has_tag(const std::string& tag) const;

    //! Reads the value of a tag parameter `param=value`. Tags are case-insensitive.
    std::optional<std::string> get_parameter(const std::string& tag) const;

    static void from_json(const nlohmann::json& value, Element& e);
};

}
