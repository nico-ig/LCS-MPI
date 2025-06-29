#pragma once

#include <mpi.h>

#include "MemoryHandler.hpp"
#include "Utils.hpp"

class MemoryHandler {
public:
    static constexpr short CACHE_LINE_SIZE = 64;
    static constexpr short NUM_CACHE_LINES = 4;

    template<typename T>
    inline static T* safeAllocate(size_t size) {  
        void* ptr = nullptr;
        ptr = malloc(size * sizeof(T));
        if (ptr == nullptr) {
            std::cerr << "Memory allocation of size " << size << " failed" << std::endl;
            MPI_Abort(MPI_COMM_WORLD, EXIT_FAILURE);
        }
        return static_cast<T*>(ptr);
    }

    template<typename T>
    static T** safeAllocate(size_t rows, size_t cols) {
        T* data = safeAllocate<T>(cols);
        T** ptr = safeAllocate<T*>(rows);
        for (size_t i = 0; i < rows; ++i) {
            ptr[i] = data;
        }
        return ptr;
    }

    static void freeMemory(void* ptr) {
        free(ptr);
    }

    static void cleanup() {
    }
};