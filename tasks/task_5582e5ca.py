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


def generate(colors=None, rows=None, cols=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing different colors
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
  """
  if colors is None:
    colors = common.sample(range(0, 10), 6)
    colors[5] = colors[4] if common.randint(0, 3) < 3 else colors[5]
    pixels = common.shuffle(common.all_pixels(size, size))
    rows, cols = zip(*pixels)

  grid, output = common.grid(size, size, 0), common.grid(size, size, colors[0])
  grid[rows[0]][cols[0]] = colors[0]
  grid[rows[1]][cols[1]] = colors[0]
  grid[rows[2]][cols[2]] = colors[0]
  grid[rows[3]][cols[3]] = colors[1]
  grid[rows[4]][cols[4]] = colors[1]
  grid[rows[5]][cols[5]] = colors[2]
  grid[rows[6]][cols[6]] = colors[3]
  grid[rows[7]][cols[7]] = colors[4]
  grid[rows[8]][cols[8]] = colors[5]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[4, 3, 0, 8, 6, 6],
               rows=[0, 0, 1, 1, 2, 2, 0, 1, 2],
               cols=[0, 1, 1, 2, 1, 2, 2, 0, 0]),
      generate(colors=[9, 1, 4, 6, 8, 8],
               rows=[0, 2, 2, 1, 1, 2, 0, 0, 1],
               cols=[2, 0, 2, 0, 2, 1, 0, 1, 1]),
      generate(colors=[6, 4, 1, 9, 8, 8],
               rows=[0, 1, 2, 0, 1, 1, 0, 2, 2],
               cols=[1, 0, 2, 0, 1, 2, 2, 0, 1]),
  ]
  test = [
      generate(colors=[8, 6, 0, 3, 4, 9],
               rows=[0, 0, 2, 0, 1, 2, 2, 1, 1],
               cols=[0, 1, 0, 2, 1, 2, 1, 0, 2]),
  ]
  return {"train": train, "test": test}
