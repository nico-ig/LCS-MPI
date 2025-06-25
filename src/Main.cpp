#include <mpi.h>
#include "Grid.hpp"
#include "DebugHooks.hpp"
#include "FileHandler.hpp"
#include "CommandLineParser.hpp"
#include "MemoryHandler.hpp"

int main(int argc, char** argv) {
  // Create a scope so we can clean up the memory only after the grid is destroyed
  {
    MPI_Init(&argc, &argv);
    CommandLineParser parser(argc, argv);

    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    
    if (parser.helpRequested()) {
      if (rank == 0) parser.showHelp();
      return 0;
    }

    ut::string hSeq;
    ut::string vSeq;

    if (rank == 0) {
      auto files = parser.getInputFiles();
      hSeq = FileHandler::readFile(files[0]);
      vSeq = FileHandler::readFile(files[1]);
    }
    
    GridProcessor::broadcastString(hSeq, rank, MPI_COMM_WORLD);
    GridProcessor::broadcastString(vSeq, rank, MPI_COMM_WORLD);

    int num_ranks = 1;
    MPI_Comm_size(MPI_COMM_WORLD, &num_ranks);

    Grid grid(hSeq, vSeq);

    ProcessorHook::processGridByBlock(num_ranks, rank, &grid);
  
    MemoryHandler::freeMemory(hSeq.data());
    MemoryHandler::freeMemory(vSeq.data());

    MPI_Finalize();
  }

  MemoryHandler::cleanup();
  return 0;
}
