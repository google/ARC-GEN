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


def generate(width=None, height=None, cols=None, lengths=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    cols: The columns of the lines.
    lengths: The lengths of the lines.
    color: The color of the lines.
  """

  def draw():
    if lengths[0] == lengths[1]: return None, None
    grid, output = common.grids(width, height)
    # Draw the top colors.
    for c in range(cols[0], cols[0] + lengths[0]):
      output[0][c] = grid[0][c] = color
    # Draw the bottom colors.
    for c in range(cols[1], cols[1] + lengths[1]):
      output[height - 1][c] = grid[height - 1][c] = color
    # Draw the yellow colors.
    yellows = 0
    for c in range(width):
      if output[0][c] == 0 or output[height - 1][c] == 0: continue
      yellows += 1
      lb = 1 if lengths[0] > lengths[1] else height // 2
      ub = height // 2 if lengths[0] > lengths[1] else height - 1
      for r in range(lb, ub):
        output[r][c] = 4
    if yellows == 0: return None, None
    # Draw the red middle.
    for c in range(width):
      output[height // 2][c] = grid[height // 2][c] = 2
    return grid, output

  if width is None:
    width, height = common.randint(4, 6), 2 * common.randint(4, 6) + 1
    color = common.random_color(exclude=[2, 4])
    while True:
      lengths = [common.randint(2, width) for _ in range(2)]
      cols = [common.randint(0, width - length) for length in lengths]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=5, height=13, cols=[1, 0], lengths=[2, 4], color=1),
      generate(width=5, height=13, cols=[1, 2], lengths=[4, 3], color=6),
      generate(width=6, height=13, cols=[3, 1], lengths=[2, 5], color=3),
      generate(width=4, height=9, cols=[1, 0], lengths=[3, 2], color=3),
  ]
  test = [
      generate(width=5, height=11, cols=[0, 1], lengths=[5, 2], color=7),
  ]
  return {"train": train, "test": test}
