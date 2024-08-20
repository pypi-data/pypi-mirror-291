#pragma once

#include <exception>
#include <stdexcept>
#include <string>


namespace jacobi {

#if defined(_WIN32) || defined(__CYGWIN__)
    #define JACOBI_EXPORT __declspec(dllexport)
#else
    #define JACOBI_EXPORT __attribute__((__visibility__("default")))
#endif


struct JACOBI_EXPORT JacobiError: public std::runtime_error {
    const std::string type, message;

    explicit JacobiError(const std::string& type, const std::string& message)
        : std::runtime_error("\n[jacobi.exception." + type + "]\n\t" + message + "\n"), type(type), message(message) { }
};


struct JACOBI_EXPORT JacobiLicenseError: public JacobiError {
    explicit JacobiLicenseError(const std::string& message): JacobiError("license", message) { }
};


struct JACOBI_EXPORT JacobiLoadProjectError: public JacobiError {
    explicit JacobiLoadProjectError(const std::string& message): JacobiError("project", message) { }
};

}
