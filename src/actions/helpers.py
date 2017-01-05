from matplotlib import pyplot

class Helpers:
    @staticmethod
    def show_matrix(matrix):
        pyplot.imshow(matrix,cmap='hot',interpolation='nearest')
        pyplot.show()
