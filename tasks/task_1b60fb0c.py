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


def generate(rows=None, cols=None, offset=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    offset: whether to offet some copies by a single pixel
    size: the width and height of the (square) grid
  """
  if rows is None:
    pixels = common.continuous_creature(common.randint(6, 12), 4, 4)
    rows, cols = zip(*pixels)
    offset = common.randint(0, 1)

  grid, output = common.grids(size, size)
  for r, c in zip(rows, cols):
    output[4 + r][4 - c + offset] = common.red()
  for r, c in zip(rows, cols):
    for bitmap in [grid, output]:
      bitmap[5 - r + offset][5 + c] = common.blue()
      bitmap[4 - c + offset][5 - r + offset] = common.blue()
      bitmap[5 + c][4 + r] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 1, 1, 1, 1, 2], cols=[0, 2, 3, 0, 1, 2, 3, 3],
               offset=0),
      generate(rows=[-1, -1, 0, 0, 1, 1, 1, 1, 1, 2, 2, 3, 3],
               cols=[3, 4, 3, 4, 0, 1, 2, 3, 4, 3, 4, 3, 4], offset=1),
      generate(rows=[-1, 0, 0, 1, 1, 1, 1, 1, 2, 2, 3],
               cols=[4, 2, 4, 0, 1, 2, 3, 4, 2, 4, 4], offset=1),
  ]
  test = [
      generate(rows=[-1, 0, 0, 1, 1, 1, 1, 1, 2, 3, 0],
               cols=[3, 2, 3, 0, 1, 2, 3, 4, 3, 3, 0], offset=0),
  ]
  return {"train": train, "test": test}
