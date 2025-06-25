#pragma once

#include "Utils.hpp"

class Grid {
private:
    ut::utype _rows;
    ut::utype _cols;

    ut::utype _v_tiles;
    ut::utype _h_tiles;

    ut::string _hSeq;
    ut::string _vSeq;

    ut::utype _block_size;

    ut::utype** _data;

    inline ut::utype _getScore() {  return _data[_rows][_cols]; }
    inline ut::utype _compute(ut::utype, ut::utype, char, char); 

public:
    Grid(ut::string, ut::string);

    inline ut::utype rows() { return _rows + 1; };
    inline ut::utype cols() { return _cols + 1; };

    inline ut::utype vBlocks() { return _v_tiles; };
    inline ut::utype hBlocks() { return _h_tiles; };


    inline ut::string hSeq() { return _hSeq; };
    inline ut::string vSeq() { return _vSeq; };
    inline ut::utype blockSize() { return _block_size; };
    inline ut::utype blockSize(ut::utype col) { return std::min(_block_size, static_cast<ut::utype>(1 + _cols - col * _block_size)); }

    ut::utype** data() { return _data; };

    void computeBlock(ut::utype i, ut::utype j);
    ut::utype* getBlockTopRow(ut::utype, ut::utype);
    ut::utype* getBlockBottomRow(ut::utype, ut::utype);

    inline void printResult() { std::cout << std::endl << "Score: " << _getScore() << std::endl; }
    ~Grid();
};

