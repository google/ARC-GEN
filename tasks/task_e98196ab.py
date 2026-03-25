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


def generate(rows=None, cols=None, idxs=None, colors=None, width=11, height=5):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the colors list
    colors: a list of colors to use for the pixels
    width: the width of the grid
    height: the height of the grid
  """
  if rows is None:
    pixels = common.random_pixels(width, height, 0.2)
    rows, cols = zip(*pixels)
    idxs = [common.randint(0, 1) for _ in pixels]
    colors = common.random_colors(2, exclude=[common.gray()])

  grid = common.grid(width, 2 * height + 1)
  output = common.grid(width, height)
  for c in range(width):
    grid[height][c] = common.gray()
  for r, c, idx in zip(rows, cols, idxs):
    output[r][c] = grid[r + height + 1 if idx else r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 2, 2, 4, 4, 1, 1, 3, 3, 4, 4],
               cols=[5, 3, 7, 1, 9, 4, 6, 2, 8, 0, 10],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], colors=[8, 1]),
      generate(rows=[0, 0, 0, 2, 2, 4, 0, 1, 1, 2, 2, 4, 4, 4],
               cols=[1, 5, 9, 3, 8, 1, 10, 0, 8, 2, 4, 0, 6, 10],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1], colors=[3, 7]),
      generate(rows=[1, 1, 1, 1, 1, 2, 3, 3, 3, 4, 0, 0, 0, 4, 4, 4],
               cols=[1, 3, 4, 6, 9, 6, 2, 4, 7, 10, 0, 5, 10, 0, 4, 8],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
               colors=[1, 2]),
  ]
  test = [
      generate(rows=[0, 1, 1, 1, 2, 3, 3, 3, 4, 0, 0, 0, 1, 2, 2, 2, 3, 4, 4],
               cols=[10, 2, 3, 8, 6, 1, 3, 10, 6, 0, 4, 6, 10, 0, 4, 10, 9, 0,
                     3],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               colors=[7, 6]),
  ]
  return {"train": train, "test": test}
