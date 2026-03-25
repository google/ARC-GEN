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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if colors is None:
    # Choose the colors along the side.
    height = common.randint(7, 8)
    row = start = common.randint(1, 9 - height)
    subset = common.random_colors(common.randint(2, 4), exclude=[5])
    while True:
      segments = [common.randint(1, 4) for _ in subset]
      if sum(segments) == height: break
    # Draw the side.
    grid = common.grid(10, 10)
    for color, segment in zip(subset, segments):
      for _ in range(segment):
        grid[row][0] = color
        row += 1
    # Draw the grey shape.
    width = common.randint(3, 5)
    while True:
      if common.randint(0, 1):
        length = common.randint(2, width)
        pos = common.randint(0, width - length)
        row = common.randint(0, height - 1)
        for col in range(pos, pos + length):
          grid[start + row][3 + col] = 5
      else:
        length = common.randint(2, height)
        pos = common.randint(0, height - length)
        col = common.randint(0, width - 1)
        for row in range(pos, pos + length):
          grid[start + row][3 + col] = 5
      # Check if every row has grey.
      good = True
      for row in range(start, start + height):
        see_grey = False
        for col in range(10):
          if grid[row][col] == 5: see_grey = True
        if not see_grey: good = False
      if not good: continue
      # Check if it's connected.
      pixels = []
      for row in range(10):
        for col in range(10):
          if grid[row][col] == 5: pixels.append((row, col))
      if common.connected(pixels): break
    colors = common.flatten(grid)

  grid, output = common.grids(10, 10)
  for i, color in enumerate(colors):
    output[i // 10][i % 10] = grid[i // 10][i % 10] = color
  for row in range(10):
    for col in range(10):
      if output[row][col]: output[row][col] = output[row][0]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       9, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       9, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       6, 0, 0, 0, 5, 5, 0, 0, 0, 0,
                       6, 0, 0, 5, 5, 5, 0, 0, 0, 0,
                       6, 0, 0, 5, 0, 5, 0, 0, 0, 0,
                       4, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       4, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       4, 0, 0, 0, 5, 5, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       8, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       8, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       8, 0, 0, 5, 5, 5, 0, 0, 0, 0,
                       2, 0, 0, 5, 0, 0, 0, 0, 0, 0,
                       2, 0, 0, 5, 0, 0, 0, 0, 0, 0,
                       2, 0, 0, 5, 5, 5, 5, 0, 0, 0,
                       2, 0, 0, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       2, 0, 0, 0, 5, 5, 0, 5, 0, 0,
                       2, 0, 0, 5, 5, 5, 5, 5, 0, 0,
                       3, 0, 0, 5, 0, 0, 0, 0, 0, 0,
                       3, 0, 0, 5, 5, 5, 0, 0, 0, 0,
                       3, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       4, 0, 0, 5, 5, 5, 5, 0, 0, 0,
                       7, 0, 0, 5, 5, 5, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
