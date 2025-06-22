#pragma once

#include "Grid.hpp"
#include "Utils.hpp"

class GridProcessor {
private:
    ut::utype _initial_row;
    ut::utype _initial_col;
    ut::utype _last_row;
    ut::utype _last_col;

    ut::utype _num_threads;
    Grid* _grid;

public:
    GridProcessor(ut::utype num_threads, Grid*);
    static void processGridByBlock(ut::utype, Grid*);
    inline void setBlockBonds(ut::utype, ut::utype, ut::utype, ut::utype);
    void processBlock();
    void _processAntidiagonal(ut::utype, ut::utype);
};

