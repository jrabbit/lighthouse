import json
import uuid
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse

from .models import BuoyClient

class HomeView(TemplateView):
    template_name = "lantern/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        # build list of clients
        client_list = BuoyClient.objects.order_by('name')   # maybe we should sort by users/popularity by default?
        # format list into context
        context['client_list'] = client_list
        # pass context to template
        return context

@method_decorator(csrf_exempt, name='dispatch')
class ProcessClientDataView(View):

    def post(self, request):
        # get json payload from request.body
        request_json = json.loads(request.body)
        # shortcut; remember -- is a copy, not a reference
        data = request_json['data']

        # send the context data to a checking function (verify using public keys? is that possible?)

        if data['type'] == "client":
            if 'id' in data:  # block create requests with client-generated IDs
                # reply 403 Forbidden for unsupported request to create a resource, as per JSON API v1.0
                return HttpResponse(status=403)
            else:
                # generate uuid and add to json
                client_id = uuid.uuid4()
                # build and save client model
                try:
                    client = BuoyClient(id=client_id)
                    for attribute in data['attributes']:
                        setattr(client, attribute, data['attributes'][attribute])
                except Exception as e:
                    # reply 400 Bad Request if client cannot be instantiated
                    return HttpResponse(status=400)

                client.save()
                # convert the updated data back into json
                request_json['data']['id'] = client_id.hex
                response_json = json.dumps(request_json)
                # reply 201 Created with resource and id, as per JSON API v1.0
                return HttpResponse(response_json, status=201)
        else:
            # reply 409 Conflict for unsupported type, as per JSON API v1.0
            return HttpResponse(status=409)

    def patch(self, request):
        request_json = json.loads(request.body)
        data = request_json['data']

        if data['type'] == "client":
            # reply 404 Not Found if object doesn't exist, as per JSON API v1.0
            if 'id' in data:
                client = get_object_or_404(BuoyClient, id=data['id'])
            else:
                return HttpResponse(status=404)
            for attribute in data['attributes']:
                # update model attribute value
                try:
                    setattr(client, attribute, data['attributes'][attribute])
                except Exception as e:
                    # field doesn't exist; reply 400 Bad Request
                    return HttpResponse(status=400)
            client.save()
            # if successful, reply with 200 OK and top-level meta data (if exists), as per JSON API v1.0
            if 'meta' in request_json:
                response_json = json.dumps(request_json['meta'])
                return HttpResponse(response_json, status=200)
            else:
                return HttpResponse(status=200)
        else:
            # reply 409 Conflict for unsupported type, as per JSON API v1.0
            return HttpResponse(status=409)

class ClientInfoView(TemplateView):
    template_name = "lantern/client.html"

    def get(self, request, client_id):
        client = get_object_or_404(BuoyClient, id=client_id)

        # get info from model & pass to template
        context_data = {} 
        context_data['client_id'] = client_id
        context_data['client_name'] = client.name
        context_data['client_url'] = client.url
        return self.render_to_response(status=200, context=context_data)
