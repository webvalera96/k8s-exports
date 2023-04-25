from kubernetes.client.rest import ApiException
from kubernetes import client, config
import json
import yaml


def convert_to_yaml(item):
    sanitize_api_response = client.ApiClient().sanitize_for_serialization(item)
    json_api_response = json.dumps(sanitize_api_response)
    yaml_api_response = yaml.dump(json.loads(json_api_response), sort_keys=False)
    return yaml_api_response


def get_custom_object(api_client, group, version, namespace, plural):
    result = []
    try:
        api_response = api_client.list_namespaced_custom_object(group, version, namespace, plural)

        for custom_object in api_response["items"]:
            result.append(convert_to_yaml(custom_object))
        return result
    except ApiException as e:
        print("Exception when calling CustomObjectsApi->list_namespaced_custom_object: %s\n" % e)


def get_destination_rules(api_client, namespace="default"):
    return get_custom_object(api_client, "networking.istio.io", "v1alpha3", namespace, "destinationrules")


def get_deployments(api_client, namespace="default"):
    result = []
    try:
        api_response = api_client.list_namespaced_deployment(namespace)

        for deploy in api_response.items:
            result.append(convert_to_yaml(deploy))
        return result
    except ApiException as e:
        print("Exception when calling AppsV1Api->list_namespaced_deployment: %s\n" % e)


if __name__ == "__main__":
    config.load_kube_config()
    v1 = client.AppsV1Api()
    v1_cr = client.CustomObjectsApi()

    deployments = get_deployments(v1, namespace="kube-system")
    destination_rules = get_destination_rules(v1_cr, namespace="default")
