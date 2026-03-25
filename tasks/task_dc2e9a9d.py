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
             bcols=None, angles=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    angles: The angles of the boxes.
  """

  def draw():
    grid, output = common.grids(width, height)
    for wide, tall, brow, bcol, angle in zip(wides, talls, brows, bcols, angles):
      r, c, w, t, h = 0, 0, 0, 0, 0
      if angle == 0: r, c, w, t, h = brow + 1, bcol, wide, (tall - 3) // 2, 3
      if angle == 1: r, c, w, t, h = brow, bcol + 1 + wide // 2, (wide - 3) // 2, tall, 3
      if angle == 2: r, c, w, t, h = brow + 1 + tall // 2, bcol, wide, (tall - 3) // 2, 3
      if angle == 3: r, c, w, t, h = brow, bcol + 1, (wide - 3) // 2, tall, 3
      common.hollow_rect(grid, w, t, r, c, h)
      common.hollow_rect(output, w, t, r, c, h)
      if angle == 0: r, c = brow, bcol + wide // 2
      if angle == 1: r, c = brow + tall // 2, bcol + wide - 1
      if angle == 2: r, c = brow + tall - 1, bcol + wide // 2
      if angle == 3: r, c = brow + tall // 2, bcol
      # We don't allow the green dot to lie out-of-bounds.
      if r < 0 or c < 0 or r >= height or c >= width: return None, None
      common.draw(grid, r, c, h)
      common.draw(output, r, c, h)
      if angle == 0: r, c, w, t, h = brow + 1 + tall // 2, bcol, wide, (tall - 3) // 2, 8
      if angle == 1: r, c, w, t, h = brow, bcol + 1, (wide - 3) // 2, tall, 1
      if angle == 2: r, c, w, t, h = brow + 1, bcol, wide, (tall - 3) // 2, 8
      if angle == 3: r, c, w, t, h = brow, bcol + 1 + wide // 2, (wide - 3) // 2, tall, 1
      common.hollow_rect(output, w, t, r, c, h)
      if angle == 0: r, c = brow + tall - 1, bcol + wide // 2
      if angle == 1: r, c = brow + tall // 2, bcol
      if angle == 2: r, c = brow, bcol + wide // 2
      if angle == 3: r, c = brow + tall // 2, bcol + wide - 1
      common.draw(output, r, c, h)
    return grid, output

  if width is None:
    width, height = common.randint(15, 30), common.randint(15, 30)
    num_boxes = min(4, (width * height) // 100 - 1)
    angles = [common.randint(0, 3) for _ in range(num_boxes)]
    while True:
      wides = [(2 * common.randint(1, 2) + 1) if angle in [0, 2] else (2 * common.randint(4, 7) + 1) for angle in angles]
      talls = [(2 * common.randint(4, 7) + 1) if angle in [0, 2] else (2 * common.randint(1, 2) + 1) for angle in angles]
      brows = [common.randint(-1 if angle in [0, 2] else 0, height - tall + (1 if angle in [0, 2] else 0)) for tall, angle in zip(talls, angles)]
      bcols = [common.randint(-1 if angle in [1, 3] else 0, width - wide + (1 if angle in [1, 3] else 0)) for wide, angle in zip(wides, angles)]
      if common.overlaps(brows, bcols, wides, talls, 1): continue
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=19, height=23, wides=[9, 5, 11], talls=[3, 11, 5],
               brows=[2, 3, 14], bcols=[11, 3, 4], angles=[3, 0, 1]),
      generate(width=17, height=22, wides=[13, 3], talls=[5, 9], brows=[3, 9],
               bcols=[3, 8], angles=[3, 2]),
      generate(width=21, height=22, wides=[3, 9, 5], talls=[11, 5, 11],
               brows=[0, 5, 11], bcols=[14, 1, 8], angles=[0, 3, 2]),
  ]
  test = [
      generate(width=29, height=28, wides=[3, 15, 11, 5], talls=[9, 5, 5, 11],
               brows=[0, 4, 11, 16], bcols=[22, 2, 12, 5], angles=[0, 3, 1, 2]),
  ]
  return {"train": train, "test": test}
