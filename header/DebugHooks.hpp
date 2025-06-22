#pragma once

#include <iomanip>
#include <iostream>
#include <omp.h>

#include "Grid.hpp"
#include "GridPrinter.hpp"
#include "GridProcessor.hpp"

namespace DebugConfig {
    struct BaseGridPrinter {
        static void print(Grid*) {}
        static void printHeader(Grid*) {}
        static void printRowHeader(ut::utype, Grid*) {}
        static char* defaultValueString() { return (char*)""; }
    };

    struct BaseProcessor {
        static void processGridByBlock(ut::utype num_threads, Grid* grid) {
            GridProcessor::processGridByBlock(num_threads, grid);
        }
    };
}

namespace DebugMatrix {
    struct Printer : public DebugConfig::BaseGridPrinter {
        static void printHeader(Grid* grid) {
            GridPrinter::printHeader(grid);
        }
        static void printRowHeader(ut::utype row, Grid* grid) {
            GridPrinter::printRowHeader(row, grid);
        }
        static char* defaultValueString() {
            return GridPrinter::defaultValueString();
        }
    };

    struct Processor : public DebugConfig::BaseProcessor {
        static void processGridByBlock(ut::utype num_threads, Grid* grid) {
            DebugConfig::BaseProcessor::processGridByBlock(num_threads, grid);
            GridPrinter::print(grid);
        }
    };
}


namespace DebugThread {
    struct Printer : public DebugConfig::BaseGridPrinter {
        static void print(Grid* grid) { GridPrinter::print(grid); }
        static void printHeader(Grid* grid) {
            GridPrinter::printPadding();
            GridPrinter::printPadding(GridPrinter::COLUMN_WIDTH / 2);
            for (ut::utype d = 1; d < grid->cols(); d++) {
                GridPrinter::printCentered(const_cast<char*>(std::to_string(d).c_str()));
            }
            std::cout << std::endl;
        }

        static void printRowHeader(ut::utype row, Grid*) {
            std::cout << std::setw(GridPrinter::COLUMN_WIDTH + 1) << row; 
            GridPrinter::printHorizontalSeparator();
        }

        static char* defaultValueString() {
            return (char*)".";
        }
    };

    struct Compute {
        static ut::utype _compute(ut::utype, ut::utype, char, char) {
            return static_cast<ut::utype>(omp_get_thread_num()) + 1;
        }
    };
}

#ifdef DEBUGLCS
    using ProcessorHook = GridProcessor;
    using PrinterHook = GridPrinter;
    using ComputeHook = Grid;

#elif DEBUGMATRIX
    using ProcessorHook = DebugMatrix::Processor;
    using PrinterHook = DebugMatrix::Printer;
    using ComputeHook = Grid;

#elif DEBUGTHREAD
    using ProcessorHook = GridProcessor;
    using PrinterHook = DebugThread::Printer;
    using ComputeHook = DebugThread::Compute;

#else
    using ProcessorHook = GridProcessor;
    using PrinterHook = DebugConfig::BaseGridPrinter;
    using ComputeHook = Grid;
#endif
