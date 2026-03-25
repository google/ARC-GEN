# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Common utility functions for ARC-GEN."""

import copy
import math
import random


def all_connected(ingrid, color):
  ingrid = copy.deepcopy(ingrid)
  width, height = len(ingrid[0]), len(ingrid)
  row, col = -1, -1
  for r in range(height):
    for c in range(width):
      if ingrid[r][c] == color: row, col = r, c
  if row == -1 or col == -1: return True
  queue = [(row, col)]
  while queue:
    r, c = queue.pop()
    neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
    for nr, nc in neighbors:
      if nr < 0 or nr >= height or nc < 0 or nc >= width: continue
      if ingrid[nr][nc] == color:
        ingrid[nr][nc] = -1
        queue.append((nr, nc))
  for r in range(height):
    for c in range(width):
      if ingrid[r][c] == color: return False
  return True


def all_pixels(width, height):
  pixels = []
  for r in range(height):
    for c in range(width):
      pixels.append((r, c))
  return pixels


def apply_gravity(ingrid, gravity):
  ingrid = ingrid if gravity < 2 else ingrid[::-1]
  ingrid = ingrid if gravity % 2 < 1 else [list(row) for row in zip(*ingrid)]
  return ingrid


def backslash(ingrid, length, row, col, color):
  """Draws a backslash in a grid."""
  for i in range(length):
    ingrid[row + i][col + i] = color


def backslash_obscured(ingrid, length, row, col, color):
  for i in range(length):
    if ingrid[row + i][col + i] != color: return True
  return False


def backslash_visible(ingrid, length, row, col, color):
  visible_corners = 0
  if ingrid[row][col] == color: visible_corners += 1
  if ingrid[row + length - 1][col + length - 1] == color: visible_corners += 1
  return visible_corners == 2


def bounce(width, height, b, k, u):
  ingrid, output = grid(width, height, b), grid(width, height, k)
  output[height - 1][0] = ingrid[height - 1][0] = u
  c, c_dir = 0, 1
  for r in range(height - 1, -1, -1):
    output[r][c] = u
    c += c_dir
    if c == 0 or c == width - 1:
      c_dir = -c_dir
  return ingrid, output


def choice(sequence):
  return random.choice(sequence)


def choices(sequence, k=1):
  return random.choices(sequence, k=k)


def connected(pixels):
  marked = [0] * len(pixels)
  def touch(idx):
    marked[idx] = 1
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
      pixel = (pixels[idx][0] + dr, pixels[idx][1] + dc)
      if pixel not in pixels: continue
      pos = pixels.index(pixel)
      if marked[pos] == 0: touch(pos)
  touch(0)
  return min(marked) == 1


def connected_sprite(width=3, height=3, tries=5):
  """Creates a connected sprite by removing some pixels from a grid."""
  while True:
    rows, cols = conway_sprite(width, height, tries)
    pixels = sorted(list(zip(rows, cols)))
    if connected(pixels): break
  return pixels


def conway_sprite(width=3, height=3, tries=5):
  """Creates a random sprite by removing some pixels from a grid.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    tries: The number of attempts to remove pixels.

  Returns:
    A tuple of two lists representing the rows and columns of the sprite.
  """
  # Start with all pixels and remove a few (unless some row or col disappears)
  rows, cols = [], []
  for r in range(height):
    for c in range(width):
      rows.append(r)
      cols.append(c)
  for _ in range(tries):
    idx = randint(0, len(rows) - 1)
    r, c = rows[idx], cols[idx]
    if rows.count(r) <= 1 or cols.count(c) <= 1: continue  # would vanish!
    del rows[idx]
    del cols[idx]
  # Shuffle the lists for good measure
  return shuffle(rows), shuffle(cols)


def continuous_creature(size, width=3, height=3):
  """Creates a contiguous creature starting from (0, 0) that fills the space.

  Args:
    size: The number of cells in the creature.
    width: The width of the grid.
    height: The height of the grid.

  Returns:
    A tuple of two lists representing the rows and columns of the sprite.
  """
  # Start at (0, 0)
  pixels, queue = [], [(0, 0)]
  while len(pixels) < size:
    idx = randint(0, len(queue) - 1)
    pixels.append(queue[idx])
    del queue[idx]
    for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
      r, c = pixels[-1][0] + dr, pixels[-1][1] + dc
      if r < 0 or r >= height or c < 0 or c >= width: continue
      if (r, c) in pixels or (r, c) in queue: continue
      queue.append((r, c))
  return pixels


