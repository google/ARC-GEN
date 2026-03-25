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


def generate(lengths=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    lengths: The lengths of the lines.
    colors: The colors of the lines.
  """

  if lengths is None:
    lines = common.randint(3, 5)
    lengths = [common.randint(1, 2 * lines) for _ in range(lines)]
    colors = common.sample([0, 1, 2, 3, 4, 5, 6, 8, 9], lines)

  lines = len(lengths)
  size = 2 * lines + 1
  grid, output = common.grids(size, size, 7)
  for c, length in enumerate(lengths):
    for r in range(length):
      grid[size - r - 1][2 * c + 1] = colors[c]
      col = 2 * ((c + lines - 1) % lines) + 1
      color = colors[(c + lines - 2) % lines]
      output[size - r - 1][col] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(lengths=[2, 3, 8, 3], colors=[9, 8, 6, 1]),
      generate(lengths=[6, 3, 4], colors=[2, 8, 5]),
      generate(lengths=[4, 5, 3, 8, 6], colors=[1, 2, 5, 4, 8]),
  ]
  test = [
      generate(lengths=[10, 1, 4, 4, 5], colors=[0, 2, 8, 9, 6]),
  ]
  return {"train": train, "test": test}
