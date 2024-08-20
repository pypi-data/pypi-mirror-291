#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "jacobi::motion" for configuration "Release"
set_property(TARGET jacobi::motion APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(jacobi::motion PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libmotion.so"
  IMPORTED_SONAME_RELEASE "libmotion.so"
  )

list(APPEND _cmake_import_check_targets jacobi::motion )
list(APPEND _cmake_import_check_files_for_jacobi::motion "${_IMPORT_PREFIX}/lib64/libmotion.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
