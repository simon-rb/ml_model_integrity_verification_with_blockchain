import json
import base64
import time
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import (
    CreateInstanceRequest,
    StartInstanceRequest,
    DescribeInstancesRequest,
)
from aliyunsdkecs.request.v20140526 import AllocateEipAddressRequest
from aliyunsdkvpc.request.v20160428.AssociateEipAddressRequest import (
    AssociateEipAddressRequest,
)

# Load configuration
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Initialize the AcsClient
client = AcsClient(
    config["access_key_id"], config["access_key_secret"], config["region_id"]
)


def create_ecs_instance():
    """Creates an ECS instance and returns its ID."""
    request = CreateInstanceRequest.CreateInstanceRequest()
    request.set_InstanceName("MyGanacheECS")
    request.set_ImageId("ubuntu_22_04_x64_20G_alibase_20240508.vhd")
    request.set_InstanceType("ecs.g6.xlarge")
    request.set_SecurityGroupId(config["security_group_id"])
    request.set_VSwitchId(config["vswitch_id"])
    request.set_SystemDiskCategory("cloud_efficiency")
    request.set_SystemDiskSize(40)

    user_data_script = """#!/bin/bash
        apt-get update && apt-get install -y docker.io
        systemctl start docker
        systemctl enable docker
        docker pull trufflesuite/ganache-cli
        docker run -d -p 8545:8545 trufflesuite/ganache-cli
        """

    encoded_user_data = base64.b64encode(user_data_script.encode("utf-8")).decode(
        "utf-8"
    )
    request.set_UserData(encoded_user_data)
    response = client.do_action_with_exception(request)
    return json.loads(response)["InstanceId"]


def allocate_eip():
    """Allocates an EIP and returns its allocation ID and IP address."""
    request = AllocateEipAddressRequest.AllocateEipAddressRequest()
    request.set_Bandwidth("10")
    response = client.do_action_with_exception(request)
    return json.loads(response)["AllocationId"], json.loads(response)["EipAddress"]


def associate_eip_with_instance(allocation_id, instance_id):
    """Associates an EIP with an ECS instance."""
    request = AssociateEipAddressRequest()
    request.set_AllocationId(allocation_id)
    request.set_InstanceId(instance_id)
    client.do_action_with_exception(request)


def wait_for_instance_status(instance_id, desired_status, timeout=600, interval=10):
    """Waits for the instance to reach a specific status."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if get_instance_status(instance_id) == desired_status:
            return True
        time.sleep(interval)
    return False


def get_instance_status(instance_id):
    """Retrieves the current status of an ECS instance."""
    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_InstanceIds(json.dumps([instance_id]))
    response = client.do_action_with_exception(request)
    return json.loads(response)["Instances"]["Instance"][0]["Status"]


def start_instance(instance_id):
    """Starts an ECS instance."""
    request = StartInstanceRequest.StartInstanceRequest()
    request.set_InstanceId(instance_id)
    client.do_action_with_exception(request)


def save_eip_to_file(eip):
    """Saves an EIP to a file."""
    eip_info = {"eip_address": eip}

    with open("eip_info.json", "w") as eip_file:
        json.dump(eip_info, eip_file)


# Main script execution
primary_eip_allocation_id, primary_eip = allocate_eip()
ecs_instance_id = create_ecs_instance()
if wait_for_instance_status(ecs_instance_id, "Stopped"):
    associate_eip_with_instance(primary_eip_allocation_id, ecs_instance_id)
    start_instance(ecs_instance_id)
    save_eip_to_file(primary_eip)
    print(
        f"Successfully started ECS instance with ID: {ecs_instance_id} and associated EIP: {primary_eip}"
    )
else:
    raise Exception("Instance did not reach 'Stopped' state in time")
