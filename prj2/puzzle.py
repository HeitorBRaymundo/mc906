import math
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






