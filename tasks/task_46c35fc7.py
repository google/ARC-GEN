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


def generate(brows=None, bcols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    colors: The colors of the boxes.
  """

  if brows is None:
    boxes = common.randint(1, 2)
    colors = common.choices([0, 1, 2, 3, 4, 5, 6, 8, 9], boxes * 8)
    while True:
      brows = [common.randint(0, 4) for _ in range(boxes)]
      bcols = [common.randint(0, 4) for _ in range(boxes)]
      if common.overlaps(brows, bcols, [3] * boxes, [3] * boxes): continue
      if common.some_abutted(brows, bcols, [3] * boxes, [3] * boxes): continue
      break

  grid, output = common.grids(7, 7, 7)
  for i, (brow, bcol) in enumerate(zip(brows, bcols)):
    output[brow + 2][bcol + 0] = grid[brow + 0][bcol + 0] = colors[i * 8 + 0]
    output[brow + 1][bcol + 2] = grid[brow + 0][bcol + 1] = colors[i * 8 + 1]
    output[brow + 0][bcol + 0] = grid[brow + 0][bcol + 2] = colors[i * 8 + 2]
    output[brow + 0][bcol + 1] = grid[brow + 1][bcol + 0] = colors[i * 8 + 3]
    output[brow + 2][bcol + 1] = grid[brow + 1][bcol + 2] = colors[i * 8 + 4]
    output[brow + 2][bcol + 2] = grid[brow + 2][bcol + 0] = colors[i * 8 + 5]
    output[brow + 1][bcol + 0] = grid[brow + 2][bcol + 1] = colors[i * 8 + 6]
    output[brow + 0][bcol + 2] = grid[brow + 2][bcol + 2] = colors[i * 8 + 7]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(brows=[0, 4], bcols=[0, 3], colors=[9, 6, 5, 8, 1, 0, 8, 9, 1, 8, 4, 4, 6, 6, 2, 4]),
      generate(brows=[2], bcols=[2], colors=[5, 2, 8, 1, 9, 4, 3, 0]),
      generate(brows=[1, 4], bcols=[3, 0], colors=[6, 5, 5, 5, 6, 1, 5, 1, 8, 8, 8, 9, 9, 0, 0, 0]),
  ]
  test = [
      generate(brows=[1, 2], bcols=[0, 4], colors=[2, 6, 5, 1, 9, 4, 0, 9, 0, 1, 9, 6, 1, 5, 9, 2]),
  ]
  return {"train": train, "test": test}
