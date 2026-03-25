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


def generate(size=None, width=None, row=None, col=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    width: The width of the box.
    row: The row of the box.
    col: The column of the box.
  """

  if size is None:
    size = common.randint(5, 30)
    width = common.randint(5, size)
    if width == 13: width = 12  # To prevent the ambiguity.
    row = common.randint(0, size - width)
    col = common.randint(0, size - width)

  grid, output = common.grids(size, size)
  i, colors = 0, [5, 2, 5, 0]
  common.hollow_rect(grid, width, width, row, col, colors[i])
  while width > 0:
    if width == 1 and size == 13: break
    common.hollow_rect(output, width, width, row, col, colors[i])
    i, width, row, col = (i + 1) % len(colors), width - 2, row + 1, col + 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=16, width=12, row=1, col=3),
      generate(size=6, width=6, row=0, col=0),
      generate(size=19, width=17, row=1, col=1),
      generate(size=13, width=9, row=1, col=1),
  ]
  test = [
      generate(size=30, width=25, row=1, col=1),
  ]
  return {"train": train, "test": test}
