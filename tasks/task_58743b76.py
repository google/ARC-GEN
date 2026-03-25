# Copyright 2026 Google LLC
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


def generate(size=None, colors=None, rows=None, cols=None, flip=None, flop=None,
             fgcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    colors: The colors of the pixels.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    flip: Whether to flip the grid.
    flop: Whether to flop the grid.
    fgcolor: The foreground color of the grid.
  """

  def draw(show_border=True):
    grid, output = common.grids(size, size)
    if show_border:
      common.rect(grid, size, 2, 0, 0, 8)
      common.rect(grid, 2, size, 0, 0, 8)
      common.rect(output, size, 2, 0, 0, 8)
      common.rect(output, 2, size, 0, 0, 8)
      for i, color in enumerate(colors):
        output[i // 2][i % 2] = grid[i // 2][i % 2] = color
    for row, col in zip(rows, cols):
      grid[row + 2][col + 2] = fgcolor
      r, c = row // ((size - 2) // 2), col // ((size - 2) // 2)
      output[row + 2][col + 2] = colors[r * 2 + c]
    if flip: grid, output = common.flip(grid), common.flip(output)
    if flop: grid, output = common.flop(grid), common.flop(output)
    return grid, output

  if size is None:
    size = 2 * common.randint(4, 7)
    colors = common.random_colors(4, exclude=[8])
    fgcolor = common.random_color(exclude=[8])
    while True:
      pixels = common.random_pixels(size - 2, size - 2, 0.2)
      if not pixels: continue
      rows, cols = zip(*pixels)
      _, output = draw(show_border=False)
      unflattened = []
      for row in output: unflattened.extend(row)
      if len(set(unflattened)) == 5: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=12, colors=[6, 4, 2, 1],
               rows=[0, 1, 1, 3, 3, 3, 4, 5, 7, 7, 8, 9, 9],
               cols=[5, 1, 8, 2, 3, 9, 1, 6, 2, 8, 8, 0, 5],
               flip=False, flop=True, fgcolor=2),
      generate(size=10, colors=[1, 4, 3, 2],
               rows=[0, 1, 2, 2, 4, 4, 5, 6, 6, 7],
               cols=[4, 1, 5, 7, 2, 5, 5, 1, 4, 7],
               flip=False, flop=False, fgcolor=1),
  ]
  test = [
      generate(size=14, colors=[4, 7, 1, 3],
               rows=[0, 1, 1, 2, 2, 4, 4, 4, 5, 6, 7, 8, 9, 9, 10, 10, 10, 11],
               cols=[10, 3, 4, 1, 7, 3, 6, 11, 10, 7, 3, 1, 8, 11, 2, 4, 8, 10],
               flip=True, flop=True, fgcolor=1),
  ]
  return {"train": train, "test": test}
