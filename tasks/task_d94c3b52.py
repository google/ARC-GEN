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


def generate(lines=None, brow=None, bcol=None):
  """Returns input and output grids according to the given parameters.

  Args:
    lines: The lines of the characters.
    brow: The row of the special.
    bcol: The column of the special.
  """

  def get_colors():
    target = lines[brow][bcol]
    colors = [[1 for _ in range(6)] for _ in range(4)]
    # First, mark all target cells.
    for row in range(4):
      for col in range(6):
        if lines[row][col] == target: colors[row][col] = 8
    # Second, scan rows for "in betweens" (ie, the target on the left or right).
    for row in range(4):
      for col in range(1, 5):
        is_left = sum([1 if lines[row][c] == target else 0 for c in range(col)])
        is_right = sum([1 if lines[row][c] == target else 0 for c in range(col + 1, 6)])
        if is_left and is_right:
          if colors[row][col] == 8: return None
          colors[row][col] = 7
    # Third, scan columns for "in betweens" (ie, the target above or below).
    for row in range(1, 3):
      for col in range(6):
        is_left = sum([1 if lines[r][col] == target else 0 for r in range(row)])
        is_right = sum([1 if lines[r][col] == target else 0 for r in range(row + 1, 4)])
        if is_left and is_right:
          if colors[row][col] == 8: return None
          colors[row][col] = 7
    return colors

  def draw():
    grid, output = common.grids(25, 17)
    colors = get_colors()
    if colors is None: return None, None  # Probably a target between 2 others.
    if 7 not in common.flatten(colors): return None, None  # No inbetwens.
    for row, line in enumerate(lines):
      for col, letter in enumerate(line):
        for dr, dc in common.letter_map()[letter]:
          r, c = 4 * row + 1 + dr, 4 * col + 1 + dc
          grid[r][c] = 8 if (row == brow and col == bcol) else 1
          output[r][c] = colors[row][col]
    return grid, output

  if lines is None:
    letters = common.sample(sorted(list(common.letter_map().keys())), 6)
    while True:
      lines = []
      for _ in range(4):
        line = ""
        for _ in range(6):
          line += common.choice(letters)
        lines.append(line)
      brow, bcol = common.randint(0, 3), common.randint(0, 5)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(lines=["H+@+IO", "@H.@H@", "+..+.I", "I+IH@+"], brow=0, bcol=3),
      generate(lines=["X+OXO+", "+XXO+X", "HO+XHO", "XHH+OX"], brow=0, bcol=2),
      generate(lines=["4+U/N+", "UY4UY/", "/N+4N+", "4/U+4Y"], brow=2, bcol=1),
  ]
  test = [
      generate(lines=["O?I.+?", "2IOIIO", "I+?.+.", "+?O+2?"], brow=0, bcol=1),
  ]
  return {"train": train, "test": test}
