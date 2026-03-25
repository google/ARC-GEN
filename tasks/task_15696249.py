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

  def draw():
    grid, output = common.grid(3, 3), common.grid(9, 9)
    for i, color in enumerate(colors):
      grid[i // 3][i % 3] = color
    rows, cols = [], []
    for r in range(3):
      if len(set([grid[r][c] for c in range(3)])) == 1: rows.append(r)
    for c in range(3):
      if len(set([grid[r][c] for r in range(3)])) == 1: cols.append(c)
    if len(rows) > 1 or len(cols) > 1: return None, None
    if len(rows) == 0 and len(cols) == 0: return None, None
    for row in range(3):
      for col in range(3):
        if row not in rows and col not in cols: continue
        for r in range(3):
          for c in range(3):
            output[row * 3 + r][col * 3 + c] = colors[r * 3 + c]
    return grid, output

  if colors is None:
    hues = common.random_colors(3)
    while True:
      colors = common.shuffle([hues[0]] * 3 + [hues[1]] * 3 + [hues[2]] * 3)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 1, 1, 6, 2, 2, 2, 2, 6]),
      generate(colors=[2, 4, 3, 2, 3, 4, 2, 3, 4]),
      generate(colors=[3, 1, 6, 3, 6, 1, 3, 1, 6]),
      generate(colors=[4, 4, 6, 3, 3, 3, 6, 6, 4]),
  ]
  test = [
      generate(colors=[6, 6, 3, 4, 4, 3, 4, 4, 3]),
  ]
  return {"train": train, "test": test}
