from rest_framework.renderers import BaseRenderer


class CustomRenderer(BaseRenderer):
    media_type = 'image/png'
    format = 'png'
    charset = None
    render_style = 'binary'


    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data