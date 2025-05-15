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


def generate(row=None, col=None, rows=None, cols=None, idxs=None, colors=None,
             size=10, zoom_size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical offset for the pinwheel
    col: a horizontal offset for the pinwheel
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the color list
    colors: a list of colors to be used
    size: the width and height of the (square) input grid
    zoom_size: the width and height of the (square) output grid
  """
  if row is None:
    row, col = common.randint(1, 3), common.randint(1, 3)
    pixels = [(1, 1), (1, 2), (2, 1), (2, 2)]
    pixels.extend(common.sample([(0, 0), (0, 2), (2, 0)], common.randint(1, 2)))
    rows, cols = [p[0] for p in pixels], [p[1] for p in pixels]
    colors = common.random_colors(common.randint(3, 5))
    idxs = [common.randint(0, len(colors) - 1) for _ in pixels]

  grid = common.grid(size, size)
  output = common.grid(zoom_size, zoom_size)
  for r, c, idx in zip(rows, cols, idxs):
    edge = 2 * zoom_size - 1
    grid[row + r][col + c] = colors[idx]
    grid[row + edge - c][col + r] = colors[idx]
    grid[row + c][col + edge - r] = colors[idx]
    grid[row + edge - r][col + edge - c] = colors[idx]
    output[r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=2, col=2, rows=[0, 1, 1, 2, 2, 2], cols=[2, 1, 2, 0, 1, 2],
               idxs=[0, 1, 2, 0, 2, 3], colors=[7, 6, 8, 4]),
      generate(row=1, col=1, rows=[0, 1, 1, 2, 2], cols=[0, 1, 2, 1, 2],
               idxs=[0, 1, 2, 3, 4], colors=[1, 3, 6, 5, 2]),
  ]
  test = [
      generate(row=2, col=2, rows=[1, 1, 2, 2, 2], cols=[1, 2, 0, 1, 2],
               idxs=[0, 0, 1, 1, 2], colors=[4, 8, 3]),
  ]
  return {"train": train, "test": test}
