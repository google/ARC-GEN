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
    colors: The colors of the pixels.
  """

  def draw():
    grid, output = common.grids(width, height)
    for i, color in enumerate(colors):
      grid[i // width][i % width] = color
    matches = 0
    for r in range(height):
      row = [color for color in colors[r * width:(r + 1) * width]]
      pair = [color for color in row if color]
      if pair == [7, 4] or pair == [4, 7] or pair == [1, 8] or pair == [8, 1]:
        matches += 1
        row = [color if color != pair[1] else 0 for color in row]
        row[row.index(pair[0]) + 1] = pair[1]
      for i, color in enumerate(row):
        output[r][i] = color
    return grid, output, matches

  if width is None:
    expected_matches = common.randint(2, 4)
    while True:
      width, height = common.randint(3, 10), common.randint(3, 10)
      colors = []
      for r in range(height):
        row = [0] * width
        if r not in [0, height - 1] or common.randint(0, 1):
          pair, wide = common.random_colors(2), common.randint(3, width)
          col = common.randint(0, width - wide)
          row[col], row[col + wide - 1] = pair[0], pair[1]
        colors += row
      _, _, matches = draw()
      if matches == expected_matches: break

  grid, output, _ = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=10, colors=[0, 0, 8, 0, 0, 0, 0, 9, 0, 0,
                                            0, 0, 6, 0, 0, 0, 0, 7, 0, 0,
                                            0, 7, 0, 0, 0, 0, 0, 0, 0, 4,
                                            0, 0, 0, 2, 0, 4, 0, 0, 0, 0,
                                            0, 0, 0, 0, 1, 0, 0, 0, 0, 8,
                                            0, 0, 3, 0, 0, 0, 9, 0, 0, 0,
                                            6, 0, 0, 0, 0, 0, 0, 4, 0, 0,
                                            0, 0, 4, 0, 0, 7, 0, 0, 0, 0,
                                            0, 0, 0, 0, 0, 0, 8, 0, 1, 0,
                                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=5, height=3, colors=[4, 0, 7, 0, 0,
                                          0, 9, 0, 0, 2,
                                          0, 0, 1, 0, 4]),
      generate(width=7, height=4, colors=[0, 8, 0, 4, 0, 0, 0,
                                          4, 0, 0, 0, 0, 0, 7,
                                          0, 0, 1, 0, 0, 8, 0,
                                          0, 9, 0, 0, 4, 0, 0]),
      generate(width=8, height=7, colors=[0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 1, 0, 8, 0, 0, 0, 0,
                                          0, 0, 6, 0, 0, 0, 0, 7,
                                          0, 0, 0, 4, 0, 7, 0, 0,
                                          3, 0, 0, 0, 4, 0, 0, 0,
                                          0, 2, 0, 0, 0, 9, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(width=4, height=4, colors=[0, 7, 0, 4,
                                          6, 0, 8, 0,
                                          8, 0, 1, 0,
                                          0, 4, 0, 3]),
  ]
  return {"train": train, "test": test}
