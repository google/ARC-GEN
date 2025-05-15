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


def generate(thicks=None, gaps=None, cols=None, lengths=None, colors=None,
             gravity=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    thicks: a list of two thickness values
    gaps: a list of two gap values
    cols: a list of two column values
    lengths: a list of two length values
    colors: a list of two color values
    gravity: which direction is gravity applied
    size: the size of the grid
  """
  if thicks is None:
    thicks = [common.randint(2, 4) for _ in range(2)]
    gaps = [common.randint(0, 1 if t < 4 else 0) for t in thicks]
    lengths = [common.randint(4, 6)]
    lengths.append(common.randint(lengths[0] + 2, 9))
    col1 = common.randint(0, size - lengths[1] - 1)
    col0 = common.randint(col1 + 1, col1 + lengths[1] - lengths[0])
    cols = [col0, col1]
    cols.append(common.randint(0, cols[0] - 1))
    colors = common.random_colors(2, exclude=[common.cyan()])
    gravity = common.randint(0, 3)

  grid, output = common.grids(size, size)
  # Draw the short block.
  for r in range(gaps[0], gaps[0] + thicks[0]):
    for c in range(cols[0], cols[0] + lengths[0]):
      output[r][c] = grid[r][c] = colors[0]
  # Draw the long block.
  for r in range(gaps[0] + thicks[0], size - gaps[1] - thicks[1]):
    for c in range(cols[0] + 1, cols[0] + lengths[0] - 1):
      output[r][c] = common.cyan()
  # Draw the bridge.
  for r in range(size - gaps[1] - thicks[1], size - gaps[1]):
    for c in range(cols[1], cols[1] + lengths[1]):
      output[r][c] = grid[r][c] = colors[1]
  grid = common.apply_gravity(grid, gravity)
  output = common.apply_gravity(output, gravity)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(thicks=[3, 3], gaps=[1, 0], cols=[1, 0], lengths=[4, 6],
               colors=[2, 7], gravity=0),
      generate(thicks=[3, 3], gaps=[0, 1], cols=[3, 1], lengths=[5, 8],
               colors=[6, 4], gravity=3),
      generate(thicks=[2, 3], gaps=[0, 0], cols=[3, 0], lengths=[6, 9],
               colors=[9, 3], gravity=2),
  ]
  test = [
      generate(thicks=[3, 4], gaps=[0, 0], cols=[1, 0], lengths=[6, 8],
               colors=[2, 1], gravity=3),
  ]
  return {"train": train, "test": test}
