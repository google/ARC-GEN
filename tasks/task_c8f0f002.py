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


def generate(width=None, idxs=None, height=3, colors=(1, 7, 8)):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    idxs: the indices of the colors to use
    height: the height of the grid
    colors: the integers used for the colors
  """
  if width is None:
    width = common.randint(4, 6)
    idxs = [common.randint(0, 2) for _ in range(width * height)]

  grid, output = [], []
  for r in range(height):
    row = [colors[idx] for idx in idxs[r * width : (r + 1) * width]]
    grid.append(row[:])
    new_row = []
    for color in row:
      new_row.append(color if color != common.orange() else common.gray())
    output.append(new_row)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=6, idxs=[0, 2, 2, 1, 1, 2,
                              0, 0, 1, 1, 0, 2,
                              1, 0, 0, 1, 1, 2]),
      generate(width=4, idxs=[1, 1, 1, 0,
                              0, 2, 0, 1,
                              1, 0, 0, 1]),
      generate(width=5, idxs=[0, 2, 0, 1, 0,
                              1, 2, 2, 0, 0,
                              1, 0, 2, 2, 1]),
  ]
  test = [
      generate(width=5, idxs=[0, 1, 1, 0, 1,
                              2, 0, 1, 1, 1,
                              2, 1, 0, 1, 2]),
  ]
  return {"train": train, "test": test}
