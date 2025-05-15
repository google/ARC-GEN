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


def generate(colors=None, brows=None, bcols=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    brows: a list of vertical coordinates where the boxes should be placed
    bcols: a list of horizontal coordinates where the boxes should be placed
    size: the width and height of the (square) grid
  """
  if colors is None:
    num_boxes = common.randint(2, 3)
    while True:
      bcols = sorted([common.randint(0, size - 2) for _ in range(num_boxes)])
      wides = [2] * num_boxes
      if not common.overlaps_1d(bcols, wides): break
    while True:
      colors, brows = [], []
      for _ in range(num_boxes):
        num_colors = common.randint(2, 4)
        color_list = common.random_colors(num_colors, exclude=[common.green()])
        brows.append(common.randint(0, size - 2 - num_colors))
        colors.extend([common.choice(color_list) for _ in range(4)])
      touching = False
      for i in range(num_boxes - 1):
        if abs(brows[i] - brows[i + 1]) < 2: touching = True
      if touching: continue
      break

  grid, output = common.grids(size, size)
  for idx in range(len(colors) // 4):
    for r in range(2):
      for c in range(2):
        grid[brows[idx] + r][bcols[idx] + c] = colors[idx * 4 + r * 2 + c]
        output[brows[idx] + r][bcols[idx] + c] = colors[idx * 4 + r * 2 + c]
    shadow = len(set(colors[idx * 4 : (idx + 1) * 4]))
    for r in range(shadow):
      for c in range(2):
        output[brows[idx] + r + 2][bcols[idx] + c] = common.green()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[9, 9, 6, 6, 8, 4, 7, 7], brows=[2, 5], bcols=[1, 5]),
      generate(colors=[4, 8, 9, 4, 2, 1, 1, 2], brows=[1, 4], bcols=[2, 6]),
      generate(colors=[2, 4, 6, 7, 9, 8, 8, 9, 7, 6, 6, 6], brows=[1, 1, 5],
               bcols=[2, 6, 4]),
  ]
  test = [
      generate(colors=[1, 1, 2, 1, 2, 9, 1, 6, 4, 7, 8, 4], brows=[1, 1, 3],
               bcols=[0, 6, 3]),
  ]
  return {"train": train, "test": test}
