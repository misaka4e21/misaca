from rest_framework.renderers import JSONRenderer

def flatten(input_array):
    result_array = []
    for element in input_array:
        if isinstance(element, list):
            result_array += flatten(element)
        else:
            result_array.append(element)
    return result_array

class ActivityStreamsRenderer(JSONRenderer):
    media_type='application/activity+json'
    def render(self, data, media_type=None, renderer_context=None):
        ctx = data.get('@context', [])
        ctx = ['https://www.w3.org/ns/activitystreams', ctx]
        ctx = flatten(ctx)
        if len(ctx)==1:
            ctx = ctx[0]
        data['@context'] = ctx
        return super().render(data, renderer_context=renderer_context)

class ActivityStreamsLDJSONRenderer(ActivityStreamsRenderer):
    media_type='application/ld+json; profile="https://www.w3.org/ns/activitystreams"'