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


def generate(rows=None, cols=None, colormap=(1, 2, 3, 4, 6)):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of row counts
    cols: a list of column counts
    colormap: a list of colors used to fill the space
  """
  if rows is None:
    rows = [common.randint(1, 10) for _ in range(3)]
    cols = [common.randint(1, 10) for _ in range(3)]

  height = sum(rows) + len(rows) - 1
  width = sum(cols) + len(cols) - 1
  grid, output = common.grids(width, height)
  # Draw horizontal lines
  r = 0
  for row in rows:
    r += row
    if r >= height: break
    for c in range(width):
      output[r][c] = grid[r][c] = common.cyan()
    r += 1
  # Draw vertical lines
  c = 0
  for col in cols:
    c += col
    if c >= width: break
    for r in range(height):
      output[r][c] = grid[r][c] = common.cyan()
    c += 1
  # Draw colorful contents
  for r in range(0, rows[0]):
    for c in range(cols[0] + 1, cols[0] + cols[1] + 1):
      output[r][c] = colormap[1]  # red
  for r in range(rows[0] + 1, rows[0] + rows[1] + 1):
    for c in range(0, cols[0]):
      output[r][c] = colormap[3]  # yellow
  for r in range(rows[0] + 1, rows[0] + rows[1] + 1):
    for c in range(cols[0] + 1, cols[0] + cols[1] + 1):
      output[r][c] = colormap[4]  # magenta
  for r in range(rows[0] + 1, rows[0] + rows[1] + 1):
    for c in range(cols[0] + cols[1] + 2, width):
      output[r][c] = colormap[2]  # green
  for r in range(rows[0] + rows[1] + 2, height):
    for c in range(cols[0] + 1, cols[0] + cols[1] + 1):
      output[r][c] = colormap[0]  # blue
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 4, 10], cols=[4, 6, 7]),
      generate(rows=[4, 2, 4], cols=[2, 6, 4]),
  ]
  test = [
      generate(rows=[6, 6, 3], cols=[3, 4, 6]),
  ]
  return {"train": train, "test": test}
