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


def generate(wides=None, talls=None, brows=None, bcols=None, prows=None,
             pcols=None, groups=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: the widths of the boxes.
    talls: the heights of the boxes.
    brows: the widths of the boxes.
    bcols: the heights of the boxes.
    prows: the widths of the pixels.
    pcols: the heights of the pixels.
    groups: the groups of the pixels.
  """

  if wides is None:
    num_boxes = common.randint(4, 6)
    while True:
      wides = [common.randint(2, 7) for _ in range(num_boxes)]
      talls = [common.randint(2, 7) for _ in range(num_boxes)]
      brows = [common.randint(0, 15 - tall) for tall in talls]
      bcols = [common.randint(0, 15 - wide) for wide in wides]
      if common.overlaps(brows, bcols, wides, talls, 1): continue
      num_pixels = sorted([common.randint(1, 7) for _ in range(num_boxes)])
      if num_pixels[0] == num_pixels[1]: continue  # we need a unique minimum
      good = True
      for i in range(num_boxes):
        if num_pixels[i] > (wides[i] * talls[i]) // 2: good = False
      if not good: continue  # Need more green than purple in each box.
      prows, pcols, groups = [], [], []
      for i in range(num_boxes):
        pixels = common.all_pixels(wides[i], talls[i])
        pixels = common.sample(pixels, num_pixels[i])
        prows.extend([p[0] for p in pixels])
        pcols.extend([p[1] for p in pixels])
        groups.extend([i] * len(pixels))
      break

  grid, output = common.grids(15, 15)
  for i in range(len(wides)):
    wide, tall, brow, bcol = wides[i], talls[i], brows[i], bcols[i]
    common.rect(grid, wide, tall, brow, bcol, 3)
    if i: common.rect(output, wide, tall, brow, bcol, 3)
  for prow, pcol, group in zip(prows, pcols, groups):
    grid[brows[group] + prow][bcols[group] + pcol] = 9
    if group: output[brows[group] + prow][bcols[group] + pcol] = 9
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[5, 3, 4, 5, 2, 4], talls=[3, 5, 4, 4, 5, 5],
               brows=[1, 0, 2, 7, 7, 9], bcols=[1, 12, 7, 0, 12, 7],
               prows=[1, 2, 1, 2, 3, 4, 1, 1, 3, 0, 1, 2, 3, 1, 3, 4, 1, 1, 3, 3, 4],
               pcols=[2, 1, 1, 1, 2, 0, 1, 2, 2, 1, 3, 1, 3, 1, 1, 0, 1, 3, 1, 2, 3],
               groups=[0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5]),
      generate(wides=[5, 3, 3, 7, 5], talls=[5, 5, 2, 6, 5],
               brows=[1, 0, 6, 8, 9], bcols=[6, 1, 2, 8, 1],
               prows=[1, 1, 1, 2, 3, 0, 1, 2, 2, 2, 4, 5, 2, 4],
               pcols=[3, 0, 2, 1, 2, 1, 0, 1, 3, 4, 2, 6, 1, 3],
               groups=[0, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 4, 4]),
      generate(wides=[7, 7, 5, 4], talls=[5, 5, 4, 5], brows=[7, 1, 1, 8],
               bcols=[6, 0, 10, 1],
               prows=[1, 2, 3, 0, 1, 2, 2, 3, 4, 0, 0, 2, 2, 1, 1, 2, 3, 3],
               pcols=[5, 1, 3, 2, 5, 1, 3, 4, 2, 2, 4, 1, 4, 1, 3, 3, 0, 2],
               groups=[0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3]),
      generate(wides=[3, 5, 4, 3, 4, 5], talls=[2, 3, 4, 6, 7, 3],
               brows=[6, 0, 1, 5, 6, 10], bcols=[5, 1, 7, 0, 11, 4],
               prows=[0, 1, 0, 2, 2, 0, 1, 2, 2, 0, 1, 2, 4, 5, 0, 1, 2, 3, 4, 5, 6, 0, 1, 1],
               pcols=[1, 2, 2, 0, 3, 1, 3, 0, 2, 2, 0, 1, 0, 2, 2, 0, 2, 1, 2, 3, 0, 3, 0, 2],
               groups=[0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5]),
  ]
  test = [
      generate(wides=[5, 6, 5, 5, 3, 4], talls=[6, 3, 6, 4, 5, 3],
               brows=[0, 1, 5, 8, 10, 12], bcols=[9, 2, 0, 6, 12, 0],
               prows=[1, 5, 0, 1, 2, 1, 1, 3, 3, 4, 0, 0, 2, 2, 1, 3, 3, 0, 1, 1, 2],
               pcols=[1, 2, 4, 1, 5, 1, 3, 1, 3, 2, 2, 3, 1, 3, 2, 1, 2, 2, 1, 3, 0],
               groups=[0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5]),
  ]
  return {"train": train, "test": test}
