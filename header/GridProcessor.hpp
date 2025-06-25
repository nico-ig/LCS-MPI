#pragma once

#include <mpi.h>

#include "Grid.hpp"
#include "Utils.hpp"

class GridProcessor {
private:
    ut::utype _initial_row;
    ut::utype _last_row;
    ut::utype _num_cols;

    ut::utype _num_ranks;
    ut::utype _rank;
    MPI_Request* _row_requests;
    Grid* _grid;

    inline void _setBlockBounds(ut::utype, ut::utype, ut::utype);
    ut::utype _getNumOfRequests(ut::utype, ut::utype);
    inline void _appendRequests(MPI_Request*, ut::utype);
    void _processRowBlocks();
    void _receiveTopRow(ut::utype i, ut::utype j);
    MPI_Request _sendBottomRow(ut::utype i, ut::utype j);
    inline int _getNextRank();

public:
    GridProcessor(ut::utype num_ranks, ut::utype rank, Grid*);
    ~GridProcessor();

    static void broadcastString(utils::string&, int, MPI_Comm);
    
    static void processGridByBlock(ut::utype, ut::utype, Grid*);
    void processBlocks(ut::utype, ut::utype);
    ut::utype getRankOfLastRow();
};

