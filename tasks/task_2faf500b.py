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


def generate(size=None, wides=None, talls=None, brows=None, bcols=None,
             angles=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    angles: The angles of the boxes.
  """

  if size is None:
    size = common.randint(6, 20)
    num_boxes = size // 4
    angles = [common.randint(0, 3) for _ in range(num_boxes)]
    while True:
      wides, talls = [], []
      for angle in angles:
        if angle in [0, 2]:
          wides.append(common.randint(2, 6))
          talls.append(2 * common.randint(3, size // 2))
        else:
          wides.append(2 * common.randint(3, size // 2))
          talls.append(common.randint(2, 6))
      brows = [common.randint(0, size - t) for t in talls]
      bcols = [common.randint(0, size - w) for w in wides]
      if not common.overlaps(brows, bcols, wides, talls, 1): break

  grid, output = common.grids(size, size)
  for wide, tall, brow, bcol, angle in zip(wides, talls, brows, bcols, angles):
    w = wide if angle in [0, 2] else (wide - 2)
    t = tall if angle in [1, 3] else (tall - 2)
    r = brow if angle in [1, 3] else (brow + 1)
    c = bcol if angle in [0, 2] else (bcol + 1)
    common.rect(grid, w, t, r, c, 9)
    common.rect(output, wide, tall, brow, bcol, 9)
    if angle in [0, 2]:
      common.rect(output, wide, 2, brow + tall // 2 - 1, bcol, 0)
      for c in range(wide):
        offset = 1 if c % 2 == angle // 2 else -2
        output[brow + tall // 2 + offset][bcol + c] = 0
        offset = 0 if c % 2 == angle // 2 else -1
        grid[brow + tall // 2 + offset][bcol + c] = 6
    if angle in [1, 3]:
      common.rect(output, 2, tall, brow, bcol + wide // 2 - 1, 0)
      for r in range(tall):
        offset = -2 if r % 2 == angle // 2 else 1
        output[brow + r][bcol + wide // 2 + offset] = 0
        offset = -1 if r % 2 == angle // 2 else 0
        grid[brow + r][bcol + wide // 2 + offset] = 6
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=12, wides=[8, 2, 8], talls=[3, 6, 3], brows=[2, 6, 7],
               bcols=[3, 9, 0], angles=[1, 0, 3]),
      generate(size=8, wides=[3], talls=[8], brows=[0], bcols=[1], angles=[2]),
      generate(size=16, wides=[4, 6, 2, 10], talls=[10, 2, 6, 4],
               brows=[1, 2, 3, 11], bcols=[12, 5, 2, 1], angles=[0, 3, 2, 3]),
  ]
  test = [
      generate(size=19, wides=[6, 8, 5, 6, 2, 2, 6],
               talls=[2, 3, 12, 14, 6, 6, 2], brows=[0, 1, 4, 5, 6, 13, 17],
               bcols=[2, 9, 2, 8, 17, 17, 1], angles=[1, 1, 0, 2, 0, 2, 3]),
  ]
  return {"train": train, "test": test}
