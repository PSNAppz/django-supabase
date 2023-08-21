from django.utils import timezone
from django.conf import settings

from rest_framework.renderers import JSONRenderer as BaseJSONRenderer


class JSONRenderer(BaseJSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        view = renderer_context.get("view", None)
        response = renderer_context.get("response", None)
        message = None
        keys = None
        if data is not None:
            if 'message' in data:
                message = data['message']
            if 'keys' in data:
                keys = data['keys']     
            if 'data' in data:
                data = data['data']      
        _data = {
            'success': getattr(view, 'success',True),
            'message': message,
        }
        
        if not response.exception:
            if response.status_code not in [200, 201, 202, 204]:
                _data = {
                    'success': getattr(view, 'success',False),
                    'message': data,
                    'data': {},
                }
            else:    
                
                if response.status_code == 204:
                    # change response code to 200
                    response.status_code = 200
                    _data = {
                        'success': getattr(view, 'success',True),
                        'message': "Content has been deleted succesfully!",
                    }
                else:
                    _data.update(data=data or {},)  
                    if keys:    
                        _data.update(keys=keys)  
        else:
            _data = {
                    'success': getattr(view, 'success',False),
                    'message': data,
                    'data': {},
                }

        _data.update(
            server_datetime=timezone.now().isoformat(),
        )

        return super().render(_data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)
