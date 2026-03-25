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


def generate(rows=None, cols=None, lengths=None, angles=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  def draw():
    # Not a huge deal, but lengths should be unique.
    if len(set(lengths)) != len(lengths): return None, None
    # We should see lines of both angles.
    if len(set(angles)) < 2: return None, None
    # The number of lines of each angle should be about the same.
    if abs(sum(angles)) > 1: return None, None
    # Most importantly, the sum of pixels for either angle should differ!
    pos = sum([length for length, angle in zip(lengths, angles) if angle == 1])
    neg = sum([length for length, angle in zip(lengths, angles) if angle == -1])
    if pos == neg: return None, None
    grid, output = common.grids(16, 16, 7)
    for row, col, length, angle in zip(rows, cols, lengths, angles):
      for i in range(length):
        if grid[row + i][col + i * angle] != 7: return None, None
        grid[row + i][col + i * angle] = 5
        output[row + i][col + i * angle] = 8 if (pos < neg) == (angle < 0) else 2
    # Check that there is nothing adjacent to any line.
    for row, col, length, angle in zip(rows, cols, lengths, angles):
      if common.get_pixel(grid, row - 1, col - angle) not in [-1, 7]: return None, None
      if common.get_pixel(grid, row + length, col + angle * length) not in [-1, 7]: return None, None
      for i in range(length):
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0),
                       (0, 2), (0, -2), (2, 0), (-2, 0)]:
          if common.get_pixel(grid, row + i + dr, col + i * angle + dc) not in [-1, 7]:
            return None, None
    return grid, output

  if rows is None:
    num_lines = common.randint(2, 7)
    while True:
      lengths = [common.randint(2, 10) for _ in range(num_lines)]
      angles = [2 * common.randint(0, 1) - 1 for _ in range(num_lines)]
      rows = [common.randint(0, 16 - length) for length in lengths]
      cols = [common.randint(0 if angle == 1 else (16 - length),
                             (16 - length) if angle == 1 else 15) for length, angle in zip(lengths, angles)]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 7], cols=[4, 10, 8], lengths=[10, 6, 9],
               angles=[1, 1, -1]),
      generate(rows=[2, 2, 3, 5, 10, 11], cols=[7, 15, 3, 2, 14, 5], lengths=[2, 7, 4, 8, 5, 3], angles=[1, -1, 1, 1, -1, -1]),
  ]
  test = [
      generate(rows=[5, 7], cols=[10, 7], lengths=[2, 3], angles=[-1, 1]),
  ]
  return {"train": train, "test": test}
