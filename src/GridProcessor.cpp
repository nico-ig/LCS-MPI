#include <mpi.h>
#include <unistd.h>

#include "Grid.hpp"
#include "GridProcessor.hpp"
#include "DebugHooks.hpp"
#include "MemoryHandler.hpp"
#include "ProfileHook.hpp"

GridProcessor::GridProcessor(ut::utype num_ranks, ut::utype rank, Grid* grid) : _num_ranks(num_ranks), _rank(rank), _grid(grid) {
    _row_requests = MemoryHandler::safeAllocate<MPI_Request>(grid->hBlocks());
}

void GridProcessor::broadcastString(utils::string& s, int rank, MPI_Comm comm) {  
    size_t len = 0;
    if (rank == 0) {
        len = s.size();
    }

    MPI_Bcast(&len, 1, MPI_UNSIGNED_LONG, 0, comm);

    char* buffer =  MemoryHandler::safeAllocate<char>(len + 1);

    if (rank == 0) {
        memcpy(buffer, s.data(), len);
        MemoryHandler::freeMemory(s.data());
    }

    MPI_Bcast(buffer, static_cast<int>(len), MPI_CHAR, 0, comm);
    buffer[len] = '\0';
    
    s = utils::string(buffer, len);
}

void GridProcessor::processGridByBlock(ut::utype num_ranks, ut::utype rank, Grid* grid) {
    ut::utype rows = grid->vBlocks();
    ut::utype cols = grid->hBlocks();

    GridProcessor processor(num_ranks, rank, grid);

    processor.processBlocks(rows, cols);

    if (rank == processor.getRankOfLastRow()) {
        grid->printResult();
    }
}

void GridProcessor::processBlocks(ut::utype rows, ut::utype cols) {
    if (_rank > rows - 1) {
        return;
    }

    size_t num_requests = GridProcessor::_getNumOfRequests(rows, cols);
    MPI_Request* requests = MemoryHandler::safeAllocate<MPI_Request>(num_requests);

    for (ut::utype i = _rank, row_cnt = 0; i < rows; i += _num_ranks, ++row_cnt) {
        ut::utype last_row = std::min(static_cast<ut::utype>(i + _num_ranks), rows);
        this->_setBlockBounds(i, last_row, cols);

        this->_processRowBlocks();
        this->_appendRequests(requests + row_cnt * _num_cols, _num_cols);
    }

    MPI_Waitall(static_cast<int>(num_requests), requests, MPI_STATUSES_IGNORE);
    MemoryHandler::freeMemory(requests);
}

ut::utype GridProcessor::_getNumOfRequests(ut::utype rows, ut::utype cols) {
    if (_num_ranks > rows) {
        return cols;
    }

    ut::utype num_blocks = rows / _num_ranks;

    if (_rank < rows % _num_ranks) {
        num_blocks++;
    }

    return num_blocks * cols;
}

inline void GridProcessor::_appendRequests(MPI_Request* dest, ut::utype count) {
    memcpy(dest, _row_requests, count * sizeof(MPI_Request));
}

ut::utype GridProcessor::getRankOfLastRow() {
    ut::utype rows = _grid->vBlocks();
    if (_num_ranks > rows) {
        return rows - 1;
    }

    if (rows % _num_ranks == 0) {
        return _num_ranks - 1;
    }

    return rows % _num_ranks - 1;
}

inline void GridProcessor::_setBlockBounds(ut::utype initial_row, ut::utype last_row, ut::utype num_cols) {
    _initial_row = initial_row;
    _last_row = last_row;
    _num_cols = num_cols;
}

void GridProcessor::_processRowBlocks() {
    for (ut::utype j = 0; j < _num_cols; ++j) {
        if (_initial_row > 0) {
            this->_receiveTopRow(_initial_row, j);
        }

        double start_time = ProfileHook::getTime();
        _grid->computeBlock(_initial_row, static_cast<ut::utype>(j));
        double end_time = ProfileHook::getTime();
        ProfileHook::addTime(start_time, end_time);
        _row_requests[j] = this->_sendBottomRow(_initial_row, j);
    }

    if (_rank == this->getRankOfLastRow()) {
        PrinterHook::print(_grid);
    }
}

void GridProcessor::_receiveTopRow(ut::utype i, ut::utype j) {
    if (_num_ranks <= 1) {
        return;
    }
    ut::utype block_size = _grid->blockSize(j);
    ut::utype* top_row = _grid->getBlockTopRow(i, j);
    MPI_Recv(top_row, static_cast<int>(block_size), ut::mpi_type, MPI_ANY_SOURCE, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
}

MPI_Request GridProcessor::_sendBottomRow(ut::utype i, ut::utype j) {
    if (_num_ranks <= 1) {
        return MPI_REQUEST_NULL;
    }
    MPI_Request send_request;
    int next_rank = this->_getNextRank();
    ut::utype block_size = _grid->blockSize(j);

    ut::utype* bottom_row = _grid->getBlockBottomRow(i, j);
    MPI_Isend(bottom_row, static_cast<int>(block_size), ut::mpi_type, next_rank, 0, MPI_COMM_WORLD, &send_request);
    return send_request;
}

inline int GridProcessor::_getNextRank()  {
    return static_cast<int>((_rank + 1) % _num_ranks);
}

GridProcessor::~GridProcessor() {
    MemoryHandler::freeMemory(_row_requests);
}