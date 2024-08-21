import math


class Real:
    def __init__(self, diagonal, ratio):
        self.diagonal = diagonal
        self.ratio = ratio
        self.width_ratio, self.height_ratio = ratio.split(":")

    def __str__(self):
        dimensions = self.get_dimensions()
        return (
            f"Width: {dimensions['width']:.2f} inches, "
            f"Height: {dimensions['height']:.2f} inches, "
            f"Area: {dimensions['area']:.2f} inches squared"
        )

    def get_dimensions(self):
        diagonal_ratio = math.sqrt(
            int(self.width_ratio) ** 2 + int(self.height_ratio) ** 2
        )
        width = (self.diagonal / diagonal_ratio) * int(self.width_ratio)
        height = (self.diagonal / diagonal_ratio) * int(self.height_ratio)
        area = width * height
        dimensions = {
            "width": width,
            "height": height,
            "area": area,
        }
        return dimensions


if __name__ == "__main__":
    real = Real(10, "16:9")
    print(real)
