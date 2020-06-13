import math
from collections import defaultdict

from PIL import Image
import numpy as np
from piece import PiecesManager, Piece


class Puzzle(PiecesManager):
    '''
    Classe para ler imagem e criar o puzzle
    '''

    def __init__(self, filepath, vsplits, hsplits):
        # Classe construtora para um puzzle - ler a imagem e divide em Pieces, de acordo com vsplits e hsplits
        # Repara-se que as dimensões das imagens devem ser multiplas de vsplits e hsplits, se não for a
        # completamos com pixels reflexivos.
        super().__init__(np.empty([vsplits, hsplits], dtype=object))
        self.filepath = filepath
        self.vsplits = vsplits
        self.hsplits = hsplits

        image = Image.open(filepath)
        self.image = np.array(image)
        if self.image.shape[2] == 4:
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            self.image = np.array(background)

        vpad = vsplits - (self.image.shape[0] % vsplits)
        hpad = hsplits - (self.image.shape[1] % hsplits)

        self.image = np.pad(self.image, ((math.floor(vpad / 2), math.ceil(vpad / 2)),
                                         (math.floor(hpad / 2), math.ceil(hpad / 2)), (0, 0)),
                            'constant', constant_values=0)

        piece_h = int(self.image.shape[0] / vsplits)
        piece_w = int(self.image.shape[1] / hsplits)

        for i in range(vsplits):
            for j in range(hsplits):
                si = i * piece_h
                sj = j * piece_w
                self.pieces[i][j] = Piece(self.image[si:si + piece_h, sj:sj + piece_w], j, i)

        for i in range(vsplits):
            for j in range(hsplits):
                up = self.get_piece(i - 1, j)
                right = self.get_piece(i, j + 1)
                down = self.get_piece(i + 1, j)
                left = self.get_piece(i, j - 1)
                self.pieces[i][j].set_neighbors(up, right, down, left)

        self.pieces_set = list(self.pieces.flatten())
        np.random.shuffle(self.pieces_set)

    def correct_solution2(self, ps):
        ps_pieces_list = list(ps.pieces.flatten())
        remaining_set = [item for item in self.pieces_set if item not in ps_pieces_list]
        track_set = set()

        new_pieces = []
        for piece in ps.pieces.flatten():
            if piece not in track_set:
                new_pieces.append(piece)
            else:
                new_pieces.append(remaining_set[0])
                del remaining_set[0]
            track_set.add(piece)

        ps.pieces = np.array(new_pieces).reshape(ps.pieces.shape)

    def correct_solution(self, ps):
        ps_pieces_list = list(ps.pieces.flatten())
        remaining_set = [item for item in self.pieces_set if item not in ps_pieces_list]
        ps.fitness_relative()

        pieces_dict = defaultdict(list)
        fitness_flatten = ps.fitness_matrix.flatten()
        for i, piece in enumerate(ps.pieces.flatten()):
            pieces_dict[piece].append({"index": i, "fitness": fitness_flatten[i]})

        new_pieces = ps.pieces.flatten()
        for key, value in pieces_dict.items():
            ordered_fitness = sorted(value, key=lambda k: k['fitness'])
            for i in range(1, len(ordered_fitness)):
                new_pieces[ordered_fitness[i]['index']] = remaining_set[0]
                del remaining_set[0]

        ps.pieces = new_pieces.reshape(ps.pieces.shape)

    def gen_shuffle_pieces(self):
        shuffle = np.copy(self.pieces.flatten())
        np.random.shuffle(shuffle)
        return shuffle.reshape(self.pieces.shape)

    def get_avg_rand_iterations(self):
        value = self.pieces.shape[0] * self.pieces.shape[1]
        factorial = 1
        while value > 1:
            factorial = factorial * value
            value = value - 1
        return factorial
