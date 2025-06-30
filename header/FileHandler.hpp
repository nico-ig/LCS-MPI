#pragma once

#include "Utils.hpp"
#include "MemoryHandler.hpp"

class FileHandler {
public:
  static ut::string readFile(char* filename) {
    FILE* file = fopen(filename, "rb");

    if (!file) {
      fprintf(stderr, "Cannot open file %s\n", filename);
      exit(EXIT_FAILURE);
    }

    fseek(file, 0, SEEK_END);
    size_t size = ftell(file);
    rewind(file);

    char* content = MemoryHandler::safeAllocate<char>(size + 1);
    size_t pos = 0;
    int ch;
    while ((ch = fgetc(file)) != EOF) {
        if (ch != '\n') {
            content[pos++] = static_cast<char>(ch);
        }
    }
    content[pos] = '\0';
    fclose(file);
    return ut::string(content, pos);
  }
};
