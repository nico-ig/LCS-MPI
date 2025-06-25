#include <cstring>

#include "Utils.hpp"
#include "Grid.hpp"
#include "DebugHooks.hpp"
#include "MemoryHandler.hpp"

Grid::Grid(ut::string hSeq, ut::string vSeq) {
    bool vSeqIsLonger = vSeq.size() > hSeq.size();

    _vSeq = vSeqIsLonger ? vSeq : hSeq;
    _hSeq = vSeqIsLonger ? hSeq : vSeq;

    _rows = static_cast<ut::utype>(_vSeq.size());
    _cols = static_cast<ut::utype>(_hSeq.size());

    _block_size = MemoryHandler::CACHE_LINE_SIZE * MemoryHandler::NUM_CACHE_LINES;

    _h_tiles = static_cast<ut::utype>(_cols / _block_size + (_cols % _block_size != 0));
    _v_tiles = static_cast<ut::utype>(_rows / _block_size + (_rows % _block_size != 0));

    _data = MemoryHandler::safeAllocate<ut::utype>(_rows + 1, _cols + 1);
    memset(_data[0], 0, (_cols + 1) * sizeof(ut::utype));
}

void Grid::computeBlock(ut::utype row, ut::utype col) {    
    ut::utype v_len = std::min(_block_size, static_cast<ut::utype>(_vSeq.size() - row * _block_size));
    char* v_data = _vSeq.data() + (row * _block_size);

    ut::utype h_len = std::min(_block_size, static_cast<ut::utype>(_hSeq.size() - col * _block_size));
    char* h_data = _hSeq.data() + (col * _block_size);

    for (ut::utype i = 0; i < v_len; ++i) {
        _data[1 + row * _block_size + i][0] = 0;
        for (ut::utype j = 0; j < h_len; ++j) {
            ut::utype block_row = static_cast<ut::utype>(1 + row * _block_size + i);
            ut::utype block_col = static_cast<ut::utype>(1 + col * _block_size + j);

            _data[block_row][block_col] = ComputeHook::_compute(block_row, block_col, v_data[i], h_data[j]);
        }   
    }
}

inline ut::utype Grid::_compute(ut::utype row, ut::utype col, char v_char, char h_char) {  
  if (v_char == h_char) {
      return _data[row - 1][col - 1] + 1;
  }
  return std::max(_data[row - 1][col], _data[row][col - 1]);
}

ut::utype* Grid::getBlockTopRow(ut::utype row, ut::utype start_col) {
    ut::utype block_row = static_cast<ut::utype>(row * _block_size);
    ut::utype block_start_col = static_cast<ut::utype>(1 + start_col * _block_size);

    block_row = std::min(block_row, _rows);
    block_start_col = std::min(block_start_col, _cols);

    return _data[block_row] + block_start_col;
}

ut::utype* Grid::getBlockBottomRow(ut::utype row, ut::utype start_col) {
    ut::utype block_row = static_cast<ut::utype>(row * _block_size + _block_size);
    ut::utype block_start_col = static_cast<ut::utype>(1 + start_col * _block_size);

    block_row = std::min(block_row, _rows);
    block_start_col = std::min(block_start_col, _cols);

    return _data[block_row] + block_start_col;
}

Grid::~Grid() {
    MemoryHandler::freeMemory(_data[0]);
    MemoryHandler::freeMemory(_data);
}

