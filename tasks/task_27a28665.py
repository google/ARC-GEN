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


def generate(idx=None, color=None, size=3, oneof=(1, 2, 3, 6)):
  """Returns input and output grids according to the given parameters.

  Args:
    idx: an index into one of many pattern types
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
    oneof: a list of possible pattern indices (of which one will be chosen)
  """
  if idx is None:
    idx, color = oneof[common.randint(0, len(oneof) - 1)], common.random_color()

  grid, output = common.grid(size, size), common.grid(1, 1)
  if idx == 1:
    grid[0][0] = grid[0][1] = grid[1][0] = grid[1][2] = grid[2][1] = color
  if idx == 2:
    grid[0][0] = grid[0][2] = grid[1][1] = grid[2][0] = grid[2][2] = color
  if idx == 3:
    grid[0][1] = grid[0][2] = grid[1][1] = grid[1][2] = grid[2][0] = color
  if idx == 6:
    grid[0][1] = grid[1][0] = grid[1][1] = grid[1][2] = grid[2][1] = color
  output[0][0] = idx
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(idx=1, color=5),
      generate(idx=2, color=8),
      generate(idx=2, color=5),
      generate(idx=3, color=1),
      generate(idx=3, color=8),
      generate(idx=1, color=4),
      generate(idx=6, color=5),
  ]
  test = [
      generate(idx=6, color=8),
      generate(idx=1, color=7),
      generate(idx=2, color=2),
  ]
  return {"train": train, "test": test}
