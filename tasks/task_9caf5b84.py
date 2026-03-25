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
    colors: A list of colors to use.
  """

  def draw():
    grid, output = common.grids(width, height)
    for i, color in enumerate(colors):
      output[i // width][i % width] = grid[i // width][i % width] = color
    subset = list(set(colors))
    counts = [(colors.count(color), color) for color in subset]
    counts = sorted(counts, reverse=True)
    if len(subset) != 5 or counts[1][0] == counts[2][0]: return None, None
    for row in range(height):
      for col in range(width):
        if output[row][col] not in [counts[0][1], counts[1][1]]:
          output[row][col] = 7
    return grid, output

  if width is None:
    width, height = 2 * common.randint(2, 3), 2 * common.randint(2, 3)
    subset = common.sample([0, 1, 2, 3, 4, 5, 6, 8, 9], 5)
    while True:
      colors = common.choices(subset, width * height)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=6, height=6,
               colors=[1, 2, 5, 5, 0, 3,
                       3, 0, 2, 3, 1, 3,
                       1, 5, 3, 5, 2, 1,
                       2, 3, 5, 1, 1, 5,
                       3, 3, 0, 1, 2, 0,
                       3, 1, 5, 1, 3, 1]),
      generate(width=4, height=4,
               colors=[0, 9, 5, 9,
                       9, 2, 5, 2,
                       0, 2, 5, 1,
                       1, 2, 9, 2]),
      generate(width=6, height=6,
               colors=[9, 1, 2, 1, 1, 2,
                       1, 1, 2, 6, 3, 6,
                       6, 1, 6, 6, 9, 6,
                       6, 2, 9, 6, 9, 3,
                       1, 2, 6, 2, 6, 1,
                       1, 6, 3, 3, 2, 3]),
      generate(width=6, height=4,
               colors=[1, 2, 1, 0, 0, 0,
                       0, 6, 1, 0, 1, 0,
                       0, 4, 1, 0, 2, 6,
                       4, 1, 2, 1, 1, 1]),
  ]
  test = [
      generate(width=4, height=6,
               colors=[6, 8, 5, 8,
                       4, 9, 6, 4,
                       5, 8, 9, 4,
                       6, 9, 9, 4,
                       8, 8, 9, 5,
                       9, 5, 6, 9]),
  ]
  return {"train": train, "test": test}
