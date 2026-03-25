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


def generate(size=None, length=None, shown=None, brows=None, bcols=None,
             angles=None, pattern=None, extra_rows=None, extra_cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  def draw():
    if common.overlaps(brows, bcols, [5] * len(brows), [5] * len(bcols)):
      return None, None
    grid, output = common.grids(size, size)
    # Draw the yellow dots.
    for brow, bcol, angle in zip(brows, bcols, angles):
      if angle != 0: output[brow][bcol] = grid[brow][bcol] = 4
      if angle != 1: output[brow][bcol + 2] = grid[brow][bcol + 2] = 4
      if angle != 2: output[brow + 2][bcol] = grid[brow + 2][bcol] = 4
      if angle != 3: output[brow + 2][bcol + 2] = grid[brow + 2][bcol + 2] = 4
    # Draw the red sprites.
    for i, (brow, bcol, angle) in enumerate(zip(brows, bcols, angles)):
      for row in range(length):
        for col in range(length):
          color = int(pattern[row * length + col])
          r = brow + 1 + ((row - length) if angle in [0, 1] else (length - row))
          c = bcol + 1 + ((col - length) if angle in [0, 2] else (length - col))
          if r < 0 or r >= size or c < 0 or c >= size: return None, None
          if output[r][c]: return None, None  # Should be empty.
          output[r][c] = color
          if i == shown: grid[r][c] = color
    if extra_rows is not None:
      for row, col in zip(extra_rows, extra_cols):
        grid[row][col] = 2
    return grid, output

  if size is None:
    size, length = common.randint(25, 30), common.randint(2, 3)
    rows, cols = common.conway_sprite(length, length, common.randint(0, length))
    pixels = list(zip(rows, cols))
    pattern = ""
    for row in range(length):
      for col in range(length):
        pattern += "2" if (row, col) in pixels else "0"
    num_boxes = common.randint(3, 8)
    shown = common.randint(0, num_boxes - 1)
    angles = [common.randint(0, 3) for _ in range(num_boxes)]
    while True:
      brows = [common.randint(0, size - 3) for _ in range(num_boxes)]
      bcols = [common.randint(0, size - 3) for _ in range(num_boxes)]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=26, length=3, shown=0, brows=[5, 7, 17, 18, 23],
               bcols=[4, 16, 16, 6, 23], angles=[0, 1, 2, 0, 0],
               pattern="220202022"),
      generate(size=30, length=2, shown=2, brows=[1, 2, 10, 10, 20, 20, 24],
               bcols=[5, 14, 5, 19, 2, 20, 9], angles=[0, 0, 3, 1, 3, 1, 0],
               pattern="2222"),
      generate(size=25, length=3, shown=1, brows=[2, 5, 13, 19],
               bcols=[15, 3, 12, 5], angles=[0, 0, 3, 2], pattern="202002222",
               extra_rows=[3, 4], extra_cols=[2, 1]),
  ]
  test = [
      generate(size=27, length=3, shown=6, brows=[2, 5, 7, 12, 15, 15, 21, 22],
               bcols=[19, 5, 16, 22, 3, 13, 19, 7],
               angles=[1, 2, 0, 3, 1, 0, 3, 0], pattern="222202220"),
  ]
  return {"train": train, "test": test}
