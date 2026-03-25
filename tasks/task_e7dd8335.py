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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    colors: A list of colors to use.
  """

  if width is None:
    base = common.randint(8, 10)
    width, height = base + common.randint(-2, 2), base + common.randint(-2, 2)
    wide = common.randint(3, width - 1)
    tall = 2 * common.randint(2, height // 2 - 1)
    brow = common.randint(0, height - tall)
    bcol = common.randint(0, width - wide)
    while True:
      sprite = common.grid(wide, tall)
      for row in range(tall):
        for col in range(wide):
          if common.randint(0, 3): continue
          sprite[row][col] = sprite[tall - row - 1][col] = 1
      pixels = []
      good = True
      for row in range(tall):
        covered = False
        for col in range(wide):
          if not sprite[row][col]: continue
          pixels.append((row, col))
          covered = True
        if not covered: good = False
      if good and common.diagonally_connected(pixels): break
    grid = common.grid(width, height)
    for row in range(tall):
      for col in range(wide):
        if not sprite[row][col]: continue
        grid[brow + row][bcol + col] = 1 if row < tall // 2 else 2
    colors = common.flatten(grid)

  grid, output = common.grids(width, height)
  for i, color in enumerate(colors):
    output[i // width][i % width] = color
    grid[i // width][i % width] = 1 if color else 0
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=9, height=8,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 1, 1, 1, 1, 0, 0, 0, 0,
                       0, 1, 0, 0, 1, 0, 0, 0, 0,
                       0, 1, 0, 0, 1, 0, 0, 0, 0,
                       0, 2, 0, 0, 2, 0, 0, 0, 0,
                       0, 2, 0, 0, 2, 0, 0, 0, 0,
                       0, 2, 2, 2, 2, 0, 0, 0, 0]),
      generate(width=7, height=7,
               colors=[0, 1, 1, 1, 1, 1, 0,
                       0, 1, 0, 1, 0, 1, 0,
                       0, 1, 0, 1, 0, 1, 0,
                       0, 2, 0, 2, 0, 2, 0,
                       0, 2, 0, 2, 0, 2, 0,
                       0, 2, 2, 2, 2, 2, 0,
                       0, 0, 0, 0, 0, 0, 0]),
      generate(width=9, height=9,
               colors=[0, 0, 0, 1, 0, 0, 0, 0, 0,
                       0, 1, 1, 1, 1, 1, 0, 0, 0,
                       0, 0, 1, 0, 1, 0, 0, 0, 0,
                       0, 0, 1, 0, 1, 0, 0, 0, 0,
                       0, 0, 2, 0, 2, 0, 0, 0, 0,
                       0, 0, 2, 0, 2, 0, 0, 0, 0,
                       0, 2, 2, 2, 2, 2, 0, 0, 0,
                       0, 0, 0, 2, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(width=11, height=9,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0,
                       0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0,
                       1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0,
                       2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 0,
                       0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0,
                       0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
