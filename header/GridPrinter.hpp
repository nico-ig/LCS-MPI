#pragma once

#include "Utils.hpp"
#include "Grid.hpp"

struct GridPrinter {
    static constexpr ut::utype COLUMN_WIDTH = 5;

    static void print(Grid* grid);

    static void printHeader(Grid* grid);
    static void printRowHeader(size_t row, Grid* grid);
    static char* defaultValueString();

    static void printHeaderSection(Grid* grid);
    static void printGrid(Grid* grid);
    static void printFooterSection(Grid* grid);

    static void printRow(ut::utype* row, size_t cols);
    static void printValue(ut::utype value);
    static void printCentered(char* text);

    static void printGridBorder(ut::utype cols);
    static void printPadding(ut::utype count = GridPrinter::COLUMN_WIDTH);
    static void printHorizontalSeparator();
};
