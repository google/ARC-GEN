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


def generate(size=None, inners=None, outers=None, fgcolor=None, bgcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    inners: The colors of the inner shape.
    outers: The colors of the outer shape.
    fgcolor: The color of the foreground.
    bgcolor: The color of the background.
  """

  if size is None:
    size = common.randint(2, 5)
    colors = common.random_colors(2, exclude=[1, 2, 5])
    fgcolor, bgcolor = colors[0], colors[1]
    inners = [0 for _ in range(size * size)]
    outers = [0 for _ in range(size * size)]
    rows, cols = common.conway_sprite(size, size)
    for r, c in zip(rows, cols):
      inners[r * size + c] = 1
    rows, cols = common.conway_sprite(size, size)
    for r, c in zip(rows, cols):
      outers[r * size + c] = 1

  width, height = min(30, (size + 3) * 4 - 1), size + 2
  grid = common.grid(width, height)
  output = common.grid(size * size, size * size, bgcolor)
  for c in range(size + 2, width, size + 3):
    for r in range(height):
      grid[r][c] = 5
  for i, inner in enumerate(inners):
    grid[i // size + 1][i % size + 1] = 1 * inner
  for i, outer in enumerate(outers):
    grid[i // size + 1][size + i % size + 4] = 2 * outer
  common.rect(grid, size, size, 1, 2 * size + 7, fgcolor)
  common.rect(grid, size, size, 1, 3 * size + 10, bgcolor)
  for row in range(size):
    for col in range(size):
      if not outers[row * size + col]: continue
      for r in range(size):
        for c in range(size):
          if not inners[r * size + c]: continue
          output[row * size + r][col * size + c] = fgcolor
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, inners=[1, 0, 1, 1, 0, 1, 1, 1, 1],
               outers=[1, 1, 0, 1, 0, 1, 0, 1, 1], fgcolor=3, bgcolor=9),
      generate(size=3, inners=[1, 1, 1, 0, 1, 0, 1, 1, 1],
               outers=[1, 1, 1, 0, 1, 0, 0, 1, 0], fgcolor=4, bgcolor=8),
      generate(size=4, inners=[1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1],
               outers=[1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1],
               fgcolor=7, bgcolor=8),
  ]
  test = [
      generate(size=5,
               inners=[1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1],
               outers=[1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
               fgcolor=3, bgcolor=4),
  ]
  return {"train": train, "test": test}
