#pragma once

#include <iostream>

namespace utils {
    template<typename T>
    struct vector {
        private:
            T* _data;
            size_t _length;
        public:
            vector() : _data(nullptr), _length(0) {}
            vector(T* data, size_t length) : _data(data), _length(length) {}
            inline constexpr size_t size() { return _length; }
            inline constexpr T* data() { return _data; }
            inline constexpr T operator[](size_t index) { return _data[index]; }
    };

    using utype = unsigned long;
    using string = vector<char>;
}

namespace ut = utils;
