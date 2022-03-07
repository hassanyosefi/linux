import subprocess
import unittest


class TestDockerLimits(unittest.TestCase):

    @staticmethod
    def iptables_reset():
        subprocess.run("iptables -w 10 -F", shell=True)

    @staticmethod
    def iptables_get_blocked_ips():
        comm = "iptables -w 10 -L INPUT -v -n | tail -n +3 | awk '{print $8}' | sort -u"
        proc = subprocess.run(comm, stdout=subprocess.PIPE, shell=True)
        output = proc.stdout
        output = output.decode()
        output = output.strip()
        return output

    def setUp(self):
        self.iptables_reset()

    def test_1(self):
        log_path = "nginx_logs_sample"
        n = 7
        comm = f"bash blocker.sh {log_path} {n}"
        subprocess.run(comm, shell=True)
        expected_blocked_ips = """119.252.76.162
129.67.24.6
130.199.3.165
137.117.180.46
137.117.183.81
137.117.184.211
137.117.184.219
148.251.112.153
148.251.23.199
173.255.243.139
174.103.128.249
178.62.213.239
180.179.174.219
185.20.227.198
186.67.186.2
192.133.141.142
193.84.27.10
200.28.3.2
200.28.3.3
209.177.145.225
216.46.173.126
217.168.17.5
50.57.209.100
54.144.73.8
54.165.189.135
54.172.110.13
54.172.164.189
54.173.226.7
54.194.93.59
54.213.131.92
54.244.94.5
54.77.28.244
54.84.191.5
5.63.153.125
5.63.157.73
65.39.197.164
72.32.152.84
74.125.60.158
80.91.33.133
84.208.15.12
85.21.237.138
89.191.68.234
94.236.106.132
94.242.57.74
94.242.58.153
94.242.58.216"""
        blocked_ips = self.iptables_get_blocked_ips()
        self.assertEqual(
            blocked_ips,
            expected_blocked_ips,
            f"\nTest with log_path: {log_path} & n: {n} ===>\n"
            f"\nblocked_ips:\n{blocked_ips}\n"
            f"\nexpected_blocked_ips:\n{expected_blocked_ips}"
        )
