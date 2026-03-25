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


def generate(width=None, height=None, bgcolor=None, wides=None, talls=None,
              halves=None, brows=None, bcols=None, tcolors=None, bcolors=None,
              a_s=None, b_s=None, c_s=None, d_s=None, e_s=None, f_s=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the boxes.
    height: The height of the boxes.
    bgcolor: The background color of the grids.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    halves: The heights of the top halves of the boxes.
    brows: The row indices of the tops of the boxes.
    bcols: The column indices of the left sides of the boxes.
    tcolors: The colors of the tops of the boxes.
    bcolors: The colors of the bottoms of the boxes.
    a_s: The left sides of the cutout rectangles.
    b_s: The right sides of the cutout rectangles.
    c_s: The left sides of the cutout rectangles.
    d_s: The right sides of the cutout rectangles.
    e_s: The heights of the cutout rectangles.
    f_s: The heights of the cutout rectangles.
  """

  if width is None:
    width, height = common.randint(12, 13), common.randint(12, 16)
    bgcolor, num_boxes = common.random_color(), common.randint(1, 2)
    while True:
      wides = [common.randint(3, 7) for _ in range(num_boxes)]
      talls = [common.randint(2, 9) for _ in range(num_boxes)]
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(1, width - wide - 1) for wide in wides]
      if not common.overlaps(brows, bcols, [w + 1 for w in wides], talls, 1): break
    halves = [common.randint(1, tall - 1) for tall in talls]
    tcolors = [common.random_color(exclude=[bgcolor]) for _ in range(num_boxes)]
    bcolors = [common.random_color(exclude=[bgcolor, tcolor]) for tcolor in tcolors]
    a_s = [common.randint(0, wide) for wide in wides]
    b_s = [common.randint(0, wide) for  wide in wides]
    c_s = [common.randint(0, wide) for wide in wides]
    d_s = [common.randint(0, wide) for  wide in wides]
    e_s = [common.randint(0, half - 1) for half in halves]
    f_s = [common.randint(0, tall - half - 1) for tall, half in zip(talls, halves)]

  grid, output = common.grids(width, height, bgcolor)
  for wide, tall, half, brow, bcol, tcolor, bcolor, a, b, c, d, e, f in zip(
      wides, talls, halves, brows, bcols, tcolors, bcolors, a_s, b_s, c_s, d_s, e_s, f_s
  ):
    for g, offset in zip([grid, output], [0, 1]):
      common.rect(g, wide, half, brow, bcol - offset, tcolor)
      common.rect(g, wide, tall - half, brow + half, bcol + offset, bcolor)
      if a < b: common.rect(g, b - a, e, brow, bcol + a - offset, bgcolor)
      if c < d: common.rect(g, d - c, f, brow + tall - f, bcol + c + offset, bgcolor)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=12, bgcolor=1, wides=[7], talls=[6], halves=[4],
               brows=[2], bcols=[2], tcolors=[4], bcolors=[2], a_s=[1], b_s=[4],
               c_s=[4], d_s=[6], e_s=[2], f_s=[1]),
      generate(width=12, height=16, bgcolor=8, wides=[7], talls=[9], halves=[4],
               brows=[1], bcols=[2], tcolors=[6], bcolors=[3], a_s=[4], b_s=[7],
               c_s=[3], d_s=[5], e_s=[2], f_s=[1]),
      generate(width=13, height=12, bgcolor=3, wides=[3, 4], talls=[2, 7],
               halves=[1, 5], brows=[2, 5], bcols=[7, 1], tcolors=[2, 8],
               bcolors=[7, 6], a_s=[3, 2], b_s=[0, 4], c_s=[3, 4], d_s=[0, 0],
               e_s=[0, 2], f_s=[0, 0]),
  ]
  test = [
      generate(width=13, height=14, bgcolor=8, wides=[4, 3], talls=[4, 4],
               halves=[3, 2], brows=[1, 9], bcols=[2, 6], tcolors=[1, 2],
               bcolors=[2, 4], a_s=[1, 3], b_s=[3, 0], c_s=[4, 1], d_s=[0, 2],
               e_s=[1, 0], f_s=[0, 1]),
  ]
  return {"train": train, "test": test}
