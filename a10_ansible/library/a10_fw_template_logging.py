#!/usr/bin/python
REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")

DOCUMENTATION = """
module: a10_logging
description:
    - 
author: A10 Networks 2018 
version_added: 1.8

options:
    
    name:
        description:
            - Logging Template Name
    
    resolution:
        description:
            - 'seconds': Logging timestamp resolution in seconds (default); '10-milliseconds': Logging timestamp resolution in 10s of milli-seconds; choices:['seconds', '10-milliseconds']
    
    log:
        
    
    include-radius-attribute:
        
    
    include-http:
        
    
    rule:
        
    
    facility:
        description:
            - 'kernel': 0: Kernel; 'user': 1: User-level; 'mail': 2: Mail; 'daemon': 3: System daemons; 'security-authorization': 4: Security/authorization; 'syslog': 5: Syslog internal; 'line-printer': 6: Line printer; 'news': 7: Network news; 'uucp': 8: UUCP subsystem; 'cron': 9: Time-related; 'security-authorization-private': 10: Private security/authorization; 'ftp': 11: FTP; 'ntp': 12: NTP; 'audit': 13: Audit; 'alert': 14: Alert; 'clock': 15: Clock-related; 'local0': 16: Local use 0; 'local1': 17: Local use 1; 'local2': 18: Local use 2; 'local3': 19: Local use 3; 'local4': 20: Local use 4; 'local5': 21: Local use 5; 'local6': 22: Local use 6; 'local7': 23: Local use 7; choices:['kernel', 'user', 'mail', 'daemon', 'security-authorization', 'syslog', 'line-printer', 'news', 'uucp', 'cron', 'security-authorization-private', 'ftp', 'ntp', 'audit', 'alert', 'clock', 'local0', 'local1', 'local2', 'local3', 'local4', 'local5', 'local6', 'local7']
    
    severity:
        description:
            - 'emergency': 0: Emergency; 'alert': 1: Alert; 'critical': 2: Critical; 'error': 3: Error; 'warning': 4: Warning; 'notice': 5: Notice; 'informational': 6: Informational; 'debug': 7: Debug; choices:['emergency', 'alert', 'critical', 'error', 'warning', 'notice', 'informational', 'debug']
    
    format:
        description:
            - 'ascii': A10 Text logging format (ASCII); 'cef': Common Event Format for logging (default); choices:['ascii', 'cef']
    
    service-group:
        description:
            - Bind a Service Group to the logging template (Service Group Name)
    
    uuid:
        description:
            - uuid of the object
    
    user-tag:
        description:
            - Customized tag
    
    source-address:
        
    

"""

EXAMPLES = """
"""

ANSIBLE_METADATA = """
"""

# Hacky way of having access to object properties for evaluation
AVAILABLE_PROPERTIES = {"facility","format","include_http","include_radius_attribute","log","name","resolution","rule","service_group","severity","source_address","user_tag","uuid",}

# our imports go at the top so we fail fast.
from a10_ansible.axapi_http import client_factory
from a10_ansible import errors as a10_ex

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
        
        facility=dict(
            type='enum' , choices=['kernel', 'user', 'mail', 'daemon', 'security-authorization', 'syslog', 'line-printer', 'news', 'uucp', 'cron', 'security-authorization-private', 'ftp', 'ntp', 'audit', 'alert', 'clock', 'local0', 'local1', 'local2', 'local3', 'local4', 'local5', 'local6', 'local7']
        ),
        format=dict(
            type='enum' , choices=['ascii', 'cef']
        ),
        include_http=dict(
            type='str' 
        ),
        include_radius_attribute=dict(
            type='str' 
        ),
        log=dict(
            type='str' 
        ),
        name=dict(
            type='str' , required=True
        ),
        resolution=dict(
            type='enum' , choices=['seconds', '10-milliseconds']
        ),
        rule=dict(
            type='str' 
        ),
        service_group=dict(
            type='str' 
        ),
        severity=dict(
            type='enum' , choices=['emergency', 'alert', 'critical', 'error', 'warning', 'notice', 'informational', 'debug']
        ),
        source_address=dict(
            type='str' 
        ),
        user_tag=dict(
            type='str' 
        ),
        uuid=dict(
            type='str' 
        ), 
    ))
    return rv

def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/fw/template/logging/{name}"
    f_dict = {}
    
    f_dict["name"] = ""

    return url_base.format(**f_dict)

def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/fw/template/logging/{name}"
    f_dict = {}
    
    f_dict["name"] = module.params["name"]

    return url_base.format(**f_dict)


def build_envelope(title, data):
    return {
        title: data
    }

def build_json(title, module):
    rv = {}
    for x in AVAILABLE_PROPERTIES:
        v = module.params.get(x)
        if v:
            rx = x.replace("_", "-")
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