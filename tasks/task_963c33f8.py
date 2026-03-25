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


def generate(size=None, bcol=None, blues=None, colors=None, extras=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    bcol: The column to start drawing lines.
    blues: Whether the lines have blue tips.
    colors: The colors of the background.
    extras: Extra offsets to add (to fix ambiguous cases).
  """

  def draw():
    grid, output = common.grids(size, size)
    # First, copy over the contents.
    for i, color in enumerate(colors):
      output[i // size][i % size] = grid[i // size][i % size] = color
    # Second, clear out the forest floor.
    for c in range(3):
      if blues[c]: continue
      for dc in range(-2, 3):
        common.draw(output, size - 1, bcol + c + dc, 7)
    # Third, draw the maroon lines.
    for c in range(3):
      for r in range(3):
        grid[r][bcol + c] = 9
        output[r][bcol + c] = 7
      if blues[c]: grid[2][bcol + c] = 1
      row = 2
      while row + 1 < size:
        if blues[c] and output[row + 1][bcol + c] == 5: break
        row += 1
      for r in range(3):
        offset = 0 if not extras else extras[c]
        output[row - r][bcol + c + offset] = 9
      if not blues[c]: continue
      output[row][bcol + c] = 1
      if row + 1 < size: continue
      # It's not clear if we should clear the forest floor for blue tips.
      for dc in range(-2, 3):
        if common.get_pixel(output, row, bcol + c + dc) == 5: return None, None
    return grid, output

  if size is None:
    size = common.randint(14, 16)
    bcol = common.randint(0, size - 3)
    while True:
      blues = [common.randint(0, 1) for _ in range(3)]
      if sum(blues) == 0: continue
      colors = [7 if common.randint(0, 15) else 5 for _ in range(size * size)]
      grid, _ = draw()
      if grid: break
  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=16, bcol=13, blues=[1, 1, 1],
               colors=[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5, 5, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5, 5, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5, 5, 7, 7,
                       7, 7, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5, 7, 7,
                       7, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 5, 5, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 5, 5, 5, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 5, 5, 5, 5, 5, 5, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]),
      generate(size=14, bcol=5, blues=[0, 1, 0],
               colors=[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 5, 5, 7, 7, 5, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7, 5, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 5, 5, 5, 5, 5, 7, 7, 7,
                       7, 7, 5, 7, 7, 7, 7, 7, 5, 5, 7, 7, 7, 7,
                       7, 5, 7, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 5, 5, 5, 5, 5, 7, 7]),
      generate(size=16, bcol=9, blues=[1, 1, 0],
               colors=[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 5, 7, 7, 5, 5, 5, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 5, 5, 5, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 5, 5, 7, 7, 7, 5,
                       7, 7, 5, 7, 7, 7, 7, 7, 7, 7, 5, 5, 7, 5, 5, 7,
                       7, 7, 5, 7, 7, 7, 5, 7, 7, 7, 5, 7, 7, 5, 7, 7,
                       5, 5, 5, 5, 7, 7, 5, 7, 7, 7, 7, 7, 5, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
               extras=[0, 0, 1]),
  ]
  test = [
      generate(size=16, bcol=3, blues=[1, 0, 0],
               colors=[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 5, 5, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       7, 7, 7, 5, 5, 7, 5, 7, 7, 7, 7, 7, 7, 7, 5, 5,
                       7, 7, 7, 7, 5, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]),
  ]
  return {"train": train, "test": test}
