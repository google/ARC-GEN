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

"""Generator."""

import common


def generate(size=None, rows=None, cols=None, idxs=None, brows=None, bcols=None,
             colors=None, shows=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the sprites list
    brows: a list of vertical coordinates of the sprites
    bcols: a list of horizontal coordinates of the sprites
    colors: a list of digits representing the colors to be used
    shows: a list of angles that should be shown
  """

  def draw(grid, output):
    legal = True
    idx_grid = common.grid(size, size)
    for row, col, idx in zip(rows, cols, idxs):
      for angle in range(4):
        r, c, color = brows[idx], bcols[idx], colors[idx * 4 + angle]
        if not color: continue
        if angle == 0: r, c = r - row, c - col
        if angle == 1: r, c = r - row, c + col + 1
        if angle == 2: r, c = r + row + 1, c - col
        if angle == 3: r, c = r + row + 1, c + col + 1
        if output[r][c]: legal = False
        output[r][c] = color
        if shows[idx] == angle or (row == 0 and col == 0): grid[r][c] = color
        # Check that we're not adjacent to another sprite.
        idx_grid[r][c] = idx + 1
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            if common.get_pixel(idx_grid, r + dr, c + dc) in [-1, 0, idx + 1]:
              continue
            legal = False
    return legal

  if size is None:
    num_sprites = common.randint(1, 3)
    while True:
      size = common.randint(12, 30)
      # Allow diagonal connections in the creatures.
      rows, cols, idxs = [], [], []
      for idx in range(num_sprites):
        pixels = common.continuous_creature(common.randint(4, 8), 5, 5)
        rows.extend([p[0] for p in pixels])
        cols.extend([p[1] for p in pixels])
        idxs.extend([idx] * len(pixels))
      brows = [common.randint(5, size - 6) for _ in range(num_sprites)]
      bcols = [common.randint(5, size - 6) for _ in range(num_sprites)]
      colors = []
      for _ in range(num_sprites):
        colors.extend(common.random_colors(4))
      shows = [common.randint(0, 3) for _ in range(num_sprites)]
      # Choose where to place the black angles.
      for idx in range(num_sprites):
        angle = common.randint(0, 3)
        if common.randint(0, 1) or shows[idx] == angle: continue
        colors[idx * 4 + angle] = 0
      grid, output = common.grids(size, size)
      if draw(grid, output): break

  grid, output = common.grids(size, size)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=30,
               rows=[0, 0, 0, 1, 1, 1, 2, 3, 0, 0, 1, 2, 2, 0, 1, 1, 2],
               cols=[0, 1, 2, 0, 2, 3, 0, 1, 0, 1, 1, 0, 2, 0, 1, 2, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2],
               brows=[11, 9, 21], bcols=[6, 16, 13],
               colors=[3, 4, 1, 2, 2, 1, 7, 4, 8, 0, 2, 3],
               shows=[2, 2, 3]),
      generate(size=20,
               rows=[0, 0, 1, 1, 1, 1, 1, 2, 2],
               cols=[0, 1, 0, 1, 2, 3, 4, 1, 3],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0],
               brows=[8], bcols=[7],
               colors=[2, 8, 4, 3],
               shows=[0]),
      generate(size=14,
               rows=[0, 1, 1, 1, 1, 2, 0, 1, 1, 2, 2],
               cols=[0, 0, 1, 2, 3, 1, 0, 1, 2, 1, 2],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
               brows=[7, 3], bcols=[4, 9],
               colors=[0, 1, 2, 4, 8, 4, 0, 6],
               shows=[2, 0]),
  ]
  test = [
      generate(size=24,
               rows=[0, 0, 1, 1, 2, 2, 2, 3, 0, 0, 0, 1, 0, 1, 1, 1, 2],
               cols=[0, 1, 0, 2, 1, 2, 3, 2, 0, 1, 2, 1, 0, 0, 1, 2, 2],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2],
               brows=[6, 6, 16], bcols=[7, 17, 13],
               colors=[8, 2, 4, 3, 3, 2, 1, 8, 1, 0, 2, 4],
               shows=[0, 2, 2]),
  ]
  return {"train": train, "test": test}
