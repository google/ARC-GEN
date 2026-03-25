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


def generate(width=None, height=None, wides=None, talls=None, rows=None,
             cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
  """

  if width is None:
    width, height = common.randint(11, 20), common.randint(11, 20)
    num_rects = common.randint(2, 3)
    while True:
      shorts = [common.randint(3, 8) for _ in range(num_rects)]
      longs = [common.randint(3, 11) for _ in range(num_rects)]
      wides, talls = [], []
      for short, long in zip(shorts, longs):
        flip = common.randint(0, 1)
        wides.append(short if flip else long)
        talls.append(long if flip else short)
      rows = [common.randint(0, height - tall) for tall in talls]
      cols = [common.randint(0, width - wide) for wide in wides]
      if not common.overlaps(rows, cols, wides, talls, 1): break

  grid, output = common.grids(width, height)
  for wide, tall, row, col in zip(wides, talls, rows, cols):
    common.rect(grid, wide, tall, row, col, 1)
    common.rect(output, wide, tall, row, col, 1)
    color = 0
    while True:
      wide, tall = wide - 2, tall - 2
      row, col = row + 1, col + 1
      if wide <= 0 or tall <= 0: break
      common.rect(output, wide, tall, row, col, color + 2)
      color = (color + 1) % 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=12, wides=[8, 3], talls=[7, 3], rows=[1, 9], cols=[1, 8]),
      generate(width=11, height=12, wides=[4, 3, 5], talls=[4, 3, 6], rows=[1, 1, 6], cols=[1, 7, 2]),
      generate(width=14, height=15, wides=[8, 7], talls=[8, 5], rows=[1, 10], cols=[2, 4]),
  ]
  test = [
      generate(width=17, height=15, wides=[11, 7, 5], talls=[6, 8, 3], rows=[0, 7, 9], cols=[2, 9, 1]),
  ]
  return {"train": train, "test": test}
