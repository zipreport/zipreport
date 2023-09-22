import os
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from shutil import rmtree

from tests.utils import RPT_FILTER_EXAMPLE_PATH
from zipreport.report import ReportFileBuilder, ReportFileLoader


class JinjaFilterTest:
    temp_dir = '/tmp'

    # pre-generated images, for convenience
    png_b64_image = b'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'
    jpg_b64_image = b'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'
    gif_b64_image = b'R0lGODlhgACAAMZiAAAp/w0t/xYw/xwz/yY5/yo8/y4//zVD/zhG/z1K/0BM/0JO/0VQ/0dS/0tV/1Nb/1Zf/1xj/2Nq/2lv/21z/251/3h9/3p//3yB/36C/4CF/4KH/4SJ/4WK/4mN/4uP/4yQ/42R/4+T/5GU/5KV/5SX/5SY/5WZ/5ib/5mc/52g/5+i/6ir/6mr/66w/7Cy/7Gz/7K0/7O1/7W3/7a4/72+/77A/8DC/8HD/8XH/8nK/8vN/83O/8/Q/9HS/9LT/9XW/9fY/9na/9ra/9rb/9zd/93e/9/g/+Dh/+Hi/+Tl/+jp/+np/+nq/+vr/+3t/+7u/+7v/+/v//Dx//Hx//Hy//T0//X1//b2//f3//f4//j4//n5//r6//v8//z8//39//7+/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////yH5BAEKAH8ALAAAAACAAIAAAAf+gGKCg4SFhoeIiYqLjI2Oj5CRkpOUlZaXmJmam5ydnp+goaKjpKWmp6ipqqusra6vsLGys7S1tre4ubq7vL2+v8DBwsPExcbHyMnKy8zNzs/Q0dLT1NXW19jZ2tvc3d7f4OHi4+Tl5ufo6err7O3uu19HNSkWDwgCCRAUJDE8Uu9NWCgAQLCgQYMSXDBB1OVgQS+GGjqcOJHDLisqAlDcSHDDIYkOIRYCyZGixVxDGpTkaOAjRZGESK48ePKWDgEzN7aM+JJnToc1a/nQ+HPizpE9kRY1GHSWkwMbE7D48QQLmCxRjtgwAZXg0ZhJwS4t2FTWBooBZmhRxKVHBwD+XwfJfOgz5DAhFA0QeXQkhMuJMOWGBfaBIo9McwkGFpQYwOJeV3A6/KCp8WPLwn5QNFJ5MGPPvWBMTACmM+C6Bx/zMjFRxCbMSscysIVhIovXoBuvnF2rwsQZiG6snBI7NeqivGn5dkgj+PDiBi+PJZh81oWJLZyXJC7WLvSf1WWVmDhCO0fugk9/zxk+1ouJDMIcEr59vePjdINpnpiEkYyJ6H2mXnfGBWOFZAed4B+A9kk3IDAeUBTEIv85FKAYsBEY3TBBULSAEopUeNCFGabnXTBhZJBXDl8gIqJBJOYGmi9LFLBRBDMUUUUXYGDxhA8aMKhhfkMqVswO0wmMaWKBRd5XDA5JjtggfkYa4wMCURJExZRcGgMFCNMNgAISVDrZpGrDHIECATMN0MENW/514pIbLrMFEDGAMMECBBDggAQXrGCDEFksUqKAc76j6KKMNuroo5BGKumklFZq6aWYZqrpppx26umnoIYq6qiklmrqqaimquqqrLbq6quwxirrrLTWaustgQAAOw=='
    svg_b64_image = b'PHN2ZyB3aWR0aD0iMTY2LjM0ODgwMzcxMDkzNzVweCIgaGVpZ2h0PSIxMjIuMDIxMjQwMjM0Mzc1cHgiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld0JveD0iMTY2LjgyNTU5ODE0NDUzMTI2IDEzLjk4OTM3OTg4MjgxMjUgMTY2LjM0ODgwMzcxMDkzNzUgMTIyLjAyMTI0MDIzNDM3NSIgc3R5bGU9ImJhY2tncm91bmQ6IHJnYmEoMCwgMCwgMCwgMCk7IiBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJ4TWlkWU1pZCI+PGRlZnM+PGZpbHRlciBpZD0iZWRpdGluZy1ob2xlIiB4PSItMTAwJSIgeT0iLTEwMCUiIHdpZHRoPSIzMDAlIiBoZWlnaHQ9IjMwMCUiPjxmZUZsb29kIGZsb29kLWNvbG9yPSIjMDAwIiByZXN1bHQ9ImJsYWNrIj48L2ZlRmxvb2Q+PGZlTW9ycGhvbG9neSBvcGVyYXRvcj0iZGlsYXRlIiByYWRpdXM9IjIiIGluPSJTb3VyY2VHcmFwaGljIiByZXN1bHQ9ImVyb2RlIj48L2ZlTW9ycGhvbG9neT48ZmVHYXVzc2lhbkJsdXIgaW49ImVyb2RlIiBzdGREZXZpYXRpb249IjQiIHJlc3VsdD0iYmx1ciI+PC9mZUdhdXNzaWFuQmx1cj48ZmVPZmZzZXQgaW49ImJsdXIiIGR4PSIyIiBkeT0iMiIgcmVzdWx0PSJvZmZzZXQiPjwvZmVPZmZzZXQ+PGZlQ29tcG9zaXRlIG9wZXJhdG9yPSJhdG9wIiBpbj0ib2Zmc2V0IiBpbjI9ImJsYWNrIiByZXN1bHQ9Im1lcmdlIj48L2ZlQ29tcG9zaXRlPjxmZUNvbXBvc2l0ZSBvcGVyYXRvcj0iaW4iIGluPSJtZXJnZSIgaW4yPSJTb3VyY2VHcmFwaGljIiByZXN1bHQ9ImlubmVyLXNoYWRvdyI+PC9mZUNvbXBvc2l0ZT48L2ZpbHRlcj48L2RlZnM+PGcgZmlsdGVyPSJ1cmwoI2VkaXRpbmctaG9sZSkiPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDE5Ny40MDIxOTA2ODUyNzIyMiwgOTguMzUyMTg2MjAzMDAyOTMpIj48cGF0aCBkPSJNMjAuMjItMjIuNDZMMjAuMjItMjIuNDZMMjAuMjItMjIuNDZRMjEuMTItMjQuODMgMjEuMTItMjYuODhMMjEuMTItMjYuODhMMjEuMTItMjYuODhRMjEuMTItMzAuNjYgMTguMDUtMzAuNjZMMTguMDUtMzAuNjZMMTguMDUtMzAuNjZRMTYuNDUtMzAuNjYgMTUuMTQtMjkuMjJMMTUuMTQtMjkuMjJMMTUuMTQtMjkuMjJRMTMuODItMjcuNzggMTMuODItMjUuOThMMTMuODItMjUuOThMMTMuODItMjUuOThRMTMuODItMjQuNzAgMTQuODUtMjMuNjhMMTQuODUtMjMuNjhMMTQuODUtMjMuNjhRMTYuMzItMjIuMjcgMjAuMTAtMTkuOTdMMjAuMTAtMTkuOTdMMjAuMTAtMTkuOTdRMjMuODctMTcuNjYgMjUuMzEtMTUuNzhMMjUuMzEtMTUuNzhMMjUuMzEtMTUuNzhRMjYuNzUtMTMuODkgMjYuNzUtMTEuMzBMMjYuNzUtMTEuMzBMMjYuNzUtMTEuMzBRMjYuNzUtOC43MCAyNS41MC02LjM0TDI1LjUwLTYuMzRMMjUuNTAtNi4zNFEyNC4yNi0zLjk3IDIyLjAyLTIuMzBMMjIuMDItMi4zMEwyMi4wMi0yLjMwUTE3LjIyIDEuMjggOS41NCAxLjI4TDkuNTQgMS4yOEw5LjU0IDEuMjhRNS4zOCAxLjI4IDIuMTgtMC45MEwyLjE4LTAuOTBMMi4xOC0wLjkwUS0xLjAyLTMuMDEtMS4wMi01LjUwTC0xLjAyLTUuNTBMLTEuMDItNS41MFEtMS4wMi04IDAuODAtOS40N0wwLjgwLTkuNDdMMC44MC05LjQ3UTIuNjItMTAuOTQgNS4zMS0xMC45NEw1LjMxLTEwLjk0TDUuMzEtMTAuOTRROC0xMC45NCA5LjY2LTkuOTJMOS42Ni05LjkyTDkuNjYtOS45MlE4LjgzLTcuODEgOC44My02LjQwTDguODMtNi40MEw4LjgzLTYuNDBROC44My0yLjE4IDEyLjQyLTIuMThMMTIuNDItMi4xOEwxMi40Mi0yLjE4UTEzLjk1LTIuMTggMTQuOTgtMy4xNEwxNC45OC0zLjE0TDE0Ljk4LTMuMTRRMTYtNC4xMCAxNi01Ljc2TDE2LTUuNzZMMTYtNS43NlExNi05LjAyIDEwLjUwLTEyLjQ4TDEwLjUwLTEyLjQ4TDEwLjUwLTEyLjQ4UTYuMDItMTUuNDIgNC45OS0xNi41OEw0Ljk5LTE2LjU4TDQuOTktMTYuNThRMy4yNi0xOC42MiAzLjI2LTIxLjE4TDMuMjYtMjEuMThMMy4yNi0yMS4xOFEzLjI2LTIzLjc0IDQuNDgtMjYuMThMNC40OC0yNi4xOEw0LjQ4LTI2LjE4UTUuNzAtMjguNjEgNy45NC0zMC4zNEw3Ljk0LTMwLjM0TDcuOTQtMzAuMzRRMTIuNjEtMzMuOTIgMjAuNzQtMzMuOTJMMjAuNzQtMzMuOTJMMjAuNzQtMzMuOTJRMjQuOTAtMzMuOTIgMjcuMzYtMzIuMjZMMjcuMzYtMzIuMjZMMjcuMzYtMzIuMjZRMjkuODItMzAuNTkgMjkuODItMjcuNzhMMjkuODItMjcuNzhMMjkuODItMjcuNzhRMjkuODItMjQuOTYgMjguMTMtMjMuMzZMMjguMTMtMjMuMzZMMjguMTMtMjMuMzZRMjYuNDMtMjEuNzYgMjMuMzYtMjEuNzZMMjMuMzYtMjEuNzZMMjMuMzYtMjEuNzZRMjEuMjUtMjEuNzYgMjAuMjItMjIuNDZaTTU1LjQyLTMxLjU1TDU1LjQyLTMxLjU1TDU1LjQyLTMxLjU1UTU3LjU0LTMzLjkyIDYxLjE4LTMzLjkyTDYxLjE4LTMzLjkyTDYxLjE4LTMzLjkyUTYzLjQyLTMzLjkyIDY1LjE1LTMyLjcwTDY1LjE1LTMyLjcwTDY1LjE1LTMyLjcwUTY2Ljg4LTMxLjQ5IDY2Ljg4LTI5LjIyTDY2Ljg4LTI5LjIyTDY2Ljg4LTI5LjIyUTY2Ljg4LTI2Ljk0IDY2LjE4LTI0LjUxTDY2LjE4LTI0LjUxTDY2LjE4LTI0LjUxUTY1LjQ3LTIyLjA4IDY0LjM4LTE5LjU4TDY0LjM4LTE5LjU4TDY0LjM4LTE5LjU4UTYyLjIxLTE0LjcyIDU5LjIwLTEwLjY5TDU5LjIwLTEwLjY5TDU5LjIwLTEwLjY5UTU0Ljk4LTQuODYgNTAuOTEtMS43OUw1MC45MS0xLjc5TDUwLjkxLTEuNzlRNDYuODUgMS4yOCA0Mi40MyAxLjI4TDQyLjQzIDEuMjhMNDIuNDMgMS4yOFEzOC44NSAxLjI4IDM2LjY3IDAuNDVMMzYuNjcgMC40NUwzNi42NyAwLjQ1UTM2LjI5LTEyLjk5IDM1LjgxLTE3Ljc5TDM1LjgxLTE3Ljc5TDM1LjgxLTE3Ljc5UTM1LjMzLTIyLjU5IDM0Ljk0LTI1LjIyTDM0Ljk0LTI1LjIyTDM0Ljk0LTI1LjIyUTM0LjMwLTMwLjM0IDMyLjM4LTMxLjU1TDMyLjM4LTMxLjU1TDMyLjM4LTMxLjU1UTMzLjg2LTMyLjgzIDM1LjMwLTMzLjM4TDM1LjMwLTMzLjM4TDM1LjMwLTMzLjM4UTM2Ljc0LTMzLjkyIDM5LjcxLTMzLjkyTDM5LjcxLTMzLjkyTDM5LjcxLTMzLjkyUTQyLjY5LTMzLjkyIDQ0LjgwLTMxLjU4TDQ0LjgwLTMxLjU4TDQ0LjgwLTMxLjU4UTQ2LjkxLTI5LjI1IDQ3LjMzLTI1LjEyTDQ3LjMzLTI1LjEyTDQ3LjMzLTI1LjEyUTQ3Ljc0LTIwLjk5IDQ3Ljc0LTE2TDQ3Ljc0LTE2TDQ3Ljc0LTE2UTQ3Ljc0LTExLjAxIDQ3LjM2LTQuOTlMNDcuMzYtNC45OUw0Ny4zNi00Ljk5UTQ5LjM0LTYuNDAgNTEuNDYtMTAuNjlMNTEuNDYtMTAuNjlMNTEuNDYtMTAuNjlRNTQuMzQtMTYuNjQgNTUuMzYtMjMuODFMNTUuMzYtMjMuODFMNTUuMzYtMjMuODFRNTUuNjgtMjUuOTggNTUuNjgtMjguMjlMNTUuNjgtMjguMjlMNTUuNjgtMjguMjlRNTUuNjgtMzAuNTkgNTUuNDItMzEuNTVaTTczLjE1LTI2Ljc1TDczLjE1LTI2Ljc1TDczLjE1LTI2Ljc1UTc1LjMzLTI5LjgyIDc4LjYyLTMxLjg3TDc4LjYyLTMxLjg3TDc4LjYyLTMxLjg3UTgxLjkyLTMzLjkyIDg1Ljk1LTMzLjkyTDg1Ljk1LTMzLjkyTDg1Ljk1LTMzLjkyUTg5Ljk4LTMzLjkyIDkxLjkwLTMyLjY0TDkxLjkwLTMyLjY0TDEwNC40NS0zMy45MkwxMDAuMTAtOS4zNEwxMDAuMTAtOS4zNFE5Ny44NiAzLjIwIDkzLjEyIDguMTNMOTMuMTIgOC4xM0w5My4xMiA4LjEzUTg4LjU4IDEyLjgwIDc5Ljc0IDEyLjgwTDc5Ljc0IDEyLjgwTDc5Ljc0IDEyLjgwUTczLjAyIDEyLjgwIDY5LjE4IDEwLjY5TDY5LjE4IDEwLjY5TDY5LjE4IDEwLjY5UTY1LjM0IDguNTggNjUuMzQgNS4wNkw2NS4zNCA1LjA2TDY1LjM0IDUuMDZRNjUuMzQgMi40MyA2Ny4zMyAwLjkzTDY3LjMzIDAuOTNMNjcuMzMgMC45M1E2OS4zMS0wLjU4IDcyLjM4LTAuNThMNzIuMzgtMC41OEw3Mi4zOC0wLjU4UTc1LjA3LTAuNTggNzcuMTIgMC42NEw3Ny4xMiAwLjY0TDc3LjEyIDAuNjRRNzguMzQgMS4yOCA3OC45MSAyLjE4TDc4LjkxIDIuMThMNzguOTEgMi4xOFE3Ny40NCAzLjQ2IDc3LjQ0IDUuNTdMNzcuNDQgNS41N0w3Ny40NCA1LjU3UTc3LjQ0IDguMzIgODAuMDAgOC4zMkw4MC4wMCA4LjMyTDgwLjAwIDguMzJRODQuMjkgOC4zMiA4Ni43Mi0xLjc5TDg2LjcyLTEuNzlMODYuNzItMS43OVE4Ny40Mi00LjU0IDg4LjAwLTcuMzBMODguMDAtNy4zMEw4OC4wMC03LjMwUTg1LjEyLTMuNzggNzguNTktMy43OEw3OC41OS0zLjc4TDc4LjU5LTMuNzhRNzQuMDUtMy43OCA3MS40Mi01Ljk1TDcxLjQyLTUuOTVMNzEuNDItNS45NVE2OC44MC04LjEzIDY4LjgwLTEzLjI1TDY4LjgwLTEzLjI1TDY4LjgwLTEzLjI1UTY4LjgwLTE2LjQ1IDY5Ljg5LTIwLjA2TDY5Ljg5LTIwLjA2TDY5Ljg5LTIwLjA2UTcwLjk4LTIzLjY4IDczLjE1LTI2Ljc1Wk04MS40Ny0xMy4wNkw4MS40Ny0xMy4wNkw4MS40Ny0xMy4wNlE4MS40Ny04LjcwIDgzLjcxLTguNzBMODMuNzEtOC43MEw4My43MS04LjcwUTg1LjI1LTguNzAgODYuNzItMTAuMzdMODYuNzItMTAuMzdMODYuNzItMTAuMzdRODcuODctMTEuNzEgODguMzItMTMuNzBMODguMzItMTMuNzBMOTEuNTgtMzAuMTRMOTEuNTgtMzAuMTRROTEuMjYtMzAuMjEgOTAuOTQtMzAuMzRMOTAuOTQtMzAuMzRMOTAuOTQtMzAuMzRROTAuMzAtMzAuNTkgODkuNDctMzAuNTlMODkuNDctMzAuNTlMODkuNDctMzAuNTlRODUuNTctMzAuNTkgODMuMjYtMjQuMTlMODMuMjYtMjQuMTlMODMuMjYtMjQuMTlRODEuNDctMTkuMjAgODEuNDctMTMuMDZaIiBmaWxsPSIjY2NjIj48L3BhdGg+PC9nPjwvZz48c3R5bGU+dGV4dCB7CiAgZm9udC1zaXplOiA2NHB4OwogIGZvbnQtZmFtaWx5OiBBcmlhbCBCbGFjazsKICBkb21pbmFudC1iYXNlbGluZTogY2VudHJhbDsKICB0ZXh0LWFuY2hvcjogbWlkZGxlOwp9PC9zdHlsZT48L3N2Zz4='

    def setup_method(self, method):
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self, method):
        if os.path.exists(self.temp_dir) and self.temp_dir != '/tmp':
            rmtree(self.temp_dir)
            self.temp_dir = '/tmp'

    def build_zpt(self):
        zptfile = Path(self.temp_dir) / 'test.zpt'
        result = ReportFileBuilder.build_file(RPT_FILTER_EXAMPLE_PATH, zptfile)
        assert result.success() is True
        zpt = ReportFileLoader.load_file(zptfile)
        assert zpt is not None
        return zpt


class ImageParser(HTMLParser):

    def reset(self):
        super().reset()
        self._images = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self._images.append(attrs)

    def get_images(self) -> list:
        result = []
        for img in self._images:
            data = {attr[0]: attr[1] for attr in img}
            result.append(data)
        return result
