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


def generate(rows=None, cols=None, colors=None, size=10, minisize=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) input grid
    minisize: the width and height of the (square) output grid
  """
  if rows is None:
    colors = [common.random_color() for _ in range(common.randint(6, 9))]
    rows = [common.randint(0, size - 1) for _ in colors]
    cols = common.sample(range(size), len(colors))
    cols.sort()

  grid, output = common.grid(size, size), common.grid(minisize, minisize)
  for r, c, color in zip(rows, cols, colors):
    grid[r][c] = color
  for idx, color in enumerate(colors):
    output[idx // minisize][idx % minisize] = color
  output[1] = output[1][::-1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[4, 2, 8, 2, 5, 7], cols=[0, 1, 2, 4, 6, 9],
               colors=[3, 1, 8, 6, 7, 9]),
      generate(rows=[5, 7, 1, 4, 2, 6, 1], cols=[0, 1, 2, 4, 6, 8, 9],
               colors=[9, 3, 4, 6, 8, 5, 2]),
      generate(rows=[8, 3, 1, 5, 1, 8, 4, 2, 0],
               cols=[0, 1, 2, 4, 5, 6, 7, 8, 9],
               colors=[2, 4, 5, 3, 9, 1, 5, 1, 3]),
  ]
  test = [
      generate(rows=[7, 3, 9, 5, 1, 8, 1, 4, 2],
               cols=[0, 1, 2, 3, 4, 5, 6, 7, 9],
               colors=[5, 2, 9, 3, 5, 4, 9, 6, 1]),
  ]
  return {"train": train, "test": test}
