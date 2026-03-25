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


def generate(wides=None, talls=None, brows=None, bcols=None, colors=None,
             angles=None, lengths=None, downs=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    colors: The colors of the boxes.
    angles: The angles of the pulls.
    lengths: The lengths of the pulls.
    downs: How far down the pulls are placed on each box.
  """

  def draw():
    pulled_colors = [color for color, angle in zip(colors, angles) if angle != -1]
    grid, output = common.grids(20, 20)
    # First, draw everything.
    for wide, tall, brow, bcol, color, angle, length, down in zip(
        wides, talls, brows, bcols, colors, angles, lengths, downs):
      for r in range(brow, brow + tall):
        for c in range(bcol, bcol + wide):
          if grid[r][c]:
            if grid[r][c] in pulled_colors: return None, None  # Can't draw over
      common.rect(grid, wide, tall, brow, bcol, color)
      if angle != -1:
        for i in range(length):
          row, col = brow, bcol
          if angle == 0: row, col = brow - 1 - i, bcol + down
          if angle == 1: row, col = brow + down, bcol + wide + i
          if angle == 2: row, col = brow + tall + i, bcol + down
          if angle == 3: row, col = brow + down, bcol - 1 - i
          if row < 0 or col < 0 or row >= 20 or col >= 20:
            return None, None  # The pixel is out of bounds.
          if grid[row][col] and grid[row][col] in pulled_colors: return None, None
          grid[row][col] = color
      row, col = brow, bcol
      if angle == 0: row, col = brow - length, bcol
      if angle == 1: row, col = brow, bcol + length
      if angle == 2: row, col = brow + length, bcol
      if angle == 3: row, col = brow, bcol - length
      if row < 0 or col < 0 or row + tall >= 20 or col + wide >= 20:
        return None, None  # The new box is out of bounds.
      for r in range(row, row + tall):
        for c in range(col, col + wide):
          if output[r][c]:
            if output[r][c] in pulled_colors: return None, None
      common.rect(output, wide, tall, row, col, color)
    # Second, check that at least three corners per box are visible.
    for wide, tall, brow, bcol, color, angle, length, down in zip(
        wides, talls, brows, bcols, colors, angles, lengths, downs):
      corners = 0
      if grid[brow][bcol] == color: corners += 1
      if grid[brow][bcol + wide - 1] == color: corners += 1
      if grid[brow + tall - 1][bcol] == color: corners += 1
      if grid[brow + tall - 1][bcol + wide - 1] == color: corners += 1
      if corners < 3: return None, None
      row, col = brow, bcol
      if angle == 0: row, col = brow - length, bcol
      if angle == 1: row, col = brow, bcol + length
      if angle == 2: row, col = brow + length, bcol
      if angle == 3: row, col = brow, bcol - length
      corners = 0
      if output[row][col] == color: corners += 1
      if output[row][col + wide - 1] == color: corners += 1
      if output[row + tall - 1][col] == color: corners += 1
      if output[row + tall - 1][col + wide - 1] == color: corners += 1
      if corners < 3: return None, None
    return grid, output

  if wides is None:
    num_boxes = common.randint(3, 5)
    colors = common.random_colors(num_boxes)
    while True:
      wides = [common.randint(3, 9) for _ in range(num_boxes)]
      talls = [common.randint(3, 9) for _ in range(num_boxes)]
      brows = [common.randint(1, 20 - tall - 1) for tall in talls]
      bcols = [common.randint(1, 20 - wide - 1) for wide in wides]
      angles = [common.randint(-1, 3) for _ in range(num_boxes)]
      lengths = [common.randint(1, 5) for _ in range(num_boxes)]
      downs = [common.randint(1, (wide - 2) if angle in [0, 2] else (tall - 2)) for wide, tall, angle in zip(wides, talls, angles)]
      if angles.count(-1) > len(angles) - 2: continue  # Need at least 2 pulls.
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[5, 6, 7, 9, 6], talls=[4, 4, 5, 4, 7], brows=[1, 8, 14, 3, 11], bcols=[2, 12, 10, 5, 3], colors=[3, 1, 8, 7, 6], angles=[-1, -1, -1, 2, 1], lengths=[0, 0, 0, 2, 2], downs=[0, 0, 0, 4, 4]),
      generate(wides=[7, 9, 6, 5, 7], talls=[6, 5, 6, 3, 3], brows=[1, 4, 11, 12, 10], bcols=[1, 4, 11, 1, 2], colors=[6, 5, 2, 3, 8], angles=[-1, 1, -1, -1, 1], lengths=[0, 3, 0, 0, 4], downs=[0, 2, 0, 0, 1]),
      generate(wides=[9, 3, 3], talls=[8, 4, 4], brows=[4, 6, 15], bcols=[2, 16, 5], colors=[3, 8, 2], angles=[-1, 3, 1], lengths=[0, 4, 6], downs=[0, 2, 1]),
  ]
  test = [
      generate(wides=[6, 4, 5, 8, 6], talls=[4, 4, 5, 5, 3], brows=[1, 2, 7, 10, 16], bcols=[1, 8, 14, 3, 7], colors=[2, 8, 1, 3, 7], angles=[-1, 3, 0, -1, 0], lengths=[0, 5, 2, 0, 2], downs=[0, 1, 2, 0, 3]),
  ]
  return {"train": train, "test": test}
