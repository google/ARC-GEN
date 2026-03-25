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


def generate(size=None, wide=None, tall=None, brow=None, bcol=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grids.
    wide: The width of the rectangle.
    tall: The height of the rectangle.
    brow: The row of the top left corner of the rectangle.
    bcol: The column of the top left corner of the rectangle.
    color: The color of the rectangle.
  """

  if size is None:
    size = common.randint(15, 30)
    angle = common.randint(0, 1)
    while True:
      wide = common.randint(1, 2) if angle == 0 else common.randint(2, 5)
      tall = common.randint(2, 5) if angle == 0 else common.randint(1, 2)
      if wide != tall: break
    brow = common.randint(5, size - tall - 5)
    bcol = common.randint(5, size - wide - 5)
    color = common.choice([3, 6])

  grid, output = common.grids(size, size)
  common.rect(grid, wide, tall, brow, bcol, color)
  rows, cols, w, t, c = [brow] * 4, [bcol] * 4, wide, tall, color
  for _ in range(30):
    for row, col in zip(rows, cols):
      common.rect(output, w, t, row, col, c)
    w, t = t, w
    rows[0] -= t
    cols[0] -= w
    rows[1] -= t
    cols[1] += t
    rows[2] += w
    cols[2] -= w
    rows[3] += w
    cols[3] += t
    c = 6 if c == 3 else 3
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=16, wide=3, tall=1, brow=7, bcol=7, color=3),
      generate(size=23, wide=2, tall=4, brow=5, bcol=6, color=6),
      generate(size=26, wide=2, tall=5, brow=5, bcol=11, color=3),
  ]
  test = [
      generate(size=16, wide=1, tall=2, brow=7, bcol=5, color=6),
  ]
  return {"train": train, "test": test}
