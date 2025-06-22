#include "Grid.hpp"
#include "GridProcessor.hpp"
#include "DebugHooks.hpp"

GridProcessor::GridProcessor(ut::utype num_threads, Grid* grid) : _num_threads(num_threads), _grid(grid) {}

void GridProcessor::processGridByBlock(ut::utype num_threads, Grid* grid) {
    ut::utype block_depth = num_threads;

    ut::utype rows = grid->vBlocks();
    ut::utype cols = grid->hBlocks();

    GridProcessor processor(num_threads, grid);

    for (ut::utype i = 0, initial_col = 0; i < rows; i += block_depth) {
        ut::utype last_row = std::min(static_cast<ut::utype>(i + block_depth), rows);
        ut::utype last_col = cols;
        processor.setBlockBonds(i, initial_col, last_row, last_col);
        processor.processBlock();
    }

    grid->printResult();
}

inline void GridProcessor::setBlockBonds(ut::utype initial_row, ut::utype initial_col, ut::utype last_row, ut::utype last_col) {
    _initial_row = initial_row;
    _initial_col = initial_col;
    _last_row = last_row;
    _last_col = last_col;
}

void GridProcessor::processBlock() {
    for (ut::utype start_col = _initial_col; start_col < _last_col; start_col++) {
        _processAntidiagonal(_initial_row, start_col);
    }

    for (ut::utype start_row = _initial_row + 1; start_row < _last_row; start_row++) {
        _processAntidiagonal(start_row, _last_col - 1);
    }
}

void GridProcessor::_processAntidiagonal(ut::utype start_row, ut::utype start_col) {
    for (long long int j = start_col; j >= 0; --j) {
        ut::utype i = static_cast<ut::utype>(start_row + start_col - j);
        if (i < _last_row) {
            _grid->computeBlock(i, static_cast<ut::utype>(j));
        }
    }
    PrinterHook::print(_grid);
}