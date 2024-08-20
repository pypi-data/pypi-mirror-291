#pragma once

#include <variant>

#include <json/json_fwd.hpp>

#include <jacobi/motions/linear_motion.hpp>
#include <jacobi/motions/low_level_motion.hpp>
#include <jacobi/motions/motion.hpp>
#include <jacobi/motions/path_following_motion.hpp>


namespace jacobi::motions {

using AnyMotion = std::variant<Motion, LinearMotion, LowLevelMotion, PathFollowingMotion>;

void from_json(const nlohmann::json& j, AnyMotion& motion);

}
