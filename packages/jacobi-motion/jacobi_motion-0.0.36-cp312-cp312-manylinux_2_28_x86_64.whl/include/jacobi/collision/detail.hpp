#pragma once


namespace jacobi {

class Obstacle;

struct CollisionDetail {
    Obstacle* first;
    Obstacle* second;
};

}
