#!/usr/bin/python

# Copyright 2018 A10 Networks
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")


DOCUMENTATION = """
module: a10_cgnv6_template_logging
description:
    - None
short_description: Configures A10 cgnv6.template.logging
author: A10 Networks 2018 
version_added: 2.4
options:
    state:
        description:
        - State of the object to be created.
        choices:
        - present
        - absent
        required: True
    a10_host:
        description:
        - Host for AXAPI authentication
        required: True
    a10_username:
        description:
        - Username for AXAPI authentication
        required: True
    a10_password:
        description:
        - Password for AXAPI authentication
        required: True
    name:
        description:
        - "None"
        required: True
    resolution:
        description:
        - "None"
        required: False
    log:
        description:
        - "Field log"
        required: False
        suboptions:
            fixed_nat:
                description:
                - "Field fixed_nat"
            map_dhcpv6:
                description:
                - "Field map_dhcpv6"
            http_requests:
                description:
                - "None"
            port_mappings:
                description:
                - "None"
            port_overloading:
                description:
                - "None"
            sessions:
                description:
                - "None"
            merged_style:
                description:
                - "None"
    include_destination:
        description:
        - "None"
        required: False
    include_inside_user_mac:
        description:
        - "None"
        required: False
    include_partition_name:
        description:
        - "None"
        required: False
    include_session_byte_count:
        description:
        - "None"
        required: False
    include_radius_attribute:
        description:
        - "Field include_radius_attribute"
        required: False
        suboptions:
            attr_cfg:
                description:
                - "Field attr_cfg"
            no_quote:
                description:
                - "None"
            insert_if_not_existing:
                description:
                - "None"
            zero_in_custom_attr:
                description:
                - "None"
            framed_ipv6_prefix:
                description:
                - "None"
            prefix_length:
                description:
                - "None"
    include_http:
        description:
        - "Field include_http"
        required: False
        suboptions:
            header_cfg:
                description:
                - "Field header_cfg"
            l4_session_info:
                description:
                - "None"
            method:
                description:
                - "None"
            request_number:
                description:
                - "None"
            file_extension:
                description:
                - "None"
    rule:
        description:
        - "Field rule"
        required: False
        suboptions:
            rule_http_requests:
                description:
                - "Field rule_http_requests"
            interim_update_interval:
                description:
                - "None"
    facility:
        description:
        - "None"
        required: False
    severity:
        description:
        - "Field severity"
        required: False
        suboptions:
            severity_string:
                description:
                - "None"
            severity_val:
                description:
                - "None"
    format:
        description:
        - "None"
        required: False
    batched_logging_disable:
        description:
        - "None"
        required: False
    log_receiver:
        description:
        - "Field log_receiver"
        required: False
        suboptions:
            radius:
                description:
                - "None"
            secret_string:
                description:
                - "None"
            encrypted:
                description:
                - "None"
    service_group:
        description:
        - "None"
        required: False
    shared:
        description:
        - "None"
        required: False
    source_port:
        description:
        - "Field source_port"
        required: False
        suboptions:
            source_port_num:
                description:
                - "None"
            any:
                description:
                - "None"
    rfc_custom:
        description:
        - "Field rfc_custom"
        required: False
        suboptions:
            header:
                description:
                - "Field header"
            message:
                description:
                - "Field message"
    custom:
        description:
        - "Field custom"
        required: False
        suboptions:
            custom_header:
                description:
                - "None"
            custom_message:
                description:
                - "Field custom_message"
            custom_time_stamp_format:
                description:
                - "None"
    uuid:
        description:
        - "None"
        required: False
    user_tag:
        description:
        - "None"
        required: False
    source_address:
        description:
        - "Field source_address"
        required: False
        suboptions:
            ip:
                description:
                - "None"
            ipv6:
                description:
                - "None"
            uuid:
                description:
                - "None"
    disable_log_by_destination:
        description:
        - "Field disable_log_by_destination"
        required: False
        suboptions:
            tcp_list:
                description:
                - "Field tcp_list"
            udp_list:
                description:
                - "Field udp_list"
            icmp:
                description:
                - "None"
            others:
                description:
                - "None"
            uuid:
                description:
                - "None"


"""

EXAMPLES = """
"""

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'community',
    'status': ['preview']
}

# Hacky way of having access to object properties for evaluation
AVAILABLE_PROPERTIES = ["batched_logging_disable","custom","disable_log_by_destination","facility","format","include_destination","include_http","include_inside_user_mac","include_partition_name","include_radius_attribute","include_session_byte_count","log","log_receiver","name","resolution","rfc_custom","rule","service_group","severity","shared","source_address","source_port","user_tag","uuid",]

# our imports go at the top so we fail fast.
try:
    from a10_ansible import errors as a10_ex
    from a10_ansible.axapi_http import client_factory
    from a10_ansible.kwbl import KW_IN, KW_OUT, translate_blacklist as translateBlacklist

except (ImportError) as ex:
    module.fail_json(msg="Import Error:{0}".format(ex))
