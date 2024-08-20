#pragma once

#include <filesystem>
#include <string>
#include <optional>
#include <vector>

#include <json/json_fwd.hpp>

#include <jacobi/utils/vector_eigen.hpp>


namespace jacobi {

struct FileReference {
    //! Path of the object (if loaded from file)
    std::filesystem::path path;

    //! Scale for loading from file
    std::optional<float> scale;

    //! Is file part of a Jacobi project
    bool inside_project {false};

    friend void to_json(nlohmann::json& j, const FileReference& o);
    friend void from_json(const nlohmann::json& j, FileReference& o);
};


//! A convex mesh collision object.
struct Convex {
    using Vector = Eigen::Vector3d;

    static std::filesystem::path base_path;

    class Triangle {
    public:
        typedef size_t index_type;
        typedef int size_type;

    private:
        index_type vids[3];

    public:
        Triangle() {}
        Triangle(index_type p1, index_type p2, index_type p3) {
            set(p1, p2, p3);
        }

        inline void set(index_type p1, index_type p2, index_type p3) {
            vids[0] = p1;
            vids[1] = p2;
            vids[2] = p3;
        }

        inline index_type operator[](index_type i) const {
            return vids[i];
        }

        inline index_type& operator[](index_type i) {
            return vids[i];
        }

        static inline size_type size() {
            return 3;
        }

        bool operator==(const Triangle& other) const {
            return vids[0] == other.vids[0] && vids[1] == other.vids[1] && vids[2] == other.vids[2];
        }

        bool operator!=(const Triangle& other) const {
            return !(*this == other);
        }
    };

public:
    //! Path of the object (if loaded from file)
    std::optional<FileReference> file_reference;

    std::vector<Vector> vertices;
    std::vector<Triangle> triangles;

    explicit Convex();
    explicit Convex(const std::filesystem::path& path, std::optional<float> scale);

    //! For wasm bindings, vertices only
    explicit Convex(uintptr_t vertices_buffer, size_t size);

    //! Load object from vertices
    explicit Convex(const std::vector<std::array<float, 3>>& verts, const std::vector<std::array<size_t, 3>>& triangs);

    //! Get vector of minimum position
    std::array<double, 3> get_bounding_box_minimum() const;

    //! Get vector of maximum position
    std::array<double, 3> get_bounding_box_maximum() const;

    //! Load *.obj or *.stl from file
    static std::vector<Convex> load_from_file(const std::filesystem::path& path, std::optional<float> scale = std::nullopt);

    //! Reference Studio file
    static Convex reference_studio_file(const std::filesystem::path& path, std::optional<float> scale = std::nullopt);

    friend void to_json(nlohmann::json& j, const Convex& value);
    friend void from_json(const nlohmann::json& j, std::vector<Convex>& value);
};


using ConvexVector = std::vector<Convex>;

}
