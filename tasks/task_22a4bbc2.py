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


def generate(width=None, widths=None, heights=None, cols=None, start=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    widths: The widths of the rectangles.
    heights: The heights of the rectangles.
    cols: The columns of the rectangles.
    start: The start of the color rotation.
  """

  if width is None:
    width = common.randint(3, 5)
    rects = common.randint(8, 16)
    widths = [common.randint(2, width) for _ in range(rects)]
    heights = [common.choice([1] * 10 + [2] * 10 + [3]) for _ in range(rects)]
    cols = [common.randint(0, width - w) for w in widths]
    start = common.randint(0, 1)

  grid, output = common.grids(width, sum(heights))
  row, end = 0, start * 3
  for w, h, c in zip(widths, heights, cols):
    common.rect(grid, w, h, row, c, [1, 8][start])
    common.rect(output, w, h, row, c, [2, 8, 1, 2, 1, 8][end])
    row += h
    start = (start + 1) % 2
    end = (end + 1) % 6
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, widths=[3, 4, 2, 4, 2, 2, 4, 2, 4, 3, 3, 3, 2, 4],
               heights=[2, 1, 2, 2, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1],
               cols=[0, 0, 2, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0], start=0),
      generate(width=5, widths=[3, 3, 3, 5, 4, 4, 3, 4, 3, 2, 3, 2],
               heights=[2, 1, 2, 1, 2, 2, 1, 2, 1, 1, 2, 2],
               cols=[1, 0, 1, 0, 1, 0, 1, 1, 0, 3, 0, 2], start=1),
      generate(width=5, widths=[3, 4, 4, 2, 3, 4, 2, 5, 3, 3, 2],
               heights=[1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1],
               cols=[0, 1, 0, 1, 2, 0, 1, 0, 0, 1, 3], start=0),
      generate(width=3, widths=[2, 3, 2, 2, 3, 2, 3, 3],
               heights=[2, 2, 2, 1, 1, 2, 3, 2],
               cols=[0, 0, 1, 0, 0, 0, 0, 0], start=0),
  ]
  test = [
      generate(width=4, widths=[3, 3, 2, 4, 3, 3, 2, 4, 4, 2, 3, 3, 4, 2, 4, 3],
               heights=[1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2],
               cols=[0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1], start=1),
  ]
  return {"train": train, "test": test}
