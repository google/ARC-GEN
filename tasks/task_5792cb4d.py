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


def generate(row=None, col=None, angles=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    thicks: The thicknesses of the boxes.
  """

  if row is None:
    while True:
      grid = common.grid(10, 10, 0)
      row, col = common.randint(1, 8), common.randint(1, 8)
      r, c, angles, colors = row, col, [], []
      while True:
        colors.append(common.choice([1, 2, 4, 5, 6, 7, 9]))
        grid[r][c] = 1
        candidates = []
        if r > 1 and grid[r - 1][c - 1] + grid[r - 1][c + 1] + grid[r - 2][c - 1] + grid[r - 2][c] + grid[r - 2][c + 1] == 0:
          candidates.append(0)
        if c < 8 and grid[r - 1][c + 1] + grid[r + 1][c + 1] + grid[r - 1][c + 2] + grid[r][c + 2] + grid[r + 1][c + 2] == 0:
          candidates.append(1)
        if r < 8 and grid[r + 1][c - 1] + grid[r + 1][c + 1] + grid[r + 2][c - 1] + grid[r + 2][c] + grid[r + 2][c + 1] == 0:
          candidates.append(2)
        if c > 1 and grid[r - 1][c - 1] + grid[r + 1][c - 1] + grid[r - 1][c - 2] + grid[r][c - 2] + grid[r + 1][c - 2] == 0:
          candidates.append(3)
        if not candidates: break
        if common.randint(0, 19) == 0: break
        angle = common.choice(candidates)
        angles.append(angle)
        if angle == 0: r -= 1
        if angle == 1: c += 1
        if angle == 2: r += 1
        if angle == 3: c -= 1
      if len(colors) > 6: break
    colors = "".join(map(str, colors))
    angles = "".join(map(str, angles))

  grid, output = common.grids(10, 10, 8)
  r, c = row, col
  for angle, color in zip(angles + "4", colors):
    grid[r][c] = int(color)
    if angle == "0": r -= 1
    if angle == "1": c += 1
    if angle == "2": r += 1
    if angle == "3": c -= 1
  r, c = row, col
  for angle, color in zip(angles + "4", colors[::-1]):
    output[r][c] = int(color)
    if angle == "0": r -= 1
    if angle == "1": c += 1
    if angle == "2": r += 1
    if angle == "3": c -= 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=4, col=2, angles="2111112", colors="47165612"),
      generate(row=1, col=2, angles="22121122211", colors="179647714421"),
  ]
  test = [
      generate(row=8, col=4, angles="330000011221100001122222223",
               colors="7117776661415555999222444111"),
  ]
  return {"train": train, "test": test}
