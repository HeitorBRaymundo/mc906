import numpy as np

class Piece:

    def __init__(self, image, posX, posY):
        self.image = image
        self.image_pad = np.pad(self.image, ((1, 1), (1, 1), (0, 0)), 'constant', constant_values=0)
        self.pos = (posY, posX)
        self.neighbors = (None, None, None, None)

    def set_neighbors(self, up, right, down, left):
        self.neighbors = (up, right, down, left)

    def eval_absolute(self, posX, posY):
        return int((posY, posX) == self.pos)

    def eval_relative(self, up, right, down, left):
        return int(up == self.neighbors[0]) + int(right == self.neighbors[1]) + \
               int(down == self.neighbors[2]) + int(left == self.neighbors[3])


class PiecesManager:

    def __init__(self, pieces):
        self.pieces = pieces

    @staticmethod
    def _pieces_to_image(pieces, attr_image):
        image = getattr(pieces[0][0], attr_image)
        piece_h = image.shape[0]
        piece_w = image.shape[1]
        channels = image.shape[2]

        result_image = np.empty([piece_h * pieces.shape[0], piece_w * pieces.shape[1], channels], dtype=np.uint8)

        for i in range(pieces.shape[0]):
            for j in range(pieces.shape[1]):
                image = getattr(pieces[i][j], attr_image)
                si = i * piece_h
                sj = j * piece_w
                result_image[si:si + piece_h, sj:sj + piece_w] = image

        return result_image

    def get_piece(self, i, j):
        if i < self.pieces.shape[0] and j < self.pieces.shape[1]:
            return self.pieces[i][j]
        return None

    def get_image(self):
        return PiecesManager._pieces_to_image(self.pieces, 'image')

    def get_image_grid(self):
        return PiecesManager._pieces_to_image(self.pieces, 'image_pad')