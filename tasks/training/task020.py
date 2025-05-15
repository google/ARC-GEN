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


def generate(row=None, col=None, radius=None, keep=None, colors=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical coordinate for the center of the board
    col: a horizontal coordinate for the center of the board
    radius: how far from the center is the blast
    keep: which cell to keep in the blast radius
    colors: a list of four digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if row is None:
    row, col = common.randint(3, size - 4), common.randint(3, size - 4)
    radius = common.randint(1, 3)
    keep = common.randint(0, 3)
    colors = [common.choice([1, 2, 3, 4, 8]) for _ in range(4)]

  grid, output = common.grids(size, size)
  output[row][col] = grid[row][col] = colors[0]
  radius_1 = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
  radius_2 = [(-2, 0), (0, 2), (2, 0), (0, -2)]
  radius_3 = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
  for idx in range(len(radius_1)):
    dr, dc = radius_1[idx]
    if radius != 1 or keep == idx: grid[row + dr][col + dc] = colors[1]
    output[row + dr][col + dc] = colors[1]
  for idx in range(len(radius_2)):
    dr, dc = radius_2[idx]
    if radius != 2 or keep == idx: grid[row + dr][col + dc] = colors[2]
    output[row + dr][col + dc] = colors[2]
  for idx in range(len(radius_3)):
    dr, dc = radius_3[idx]
    if radius != 3 or keep == idx: grid[row + dr][col + dc] = colors[3]
    output[row + dr][col + dc] = colors[3]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=3, col=4, radius=3, keep=0, colors=[3, 2, 8, 3]),
      generate(row=4, col=4, radius=3, keep=0, colors=[4, 4, 3, 2]),
      generate(row=3, col=5, radius=1, keep=0, colors=[1, 4, 8, 8]),
  ]
  test = [
      generate(row=4, col=3, radius=2, keep=0, colors=[1, 2, 4, 1]),
  ]
  return {"train": train, "test": test}
