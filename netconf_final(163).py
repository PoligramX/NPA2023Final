from ncclient import manager
import xmltodict
import re

m = manager.connect(
    host="10.0.15.189",
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )

def create():
   netconf_config = """
   <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
   <interface>
       <name>loopback{student_id}</name>
       <description>Loopback interface for student {student_id}</description>
       <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
       <enabled>true</enabled>
       <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
           <address>
               <ip>172.30.{last_3_digits}.1</ip>
               <netmask>255.255.255.0</netmask>
           </address>
       </ipv4>
    </interface>
    </interfaces>
    """

   try:
       match = re.match(r"/(\d+) create", command)
       if match:
           student_id = match.group(1)
           last_3_digits = student_id[-3:]

           netconf_get_reply = netconf_get_config(source="running", filter=f"<filter><interfaces><interface><name>loopback{student_id}</name></interface></interfaces></filter>")
           if f"<name>loopback{student_id}</name>" in netconf_get_reply.xml:
               message = f"Cannot create: Interface loopback{student_id}"
           else:
               netconf_config = netconf_config.format(student_id=student_id, last_3_digits=last_3_digits)
               netconf_reply = netconf_edit_config(netconf_config)
               if '<ok/>' in netconf_reply.xml:
                   message = f"Interface loopback{student_id} is created successfully"

        #    send_message_to_webex_team_room(message)
       else:
           print("Error: Invalid command format")
   except Exception as e:
       print(f"Error: {e}")

def delete():
    try:
       match = re.match(r"/(\d+) delete", command)
       if match:
           student_id = match.group(1)

           netconf_get_reply = netconf_get_config(source="running", filter=f"<filter><interfaces><interface><name>loopback{student_id}</name></interface></interfaces></filter>")
           if f"<name>loopback{student_id}</name>" in netconf_get_reply.xml:
               netconf_config = f"<interfaces xmlns='urn:ietf:params:xml:ns:yang:ietf-interfaces'><interface operation='delete'><name>loopback{student_id}</name></interface></interfaces>"
               netconf_reply = netconf_edit_config(netconf_config)
               if '<ok/>' in netconf_reply.xml:
                   message = f"Interface loopback{student_id} is deleted successfully"
           else:
               message = f"Cannot delete: Interface loopback{student_id}"

        #    send_message_to_webex_team_room(message)
       else:
           print("Error: Invalid command format")
    except Exception as e:
        print(f"Error: {e}")


def enable():
    netconf_config = """
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
        <name>loopback{student_id}</name>
        <enabled>true</enabled>
    </interface>
    </interfaces>
    """

    try:
        match = re.match(r"/(\d+) enable", command)
        if match:
           student_id = match.group(1)

        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)

        if '<ok/>' in xml_data:
            return f"Interface loopback{student_id} is enabled successfully"
    except:
        print("Error!")


def disable():
    netconf_config = """
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
        <name>loopback{student_id}</name>
        <enabled>false</enabled>
    </interface>
    </interfaces>
    """

    try:
        match = re.match(r"/(\d+) enable", command)
        if match:
           student_id = match.group(1)
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070123 is shutdowned successfully"
    except:
        print("Error!")

def netconf_edit_config(netconf_config):
   return m.edit_config(target="running", config=netconf_config)

def status():
    netconf_filter = """
    <filter>
    <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>loopback{student_id}</name>
    </interface>
    </interfaces-state>
    </filter>
    """

    try:
        match = re.match(r"/(\d+) enable", command)
        if match:
           student_id = match.group(1)
        netconf_filter = netconf_filter.format(student_id=student_id)
        netconf_reply = m.get(filter=netconf_filter)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)
        if netconf_reply_dict['nc:rpc-reply']['nc:data']:
            admin_status = netconf_reply_dict['nc:rpc-reply']['nc:data']['interfaces-state']['interface']['admin-status']
            oper_status = netconf_reply_dict['nc:rpc-reply']['nc:data']['interfaces-state']['interface']['oper-status']
            if admin_status == 'up' and oper_status == 'up':
                return f"Interface loopback{student_id} is enabled"
            elif admin_status == 'down' and oper_status == 'down':
                return f"Interface loopback{student_id} is disabled"
        else:
            return f"No Interface loopback{student_id}"
    except:
        print("Error!")