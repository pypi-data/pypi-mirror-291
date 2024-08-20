#pragma once

#include <atomic>
#include <condition_variable>
#include <mutex>
#include <queue>
#include <thread>


namespace jacobi::utils {

template<class Task, class Worker>
class TaskQueue {
    // Worker
    Worker& worker;

    // Background thread
    std::thread thread;
    std::atomic<bool> keep_running {true};

    // Main queue for storage
    std::queue<Task> queue;

    // Queue synchronization
    std::mutex mutex_;
    std::condition_variable cv;

public:
    explicit TaskQueue(Worker& worker): worker(worker) { thread = std::thread(&TaskQueue::run, this); }
    TaskQueue(const TaskQueue&) = delete;
    TaskQueue(TaskQueue&&) = delete;
    TaskQueue& operator=(const TaskQueue&) = delete;
    TaskQueue& operator=(TaskQueue&&) = delete;

    ~TaskQueue() {
        {
            std::lock_guard<std::mutex> lock(mutex_);
            keep_running = false;
        }
        cv.notify_one();
        thread.join();
    }

    void run() {
        while (keep_running) {
            std::unique_lock<std::mutex> lock(mutex_);
            cv.wait(lock, [&] { return !queue.empty() || !keep_running; }); // Wait until the queue has a log or logger should exit

            if (!queue.empty()) {
                const auto task = std::move(queue.front());
                queue.pop();
                lock.unlock();

                worker.process(task);

                lock.lock();
            }
        }
    }

    void push(const Task& task) {
        std::unique_lock<std::mutex> lock(mutex_);
        queue.push(task);
        cv.notify_one();
    }
};

}
