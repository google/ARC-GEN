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


def generate(rows=None, cols=None, colors=None, size=13, minisize=4):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) input grid
    minisize: the width and height of the (square) output grid
  """
  if rows is None:
    colors = common.random_colors(4)
    while True:
      rows = [common.randint(0, size - 2) for _ in range(4)]
      cols = [common.randint(0, size - 2) for _ in range(4)]
      lengths = [2] * 4
      if not common.overlaps(rows, cols, lengths, lengths, 1): break

  grid, output = common.grid(size, size), common.grid(minisize, minisize)
  output[0][0] = grid[rows[0]][cols[0]] = colors[0]
  output[0][1] = grid[rows[0]][cols[0] + 1] = colors[0]
  output[1][0] = grid[rows[0] + 1][cols[0]] = colors[0]
  output[0][2] = grid[rows[1]][cols[1]] = colors[1]
  output[0][3] = grid[rows[1]][cols[1] + 1] = colors[1]
  output[1][3] = grid[rows[1] + 1][cols[1] + 1] = colors[1]
  output[2][0] = grid[rows[2]][cols[2]] = colors[2]
  output[3][0] = grid[rows[2] + 1][cols[2]] = colors[2]
  output[3][1] = grid[rows[2] + 1][cols[2] + 1] = colors[2]
  output[2][3] = grid[rows[3]][cols[3] + 1] = colors[3]
  output[3][2] = grid[rows[3] + 1][cols[3]] = colors[3]
  output[3][3] = grid[rows[3] + 1][cols[3] + 1] = colors[3]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 3, 9, 7], cols=[6, 1, 3, 7], colors=[8, 2, 3, 1]),
      generate(rows=[3, 1, 9, 5], cols=[2, 8, 4, 7], colors=[1, 8, 4, 2]),
  ]
  test = [
      generate(rows=[9, 2, 6, 2], cols=[2, 10, 6, 2], colors=[3, 8, 1, 6]),
  ]
  return {"train": train, "test": test}