def create_linegrid(bitmap, spacing, linecolor):
  """Creates a grid with lines and a bitmap.

  Args:
    bitmap: A 2D list of colors representing the bitmap.
    spacing: The spacing between lines.
    linecolor: The color of the lines.

  Returns:
    A 2D list representing the grid with lines and the bitmap.
  """
  actual_size = len(bitmap) * (spacing + 1) - 1
  ingrid = grid(actual_size, actual_size, 0)
  for r in range(actual_size):
    for c in range(actual_size):
      ingrid[r][c] = ingrid[r][c] if (r + 1) % (spacing + 1) != 0 else linecolor
      ingrid[r][c] = ingrid[r][c] if (c + 1) % (spacing + 1) != 0 else linecolor
  for r, row in enumerate(bitmap):
    for c, color in enumerate(row):
      for dr in range(spacing):
        for dc in range(spacing):
          ingrid[r * (spacing + 1) + dr][c * (spacing + 1) + dc] = color
  return ingrid


def deepcopy(ingrid):
  return copy.deepcopy(ingrid)


def diagonally_connected(pixels):
  marked = [0] * len(pixels)
  def touch(idx):
    marked[idx] = 1
    for dr in [-1, 0, 1]:
      for dc in [-1, 0, 1]:
        pixel = (pixels[idx][0] + dr, pixels[idx][1] + dc)
        if pixel not in pixels: continue
        pos = pixels.index(pixel)
        if marked[pos] == 0: touch(pos)
  touch(0)
  return min(marked) == 1


def diagonally_connected_sprite(width=3, height=3, tries=5):
  """Creates a diagonally connected sprite by removing pixels from a grid."""
  while True:
    rows, cols = conway_sprite(width, height, tries)
    pixels = sorted(list(zip(rows, cols)))
    if diagonally_connected(pixels): break
  return pixels


def diamond(ingrid, row, col, length, color, expected_color=None):
  for r in range(-length, length + 1):
    for c in range(-length, length + 1):
      radius = abs(r) + abs(c)
      if radius == length:
        if expected_color is not None:
          if get_pixel(ingrid, row + r, col + c) not in [-1, expected_color]:
            return False
        draw(ingrid, row + r, col + c, color)
  return True


def diamond_check_inside(ingrid, row, col, length, color):
  for r in range(-length, length + 1):
    for c in range(-length, length + 1):
      radius = abs(r) + abs(c)
      if radius < length and get_pixel(ingrid, row + r, col + c) not in [-1, color]:
        return False
  return True


def draw(ingrid, r, c, color):
  if r >= 0 and c >= 0 and r < len(ingrid) and c < len(ingrid[r]):
    ingrid[r][c] = color


def edgefree_pixels(ingrid):
  """Returns pixels that are edgefree (no adjacent neighbors along an edge)."""
  width, height = len(ingrid[0]), len(ingrid)
  def get_val(r, c):
    if r < 0 or r >= height or c < 0 or c >= width: return 0
    return 1 if ingrid[r][c] > 0 else 0
  pixels = []
  for r in range(height):
    for c in range(width):
      if ingrid[r][c] == 0: continue
      friends = 0
      for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        friends += get_val(r + dr, c + dc)
      if friends > 0: continue
      pixels.append((r, c))
  return pixels


def fill(ingrid, r, c, color):
  prev = ingrid[r][c]
  queue = [(r, c)]
  while queue:
    r, c = queue.pop()
    if get_pixel(ingrid, r, c) != prev: continue
    ingrid[r][c] = color
    queue.extend([(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)])


def flatten(ingrid):
  flattened = []
  for row in ingrid:
    flattened.extend(row)
  return flattened


def flip(ingrid):
  return ingrid[::-1]


def flip_horiz(ingrid):
  return [row[::-1] for row in ingrid]


def flop(ingrid):
  return [row[::-1] for row in ingrid]


def get_pixel(ingrid, r, c):
  if r >= 0 and c >= 0 and r < len(ingrid) and c < len(ingrid[r]):
    return ingrid[r][c]
  return -1


def grid(width, height, color=0):
  return [[color for _ in range(width)] for _ in range(height)]


def grids(width, height, color=0):
  return grid(width, height, color), grid(width, height, color)


def grid_enhance(size, enhance, rows, cols, idxs, colors, b):
  ingrid, output = grid(size, size, b), grid(size * enhance, size * enhance, b)
  for r, c, idx in zip(rows, cols, idxs):
    ingrid[r][c] = colors[idx]
    for dr in range(enhance):
      for dc in range(enhance):
        output[r * enhance + dr][c * enhance + dc] = colors[idx]
  return ingrid, output


