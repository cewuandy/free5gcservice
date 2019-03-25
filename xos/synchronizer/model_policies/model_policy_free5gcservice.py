import base64
import jinja2
import json
import yaml
from synchronizers.new_base.modelaccessor import *
from synchronizers.new_base.policy import Policy

from xosconfig import Config
from multistructlog import create_logger

log = create_logger(Config().get('logging'))


class Free5GCServicePolicy(Policy):
    model_name = "Free5GCService"

    def handle_create(self, service_instance):
        log.info("handle_create Free5GCService")
        return self.handle_update(service_instance)

    def handle_update(self, service_instance):
        log.info("handle_update Free5GCService")
        type = service_instance.component_type.lower()
        name = type + "%s" % service_instance.id
        log.info(self)
        log.info(service_instance)
        log.info(KubernetesService.objects.first())
        instance = Free5GCServiceInstance(name=name, owner=service_instance,
                                          type=service_instance.component_type, no_sync=False)
        instance.save()

    def handle_delete(self, service_instance):
        log.info("handle_delete Free5GCService")
        service_instance.compute_instance.delete()
        service_instance.compute_instance = None
        service_instance.save(update_fields=["compute_instance"])
