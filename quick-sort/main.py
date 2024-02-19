import pygame as pg
import math
import random

def quick_sort(draw_info):
    lst = draw_info.lst

    def partition(array, low, high):
        pivot = array[high]
        i = low - 1
        for j in range(low, high):
            if array[j] < pivot:
                i += 1
                array[i], array[j] = array[j], array[i]
                draw_list(draw_info, { i: draw_info.GREEN, j: draw_info.RED}, True)
                yield True

        array[i + 1], array[high] = array[high], array[i + 1]

        draw_list(draw_info, {i + 1: draw_info.GREEN, high: draw_info.RED}, True)
        yield True
        return i + 1

    def quick_sort(array, low, high):
        if low < high:
            pi = yield from partition(array, low, high)
            yield from quick_sort(array, low, pi - 1)
            yield from quick_sort(array, pi + 1, high)

    yield from quick_sort(lst, 0, len(lst) - 1)

    return lst

def merge_sort(draw_info):
    lst = draw_info.lst

    def merge(array, l, m, r):
        n1 = m - l + 1
        n2 = r - m

        L = [0] * (n1)
        R = [0] * (n2)

        for i in range(0, n1):
            L[i] = array[l + i]

        for j in range(0, n2):
            R[j] = array[m + 1 + j]

        i = 0
        j = 0
        k = l

        while i < n1 and j < n2:
            if L[i] <= R[j]:
                array[k] = L[i]
                i += 1
            else:
                array[k] = R[j]
                j += 1
            k += 1
            draw_list(draw_info, {k: draw_info.GREEN, l + i: draw_info.RED, m + 1 + j: draw_info.RED}, True)
            yield True

        while i < n1:
            array[k] = L[i]
            i += 1
            k += 1
            draw_list(draw_info, {k: draw_info.GREEN, l + i: draw_info.RED}, True)
            yield True

        while j < n2:
            array[k] = R[j]
            j += 1
            k += 1
            draw_list(draw_info, {k: draw_info.GREEN, m + 1 + j: draw_info.RED}, True)
            yield True

    def merge_sort(array, l, r):
        if l < r:
            m = (l + (r - 1)) // 2

            yield from merge_sort(array, l, m)
            yield from merge_sort(array, m + 1, r)
            yield from merge(array, l, m, r)

    yield from merge_sort(lst, 0, len(lst) - 1)

    return lst


class DrawInformation:
	BLACK = (255, 118, 117)
	WHITE = (45, 52, 54)
	GREEN = 0, 255, 0
	RED = 255, 0, 0
	BACKGROUND_COLOR = WHITE

	GRADIENTS = [
		(128, 128, 128),
		(160, 160, 160),
		(192, 192, 192)
	]

	SIDE_PAD = 100
	TOP_PAD = 150

	def __init__(self, width, height, lst):
		self.width = width
		self.height = height

		self.window = pg.display.set_mode((width, height))
		pg.display.set_caption("Quick sort")
		self.set_list(lst)

	def set_list(self, lst):
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)

		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD // 2


def generate_starting_list(n, min_val, max_val):
    lst = [i for i in range(min_val, max_val + 1)]

    for i in range(n):
        rand1 = random.randint(0, n - 1)
        rand2 = random.randint(0, n - 1)
        lst[rand1], lst[rand2] = lst[rand2], lst[rand1]

    return lst

def draw(draw_info):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    draw_list(draw_info)
    pg.display.update()

def draw_list(draw_info, color_positions=None, clear_bg=False):
	if color_positions is None:
		color_positions = {}
	lst = draw_info.lst

	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pg.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.GRADIENTS[i % 3]

		if i in color_positions:
			color = color_positions[i] 

		pg.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

	if clear_bg:
		pg.display.update()


def main():
    run = True
    clock = pg.time.Clock()

    n = 200
    min_val = 1
    max_val = 200

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1920, 1080, lst)

    sorting = False

    sorting_algorithm_generator = None
    sorting_algorithm = merge_sort

    while run:
        clock.tick(30)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type != pg.KEYDOWN:
                continue

            if event.key == pg.K_SPACE:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False

            if event.key == pg.K_RETURN and sorting is False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info)

            if event.key == pg.K_m:
                sorting_algorithm = merge_sort
                sorting = False
            if event.key == pg.K_q:
                sorting_algorithm = quick_sort
                sorting = False


if __name__ == "__main__":
    main()