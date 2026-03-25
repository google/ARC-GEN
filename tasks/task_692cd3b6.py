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


def generate(brows=None, bcols=None, angles=None, flip=None):
  """Returns input and output grids according to the given parameters.

  Args:
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    angles: The angles of the boxes.
    flip: Whether to flip the grids.
  """

  if brows is None:
    brows, bcols, angles = [], [], [common.randint(0, 3) for _ in range(2)]
    brows.append(common.randint(1 if angles[0] != 0 else 2, 4))
    brows.append(common.randint(10, 13 if angles[1] != 2 else 12))
    bcols.append(common.randint(1 if angles[0] != 3 else 2, 4))
    bcols.append(common.randint(10, 13 if angles[1] != 1 else 12))
    flip = common.randint(0, 1)

  grid, output = common.grids(15, 15)
  # Draw the red/grey boxes.
  for brow, bcol, angle in zip(brows, bcols, angles):
    common.rect(grid, 3, 3, brow - 1, bcol - 1, 2)
    common.rect(output, 3, 3, brow - 1, bcol - 1, 2)
    output[brow][bcol] = grid[brow][bcol] = 5
    row, col = brow, bcol
    if angle == 0: row -= 1
    if angle == 1: col += 1
    if angle == 2: row += 1
    if angle == 3: col -= 1
    grid[row][col], output[row][col] = 0, 4
  # Draw the big yellow box.
  lb_row, lb_col, ub_row, ub_col = brows[0], bcols[0], brows[1], bcols[1]
  if angles[0] == 0: lb_row, lb_col = lb_row - 2, lb_col + 2
  if angles[0] == 1: lb_col = lb_col + 2
  if angles[0] == 2: lb_row = lb_row + 2
  if angles[0] == 3: lb_row, lb_col = lb_row + 2, lb_col - 2
  if angles[1] == 0: ub_row = ub_row - 2
  if angles[1] == 1: ub_row, ub_col = ub_row - 2, ub_col + 2
  if angles[1] == 2: ub_row, ub_col = ub_row + 2, ub_col - 2
  if angles[1] == 3: ub_col = ub_col - 2
  wide, tall = ub_col - lb_col + 1, ub_row - lb_row + 1
  common.rect(output, wide, tall, lb_row, lb_col, 4)
  # Draw the extra yellow bits.
  if angles[0] == 0: output[brows[0] - 2][bcols[0]] = 4
  if angles[0] == 0: output[brows[0] - 2][bcols[0] + 1] = 4
  if angles[0] == 3: output[brows[0]][bcols[0] - 2] = 4
  if angles[0] == 3: output[brows[0] + 1][bcols[0] - 2] = 4
  if angles[1] == 1: output[brows[1]][bcols[1] + 2] = 4
  if angles[1] == 1: output[brows[1] - 1][bcols[1] + 2] = 4
  if angles[1] == 2: output[brows[1] + 2][bcols[1]] = 4
  if angles[1] == 2: output[brows[1] + 2][bcols[1] - 1] = 4
  if flip: grid, output = common.flip(grid), common.flip(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(brows=[3, 10], bcols=[2, 10], angles=[2, 1], flip=True),
      generate(brows=[3, 11], bcols=[3, 12], angles=[2, 3], flip=False),
      generate(brows=[2, 13], bcols=[2, 10], angles=[0, 1], flip=False),
  ]
  test = [
      generate(brows=[3, 12], bcols=[3, 10], angles=[3, 1], flip=True),
  ]
  return {"train": train, "test": test}
