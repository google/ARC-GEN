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


def generate(width=None, height=None, values=None, thicks=None, cdirs=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if width is None:
    base = common.randint(5, 12)
    width, height = base + common.randint(-2, 2), base + common.randint(-2, 2)
    num_h, num_v = base // 4, base // 4
    if base > 8 and common.randint(0, 1): num_h += 1
    if base > 8 and common.randint(0, 1): num_v += 1
    while True:
      h_thicks = [common.randint(1, min(3, height - 2)) for _ in range(num_v)]
      v_thicks = [common.randint(1, min(3, width - 2)) for _ in range(num_v)]
      h_vals = [common.randint(1, height - thick - 1) for thick in h_thicks]
      v_vals = [common.randint(1, width - thick - 1) for thick in v_thicks]
      if common.overlaps_1d(h_vals, h_thicks, 1): continue
      if common.overlaps_1d(v_vals, v_thicks, 1): continue
      values, thicks, cdirs = [], [], []
      while h_thicks or v_thicks:
        if common.randint(0, 1):
          if not h_thicks: continue
          thicks, values = thicks + [h_thicks.pop()], values + [h_vals.pop()]
          cdirs.append(0)
        else:
          if not v_thicks: continue
          thicks, values = thicks + [v_thicks.pop()], values + [v_vals.pop()]
          cdirs.append(1)
      if cdirs[-1] != cdirs[-2]: break
    colors = common.random_colors(len(values))

  grid, output = common.grid(width, height), common.grid(1, 1, colors[-1])
  for value, thick, cdir, color in zip(values, thicks, cdirs, colors):
    if cdir:
      common.rect(grid, thick, height, 0, value, color)
    else:
      common.rect(grid, width, thick, value, 0, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=11, values=[1, 4, 6, 8, 3],
               thicks=[1, 2, 2, 1, 2], cdirs=[0, 1, 0, 1, 0],
               colors=[2, 3, 4, 5, 1]),
      generate(width=11, height=9, values=[2, 3, 5, 8], thicks=[1, 2, 2, 1],
               cdirs=[0, 1, 0, 1], colors=[3, 4, 6, 8]),
      generate(width=11, height=11, values=[1, 1, 7, 6, 4],
               thicks=[3, 2, 2, 2, 1], cdirs=[0, 1, 1, 0, 1],
               colors=[1, 2, 8, 4, 6]),
      generate(width=3, height=3, values=[1, 1], thicks=[1, 1], cdirs=[1, 0],
               colors=[1, 3]),
      generate(width=12, height=8, values=[2, 1, 7, 5], thicks=[2, 2, 1, 1],
               cdirs=[0, 1, 1, 0], colors=[3, 2, 8, 6]),
  ]
  test = [
      generate(width=13, height=11, values=[2, 3, 6, 9], thicks=[2, 2, 1, 1],
               cdirs=[0, 1, 0, 1], colors=[1, 3, 6, 7]),
  ]
  return {"train": train, "test": test}
