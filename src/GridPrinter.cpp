#include <cstdio>
#include <iomanip>
#include <iostream>
#include <cstring>

#include "DebugHooks.hpp"
#include "GridPrinter.hpp"

void GridPrinter::print(Grid* grid) {
    printHeaderSection(grid);
    printGrid(grid);
    printFooterSection(grid);
}

void GridPrinter::printHeaderSection(Grid* grid) {
    printPadding();
    PrinterHook::printHeader(grid);
    printPadding(GridPrinter::COLUMN_WIDTH + 1);
    printGridBorder(grid->cols());
}

void GridPrinter::printHeader(Grid* grid) {
  printPadding();
  printPadding(GridPrinter::COLUMN_WIDTH / 2);
  for (char c : std::string(grid->hSeq().data())) {
    char buf[2] = {c, '\0'};
    GridPrinter::printCentered(buf);
  }
  std::cout << std::endl;
}

void GridPrinter::printGrid(Grid* grid) {
    auto data = grid->data();
    for (ut::utype i = 0; i < grid->rows(); ++i) {
        PrinterHook::printRowHeader(i, grid);
        printRow(data[i], grid->cols());
        printHorizontalSeparator();
        std::cout << std::endl;
    }
}

void GridPrinter::printRowHeader(size_t row, Grid* grid) {
    printPadding();
    char* vSeq = grid->vSeq().data();
    std::cout << (row == 0 ? " " : std::string(1, vSeq[row-1]));
    printHorizontalSeparator();
}

 void GridPrinter::printRow(ut::utype* row, size_t cols) {
    for (size_t j = 0; j < cols; ++j) {
        printValue(row[j]);
    }
}

void GridPrinter::printValue(ut::utype value) {
    if (value == 0) {
        printCentered(PrinterHook::defaultValueString());
    } else {
        printCentered(const_cast<char*>(std::to_string(value).c_str()));
    }
}

char* GridPrinter::defaultValueString() {
    return (char*)"0";
}

void GridPrinter::printCentered(char* text) {
    ut::utype padding = static_cast<ut::utype>((GridPrinter::COLUMN_WIDTH - strnlen(text, 8)) / 2);
    printPadding(padding);
    std::cout << text;
    printPadding(padding);
}

void GridPrinter::printFooterSection(Grid* grid) {
    printPadding(GridPrinter::COLUMN_WIDTH + 1);
    printGridBorder(grid->cols());
}

void GridPrinter::printPadding(ut::utype count) {
    std::cout << std::string(count, ' ');
}

void GridPrinter::printGridBorder(ut::utype cols) {
    ut::utype width = cols * GridPrinter::COLUMN_WIDTH;
    std::cout << "+" << std::string(width, '-') << "+" << std::endl;
}

void GridPrinter::printHorizontalSeparator() {
    std::cout << "|";
}
