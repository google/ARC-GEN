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


def generate(jcol=None, brow=None, bcol=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    jcol: The column of the J.
    colors: A list of colors to use.
  """

  def draw():
    # Certain parts of the shape need to be colored in.
    if colors[2] + colors[3] == 0: return None, None
    if colors[4] + colors[5] == 0: return None, None
    if colors[0] + colors[2] + colors[4] == 0: return None, None
    if colors[1] + colors[3] + colors[5] == 0: return None, None
    # The shape and the J can't overlap.
    if bcol >= jcol - 4 and bcol <= jcol + 1: return None, None
    grid, output = common.grids(11, 11, 7)
    # Draw the pink J.
    output[0][jcol] = grid[6][jcol] = 6
    output[1][jcol] = grid[7][jcol] = 6
    output[2][jcol] = grid[8][jcol] = 6
    output[3][jcol - 1] = grid[9][jcol - 1] = 6
    output[2][jcol - 2] = grid[8][jcol - 2] = 6
    # Draw the shape.
    for i, color in enumerate(colors):
      if not color: continue
      grid[brow + i // 2][bcol + i % 2] = color
      output[i // 2][jcol - 3 + i % 2] = color
    # Draw the yellow line.
    for c in range(11):
      if grid[5][c] != 7: return None, None
      output[5][c] = grid[5][c] = 4
    return grid, output

  if jcol is None:
    hue = common.random_color(exclude=[4, 6, 7])
    # Choose the shape colors.
    while True:
      colors = [hue * common.randint(0, 1) for _ in range(6)]
      jcol = common.randint(3, 10)
      brow = common.randint(5, 8)
      bcol = common.randint(0, 9)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(jcol=10, brow=5, bcol=4, colors=[0, 0, 2, 0, 2, 2]),
      generate(jcol=8, brow=7, bcol=1, colors=[0, 0, 8, 8, 8, 8]),
      generate(jcol=5, brow=5, bcol=8, colors=[0, 0, 0, 1, 1, 0]),
  ]
  test = [
      generate(jcol=8, brow=7, bcol=2, colors=[0, 8, 8, 0, 0, 8]),
  ]
  return {"train": train, "test": test}
