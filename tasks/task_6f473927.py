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
    width: The width of the input grid.
    height: The height of the input grid.
    colors: A list of colors to use.
  """

  def draw():
    # First, verify that the shape exists and is diagonally connected.
    rows, cols = [], []
    for row in range(height):
      for col in range(width):
        if colors[row * width + col]:
          rows.append(row)
          cols.append(col)
    if not rows or not cols: return None, None
    if not common.diagonally_connected(list(zip(rows, cols))): return None, None
    # Second, draw the shape.
    grid, output = common.grid(width, height), common.grid(2 * width, height)
    rite = 1 if sum([colors[r * width] for r in range(height)]) else 0
    left = 1 if sum([colors[r * width + width - 1] for r in range(height)]) else 0
    if rite == left: return None, None  # Both columns are clear, no good.
    common.rect(output, width, height, 0, (1 - rite) * width, 8)
    for i, color in enumerate(colors):
      grid[i // width][i % width] = color
      output[i // width][rite * width + i % width] = color
      if not color: continue
      output[i // width][2 * width - 1 - (rite * width + i % width)] = 0
    return grid, output

  if width is None:
    width = common.randint(3, 6)
    height = common.randint(width, 2 * width)
    while True:
      colors = [0 if common.randint(0, 3) else 2 for _ in range(width * height)]
      side = common.randint(0, 1)  # Clear either the left or right side.
      for r in range(height):
        colors[r * width + side * (width - 1)] = 0
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=3, colors=[0, 2, 0,
                                          0, 2, 2,
                                          0, 0, 2]),
      generate(width=6, height=8, colors=[2, 0, 0, 0, 0, 0,
                                          2, 2, 2, 0, 0, 0,
                                          0, 0, 2, 0, 0, 0,
                                          0, 2, 2, 2, 0, 0,
                                          0, 0, 2, 2, 0, 0,
                                          2, 2, 0, 0, 0, 0,
                                          2, 2, 2, 2, 2, 0,
                                          2, 0, 0, 0, 0, 0]),
      generate(width=3, height=3, colors=[2, 2, 0,
                                          2, 0, 0,
                                          2, 2, 0]),
      generate(width=5, height=10, colors=[0, 0, 0, 0, 0,
                                           0, 0, 0, 0, 2,
                                           0, 0, 0, 2, 0,
                                           0, 0, 2, 0, 2,
                                           0, 2, 2, 2, 2,
                                           0, 0, 0, 0, 2,
                                           0, 0, 2, 2, 0,
                                           0, 0, 0, 0, 2,
                                           0, 0, 0, 2, 2,
                                           0, 0, 0, 0, 0]),
  ]
  test = [
      generate(width=6, height=12, colors=[0, 0, 0, 0, 0, 0,
                                           0, 0, 0, 0, 0, 2,
                                           0, 0, 0, 0, 2, 0,
                                           0, 0, 0, 2, 2, 2,
                                           0, 0, 0, 0, 2, 2,
                                           0, 2, 2, 2, 0, 0,
                                           0, 0, 0, 2, 2, 2,
                                           0, 0, 0, 0, 0, 2,
                                           0, 0, 0, 0, 2, 2,
                                           0, 0, 0, 0, 2, 2,
                                           0, 0, 0, 0, 0, 0,
                                           0, 0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
