from piece import PiecesManager
import numpy as np


class ProposedSolution(PiecesManager):
    # chromosome

    def __init__(self, pieces):
        super().__init__(pieces)
        self.fitness = np.inf
        self.fitness_matrix = np.full(self.pieces.shape, np.inf)
        self.fitness_row = np.full(self.pieces.shape[0], np.inf)
        self.fitness_column = np.full(self.pieces.shape[1], np.inf)

    def fitness_relative(self):
        """
        Conta o numero total de vizinhos errados
        """
        self.fitness_matrix = np.array([[self.pieces[i][j].eval_relative(self.get_piece(i - 1, j),
                                                                         self.get_piece(i, j + 1),
                                                                         self.get_piece(i + 1, j),
                                                                         self.get_piece(i, j - 1))
                                         for j in range(self.pieces.shape[1])] for i in range(self.pieces.shape[0])])

        self.fitness_column = np.sum(self.fitness_matrix, axis=0)
        self.fitness_row = np.sum(self.fitness_matrix, axis=1)
        self.fitness = np.sum(self.fitness_matrix)
        return self.fitness

    def clone(self):
        ps = ProposedSolution(np.copy(self.pieces))
        ps.fitness_matrix = np.copy(self.fitness_matrix)
        ps.fitness_row = np.copy(self.fitness_row)
        ps.fitness_column = np.copy(self.fitness_column)
        return ps

    def __eq__(self, other):
        return self.fitness == other.fitness and self.fitness == other.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __repr__(self):
        return str(self.fitness)