def grid_intersect(width, height, rows, cols, b, s, y, n, m):
  ingrid, output = grid(2 * width + 1, height, n), grid(width, height, b)
  for r, c in zip(rows, cols):
    ingrid[r][c] = y
  for r in range(height):
    ingrid[r][width] = s
  for r in range(height):
    for c in range(width):
      if ingrid[r][c] == n or ingrid[r][c + width + 1] == n: continue
      output[r][c] = m
  return ingrid, output


def has_neighbor(size, bitmap, r, c):
  for dr in [-1, 0, 1]:
    for dc in [-1, 0, 1]:
      if r + dr < 0 or r + dr >= size or c + dc < 0 or c + dc >= size: continue
      if bitmap[r + dr][c + dc] > 0: return True
  return False


def hollow_conway(width=3, height=3, tries=5):
  """Creates a (potentially hollow) sprite by removing some pixels from a grid.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    tries: The number of attempts to remove pixels.

  Returns:
    A tuple of two lists representing the rows and columns of the sprite.
  """
  # Start with all pixels and remove a few (unless some row or col disappears)
  rows, cols = [], []
  for r in range(height):
    for c in range(width):
      rows.append(r)
      cols.append(c)
  for _ in range(tries):
    idx = randint(0, len(rows) - 1)
    r, c = rows[idx], cols[idx]
    if rows.count(r) <= 1 and r in [0, height - 1]: continue
    if cols.count(c) <= 1 and c in [0, width - 1]: continue
    del rows[idx]
    del cols[idx]
  # Shuffle the lists for good measure
  return shuffle(rows), shuffle(cols)


def hollow_rect(ingrid, width, height, row, col, color, must_be_zero=False):
  """Draws a hollow rectangle in a grid."""
  for r in range(height):
    for c in range(width):
      if r in [0, height - 1] or c in [0, width - 1]:
        if must_be_zero and get_pixel(ingrid, row + r, col + c) not in [-1, 0]:
          return False
        draw(ingrid, row + r, col + c, color)
  return True


def hollywood_squares(minisize=3, b=0, g=5, spacing=3):
  size = minisize * spacing + 2
  ingrid = grid(size, size, b)
  for r in range(size):
    for c in range(size):
      line = r % (spacing + 1) == spacing or c % (spacing + 1) == spacing
      ingrid[r][c] = g if line else b
  return ingrid


def hpwl(width, height, rows, cols, b, s, e, p):
  ingrid, output = grids(width, height, b)
  output[rows[0]][cols[0]] = ingrid[rows[0]][cols[0]] = s
  output[rows[1]][cols[1]] = ingrid[rows[1]][cols[1]] = e
  col_dir = 1 if cols[0] < cols[1] else -1
  row_dir = 1 if rows[0] < rows[1] else -1
  for c in range(cols[0] + col_dir, cols[1], col_dir):
    output[rows[0]][c] = p
  for r in range(rows[0], rows[1], row_dir):
    output[r][cols[1]] = p
  return ingrid, output


def isclose(a, b):
  return math.isclose(a, b)


def is_surrounded(bitmap, r, c):
  for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
    if get_pixel(bitmap, r + dr, c + dc) <= 0: return False
  return True


def is_symmetric(colors):
  for r in range(3):
    for c in range(3):
      if colors[r * 3 + c] != colors[r * 3 + 2 - c]: return False
      if colors[r * 3 + c] != colors[(2 - r) * 3 + c]: return False
  return True


def letter_map():
  return {
      "+": [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
      ".": [(1, 1)],
      "/": [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2)],
      "1": [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1), (2, 2)],
      "2": [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
      "4": [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)],
      "7": [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
      ":": [(0, 0), (1, 1), (1, 2), (2, 0)],
      "=": [(0, 0), (0, 1), (0, 2), (2, 0), (2, 1), (2, 2)],
      ">": [(0, 0), (0, 1), (1, 2), (2, 0), (2, 1)],
      "?": [(0, 1), (1, 0), (1, 1), (2, 2)],
      "@": [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
      "A": [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2)],
      "C": [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0), (2, 1), (2, 2)],
      "H": [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2)],
      "I": [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (2, 2)],
      "L": [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
      "N": [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)],
      "O": [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
      "T": [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
      "U": [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
      "V": [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1)],
      "X": [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)],
      "Y": [(0, 0), (0, 2), (1, 1), (2, 1)],
      "|": [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)],
  }


