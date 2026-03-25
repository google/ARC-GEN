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


def generate(length=None, colors=None, hflip=None, vflip=None, size=19):
  """Returns input and output grids according to the given parameters.

  Args:
    length: the length of the input colors square
    colors: a list of digits representing the colors to be used
    hflip: whether to flip the input horizontally
    vflip: whether to flip the input vertically
    size: the width and height of the (square) grid
  """
  if length is None:
    length = common.randint(2, 4)
    bitmap = common.grid(length, length)
    color_list, idx = common.shuffle(range(1, 10)), 0
    # Usually choose diagonals, and (sometimes) add a nextdoor color.
    for i in range(length):
      if i + 1 == length and common.randint(0, 1): continue  # Maybe skip last.
      bitmap[i][i] = color_list[idx]
      idx += 1
      if i + 1 == length: continue  # No room to add a nextdoor color.
      if i and bitmap[i][i - 1]:
        continue  # Avoid three colors in a row.
      if common.randint(0, 1): continue  # Sometimes don't add a nextdoor color.
      bitmap[i][i + 1] = bitmap[i + 1][i] = color_list[idx]
      idx += 1
    colors = []
    for row in bitmap:
      colors.extend(row)
    hflip, vflip = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(size, size)
  for r in range(length):
    for c in range(length):
      if not colors[r * length + c]: continue
      # Draw the mirrored pixels
      grid[2 * r + 1][2 * c + 1] = colors[r * length + c]
      output[2 * r + 1][2 * c + 1] = colors[r * length + c]
      output[2 * r + 1][size - 2 * c - 2] = colors[r * length + c]
      output[size - 2 * r - 2][2 * c + 1] = colors[r * length + c]
      output[size - 2 * r - 2][size - 2 * c - 2] = colors[r * length + c]
      # If we see pixels to our right and below, we should draw a dotted square.
      if r != c or r + 1 == length: continue
      if not colors[r * length + c + 1]: continue
      for i in range(2 * r + 3, size - 2 * r - 2, 2):
        output[i][2 * c + 1] = colors[r * length + c + 1]
        output[i][size - 2 * c - 2] = colors[r * length + c + 1]
      for i in range(2 * c + 3, size - 2 * c - 2, 2):
        output[2 * r + 1][i] = colors[r * length + c + 1]
        output[size - 2 * r - 2][i] = colors[r * length + c + 1]
  if hflip:
    grid, output = common.flip_horiz(grid), common.flip_horiz(output)
  if vflip:
    grid, output = grid[::-1], output[::-1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(length=2, colors=[8, 1, 1, 2], hflip=0, vflip=0),
      generate(length=3, colors=[3, 0, 0, 0, 4, 1, 0, 1, 0], hflip=1, vflip=0),
      generate(length=3, colors=[4, 3, 0, 3, 1, 0, 0, 0, 8], hflip=0, vflip=0),
  ]
  test = [
      generate(length=4,
               colors=[1, 3, 0, 0, 3, 2, 0, 0, 0, 0, 4, 8, 0, 0, 8, 0], hflip=0,
               vflip=1),
  ]
  return {"train": train, "test": test}
