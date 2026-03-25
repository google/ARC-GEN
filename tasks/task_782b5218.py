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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if colors is None:
    bgcolor, length = common.random_color(exclude=[2]), common.randint(1, 4)
    while True:
      # Set the random background.
      colors = common.grid(10, 10)
      for r in range(10):
        for c in range(10):
          colors[r][c] = bgcolor * common.randint(0, 1)
      # Choose the pattern.
      pattern = [(0, 0)]
      for _ in range(length - 1):
        if common.randint(0, 1):
          diff = 2 * common.randint(0, 1) - 1
          pattern.append((pattern[-1][0] + diff, pattern[-1][1]))
        diff = common.randint(-1, 1)
        pattern.append((pattern[-1][0] + diff, pattern[-1][1] + 1))
      # Draw the pattern.
      row, drift = common.randint(2, 7), 0
      if row == 2: drift = 1
      if row == 7: drift = -1
      last_row, good = None, True
      for col in range(0, 10, length):
        for r, c in pattern:
          if last_row is not None and abs(row + r - last_row) > 1:
            good = False  # Don't leave an open gap between pixels.
          if row + r < 0: good = False  # Don't go beyond the top
          common.draw(colors, row + r, col + c, 2)
          last_row = row + r
        row += drift
      if good: break
    colors = common.flatten(colors)

  grid, output = common.grids(10, 10)
  for i, color in enumerate(colors):
    grid[i // 10][i % 10] = color
    if color == 2: output[i // 10][i % 10] = color
  hues = set(colors)
  hues.remove(0)
  hues.remove(2)
  for col in range(10):
    row = 0
    while row < 10 and output[row][col] == 0: row += 1
    while row < 10 and output[row][col] == 2: row += 1
    while row < 10:
      output[row][col] = list(hues)[0]
      row += 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 0, 1, 1, 1, 1, 1, 1, 1, 0,
                       0, 0, 1, 0, 1, 1, 0, 1, 0, 1,
                       1, 1, 0, 0, 1, 1, 1, 1, 1, 0,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       0, 0, 1, 1, 0, 0, 0, 0, 0, 0,
                       1, 1, 0, 1, 0, 0, 0, 0, 1, 0,
                       0, 1, 1, 1, 0, 1, 1, 0, 1, 0,
                       1, 1, 0, 0, 0, 1, 0, 0, 1, 0,
                       0, 0, 1, 0, 0, 0, 1, 1, 0, 0,
                       0, 1, 1, 1, 0, 1, 1, 0, 0, 1]),
      generate(colors=[5, 5, 5, 0, 5, 0, 0, 0, 5, 5,
                       5, 0, 0, 5, 5, 0, 5, 0, 5, 5,
                       0, 5, 5, 0, 5, 5, 0, 5, 0, 0,
                       2, 0, 5, 5, 2, 0, 5, 0, 2, 5,
                       5, 2, 0, 2, 0, 2, 0, 2, 0, 2,
                       0, 0, 2, 5, 5, 5, 2, 0, 5, 0,
                       5, 5, 0, 0, 0, 5, 5, 5, 5, 5,
                       0, 5, 0, 5, 5, 0, 5, 0, 5, 5,
                       0, 5, 5, 0, 5, 0, 5, 0, 5, 5,
                       5, 5, 0, 0, 5, 5, 5, 5, 5, 5]),
      generate(colors=[0, 8, 8, 0, 8, 0, 8, 8, 0, 0,
                       2, 0, 8, 8, 0, 8, 0, 0, 0, 8,
                       2, 2, 8, 0, 0, 0, 0, 0, 0, 0,
                       0, 2, 2, 0, 8, 0, 0, 0, 0, 0,
                       8, 8, 2, 2, 0, 0, 0, 8, 8, 0,
                       8, 8, 8, 2, 2, 8, 0, 0, 0, 0,
                       0, 0, 0, 0, 2, 2, 8, 8, 8, 0,
                       8, 0, 8, 0, 0, 2, 2, 8, 8, 8,
                       8, 8, 0, 0, 0, 0, 2, 2, 8, 0,
                       0, 8, 0, 8, 0, 8, 8, 2, 2, 8]),
  ]
  test = [
      generate(colors=[9, 9, 9, 0, 0, 0, 0, 0, 0, 0,
                       9, 9, 9, 0, 9, 0, 0, 9, 0, 0,
                       9, 0, 0, 0, 9, 0, 9, 0, 0, 0,
                       0, 0, 9, 9, 9, 0, 9, 0, 0, 0,
                       0, 2, 2, 2, 0, 2, 2, 2, 9, 2,
                       2, 2, 0, 2, 2, 2, 9, 2, 2, 2,
                       9, 0, 0, 9, 9, 9, 0, 9, 9, 0,
                       0, 0, 0, 0, 9, 0, 9, 0, 0, 9,
                       0, 9, 9, 0, 0, 0, 0, 9, 9, 0,
                       9, 0, 9, 0, 0, 9, 0, 9, 0, 0]),
  ]
  return {"train": train, "test": test}
