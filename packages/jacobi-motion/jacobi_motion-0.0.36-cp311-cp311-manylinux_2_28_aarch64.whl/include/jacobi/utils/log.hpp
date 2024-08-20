#pragma once

#include <algorithm>
#include <cctype>
#include <cstdlib>
#include <iostream>
#include <optional>
#include <string>

#include <jacobi/utils/task_queue.hpp>


namespace jacobi {

//! Helper for environment variables
class env {
public:
    //! Compare two strings as lowercase
    static bool are_equal_ignore_case(const std::string& s1, const std::string& s2) {
        return std::equal(s1.begin(), s1.end(), s2.begin(), s2.end(), [](char a, char b) {
            return tolower(a) == tolower(b);
        });
    }

    //! Get an environment variable
    static std::optional<std::string> get(const std::string& name) {
        const char *var = std::getenv(name.c_str());
        if (var) {
            return std::string {var};
        }
        return std::nullopt;
    }

    //! Check that a boolean environment variable is on
    static bool is_on(const std::string& name) {
        const auto& var = get(name);
        if (!var) {
            return false;
        }

        return are_equal_ignore_case(var.value(), "on") || are_equal_ignore_case(var.value(), "true");
    }
};


//! Helper for general logging
class log {
public:
    enum Level {
        Debug = 0,
        Info,
        Warn,
        Error,
    };

    static Level get_default_level() {
        const auto& level = env::get("JACOBI_LOG_LEVEL");
        if (level) {
            if (env::are_equal_ignore_case(level.value(), "debug")) {
                return Level::Debug;
            } else if (env::are_equal_ignore_case(level.value(), "info")) {
                return Level::Info;
            } else if (env::are_equal_ignore_case(level.value(), "warn")) {
                return Level::Warn;
            } else if (env::are_equal_ignore_case(level.value(), "error")) {
                return Level::Error;
            }
        }
        return Level::Warn;
    }

    // The default level
    inline static Level level = get_default_level();

private:
    struct Log {
        Level level;
        std::string message;
    };

    class LogPrinter {
        const std::string font_red_bold {"\033[1;31m"};
        const std::string font_yellow_bold {"\033[1;33m"};
        const std::string font_blue {"\033[34m"};
        const std::string font_gray {"\033[37m"};
        const std::string font_reset {"\033[0m"};

    public:
        LogPrinter() { };  // Required because of clang bug

        void process(const Log& log) const {
            switch (log.level) {
                case Level::Error: {
                    std::cout << font_red_bold << log.message << font_reset << std::endl;
                } break;
                case Level::Warn: {
                    std::cout << font_yellow_bold << log.message << font_reset << std::endl;
                } break;
                case Level::Debug: {
                    std::cout << font_gray << log.message << font_reset << std::endl;
                } break;
                default: {
                    std::cout << log.message << std::endl;
                }
            }
        }
    };

    // The background console sink
    static inline LogPrinter log_printer;
    static inline utils::TaskQueue<Log, LogPrinter> async_printer {log_printer};

    template<Level message_level>
    static void log_(const std::string& type, const std::string& message) {
        if (level > message_level) {
            return;
        }

        async_printer.push(Log { message_level, "[jacobi." + type + "] " + message });
    }

public:
    static void debug(const std::string& type, const std::string& message) {
        log_<Level::Debug>(type, message);
    }

    static void info(const std::string& type, const std::string& message) {
        log_<Level::Info>(type, message);
    }

    static void warn(const std::string& type, const std::string& message) {
        log_<Level::Warn>(type, message);
    }

    static void error(const std::string& type, const std::string& message) {
        log_<Level::Error>(type, message);
    }
};

}
