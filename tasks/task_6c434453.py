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


def generate(rows=None, cols=None, idxs=None, size=10, num=5):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of sprite types (0=box, 1=plus, 2=minus, etc.)
    size: the width and height of the (square) grid
    num: the number of sprites to generate
  """

  def draw_sprite(bitmap, r, c, idx, color):
    p = None
    p = p if idx != 0 else [(0,0),(0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2)]
    p = p if idx != 1 else [(0,1),(1,0),(1,1),(1,2),(2,1)]
    p = p if idx != 2 else [(2,1),(2,2)]
    p = p if idx != 3 else [(0,0),(0,1),(1,0),(1,1)]
    p = p if idx != 4 else [(0,0),(1,0),(1,1),(1,2)]
    p = p if idx != 5 else [(1,1),(1,2),(2,1),(2,2)]
    for pixel in p:
      bitmap[r + pixel[0]][c + pixel[1]] = color

  def draw(grid, output, sprite_grid):
    for r, c, idx in zip(rows, cols, idxs):
      draw_sprite(grid, r, c, idx, common.blue())
      color = common.red() if idx == 0 else common.blue()
      draw_sprite(output, r, c, 1 if idx == 0 else idx, color)
      draw_sprite(sprite_grid, r, c, idx, idx + 1)
    for r in range(size):
      for c in range(size):
        if not sprite_grid[r][c]: continue
        for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
          color = common.get_pixel(sprite_grid, r + dr, c + dc)
          if color not in [-1, 0, sprite_grid[r][c]]: return False
    return True

  if rows is None:
    while True:
      rows = [common.randint(0, size - 3) for _ in range(num)]
      cols = [common.randint(0, size - 3) for _ in range(num)]
      idxs = [common.randint(0, 5) for _ in range(num)]
      if 0 not in idxs: continue  # We need at least one box to convert!
      overlaps = False
      # First, check if there are "strict" overlaps (based on boundaries).
      for j in range(num):
        for i in range(j):
          if abs(rows[i] - rows[j]) > 2 or abs(cols[i] - cols[j]) > 2:
            continue
          overlaps = True
      # Second, check if the edges of any two sprite pixels are adjacent.
      bitmap = common.grid(size, size)
      for i, idx in enumerate(idxs):
        r, c = rows[i], cols[i]
        draw_sprite(bitmap, r, c, idx, i + 1)
      for r in range(1, size - 1):
        for c in range(1, size - 1):
          if not bitmap[r][c]: continue
          for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if bitmap[r + dr][c + dc] in [common.black(), bitmap[r][c]]:
              continue
            overlaps = True
      grid, output = common.grids(size, size)
      sprite_grid = common.grid(size, size)
      if not draw(grid, output, sprite_grid): continue
      if not overlaps: break

  grid, output = common.grids(size, size)
  sprite_grid = common.grid(size, size)
  draw(grid, output, sprite_grid)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 4, 6, 5], cols=[0, 6, 0, 3, 7],
               idxs=[0, 1, 1, 0, 2]),
      generate(rows=[0, 1, 3, 5, 7], cols=[4, 0, 7, 1, 6],
               idxs=[0, 3, 1, 0, 4]),
  ]
  test = [
      generate(rows=[0, 2, 4, 7, 7], cols=[7, 1, 5, 1, 7],
               idxs=[1, 0, 2, 0, 5]),
  ]
  return {"train": train, "test": test}
