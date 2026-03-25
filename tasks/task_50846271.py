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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    colors: a list of colors to be used in the input grid
  """
  if width is None:
    height = common.randint(10, 25)
    width = height + common.randint(-3, 3)
    # First, create random static.
    pixels = common.random_pixels(width, height)
    rows, cols = zip(*pixels)
    grid = common.grid(width, height)
    for r, c in zip(rows, cols):
      grid[r][c] = common.gray()
    # Second, create a few crosses underneath.
    length = common.randint(2, 3)
    rows, cols, lens = [], [], []
    for _ in range(4):
      r = common.randint(length, height - length - 1)
      c = common.randint(length, width - length - 1)
      if common.overlaps(rows + [r], cols + [c], lens + [2 * length],
                         lens + [2 * length], 2): continue
      rows.append(r)
      cols.append(c)
      lens.append(2 * length)
      for idx in range(-length, length + 1):  # TODO: ensure center&length known
        if grid[r][c + idx]:
          grid[r][c + idx] = common.cyan()
        else:
          grid[r][c + idx] = common.red()
        if grid[r + idx][c]:
          grid[r + idx][c] = common.cyan()
        else:
          grid[r + idx][c] = common.red()
    # Finally, flatten the colors into a list.
    colors = []
    for r in range(height):
      for c in range(width):
        colors.append(grid[r][c])

  grid, output = common.grids(width, height)
  for r in range(height):
    for c in range(width):
      output[r][c] = colors[r * width + c]
      if colors[r * width + c] != common.cyan():
        grid[r][c] = colors[r * width + c]
      else:
        grid[r][c] = common.gray()

  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=22, height=20,
               colors=[0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 5, 5, 5, 5, 5, 0, 0, 5,
                       0, 0, 0, 0, 5, 0, 0, 5, 5, 5, 5, 0, 0, 5, 0, 5, 0, 5, 0,
                       0, 5, 0, 0, 5, 5, 5, 0, 5, 5, 0, 5, 5, 5, 0, 0, 5, 5, 2,
                       0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 5, 5, 0, 0, 0, 5, 0,
                       0, 0, 2, 5, 5, 5, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0,
                       0, 0, 5, 0, 0, 2, 5, 5, 0, 0, 5, 0, 5, 5, 0, 0, 5, 0, 0,
                       5, 0, 0, 0, 5, 2, 8, 2, 8, 8, 8, 2, 5, 0, 5, 0, 0, 0, 0,
                       5, 5, 0, 5, 0, 0, 0, 0, 0, 5, 0, 2, 5, 0, 0, 5, 0, 0, 5,
                       5, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 5, 0, 2, 5, 0, 5, 5,
                       0, 5, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 2, 0,
                       0, 0, 0, 0, 0, 5, 0, 5, 5, 0, 0, 5, 0, 0, 0, 0, 0, 5, 5,
                       0, 5, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 5, 0, 5, 5, 5,
                       5, 5, 0, 0, 0, 0, 5, 0, 5, 5, 5, 0, 5, 5, 0, 5, 5, 0, 0,
                       8, 0, 0, 5, 0, 5, 5, 0, 5, 5, 0, 5, 5, 0, 0, 5, 5, 0, 0,
                       5, 5, 0, 2, 5, 5, 5, 0, 0, 5, 0, 0, 0, 0, 0, 5, 5, 0, 0,
                       0, 5, 0, 5, 0, 0, 8, 5, 5, 0, 0, 0, 0, 0, 5, 0, 0, 5, 5,
                       0, 0, 0, 5, 0, 0, 2, 8, 8, 2, 2, 2, 2, 0, 0, 0, 5, 5, 0,
                       5, 0, 0, 5, 0, 5, 0, 0, 5, 5, 0, 0, 8, 5, 0, 5, 0, 0, 5,
                       0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 2, 0, 5, 5,
                       0, 5, 0, 0, 5, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 5, 5, 0, 2,
                       5, 0, 0, 0, 5, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 5, 0, 5, 5,
                       5, 0, 0, 0, 5, 5, 5, 5, 0, 0, 5, 5, 0, 5, 0, 0, 0, 5, 5,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 5, 0,
                       0, 0, 5]),
      generate(width=20, height=20,
               colors=[0, 5, 0, 5, 0, 0, 0, 5, 5, 0, 5, 5, 0, 0, 0, 5, 5, 0, 5,
                       5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 0, 5, 0, 0, 5, 0, 0, 0, 5,
                       5, 0, 0, 5, 0, 5, 5, 0, 8, 5, 0, 5, 0, 0, 5, 0, 0, 5, 0,
                       0, 5, 5, 5, 0, 0, 5, 5, 0, 2, 5, 0, 5, 0, 5, 0, 0, 0, 5,
                       5, 5, 5, 5, 0, 5, 0, 5, 2, 8, 2, 2, 2, 0, 5, 5, 0, 5, 0,
                       5, 5, 0, 0, 0, 5, 5, 0, 0, 5, 5, 2, 5, 5, 5, 0, 5, 0, 0,
                       5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 8, 5, 0, 0, 5, 5, 0,
                       0, 5, 0, 0, 5, 0, 5, 0, 0, 0, 5, 0, 5, 0, 5, 5, 5, 0, 5,
                       5, 5, 0, 0, 5, 5, 0, 5, 5, 0, 0, 0, 5, 0, 0, 5, 5, 5, 5,
                       0, 5, 5, 8, 0, 0, 5, 0, 5, 5, 0, 0, 5, 0, 5, 5, 5, 0, 5,
                       5, 0, 5, 0, 8, 5, 5, 5, 5, 5, 5, 0, 5, 5, 0, 5, 5, 5, 5,
                       5, 0, 5, 2, 8, 2, 2, 2, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0,
                       0, 5, 5, 5, 0, 0, 8, 0, 0, 5, 0, 5, 0, 0, 5, 0, 0, 5, 0,
                       5, 5, 0, 5, 5, 5, 5, 8, 5, 5, 5, 5, 0, 5, 5, 0, 0, 5, 5,
                       0, 8, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0,
                       5, 5, 8, 0, 5, 5, 0, 5, 5, 5, 5, 0, 0, 5, 5, 0, 0, 5, 0,
                       5, 8, 8, 2, 2, 8, 5, 0, 0, 5, 0, 0, 5, 5, 0, 0, 0, 5, 5,
                       0, 0, 5, 5, 2, 5, 0, 5, 5, 0, 0, 5, 0, 5, 5, 0, 0, 0, 0,
                       5, 0, 5, 0, 5, 8, 0, 5, 5, 5, 0, 0, 5, 0, 0, 0, 5, 0, 0,
                       0, 5, 0, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 0, 0, 5, 5,
                       5, 5, 5, 0, 5, 0, 5, 0, 5, 5, 0, 0, 5, 5, 0, 0, 0, 0, 0,
                       5]),
      generate(width=19, height=18,
               colors=[0, 0, 5, 0, 5, 0, 5, 5, 5, 5, 0, 5, 5, 0, 0, 0, 5, 5, 0,
                       0, 0, 5, 5, 5, 0, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 5, 0, 5,
                       0, 5, 5, 5, 0, 5, 0, 5, 5, 0, 0, 0, 5, 5, 5, 0, 5, 0, 0,
                       5, 5, 5, 5, 5, 0, 0, 0, 5, 5, 5, 5, 5, 5, 0, 0, 5, 0, 0,
                       5, 5, 0, 0, 0, 5, 5, 5, 0, 5, 5, 8, 5, 0, 0, 0, 5, 0, 0,
                       5, 0, 0, 0, 0, 0, 5, 0, 5, 0, 5, 2, 5, 0, 0, 5, 0, 5, 5,
                       5, 0, 5, 0, 0, 5, 5, 0, 5, 2, 2, 8, 2, 2, 5, 5, 0, 5, 0,
                       0, 8, 0, 5, 5, 5, 5, 5, 0, 5, 0, 8, 5, 5, 5, 0, 5, 5, 5,
                       5, 8, 5, 0, 5, 5, 5, 5, 0, 0, 5, 2, 5, 5, 5, 0, 0, 0, 0,
                       8, 2, 2, 8, 0, 0, 5, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0,
                       5, 2, 5, 5, 5, 0, 0, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 0, 5,
                       0, 2, 5, 0, 5, 5, 0, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 0,
                       0, 5, 0, 0, 5, 5, 0, 0, 5, 5, 0, 0, 5, 0, 0, 5, 0, 0, 0,
                       5, 0, 0, 5, 5, 5, 5, 5, 0, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5,
                       0, 5, 5, 5, 0, 0, 5, 0, 0, 0, 5, 0, 5, 5, 5, 5, 0, 0, 0,
                       5, 5, 0, 0, 5, 5, 5, 5, 0, 5, 5, 0, 5, 0, 5, 0, 0, 0, 0,
                       5, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 5, 0, 5,
                       0, 5, 5, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 5, 5, 5,
                       5]),
      generate(width=12, height=11,
               colors=[0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 5, 5, 0, 5, 0, 0, 0, 0,
                       0, 5, 0, 0, 5, 5, 0, 5, 0, 0, 5, 5, 0, 2, 0, 5, 0, 5, 5,
                       0, 0, 5, 0, 5, 0, 2, 5, 0, 5, 5, 0, 0, 5, 5, 5, 2, 8, 2,
                       2, 2, 0, 5, 5, 5, 0, 5, 5, 0, 5, 2, 0, 0, 5, 5, 5, 5, 0,
                       5, 0, 0, 5, 8, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0,
                       0, 0, 5, 5, 0, 5, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 5, 5,
                       5, 5, 5, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 5, 5, 5, 5]),
  ]
  test = [
      generate(width=22, height=19,
               colors=[0, 5, 0, 5, 0, 0, 5, 5, 0, 5, 0, 0, 0, 5, 0, 5, 0, 0, 0,
                       5, 5, 0, 0, 5, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 5, 5, 0, 0,
                       0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 5, 5, 8, 0, 0, 0, 0, 5, 5,
                       0, 0, 5, 5, 0, 0, 5, 5, 5, 0, 0, 5, 5, 0, 5, 8, 5, 0, 5,
                       0, 5, 0, 5, 0, 5, 5, 0, 5, 5, 5, 0, 0, 5, 0, 5, 2, 2, 8,
                       2, 2, 5, 0, 0, 5, 0, 5, 5, 5, 0, 0, 5, 5, 0, 0, 0, 0, 5,
                       0, 5, 2, 5, 5, 5, 0, 5, 0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 5,
                       5, 0, 0, 5, 5, 2, 0, 5, 5, 0, 0, 0, 8, 0, 0, 0, 5, 5, 5,
                       5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 8, 0, 5, 0,
                       0, 5, 0, 5, 0, 5, 5, 5, 5, 5, 0, 0, 5, 5, 0, 5, 2, 8, 2,
                       8, 8, 0, 0, 5, 5, 5, 0, 0, 0, 0, 5, 5, 5, 0, 0, 5, 0, 0,
                       0, 5, 8, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 5,
                       0, 5, 0, 5, 5, 2, 5, 0, 5, 0, 0, 5, 5, 0, 0, 5, 5, 5, 0,
                       0, 0, 5, 5, 5, 5, 0, 0, 5, 0, 5, 5, 0, 0, 0, 5, 5, 5, 5,
                       0, 0, 5, 8, 5, 0, 0, 5, 5, 0, 5, 0, 5, 5, 0, 0, 5, 5, 0,
                       5, 0, 0, 5, 5, 5, 8, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 5, 0,
                       0, 5, 0, 5, 5, 5, 0, 8, 8, 2, 2, 2, 5, 5, 5, 0, 5, 8, 5,
                       0, 5, 0, 0, 5, 5, 0, 5, 0, 0, 0, 5, 2, 5, 0, 5, 0, 5, 0,
                       5, 8, 5, 5, 0, 0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 2, 0, 5, 5,
                       0, 0, 2, 2, 2, 2, 2, 5, 0, 5, 0, 5, 5, 5, 0, 5, 0, 0, 5,
                       0, 5, 0, 0, 0, 0, 0, 8, 0, 5, 5, 5, 0, 5, 5, 0, 5, 5, 5,
                       5, 5, 0, 5, 0, 5, 5, 5, 5, 0, 8, 0, 0, 5, 5, 0, 5, 0,
                       5]),
  ]
  return {"train": train, "test": test}
