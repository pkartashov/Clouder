import unittest
from pprint import pprint
import api
import dataio

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.storage.types import Provider

class Clouder:

    cls = get_driver(Provider.RACKSPACE)
    driver = cls('my username', 'my api key')

    pprint(driver.list_sizes())
    pprint(driver.list_nodes())

    decider= None

    def pick_cloud (decider):

        return decider


    def download_files ():

        monkey.patch_all()

        def __new__(cls, *args, **kwargs):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

        def __init__(self, api_version):
            if api_version != "" and api_version != None:
                self.api_version = api_version

        USERNAME = "username"
        API_KEY = "api key"

        cls = get_driver(Provider.CLOUDFILES_US)
        driver = cls(USERNAME, API_KEY)

        def download_obj(container, obj):
            driver = cls(USERNAME, API_KEY)
            obj = driver.get_object(container_name=container.name, object_name=obj.name)
            filename = os.path.basename(obj.name)
            path = os.path.join(os.path.expanduser("~/Downloads"), filename)
            print("Downloading: %s to %s" % (obj.name, path))
            obj.download(destination_path=path)

        containers = driver.list_containers()

        jobs = []
        pool = Pool(20)

        for index, container in enumerate(containers):
            objects = container.list_objects()

            for obj in objects:
                pool.spawn(download_obj, container, obj)

        pool.join()


    def obtain_all_testable_nodes ():

            EC2_ACCESS_ID = "your access id"
            EC2_SECRET_KEY = "your secret key"
            RACKSPACE_USER = "your username"
            RACKSPACE_KEY = "your key"

            EC2Driver = get_driver(Provider.EC2)
            RackspaceDriver = get_driver(Provider.RACKSPACE)

            drivers = [
                EC2Driver(EC2_ACCESS_ID, EC2_SECRET_KEY),
                RackspaceDriver(RACKSPACE_USER, RACKSPACE_KEY),
            ]

            nodes = []
            for driver in drivers:
                nodes += driver.list_nodes()
            print(nodes)
            # [ <Node: provider=Amazon, status=RUNNING, name=bob, ip=1.2.3.4.5>,
            #   <Node: provider=Rackspace, status=REBOOT, name=korine, ip=6.7.8.9>, ... ]

            # Reboot all nodes named 'test'
            [node.reboot() for node in nodes if node.name == "test"]




    def test_AWS_load_balaer (ACCESS_ID,  SECRET_KEY):
        cls = get_driver(Provider.ELB)
        driver = cls(key=ACCESS_ID, secret=SECRET_KEY)

        print(driver.list_balancers())

        # members associated with the load balancer
        members = (Member(None, "192.168.88.1", 8000), Member(None, "192.168.88.2", 8080))
        # creates a new balancer named 'MyLB'
        new_balancer = driver.create_balancer(
            name="MyLB",
            algorithm=Algorithm.ROUND_ROBIN,
            port=80,
            protocol="http",
            members=members,
        )
        print(new_balancer)

        # create load balancer policy
        print(
            driver.ex_create_balancer_policy(
                name="MyLB",
                policy_name="EnableProxyProtocol",
                policy_type="ProxyProtocolPolicyType",
                policy_attributes={"ProxyProtocol": "true"},
            )
        )

        # delete load balancer policy
        print(
            driver.ex_delete_balancer_policy(name="MyLB", policy_name="EnableProxyProtocol")
        )

        # set load balancer policies for backend server
        print(
            driver.ex_set_balancer_policies_backend_server(
                name="MyLB", port=80, policies=["MyDurationStickyPolicy"]
            )
        )

        # create the listeners for the balancers
        uid = "arn:aws:iam::123456789012:server-certificate/servercert"
        print(
            driver.ex_create_balancer_listeners(
                name="MyLB", listeners=[[1024, 65533, "HTTPS", uid]]
            )
        )

        # set the listeners policies for the balancers
        print(
            driver.ex_set_balancer_policies_listener(
                name="MyLB", port=80, policies=["MyDurationStickyPolicy"]
            )
        )

    @staticmethod
    def test_GCP_load_balaer():
            start_time = datetime.datetime.now()
            display("Load-balancer demo/test start time: %s" % str(start_time))
            gce = get_gce_driver()
            gcelb = get_gcelb_driver(gce)

            # Get project info and print name
            project = gce.ex_get_project()
            display("Project: %s" % project.name)

            # Existing Balancers
            balancers = gcelb.list_balancers()
            display("Load Balancers", balancers)

            # Protocols
            protocols = gcelb.list_protocols()
            display("Protocols", protocols)

            # Healthchecks
            healthchecks = gcelb.ex_list_healthchecks()
            display("Health Checks", healthchecks)

            # This demo is based on the GCE Load Balancing Quickstart described here:
            # https://developers.google.com/compute/docs/load-balancing/lb-quickstart

            # == Clean-up and existing demo resources ==
            all_nodes = gce.list_nodes(ex_zone="all")
            firewalls = gce.ex_list_firewalls()
            display('Cleaning up any "%s" resources' % DEMO_BASE_NAME)
            clean_up(gce, DEMO_BASE_NAME, all_nodes, balancers + healthchecks + firewalls)

            # == Create 3 nodes to balance between ==
            startup_script = (
                "apt-get -y update && " "apt-get -y install apache2 && " "hostname > /var/www/index.html"
            )
            tag = "%s-www" % DEMO_BASE_NAME
            base_name = "%s-www" % DEMO_BASE_NAME
            image = gce.ex_get_image("debian-7")
            size = gce.ex_get_size("n1-standard-1")
            number = 3
            display("Creating %d nodes" % number)
            metadata = {"items": [{"key": "startup-script", "value": startup_script}]}
            lb_nodes = gce.ex_create_multiple_nodes(
                base_name,
                size,
                image,
                number,
                ex_tags=[tag],
                ex_metadata=metadata,
                ex_disk_auto_delete=True,
                ignore_errors=False,
            )
            display("Created Nodes", lb_nodes)

            # == Create a Firewall for instances ==
            display("Creating a Firewall")
            name = "%s-firewall" % DEMO_BASE_NAME
            allowed = [{"IPProtocol": "tcp", "ports": ["80"]}]
            firewall = gce.ex_create_firewall(name, allowed, target_tags=[tag])
            display("    Firewall %s created" % firewall.name)

            # == Create a Health Check ==
            display("Creating a HealthCheck")
            name = "%s-healthcheck" % DEMO_BASE_NAME

            # These are all the default values, but listed here as an example.  To
            # create a healthcheck with the defaults, only name is required.
            hc = gcelb.ex_create_healthcheck(
                name,
                host=None,
                path="/",
                port="80",
                interval=5,
                timeout=5,
                unhealthy_threshold=2,
                healthy_threshold=2,
            )
            display("Healthcheck %s created" % hc.name)

            # == Create Load Balancer ==
            display("Creating Load Balancer")
            name = "%s-lb" % DEMO_BASE_NAME
            port = 80
            protocol = "tcp"
            algorithm = None
            members = lb_nodes[:2]  # Only attach the first two initially
            healthchecks = [hc]
            balancer = gcelb.create_balancer(
                name, port, protocol, algorithm, members, ex_healthchecks=healthchecks
            )
            display("    Load Balancer %s created" % balancer.name)

            # == Attach third Node ==
            display("Attaching additional node to Load Balancer")
            member = balancer.attach_compute_node(lb_nodes[2])
            display("      Attached {} to {}".format(member.id, balancer.name))

            # == Show Balancer Members ==
            members = balancer.list_members()
            display("Load Balancer Members")
            for member in members:
                display("      ID: {} IP: {}".format(member.id, member.ip))

            # == Remove a Member ==
            display("Removing a Member")
            detached = members[0]
            detach = balancer.detach_member(detached)
            if detach:
                display("      Member {} detached from {}".format(detached.id, balancer.name))

            # == Show Updated Balancer Members ==
            members = balancer.list_members()
            display("Updated Load Balancer Members")
            for member in members:
                display("      ID: {} IP: {}".format(member.id, member.ip))

            # == Reattach Member ==
            display("Reattaching Member")
            member = balancer.attach_member(detached)
            display("      Member {} attached to {}".format(member.id, balancer.name))

            # == Test Load Balancer by connecting to it multiple times ==
            PAUSE = 60
            display("Sleeping for %d seconds for LB members to serve..." % PAUSE)
            time.sleep(PAUSE)
            rounds = 200
            url = "http://%s/" % balancer.ip
            line_length = 75
            display("Connecting to {} {} times".format(url, rounds))
            for x in range(rounds):
                response = url_req.urlopen(url)
                output = str(response.read(), encoding="utf-8").strip()
                if "www-001" in output:
                    padded_output = output.center(line_length)
                elif "www-002" in output:
                    padded_output = output.rjust(line_length)
                else:
                    padded_output = output.ljust(line_length)
                sys.stdout.write("\r%s" % padded_output)
                sys.stdout.flush()
                time.sleep(0.25)

            print("")
            if CLEANUP:
                balancers = gcelb.list_balancers()
                healthchecks = gcelb.ex_list_healthchecks()
                nodes = gce.list_nodes(ex_zone="all")
                firewalls = gce.ex_list_firewalls()

                display("Cleaning up %s resources created" % DEMO_BASE_NAME)
                clean_up(gce, DEMO_BASE_NAME, nodes, balancers + healthchecks + firewalls)

            end_time = datetime.datetime.now()
            display("Total runtime: %s" % str(end_time - start_time))

gem = Clouder
DR = gem.driver

class SuiteBuilder:

    @staticmethod
    def _build ():
        return ("build")

    @staticmethod
    def deploy ():
        return ("deploy")

    @staticmethod
    def _run ():
        return ("run")

    @staticmethod
    def _ignore ():
        return ("ignore")

    @staticmethod
    def _retry ():
        return ("retry")

    @staticmethod
    def _pause ():
        return ("pause")

    @staticmethod
    def _restart_override ():
        return ("restart_overrid")

    @staticmethod
    def _restart_append ():
        return ("restart_append")

    @unittest.TestSuite

    def PrepData (file, sheet):
        dt = dataio.get_test_data_arr(file, sheet, 0)
        unittest.TestResult ="ds"
        return dt


