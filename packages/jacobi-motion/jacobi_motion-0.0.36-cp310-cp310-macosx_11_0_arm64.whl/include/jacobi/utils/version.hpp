#pragma once

#include <string>


namespace jacobi {

//! General version number
struct VersionNumber {
    size_t major;
    size_t minor;
    size_t patch;

    bool operator>=(const VersionNumber& other) const {
        if (major < other.major) return false;
        if (major > other.major) return true;
        if (minor < other.minor) return false;
        if (minor > other.minor) return true;
        return patch >= other.patch;
    }

    std::string to_string() const {
        return std::to_string(major) + "." + std::to_string(minor) + "." + std::to_string(patch);
    }
};

extern const VersionNumber version_number;

//! The minimum required driver version
extern const VersionNumber min_driver_version_number;

}
