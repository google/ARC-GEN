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


def generate(wides=None, talls=None, bgcolor=None, fgcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    bgcolor: The color of the background.
    fgcolor: The color of the foreground.
  """

  if wides is None:
    num_boxes = common.randint(4, 6)
    talls = [common.randint(1, 6) for _ in range(num_boxes)]
    wides = [common.randint(1, min(5, 9 // tall)) for tall in talls]
    colors = common.random_colors(2)
    bgcolor, fgcolor = colors[0], colors[1]

  longests = [max(wide, tall) for wide, tall in zip(wides, talls)]
  in_width, in_height = sum(wides) + len(wides) - 1, max(talls)
  out_width, out_height = sum(longests) + len(longests) - 1, 10
  grid = common.grid(in_width, in_height, bgcolor)
  output = common.grid(out_width, out_height, bgcolor)
  # Draw the original boxes
  col = 0
  for wide, tall in zip(wides, talls):
    common.rect(grid, wide, tall, 0, col, fgcolor)
    col += wide + 1
  # Draw the short ones on top
  col = 0
  for wide, tall in zip(wides, talls):
    w, t = wide, tall
    if t > w: w, t = t, w
    common.rect(output, w, t, 0, col, fgcolor)
    col += w + 1
  # Draw the long ones on bottom
  col = 0
  for wide, tall in zip(wides, talls):
    w, t = wide, tall
    if t < w: w, t = t, w
    common.rect(output, w, t, out_height - t, col, fgcolor)
    col += w + 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[2, 1, 1, 2, 1, 1], talls=[1, 2, 1, 3, 1, 4],
               bgcolor=1, fgcolor=8),
      generate(wides=[3, 1, 2, 1, 3, 1], talls=[1, 3, 2, 4, 2, 5],
               bgcolor=3, fgcolor=7),
      generate(wides=[1, 2, 4, 1], talls=[6, 2, 1, 1],
               bgcolor=6, fgcolor=7),
  ]
  test = [
      generate(wides=[1, 1, 1, 3, 2, 1], talls=[1, 1, 1, 3, 1, 2],
               bgcolor=9, fgcolor=2),
  ]
  return {"train": train, "test": test}
