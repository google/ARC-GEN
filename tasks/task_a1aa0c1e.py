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


def generate(colors=None, rows=None, cols=None, lengths=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: The colors to use for the levels.
    rows: The rows of the levels.
    cols: The columns of the ladders (last one is the grey pixel).
    lengths: The lengths of the ladders.
  """

  if colors is None:
    colors = common.random_colors(3, exclude=[5, 9]) + [9]
    row = common.randint(1, 2)
    while True:
      gaps = [common.randint(4, 8) for _ in range(3)]
      if row + sum(gaps) in [19, 20]: break
    rows = [row]
    rows.append(rows[-1] + gaps[0])
    rows.append(rows[-1] + gaps[1])
    rows.append(rows[-1] + gaps[2])
    while True:
      cols = [common.randint(1, 19) for _ in range(4)]
      if abs(cols[3] - cols[2]) > 2: break
    while True:
      lengths = [gap - 1 for gap in gaps]  # Assume full ladders.
      for i in range(2):  # The first two ladders *could* be shorter or gone.
        outcome = common.randint(0, 3)
        if outcome == 0:
          lengths[i] = 0
        elif outcome == 1:
          lengths[i] = common.randint(1, gaps[i] - 2)
      if len(set(lengths)) in [1, 3]: break

  grid, output = common.grid(21, 21), common.grid(5, 3)
  for i, (color, row, col) in enumerate(zip(colors, rows, cols)):
    # Draw the floor.
    for c in range(21):
      grid[row][c] = color
    # Draw the ladder.
    if i < 3:
      length = lengths[i]
      for r in range(length):
        for dc in [-1, 0, 1]:
          if r % 2 or dc: grid[row + 1 + r][col + dc] = color
    else:
      grid[row - 1][col] = 5
  sorted_lengths = sorted(lengths)
  for r, color in enumerate(colors):
    if r == 3: break
    output[r][3] = 9
    if not lengths[r]: continue
    if lengths[r] == sorted_lengths[1]:
      output[r][0] = output[r][1] = color
    elif lengths[r] == sorted_lengths[0]:
      output[r][0] = color
    else:
      output[r][0] = output[r][1] = output[r][2] = color
  if rows[1] + lengths[1] + 1 != rows[2]:
    output[2][4] = 5
  elif rows[0] + lengths[0] + 1 != rows[1]:
    output[1][4] = 5
  else:
    output[0][4] = 5
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[4, 8, 3, 9], rows=[1, 5, 11, 19], cols=[1, 13, 4, 13],
               lengths=[0, 5, 7]),
      generate(colors=[4, 7, 1, 9], rows=[2, 6, 12, 20], cols=[10, 10, 10, 16],
               lengths=[3, 5, 7]),
      generate(colors=[8, 6, 4, 9], rows=[1, 7, 14, 20], cols=[11, 4, 16, 10],
               lengths=[5, 5, 5]),
  ]
  test = [
      generate(colors=[3, 4, 2, 9], rows=[1, 8, 12, 20], cols=[12, 3, 8, 5],
               lengths=[5, 3, 7]),
  ]
  return {"train": train, "test": test}
