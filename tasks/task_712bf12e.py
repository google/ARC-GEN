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
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    thicks: The thicknesses of the boxes.
  """

  def draw():
    grid, output = common.grids(width, height)
    for i, color in enumerate(colors):
      output[i // width][i % width] = grid[i // width][i % width] = color
    for col in range(width):
      r, c = height - 1, col
      if grid[r][c] != 2: continue
      if output[r][c - 1] == 2: return None, None  # Shouldn't happen!
      while True:
        if r == 0 or output[r - 1][c] == 0: r -= 1
        elif output[r - 1][c] == 5: c += 1
        else: return None, None  # output must be red, which is not allowed.
        if r < 0 or c >= width or output[r][c] == 5: break
        output[r][c] = 2
    return grid, output

  if width is None:
    width, height = common.randint(12, 15), common.randint(12, 15)
    while True:
      colors = [common.randint(0, 3) for _ in range(width * height)]
      colors = [0 if color else 5 for color in colors]
      cols = sorted(common.sample(list(range(1, width - 1)), 3))
      for col in cols:
        colors[width * (height - 1) + col] = 2
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=13,
               colors=[0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0,
                       0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0,
                       0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0,
                       0, 5, 5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       5, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5,
                       5, 0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 0,
                       5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 5, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 5, 0, 0, 0,
                       5, 0, 2, 0, 0, 2, 0, 5, 5, 0, 2, 0, 0, 0]),
      generate(width=13, height=12,
               colors=[0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0,
                       0, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0,
                       5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0,
                       0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5,
                       0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0,
                       5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5,
                       0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 5, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0,
                       0, 5, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 5, 0, 0,
                       0, 0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0]),
      generate(width=15, height=13,
               colors=[0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 5,
                       0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0,
                       5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 0,
                       0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0,
                       5, 5, 0, 0, 0, 0, 0, 5, 0, 5, 5, 0, 0, 0, 5,
                       0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       0, 0, 0, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0,
                       0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 5, 0, 0,
                       0, 5, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0,
                       0, 0, 5, 0, 0, 0, 0, 0, 0, 5, 5, 0, 5, 0, 0,
                       0, 5, 5, 2, 0, 0, 0, 2, 0, 2, 0, 0, 5, 5, 0]),
  ]
  test = [
      generate(width=13, height=13,
               colors=[0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 5, 5,
                       0, 0, 0, 0, 0, 5, 0, 5, 0, 5, 5, 5, 0,
                       0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0,
                       5, 0, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 5,
                       0, 0, 5, 5, 0, 5, 0, 0, 0, 0, 0, 0, 5,
                       0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0,
                       0, 0, 5, 5, 0, 5, 0, 5, 0, 0, 0, 0, 0,
                       5, 0, 0, 0, 0, 5, 5, 0, 5, 0, 0, 0, 0,
                       0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0,
                       0, 5, 0, 5, 0, 0, 0, 5, 0, 5, 0, 5, 0,
                       0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0,
                       5, 0, 5, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 2, 0, 0, 0, 2, 0, 2, 5, 5, 0]),
  ]
  return {"train": train, "test": test}
