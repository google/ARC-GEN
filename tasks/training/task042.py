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


def generate(rows=None, cols=None, flips=None, magnify=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    flips: a list of 0 or 1 values (should the boxes be flipped?)
    magnify: how much the boxes should be enlarged
    size: the width and height of the (square) grid
  """
  if rows is None:
    magnify = common.randint(1, 3)
    row = common.randint(1, size - 2 * magnify - 1)
    col = common.randint(1, size - 2 * magnify - 1)
    rows, cols = [row], [col]
    if col + 6 * magnify < size and common.randint(0, 1):
      row = common.randint(1, size - 2 * magnify - 1)
      col = common.randint(col + 3 * magnify, size - 2 * magnify - 1)
      rows.append(row)
      cols.append(col)
    flips = [common.randint(0, 1) for _ in rows]

  grid, output = common.grids(size, size)
  for r, col, flip in zip(rows, cols, flips):
    for dr in range(magnify):
      for dc in range(magnify):
        c0 = col - magnify if flip else col + 2 * magnify
        c1 = col + magnify if flip else col
        c2 = col if flip else col + magnify
        c3 = col + 2 * magnify if flip else col - magnify
        common.draw(grid, r + dr, c1 + dc, common.green())
        common.draw(grid, r + dr + magnify, c2 + dc, common.green())
        common.draw(output, r + dr, c1 + dc, common.green())
        common.draw(output, r + dr + magnify, c2 + dc, common.green())
        common.draw(output, r + dr - magnify, c0 + dc, common.cyan())
        common.draw(output, r + dr + 2 * magnify, c3 + dc, common.cyan())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[3, 6], cols=[2, 6], flips=[0, 1], magnify=1),
      generate(rows=[3], cols=[1], flips=[1], magnify=2),
      generate(rows=[3], cols=[3], flips=[0], magnify=1),
  ]
  test = [
      generate(rows=[2], cols=[3], flips=[1], magnify=3),
  ]
  return {"train": train, "test": test}
