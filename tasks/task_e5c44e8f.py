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


def generate(prow=None, pcol=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    prow: The row of the green pixel.
    pcol: The column of the green pixel.
    rows: The rows of the red pixels.
    cols: The columns of the red pixels.
  """

  if prow is None:
    prow, pcol = common.randint(4, 6), common.randint(4, 6)
    rows, cols = [], []
    num_reds = common.randint(0, 10)
    for _ in range(num_reds):
      rows.append(common.randint(0, 10))
      cols.append(common.randint(0, 10))

  grid, output = common.grids(11, 11)
  for row, col in zip(rows, cols):
    output[row][col] = grid[row][col] = 2
  output[prow][pcol] = grid[prow][pcol] = 3
  rdir, cdir, length = -1, 0, 2
  for _ in range(21):
    bad = False
    for _ in range(length):
      if common.get_pixel(output, prow, pcol) == 2:
        bad = True
        break
      common.draw(output, prow, pcol, 3)
      prow, pcol = prow + rdir, pcol + cdir
    if bad: break
    if rdir == -1: rdir, cdir = 0, 1
    elif cdir == 1: rdir, cdir = 1, 0
    elif rdir == 1: rdir, cdir = 0, -1
    elif cdir == -1: rdir, cdir = -1, 0
    if cdir == 0: length += 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(prow=5, pcol=5, rows=[0, 0, 2, 3, 3, 8, 8, 9, 10],
               cols=[2, 7, 10, 1, 8, 2, 10, 0, 5]),
      generate(prow=4, pcol=5, rows=[], cols=[]),
      generate(prow=4, pcol=4, rows=[0, 0, 1, 4, 5, 6, 8, 8, 9, 10],
               cols=[6, 10, 1, 9, 1, 8, 0, 3, 8, 5]),
  ]
  test = [
      generate(prow=5, pcol=6, rows=[0, 1, 1, 3, 5, 5, 8, 9, 9, 10],
               cols=[10, 1, 6, 1, 3, 8, 0, 1, 10, 6]),
  ]
  return {"train": train, "test": test}
