import base64
from tests.render.filters.base import JinjaFilterTest, ImageParser
from zipreport.template import JinjaRender
from zipreport.template.jinja import filters


class TestJinjaFilters(JinjaFilterTest):
    # must match filter tag in the template
    expected_png_attrs = {
        "alt": "label for png",
        "width": '128',
        "height": '128',
        "class": "css class",
    }
    expected_jpg_attrs = {
        "alt": "label for jpg",
        "width": '128',
        "height": '128',
        "class": "css class",
    }
    expected_gif_attrs = {
        "alt": "label for gif",
        "width": '128',
        "height": '128',
        "class": "css class",
    }
    expected_svg_attrs = {
        "alt": "label for svg",
        "width": '128',
        "height": '128',
        "class": "css class",
    }

    def test_filter_graphics(self):
        def graphics(data):
            # return bytes for the image
            return base64.decodebytes(data)

        zpt = self.build_zpt()
        render = JinjaRender(zpt)
        result = render.render({
            "png_graphic": graphics,
            "png_graphic_data": self.png_b64_image,
            "gif_graphic": graphics,
            "gif_graphic_data": self.gif_b64_image,
            "jpg_graphic": graphics,
            "jpg_graphic_data": self.jpg_b64_image,
            "svg_graphic": graphics,
            "svg_graphic_data": self.svg_b64_image,
        })

        parser = ImageParser()
        parser.feed(str(result))
        images = parser.get_images()
        assert len(images) == 4
        i = 0
        for expected in [self.expected_png_attrs, self.expected_jpg_attrs, self.expected_gif_attrs,
                         self.expected_svg_attrs]:
            for attr in expected.keys():
                assert attr in images[i].keys()
                assert images[i][attr] == expected[attr]
            assert zpt.exists(images[i]['src']) is True
            i += 1
