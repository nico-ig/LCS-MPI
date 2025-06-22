#pragma once

#include "MemoryHandler.hpp"
#include "Utils.hpp"

class MemoryHandler {
public:
    static constexpr short CACHE_LINE_SIZE = 64;

    template<typename T>
    inline static T* safeAllocate(size_t size) {   
        return static_cast<T*>(calloc(size, sizeof(T)));
    }

    template<typename T>
    static T** safeAllocate(size_t rows, size_t cols) {
        T** ptr = safeAllocate<T*>(rows);

        for (size_t i = 0; i < rows; ++i) {
            ptr[i] = safeAllocate<T>(cols);
        }
        
        return ptr;
    }

    static void freeMemory(void* ptr) {
        free(ptr);
    }

    static void cleanup() {
    }
};