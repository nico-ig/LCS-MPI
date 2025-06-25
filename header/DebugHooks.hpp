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
        static void processGridByBlock(ut::utype num_ranks, ut::utype rank, Grid* grid) {
            GridProcessor::processGridByBlock(num_ranks, rank, grid);
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
        static void processGridByBlock(ut::utype num_ranks, ut::utype rank, Grid* grid) {
            DebugConfig::BaseProcessor::processGridByBlock(num_ranks, rank, grid);
            GridPrinter::print(grid);
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

#else
    using ProcessorHook = GridProcessor;
    using PrinterHook = DebugConfig::BaseGridPrinter;
    using ComputeHook = Grid;
#endif