except (Exception) as ex:
    module.fail_json(msg="General Exception in Ansible module import:{0}".format(ex))


def get_default_argspec():
    return dict(
        a10_host=dict(type='str', required=True),
        a10_username=dict(type='str', required=True),
        a10_password=dict(type='str', required=True, no_log=True),
        state=dict(type='str', default="present", choices=["present", "absent"])
    )

def get_argspec():
    rv = get_default_argspec()
    rv.update(dict(
        name=dict(type='str',required=True,),
        resolution=dict(type='str',choices=['seconds','10-milliseconds']),
        log=dict(type='dict',fixed_nat=dict(type='dict',fixed_nat_http_requests=dict(type='str',choices=['host','url']),fixed_nat_port_mappings=dict(type='str',choices=['both','creation']),fixed_nat_sessions=dict(type='bool',),fixed_nat_merged_style=dict(type='bool',),user_ports=dict(type='dict',user_ports=dict(type='bool',),days=dict(type='int',),start_time=dict(type='str',))),map_dhcpv6=dict(type='dict',map_dhcpv6_prefix_all=dict(type='bool',),map_dhcpv6_msg_type=dict(type='list',map_dhcpv6_msg_type=dict(type='str',choices=['prefix-assignment','prefix-renewal','prefix-release']))),http_requests=dict(type='str',choices=['host','url']),port_mappings=dict(type='str',choices=['creation','disable']),port_overloading=dict(type='bool',),sessions=dict(type='bool',),merged_style=dict(type='bool',)),
        include_destination=dict(type='bool',),
        include_inside_user_mac=dict(type='bool',),
        include_partition_name=dict(type='bool',),
        include_session_byte_count=dict(type='bool',),
        include_radius_attribute=dict(type='dict',attr_cfg=dict(type='list',attr=dict(type='str',choices=['imei','imsi','msisdn','custom1','custom2','custom3']),attr_event=dict(type='str',choices=['http-requests','port-mappings','sessions'])),no_quote=dict(type='bool',),insert_if_not_existing=dict(type='bool',),zero_in_custom_attr=dict(type='bool',),framed_ipv6_prefix=dict(type='bool',),prefix_length=dict(type='str',choices=['32','48','64','80','96','112'])),
        include_http=dict(type='dict',header_cfg=dict(type='list',http_header=dict(type='str',choices=['cookie','referer','user-agent','header1','header2','header3']),max_length=dict(type='int',),custom_header_name=dict(type='str',),custom_max_length=dict(type='int',)),l4_session_info=dict(type='bool',),method=dict(type='bool',),request_number=dict(type='bool',),file_extension=dict(type='bool',)),
        rule=dict(type='dict',rule_http_requests=dict(type='dict',dest_port=dict(type='list',dest_port_number=dict(type='int',),include_byte_count=dict(type='bool',)),log_every_http_request=dict(type='bool',),max_url_len=dict(type='int',),include_all_headers=dict(type='bool',),disable_sequence_check=dict(type='bool',)),interim_update_interval=dict(type='int',)),
        facility=dict(type='str',choices=['kernel','user','mail','daemon','security-authorization','syslog','line-printer','news','uucp','cron','security-authorization-private','ftp','ntp','audit','alert','clock','local0','local1','local2','local3','local4','local5','local6','local7']),
        severity=dict(type='dict',severity_string=dict(type='str',choices=['emergency','alert','critical','error','warning','notice','informational','debug']),severity_val=dict(type='int',)),
        format=dict(type='str',choices=['binary','compact','custom','default','rfc5424','cef']),
        batched_logging_disable=dict(type='bool',),
        log_receiver=dict(type='dict',radius=dict(type='bool',),secret_string=dict(type='str',),encrypted=dict(type='str',)),
        service_group=dict(type='str',),
        shared=dict(type='bool',),
        source_port=dict(type='dict',source_port_num=dict(type='int',),any=dict(type='bool',)),
        rfc_custom=dict(type='dict',header=dict(type='dict',use_alternate_timestamp=dict(type='bool',)),message=dict(type='dict',ipv6_tech=dict(type='list',tech_type=dict(type='str',choices=['lsn','nat64','ds-lite','sixrd-nat64']),fixed_nat_allocated=dict(type='str',),fixed_nat_freed=dict(type='str',),port_allocated=dict(type='str',),port_freed=dict(type='str',),port_batch_allocated=dict(type='str',),port_batch_freed=dict(type='str',),port_batch_v2_allocated=dict(type='str',),port_batch_v2_freed=dict(type='str',)),http_request_got=dict(type='str',),session_created=dict(type='str',),session_deleted=dict(type='str',))),
        custom=dict(type='dict',custom_header=dict(type='str',choices=['use-syslog-header']),custom_message=dict(type='dict',custom_fixed_nat_allocated=dict(type='str',),custom_fixed_nat_interim_update=dict(type='str',),custom_fixed_nat_freed=dict(type='str',),custom_http_request_got=dict(type='str',),custom_port_allocated=dict(type='str',),custom_port_batch_allocated=dict(type='str',),custom_port_batch_freed=dict(type='str',),custom_port_batch_v2_allocated=dict(type='str',),custom_port_batch_v2_freed=dict(type='str',),custom_port_batch_v2_interim_update=dict(type='str',),custom_port_freed=dict(type='str',),custom_session_created=dict(type='str',),custom_session_deleted=dict(type='str',)),custom_time_stamp_format=dict(type='str',)),
        uuid=dict(type='str',),
        user_tag=dict(type='str',),
        source_address=dict(type='dict',ip=dict(type='str',),ipv6=dict(type='str',),uuid=dict(type='str',)),
        disable_log_by_destination=dict(type='dict',tcp_list=dict(type='list',tcp_port_start=dict(type='int',),tcp_port_end=dict(type='int',)),udp_list=dict(type='list',udp_port_start=dict(type='int',),udp_port_end=dict(type='int',)),icmp=dict(type='bool',),others=dict(type='bool',),uuid=dict(type='str',))
    ))

    return rv

