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


def generate(size=None, pair=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the box.
    pair: The pair of colors.
    colors: The colors of the grid.
  """

  if size is None:
    size = 2 * common.randint(3, 4)
    pair = common.random_colors(2, exclude=[5])
    colors = []
    for _ in range(100):
      color = common.randint(0, 2)
      colors.append(0 if color == 0 else pair[color - 1])

  grid, output = common.grids(10, 10)
  for i, color in enumerate(colors):
    r, c = i // 10, i % 10
    output[r][c] = grid[r][c] = color
    if r < 5 - size // 2 or r >= 5 + size // 2: continue
    if c < 5 - size // 2 or c >= 5 + size // 2: continue
    if grid[r][c] == pair[0]: output[r][c] = pair[1]
    if grid[r][c] == pair[1]: output[r][c] = pair[0]
  for g in [grid, output]:
    for i in range(size):
      g[5 - size // 2][5 - size // 2 + i] = 5
      g[5 + size // 2 - 1][5 - size // 2 + i] = 5
      g[5 - size // 2 + i][5 - size // 2] = 5
      g[5 - size // 2 + i][5 + size // 2 - 1] = 5
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=8, pair=[6, 8], colors=[0, 0, 8, 6, 0, 6, 0, 8, 0, 8,
                                            8, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                            0, 0, 0, 8, 8, 6, 6, 0, 0, 8,
                                            6, 0, 6, 6, 6, 8, 0, 6, 0, 8,
                                            0, 0, 6, 6, 8, 6, 0, 6, 0, 8,
                                            6, 0, 8, 8, 8, 6, 8, 0, 0, 8,
                                            6, 0, 6, 8, 6, 8, 6, 8, 0, 8,
                                            0, 0, 6, 0, 6, 8, 8, 8, 0, 8,
                                            8, 0, 0, 0, 0, 0, 0, 0, 0, 6,
                                            8, 8, 8, 0, 8, 8, 6, 0, 6, 6]),
      generate(size=6, pair=[4, 9], colors=[9, 4, 0, 0, 4, 9, 0, 0, 9, 9,
                                            4, 9, 9, 4, 9, 9, 0, 0, 9, 0,
                                            0, 0, 0, 5, 5, 5, 5, 5, 0, 9,
                                            9, 4, 0, 9, 0, 9, 9, 5, 0, 4,
                                            4, 4, 0, 0, 0, 4, 0, 5, 4, 4,
                                            9, 4, 0, 4, 9, 0, 9, 5, 0, 0,
                                            0, 9, 0, 0, 4, 0, 0, 5, 0, 4,
                                            0, 4, 0, 5, 5, 5, 5, 5, 4, 4,
                                            9, 0, 9, 9, 4, 0, 9, 0, 0, 0,
                                            9, 9, 9, 0, 9, 4, 9, 9, 0, 0]),
      generate(size=8, pair=[2, 3], colors=[0, 0, 3, 3, 3, 3, 2, 0, 2, 0,
                                            3, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                                            3, 0, 3, 2, 2, 2, 2, 0, 0, 2,
                                            0, 0, 0, 3, 0, 3, 2, 2, 0, 2,
                                            3, 0, 2, 0, 2, 3, 2, 2, 0, 3,
                                            3, 0, 3, 3, 0, 2, 3, 3, 0, 3,
                                            3, 0, 3, 3, 3, 0, 3, 2, 0, 2,
                                            0, 0, 3, 0, 3, 3, 3, 0, 0, 3,
                                            0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                                            2, 0, 3, 3, 3, 2, 3, 2, 3, 0]),
  ]
  test = [
      generate(size=8, pair=[1, 7], colors=[7, 0, 1, 1, 7, 0, 0, 7, 7, 7,
                                            1, 0, 0, 0, 0, 0, 0, 0, 0, 7,
                                            1, 0, 0, 0, 1, 0, 1, 7, 0, 7,
                                            0, 0, 7, 1, 7, 0, 1, 7, 0, 1,
                                            7, 0, 7, 7, 0, 1, 7, 1, 0, 1,
                                            7, 0, 0, 1, 7, 0, 7, 7, 0, 1,
                                            1, 0, 7, 7, 1, 1, 1, 1, 0, 0,
                                            0, 0, 1, 7, 7, 7, 7, 0, 0, 7,
                                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                            0, 1, 7, 1, 0, 7, 0, 0, 7, 7]),
  ]
  return {"train": train, "test": test}