def overlaps(rows, cols, wides, talls, spacing=0):
  for j in range(len(rows)):
    for i in range(j):
      if rows[i] + talls[i] + spacing <= rows[j]: continue
      if rows[j] + talls[j] + spacing <= rows[i]: continue
      if cols[i] + wides[i] + spacing <= cols[j]: continue
      if cols[j] + wides[j] + spacing <= cols[i]: continue
      return True
  return False


def overlaps_1d(cols, wides, spacing=0):
  for j in range(len(cols)):
    for i in range(j):
      if cols[i] + wides[i] + spacing <= cols[j]: continue
      if cols[j] + wides[j] + spacing <= cols[i]: continue
      return True
  return False


def randint(start, stop):
  return random.randint(start, stop)


def randints(start, stop, count):
  return [random.randint(start, stop) for _ in range(count)]


def random_aitch(width, height):
  pixels = []
  for r in range(height):
    pixels.append((r, 0))
  for r in range(height // 2, height):
    pixels.append((r, width - 1))
  for c in range(1, width):
    pixels.append((height // 2, c))
  return pixels


def random_color(exclude=None):
  colors = list(range(1, 10))
  if exclude is not None:
    for color in exclude:
      if color in colors: colors.remove(color)
  return colors[randint(0, len(colors) - 1)]


def random_colors(num, exclude=None):
  colors = list(range(1, 10))
  if exclude is not None:
    for color in exclude:
      if color in colors: colors.remove(color)
  colors = sample(colors, num)
  return colors


def random_el(width, height):
  pixels = []
  for r in range(height):
    pixels.append((r, 0))
  for c in range(1, width):
    pixels.append((height - 1, c))
  return pixels


def random_pixels(width, height, prob=0.5):
  pixels = []
  for r in range(height):
    for c in range(width):
      if random.random() > prob: continue
      pixels.append((r, c))
  return pixels


def random_you(width, height):
  pixels = []
  for r in range(height):
    pixels.append((r, 0))
    pixels.append((r, width - 1))
  for c in range(1, width - 1):
    pixels.append((height - 1, c))
  return pixels


def rect(ingrid, width, height, row, col, color):
  """Draws a rectangle in a grid."""
  for r in range(height):
    for c in range(width):
      draw(ingrid, row + r, col + c, color)


def rect_obscured(ingrid, width, height, row, col, color):
  """Determines if a rectangle is (partially) obscured."""
  for r in range(height):
    for c in range(width):
      if ingrid[row + r][col + c] != color: return True
  return False


def rect_visible(ingrid, width, height, row, col, color):
  visible_corners = 0
  if ingrid[row][col] == color: visible_corners += 1
  if ingrid[row + height - 1][col] == color: visible_corners += 1
  if ingrid[row][col + width - 1] == color: visible_corners += 1
  if ingrid[row + height - 1][col + width - 1] == color: visible_corners += 1
  return visible_corners >= 3


def rectangle_nibbles(wide, tall, coldiff):
  rows, cols = [], []
  for c in range(wide):
    for r in [0, tall - 1]:
      # Magnets need to touch.
      if r > 0 and (c == coldiff or (c == 0 and coldiff < 0)): continue
      if randint(0, 1): continue
      rows.append(r)
      cols.append(c)
      if tall < 3: break  # Too thin to risk taking another bite.
  return rows, cols


def remove_diagonal_neighbors(pixels):
  neighbor_free = []
  for j, pixel in enumerate(pixels):
    is_neighbor = False
    for i in range(j):
      other = pixels[i]
      if abs(other[0] - pixel[0]) <= 1 and abs(other[1] - pixel[1]) <= 1:
        is_neighbor = True
    if not is_neighbor: neighbor_free.append(pixel)
  return neighbor_free


def remove_duplicates(original_list):
  return list(dict.fromkeys(original_list))


def remove_neighbors(pixels):
  neighbor_free = []
  for j, pixel in enumerate(pixels):
    is_neighbor = False
    for i in range(j):
      other = pixels[i]
      if abs(other[0] - pixel[0]) == 0 and abs(other[1] - pixel[1]) == 1:
        is_neighbor = True
      if abs(other[0] - pixel[0]) == 1 and abs(other[1] - pixel[1]) == 0:
        is_neighbor = True
    if not is_neighbor: neighbor_free.append(pixel)
  return neighbor_free


def sample(sequence, k):
  return random.sample(sequence, k)


def shave(wide, tall, row, col):
  """Shaves a rectangle down from some direction."""
  wides, talls, rows, cols = [], [], [], []
  direction = randint(0, 3)
  if direction in [0, 1]:
    left, right = col, col + wide
    for r in range(tall):
      wides.append(right - left)
      talls.append(1)
      rows.append((row + r) if direction == 0 else (row + tall - 1 - r))
      cols.append(left)
      diff = randint(0, 1)
      if left + diff < right: left += diff
      diff = randint(0, 1)
      if left < right - diff: right -= diff
  if direction in [2, 3]:
    bottom, top = row, row + tall
    for c in range(wide):
      wides.append(1)
      talls.append(top - bottom)
      rows.append(bottom)
      cols.append((col + c) if direction == 2 else (col + wide - 1 - c))
      diff = randint(0, 1)
      if bottom + diff < top: bottom += diff
      diff = randint(0, 1)
      if bottom < top - diff: top -= diff
  return wides, talls, rows, cols


def shuffle(sequence):
  return sample(sequence, len(sequence))


def slash(ingrid, length, row, col, color):
  """Draws a slash in a grid."""
  for i in range(length):
    ingrid[row + i][col + length - 1 - i] = color


def slash_obscured(ingrid, length, row, col, color):
  for i in range(length):
    if ingrid[row + i][col + length - 1 - i] != color: return True
  return False


def slash_visible(ingrid, length, row, col, color):
  visible_corners = 0
  if ingrid[row][col + length - 1] == color: visible_corners += 1
  if ingrid[row + length - 1][col] == color: visible_corners += 1
  return visible_corners == 2


def some_abutted(rows, cols, wides, talls):
  for j in range(len(rows)):
    for i in range(j):
      if rows[i] + talls[i] == rows[j] or rows[j] + talls[j] == rows[i]:
        if cols[i] + wides[i] <= cols[j] or cols[j] + wides[j] <= cols[i]:
          continue
        return True
      if cols[i] + wides[i] == cols[j] or cols[j] + wides[j] == cols[i]:
        if rows[i] + talls[i] <= rows[j] or rows[j] + talls[j] <= rows[i]:
          continue
        return True
  return False


def int_sqrt(x):
  return int(math.sqrt(x))


def rand_sprite(name, width, height):
  xpose, pixels = randint(0, 1), []
  if xpose: width, height = height, width
  if name == "el": pixels = random_el(width, height)
  if name == "you": pixels = random_you(width, height)
  if name == "aitch": pixels = random_aitch(width, height)
  if xpose: width, height = height, width
  if xpose: pixels = [(p[1], p[0]) for p in pixels]
  gravity = randint(0, 3)
  if gravity in [1, 3]: pixels = [(height - p[0] - 1, p[1]) for p in pixels]
  if gravity in [2, 3]: pixels = [(p[0], width - p[1] - 1) for p in pixels]
  return pixels


def square_with_unique_max_color(size, color_list):
  while True:
    idxs = [randint(0, len(color_list) - 1) for _ in range(size * size)]
    colors = [color_list[idx] for idx in idxs]
    mode = max(set(colors), key=colors.count)
    modes = [c for c in color_list if colors.count(c) == colors.count(mode)]
    if len(modes) == 1: return colors


def sqrt(x):
  return math.sqrt(x)


def transpose(ingrid):
  w, h = len(ingrid[0]), len(ingrid)
  return [[ingrid[i][j] for i in range(h)] for j in range(w)]


def transpose_inverted(ingrid):
  w, h = len(ingrid[0]), len(ingrid)
  return [[ingrid[h - i - 1][w - j - 1] for i in range(h)] for j in range(w)]


def upsample(ingrid, mult):
  width, height = len(ingrid[0]), len(ingrid)
  output = grid(width * mult, height * mult)
  for row in range(height):
    for col in range(width):
      for dr in range(mult):
        for dc in range(mult):
          output[row * mult + dr][col * mult + dc] = ingrid[row][col]
  return output


internal_colors = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def black():
  return internal_colors[0]


def blue():
  return internal_colors[1]


def red():
  return internal_colors[2]


def green():
  return internal_colors[3]


def yellow():
  return internal_colors[4]


def gray():
  return internal_colors[5]


def pink():
  return internal_colors[6]


def orange():
  return internal_colors[7]


def cyan():
  return internal_colors[8]


def maroon():
  return internal_colors[9]


def set_colors(colors):
  global internal_colors
  internal_colors = colors

