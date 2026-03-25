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


def generate(rows=None, cols=None, idxs=None, colors=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the color list
    colors: a list of colors to be used
    size: the width and height of the (square) input grid
  """
  if rows is None:
    pixels = common.sample(common.all_pixels(size, size), common.randint(5, 9))
    rows, cols = zip(*pixels)
    colors = common.random_colors(common.randint(2, 4))
    idxs = [common.randint(0, len(colors) - 1) for _ in pixels]

  grid, output = common.grid(size, size), common.grid(2 * size, 2 * size)
  for r, c, idx in zip(rows, cols, idxs):
    grid[r][c] = colors[idx]
    output[r][c] = colors[idx]
    output[2 * size - c - 1][r] = colors[idx]
    output[c][2 * size - r - 1] = colors[idx]
    output[2 * size - r - 1][2 * size - c - 1] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 1, 2, 2], cols=[0, 1, 0, 1, 2, 1, 2],
               idxs=[0, 1, 0, 1, 2, 2, 3], colors=[8, 5, 3, 2]),
      generate(rows=[0, 0, 0, 1, 1, 1, 2, 2, 2],
               cols=[0, 1, 2, 0, 1, 2, 0, 1, 2],
               idxs=[0, 1, 2, 0, 2, 2, 1, 3, 2], colors=[3, 8, 2, 5]),
      generate(rows=[0, 1, 1, 1, 2], cols=[1, 0, 1, 2, 1], idxs=[0, 1, 1, 1, 0],
               colors=[3, 6]),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 1, 2, 2, 2], cols=[0, 1, 0, 1, 2, 0, 1, 2],
               idxs=[0, 1, 0, 1, 2, 3, 2, 2], colors=[2, 5, 1, 3]),
  ]
  return {"train": train, "test": test}
