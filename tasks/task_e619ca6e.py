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


def generate(width=None, height=None, wides=None, talls=None, brows=None,
             bcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if width is None:
    width, height = common.randint(20, 30), common.randint(20, 30)
    num_boxes = common.randint(1, 3)
    cdirs = [common.randint(0, 1) for _ in range(num_boxes)]
    wides = [2 if cdir else common.randint(3, 5) for cdir in cdirs]
    talls = [common.randint(3, 5) if cdir else 2 for cdir in cdirs]
    if not common.randint(0, 9): wides[0] = talls[0] = 3
    while True:
      brows = [common.randint(3, height // 2) for _ in range(num_boxes)]
      bcols = [common.randint(3, width - wide - 3) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, 5): break

  grid, output = common.grids(width, height)
  for wide, tall, brow, bcol in zip(wides, talls, brows, bcols):
    common.rect(grid, wide, tall, brow, bcol, 3)
    delta = 0
    for row in range(brow, height, tall):
      common.rect(output, wide, tall, row, bcol - delta, 3)
      common.rect(output, wide, tall, row, bcol + delta, 3)
      delta += wide
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=22, height=25, wides=[5], talls=[2], brows=[9], bcols=[6]),
      generate(width=29, height=29, wides=[3, 3, 2], talls=[2, 3, 4],
               brows=[3, 6, 13], bcols=[4, 21, 10]),
      generate(width=27, height=29, wides=[3, 2], talls=[2, 4], brows=[5, 13],
               bcols=[8, 16]),
  ]
  test = [
      generate(width=28, height=29, wides=[2, 4], talls=[4, 2], brows=[8, 19],
               bcols=[6, 15]),
  ]
  return {"train": train, "test": test}
