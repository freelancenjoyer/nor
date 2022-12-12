from datetime import datetime
from threading import Timer
from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result, print_title
from nornir_jinja2.plugins.tasks import template_file
from nornir_netmiko import netmiko_send_command, netmiko_send_config
import keyring

def get_access_ports(task):
    # This task runs the 'show interface switchport' command and makes it machine readable through TextFSM
    r = task.run(
        name = "Getting switchports",
        task = netmiko_send_command,
        command_string = "show interface switchport",
        use_textfsm = True
    )

    # Create an empty list called 'access_ports' for each host, so we can store our access ports in here
    task.host['access_ports'] = []
    # Loop through all interfaces gathered in the previous task, save access port information to the list
    for interface in r.result:
        if interface['admin_mode'] == "static access":
            task.host['access_ports'].append(dict(interface))
    # Print out all the access ports found for the host to make it more visual
    for access_port in task.host['access_ports']:
        print(task.host.name + ' Interface ' + access_port['interface'] + ' is access port')

def generate_config(task, j2path, j2template):
    r = task.run(
        name = "Generating configuration with jinja2 template",
        task = template_file,
        template = j2template,
        path = j2path
    )
    task.host["config"] = r.result

def push_config(task):
    task.run(
        name = "Push jinja2 generated configuration to host",
        task = netmiko_send_config,
        config_commands = task.host["config"].splitlines()
    )

def main1():
    # Set the environment variable so Python can find network-to-code templates folder
    #os.environ["NET_TEXTFSM"] = "ntc-templates/templates"
    # Init Nornir with our config file - You can follow it up with a filter
    nr = InitNornir(config_file="config.yaml")
    
    # Ask for our users password so we can access the hosts
    nr.inventory.defaults.username = "username"
    nr.inventory.defaults.password = "password"
    
    # Gather all access ports for our devices and print the result
    result_access = nr.run(task = get_access_ports)
    print_result(result_access, vars=["diff","exception"])

    # Generate the configuration for each host, whilst specifying our jinja2 folder and template
    result_gen_config = nr.run(task = generate_config, j2path= "templates/", j2template = "8021x_mon.j2")
    print_result(result_gen_config, vars=["diff","exception"])

    # Push the generated configuration to our hosts
    result_push_config = nr.run(task = push_config)
    print_result(result_push_config, vars=["diff","exception"])

#main1()


x=datetime.today()
y=x.replace(day=x.day+0, hour=16, minute=45, second=20, microsecond=0)
delta_t=y-x

secs=delta_t.seconds+1

def intime():
    main1()

t = Timer(secs, intime)
t.start()
t.join()
