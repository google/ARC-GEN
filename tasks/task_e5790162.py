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


def generate(width=None, height=None, row=None, lengths=None, flip=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    row: The row of the pixel.
    lengths: The lengths of the lines.
    flip: Whether to flip the grid.
  """

  def draw():
    grid, output = common.grids(width, height)
    r, c = row, 0
    grid[r][c] = 3
    for i, length in enumerate(lengths):
      for j in range(length):
        if r >= height or c >= width: return None, None
        output[r][c] = 3
        if j + 1 == length and i + 1 < len(lengths):
          if i % 2 == 0:
            if r >= height or c + 1 >= width: return None, None
            output[r][c + 1] = grid[r][c + 1] = 8 if flip else 6
          else:
            if r + 1 >= height or c >= width: return None, None
            output[r + 1][c] = grid[r + 1][c] = 6 if flip else 8
          continue
        if i % 2 == 0: c += 1
        else: r += 1
    if flip: grid, output = common.flip(grid), common.flip(output)
    return grid, output

  if width is None:
    while True:
      width, height = common.randint(6, 12), common.randint(6, 12)
      row = common.randint(2, 4)
      flip = common.randint(0, 1)
      r, c, lengths = row, 0, []
      while r + 1 < height and c + 1 < width:
        length = common.randint(3, 5)
        if len(lengths) % 2 == 0:
          if c + length - 1 >= width: length = width - c
          c += length - 1
        else:
          if r + length - 1 >= height: length = height - r
          r += length - 1
        lengths.append(length)
      if 0 in lengths: continue  # These don't occur in the test cases.
      if 1 in lengths: continue  # These don't occur in the test cases.
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=6, height=6, row=3, lengths=[4, 3], flip=True),
      generate(width=6, height=8, row=3, lengths=[4, 3, 3], flip=False),
      generate(width=8, height=8, row=2, lengths=[4, 3, 4, 4], flip=False),
      generate(width=8, height=9, row=4, lengths=[3, 4, 4, 2], flip=True),
      generate(width=6, height=6, row=2, lengths=[3, 4], flip=False),
  ]
  test = [
      generate(width=12, height=10, row=2, lengths=[3, 4, 5, 3, 4, 2, 3], flip=True),
  ]
  return {"train": train, "test": test}