def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/cgnv6/template/logging/{name}"
    f_dict = {}
    f_dict["name"] = ""

    return url_base.format(**f_dict)

def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/cgnv6/template/logging/{name}"
    f_dict = {}
    f_dict["name"] = module.params["name"]

    return url_base.format(**f_dict)


def build_envelope(title, data):
    return {
        title: data
    }

def _to_axapi(key):
    return translateBlacklist(key, KW_OUT).replace("_", "-")

def _build_dict_from_param(param):
    rv = {}

    for k,v in param.items():
        hk = _to_axapi(k)
        if isinstance(v, dict):
            v_dict = _build_dict_from_param(v)
            rv[hk] = v_dict
        if isinstance(v, list):
            nv = [_build_dict_from_param(x) for x in v]
            rv[hk] = nv
        else:
            rv[hk] = v

    return rv

def build_json(title, module):
    rv = {}

    for x in AVAILABLE_PROPERTIES:
        v = module.params.get(x)
        if v:
            rx = _to_axapi(x)

            if isinstance(v, dict):
                nv = _build_dict_from_param(v)
                rv[rx] = nv
            if isinstance(v, list):
                nv = [_build_dict_from_param(x) for x in v]
                rv[rx] = nv
            else:
                rv[rx] = module.params[x]

    return build_envelope(title, rv)

def validate(params):
    # Ensure that params contains all the keys.
    requires_one_of = sorted([])
    present_keys = sorted([x for x in requires_one_of if params.get(x)])
    
    errors = []
    marg = []
    
    if not len(requires_one_of):
        return REQUIRED_VALID

    if len(present_keys) == 0:
        rc,msg = REQUIRED_NOT_SET
        marg = requires_one_of
    elif requires_one_of == present_keys:
        rc,msg = REQUIRED_MUTEX
        marg = present_keys
    else:
        rc,msg = REQUIRED_VALID
    
    if not rc:
        errors.append(msg.format(", ".join(marg)))
    
    return rc,errors

def exists(module):
    try:
        module.client.get(existing_url(module))
        return True
    except a10_ex.NotFound:
        return False

def create(module, result):
    payload = build_json("logging", module)
    try:
        post_result = module.client.post(new_url(module), payload)
        result.update(**post_result)
        result["changed"] = True
    except a10_ex.Exists:
        result["changed"] = False
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def delete(module, result):
    try:
        module.client.delete(existing_url(module))
        result["changed"] = True
    except a10_ex.NotFound:
        result["changed"] = False
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def update(module, result):
    payload = build_json("logging", module)
    try:
        post_result = module.client.put(existing_url(module), payload)
        result.update(**post_result)
        result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def present(module, result):
    if not exists(module):
        return create(module, result)
    else:
        return update(module, result)

def absent(module, result):
    return delete(module, result)

def run_command(module):
    run_errors = []

    result = dict(
        changed=False,
        original_message="",
        message=""
    )

    state = module.params["state"]
    a10_host = module.params["a10_host"]
    a10_username = module.params["a10_username"]
    a10_password = module.params["a10_password"]
    # TODO(remove hardcoded port #)
    a10_port = 443
    a10_protocol = "https"

    valid = True

    if state == 'present':
        valid, validation_errors = validate(module.params)
        map(run_errors.append, validation_errors)
    
    if not valid:
        result["messages"] = "Validation failure"
        err_msg = "\n".join(run_errors)
        module.fail_json(msg=err_msg, **result)

    module.client = client_factory(a10_host, a10_port, a10_protocol, a10_username, a10_password)

    if state == 'present':
        result = present(module, result)
    elif state == 'absent':
        result = absent(module, result)
    return result

def main():
    module = AnsibleModule(argument_spec=get_argspec())
    result = run_command(module)
    module.exit_json(**result)

# standard ansible module imports
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == '__main__':
    main()