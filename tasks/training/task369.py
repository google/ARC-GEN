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


def generate(colors=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if colors is None:
    bitmap = common.grid(size, size, common.gray())
    for r in range(size):
      for c in range(size):
        if not common.randint(0, 5): continue
        num_pixels, pixels = common.randint(1, 4), []
        dr, dc = (0, 1) if common.randint(0, 1) else (1, 0)
        if num_pixels in [3, 2, 1]: pixels.append((r, c))
        if num_pixels in [3, 2]: pixels.append((r + dr, c + dc))
        if num_pixels in [3]: pixels.append((r + 2 * dr, c + 2 * dc))
        if num_pixels == 4:  # Not actually 4, but it's part of a square.
          pixels.append((r, c))
          pixels.append((r, c + 1))
          pixels.append((r + 1, c))
          pixels.append((r + 1, c + 1))
          del pixels[common.randint(0, 3)]
          num_pixels = 3
        overlaps = False
        for r, c in pixels:
          if r >= size or c >= size:
            overlaps = True
            continue
          if r > 0 and bitmap[r - 1][c] != common.gray(): overlaps = True
          if r + 1 < size and bitmap[r + 1][c] != common.gray(): overlaps = True
          if c > 0 and bitmap[r][c - 1] != common.gray(): overlaps = True
          if c + 1 < size and bitmap[r][c + 1] != common.gray(): overlaps = True
        if overlaps: continue
        for r, c in pixels:
          bitmap[r][c] = 4 - num_pixels
    colors = []
    for row in bitmap:
      colors.extend(row)

  grid, output = common.grids(size, size)
  for r in range(size):
    for c in range(size):
      color = colors[r * size + c]
      grid[r][c] = color if color == common.gray() else common.black()
      output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[5, 5, 5, 5, 3, 5, 5, 5, 3, 5, 1, 1, 5, 5, 5, 5, 5, 5, 5,
                       5, 1, 5, 5, 5, 5, 5, 1, 1, 5, 2, 5, 5, 3, 5, 5, 5, 5, 1,
                       5, 2, 5, 5, 5, 5, 2, 2, 5, 5, 5, 5, 2, 5, 3, 5, 5, 5, 5,
                       3, 5, 2, 2, 5, 5, 5, 2, 2, 5, 5, 5, 2, 5, 5, 5, 5, 5, 5,
                       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 3, 5, 5, 5, 5,
                       5, 5, 3, 5, 2]),
      generate(colors=[5, 5, 5, 5, 5, 2, 2, 5, 5, 5, 2, 2, 5, 3, 5, 5, 5, 5, 5,
                       3, 5, 5, 5, 5, 5, 2, 5, 2, 2, 5, 5, 3, 5, 5, 5, 2, 5, 5,
                       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 3, 5, 5, 5, 5, 5, 2, 5, 5,
                       5, 5, 5, 2, 2, 5, 5, 2, 5, 1, 1, 5, 3, 5, 5, 5, 5, 5, 5,
                       5, 1, 5, 5, 1, 5, 5, 5, 5, 5, 3, 5, 5, 3, 1, 1, 5, 5, 5,
                       5, 5, 5, 3, 5]),
      generate(colors=[2, 2, 5, 5, 3, 5, 5, 5, 1, 5, 5, 5, 1, 1, 5, 5, 5, 5, 1,
                       5, 5, 2, 5, 1, 5, 3, 5, 5, 1, 5, 5, 2, 5, 5, 1, 5, 5, 5,
                       5, 5, 5, 5, 5, 1, 1, 5, 5, 2, 5, 2, 5, 5, 2, 5, 5, 5, 5,
                       2, 5, 2, 5, 5, 2, 5, 5, 3, 5, 5, 5, 5, 5, 5, 5, 3, 5, 5,
                       5, 5, 5, 5, 5, 3, 5, 5, 5, 3, 5, 3, 5, 5, 5, 5, 3, 5, 5,
                       5, 5, 5, 5, 5]),
  ]
  test = [
      generate(colors=[3, 5, 5, 5, 5, 5, 1, 1, 5, 5, 5, 5, 5, 3, 5, 5, 1, 5, 2,
                       5, 5, 5, 1, 5, 5, 5, 5, 5, 2, 5, 5, 1, 1, 5, 5, 5, 5, 5,
                       5, 5, 2, 5, 5, 5, 5, 5, 2, 5, 5, 5, 2, 5, 5, 3, 5, 5, 2,
                       5, 1, 1, 5, 5, 2, 5, 5, 5, 5, 5, 1, 5, 5, 5, 2, 5, 5, 5,
                       5, 5, 5, 3, 2, 2, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 3,
                       5, 1, 1, 5, 3]),
  ]
  return {"train": train, "test": test}
