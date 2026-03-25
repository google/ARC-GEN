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


def generate(width=None, height=None, brows=None, bcols=None, rows=None,
             cols=None, groups=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    groups: The groups of the pixels.
  """

  if width is None:
    if common.randint(0, 1):
      width, height = 7, 7
      brows, bcols = [common.randint(1, 2)], [common.randint(1, 2)]
      rows, cols = common.conway_sprite(4, 4)
      groups = [0] * len(rows)
    else:
      width, height = 12, 8
      all_coords = [(0, 0), (0, 4), (0, 8), (4, 0), (4, 4), (4, 8)]
      coords = common.sample(all_coords, 3)
      brows, bcols = zip(*coords)
      rows, cols, groups = [], [], []
      for group in range(3):
        prows, pcols = common.conway_sprite(4, 4)
        rows.extend(prows)
        cols.extend(pcols)
        groups.extend([group] * len(prows))

  grid, output = common.grids(width, height)
  for brow, bcol in zip(brows, bcols):
    common.rect(output, 4, 4, brow, bcol, 2)
  for row, col, group in zip(rows, cols, groups):
    grid[brows[group] + row][bcols[group] + col] = 8
    output[brows[group] + row][bcols[group] + col] = 8
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=8, brows=[0, 0, 4], bcols=[0, 4, 8],
               rows=[0, 1, 1, 2, 2, 2, 3, 3, 0, 1, 1, 2, 2, 2, 3, 3, 3, 0, 1, 2, 2, 2, 2, 3],
               cols=[1, 1, 2, 1, 2, 3, 0, 1, 0, 0, 3, 0, 1, 2, 0, 1, 2, 1, 1, 0, 1, 2, 3, 1],
               groups=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2]),
      generate(width=12, height=8, brows=[0, 4], bcols=[4, 8],
               rows=[0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3],
               cols=[1, 0, 1, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 0, 1, 2, 0, 1, 3, 0, 1],
               groups=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
      generate(width=7, height=7, brows=[1], bcols=[1],
               rows=[0, 0, 1, 1, 1, 1, 2, 3], cols=[0, 3, 0, 1, 2, 3, 2, 1],
               groups=[0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(width=12, height=8, brows=[0, 4, 4], bcols=[8, 0, 4],
               rows=[0, 0, 1, 2, 3, 3, 3, 3, 0, 0, 0, 1, 1, 2, 3, 0, 1, 1, 1, 2, 2, 3, 3],
               cols=[2, 3, 1, 0, 0, 1, 2, 3, 0, 1, 3, 1, 3, 2, 3, 0, 0, 2, 3, 0, 3, 0, 3],
               groups=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2]),
  ]
  return {"train": train, "test": test}
