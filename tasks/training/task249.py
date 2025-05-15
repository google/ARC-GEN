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


def generate(width=None, height=None, rows=None, cols=None, idxs=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the colors list
    colors: a list of digits representing colors to be used
  """
  if width is None:
    width, height = common.randint(3, 5), common.randint(3, 5)
    pixels = common.random_pixels(width, height)
    rows, cols = zip(*pixels)
    colors = common.random_colors(width * height // 3)
    idxs = [common.randint(0, len(colors) - 1) for _ in pixels]

  grid = common.grid(width, height)
  output = common.grid(2 * width, height)
  for r, c, idx in zip(rows, cols, idxs):
    output[r][width + c] = output[r][c] = grid[r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=3, rows=[0, 1, 1, 1], cols=[1, 0, 1, 2],
               idxs=[0, 0, 0, 1], colors=[5, 2]),
      generate(width=3, height=4, rows=[0, 1, 1, 2, 2, 2, 3],
               cols=[0, 0, 1, 0, 1, 2, 1], idxs=[0, 1, 0, 1, 2, 3, 2],
               colors=[3, 2, 1, 8]),
      generate(width=4, height=4,
               rows=[0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3],
               cols=[0, 1, 2, 0, 1, 2, 0, 1, 2, 3, 2],
               idxs=[0, 1, 2, 1, 0, 2, 0, 1, 3, 3, 4], colors=[5, 2, 3, 8, 6]),
  ]
  test = [
      generate(width=4, height=5, rows=[0, 1, 1, 2, 2, 3, 3, 3, 4],
               cols=[0, 0, 1, 1, 2, 0, 1, 2, 3],
               idxs=[0, 0, 1, 1, 2, 2, 2, 3, 3], colors=[4, 5, 6, 1]),
  ]
  return {"train": train, "test": test}
