from logging import getLogger, getLevelName, Formatter, StreamHandler
from dataclasses import dataclass
from tarfile import TarFile

import subprocess
import traceback
import requests
from requests_toolbelt import MultipartEncoder
import tempfile
import termios
import select
import socket
import json
import time
import tty
import sys
import shutil
import re
import os

from .message import MessageType, Message, JobIOMessage, JobStatus


logger = getLogger(__name__)
logger.setLevel(getLevelName('DEBUG'))
log_formatter = \
    Formatter("%(asctime)s [%(levelname)s] %(funcName)s: "
              "%(message)s [%(threadName)s] ")
console_handler = StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)


def section_start(section_name: str, title: str, collapsed: bool = True) -> None:
    collapsed_cmd = "[collapsed=true]" if collapsed else ""
    print(f"\n\r\033[0Ksection_start:{int(time.time())}:{section_name}{collapsed_cmd}\r\033[0K{title}",
          flush=True)


def section_end(section_name: str) -> None:
    print(f"\n\r\033[0Ksection_end:{int(time.time())}:{section_name}\r\033[0K", flush=True)


def indent(v, indent):
    return "\n".join([indent * " " + line for line in v.splitlines()])


@dataclass
class Response:
    version: int = 0
    error_msg: str = None


class Job:
    def __init__(self, executor_url, job_desc, wait_if_busy=False, callback_host=None,
                 machine_tags=None, machine_id=None, job_id=None, share_directory=None,
                 minio_creds=None, minio_groups=None):
        self.executor_url = executor_url
        self.job_desc = job_desc
        self.wait_if_busy = wait_if_busy
        self.callback_host = callback_host

        self.machine_tags = machine_tags
        self.machine_id = machine_id
        self.job_id = job_id
        self.share_directory = share_directory
        self.minio_creds = minio_creds
        self.minio_groups = minio_groups if minio_groups is not None else []

    def _create_archive(self):
        start = time.monotonic()
        with (tempfile.NamedTemporaryFile(mode='wb', suffix='tar', delete=False) as fp,
              TarFile.open(fileobj=fp, mode='w') as tar):
            tar.add(self.share_directory, arcname="")
            return fp.name, time.monotonic() - start

    def _parse_response(self, r):
        try:
            ret = r.json()
        except Exception:
            return Response(error_msg=r.text)

        version = ret.get("version", None)

        if version is None:
            return Response(error_msg=ret.get("error"))
        elif version == 0:
            return Response(error_msg=ret.get("reason"))
        elif version == 1:
            return Response(**ret)
        else:
            raise ValueError(f"Unsupported response version {version}")

    def _setup_connection(self):
        def queue_job():
            first_wait = True
            corrupted_tarball_attempts_count = 5

            while True:
                fields = {
                    'metadata': ('metadata', json.dumps(metadata), 'application/json'),
                    'job': ('job', self.job_desc, 'application/x-yaml')
                }

                start_job_file_archive = None
                try:
                    # If we have a share directory, add it to the fields
                    if start_job_file_archive_path:
                        start_job_file_archive = open(start_job_file_archive_path, 'rb')
                        fields['job_bucket_initial_state_tarball_file'] = ('job_bucket_initial_state_tarball_file',
                                                                           start_job_file_archive,
                                                                           'application/octet-stream')

                    m = MultipartEncoder(fields=fields)
                    r = requests.post(f"{self.executor_url}/api/v1/jobs", data=m,
                                      headers={'Content-Type': m.content_type})
                finally:
                    if start_job_file_archive:
                        start_job_file_archive.close()

                response = self._parse_response(r)

                if r.status_code == 200:
                    return True, response
                elif r.status_code == 409 and self.wait_if_busy:
                    if first_wait:
                        print("No machines available for the job, waiting: ", end="", flush=True)
                        first_wait = False
                    else:
                        print(".", end="", flush=True)
                    time.sleep(1)
                elif r.status_code == 420:
                    corrupted_tarball_attempts_count -= 1

                    if corrupted_tarball_attempts_count > 0:
                        count = corrupted_tarball_attempts_count
                        print(f"WARNING: The tarball got corrupted in transit, trying again up to {count} times!")
                        time.sleep(1)
                    else:
                        print("ERROR: The share directory's tarball can't be transmitted correctly")
                        return False, response
                else:
                    error = indent(response.error_msg, 4)
                    print(f"\nERROR: Could not queue the job. Reason:\n\n{error}\n", file=sys.stderr)

                    return False, response

        # Set up a TCP server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_server:
            tcp_server.bind(('', 0))
            tcp_server.listen(1)
            local_port = tcp_server.getsockname()[1]

            # Queue the job
            metadata = {
                "version": 1,
                "job_id": self.job_id,
                "minio": {
                    "credentials": {},
                    "groups": self.minio_groups
                },
                "callback": {
                    "port": local_port
                }
            }
            if self.callback_host is not None:
                metadata['callback']['host'] = self.callback_host

            if self.minio_creds is not None:
                metadata['minio']['credentials'] = {
                    "access_key": self.minio_creds.access_key,
                    "secret_key": self.minio_creds.secret_key
                }

            if self.machine_id is not None or (self.machine_tags is not None and len(self.machine_tags) > 0):
                metadata['target'] = {
                    "id": self.machine_id,
                    "tags": self.machine_tags
                }

            start_job_file_archive_path = None
            try:
                if self.share_directory:
                    print("Packing up the share_directory")
                    start_job_file_archive_path, exec_time = self._create_archive()
                    archive_stats = os.stat(start_job_file_archive_path)
                    print(f"--> Wrote {archive_stats.st_size} bytes into tar archive in {exec_time:.2}s...")

                success, response = queue_job()
                if not success:
                    return None, response
            finally:
                if start_job_file_archive_path is not None:
                    os.unlink(start_job_file_archive_path)

            # We should not have a connection queued, accept it with a timeout
            print(f"Waiting for the executor to connect to our local port {local_port}")
            tcp_server.settimeout(15)
            try:
                wait_start = time.monotonic()
                sock, _ = tcp_server.accept()
                wait_time = time.monotonic() - wait_start
                print(f"Connection established after {wait_time:.3f} s: Switch to proxy mode")
            except socket.timeout:
                raise ValueError("The server failed to initiate a connection")

            # Set the resulting socket's timeout to blocking
            sock.settimeout(None)

        return sock, response

    def _read_executor_message_v0(self, job_socket):
        # Local cache
        final_lines = getattr(self, "final_lines", None)
        if final_lines is None:
            self.final_lines = final_lines = bytearray()

        # Get the data
        buf = job_socket.recv(4096)
        if len(buf) == 0:
            # The job is over, check the job status!
            try:
                m = re.search(b'<-- End of the session: (?P<status>\\w+) -->', final_lines)
                if m is not None:
                    status_str = m.groupdict({}).get("status", b'UNKNOWN').decode()
                    return JobStatus.from_str(status_str)
            except Exception:
                traceback.print_exc()

        sys.stdout.buffer.write(buf)
        sys.stdout.buffer.flush()

        # Keep in memory the final lines, for later parsing
        final_lines += buf
        final_lines = final_lines[-100:]

        return None

    def _handle_end_message(self, session_end_msg):
        if session_end_msg.job_bucket and self.share_directory:
            try:
                section_start("executorctl_mcli_dl", "Downloading the job bucket")

                bucket = session_end_msg.job_bucket
                os.environ['MC_HOST_client'] = bucket.minio_access_url

                for i in range(3):
                    try:
                        subprocess.check_call(["mcli", "--no-color", "mirror",
                                               "--overwrite", "--remove", f'client/{bucket.bucket_name}',
                                               self.share_directory])
                        # Success \o/
                        return
                    except subprocess.CalledProcessError:
                        # We had a failure... try again after sleeping
                        time.sleep(2 ** (i + 1))
                        continue

                print("WARNING: Repeatedly failed to download the job bucket, some job files may be missing")
            finally:
                section_end("executorctl_mcli_dl")

    def _read_executor_message_v1(self, job_socket):
        try:
            msg = Message.next_message(job_socket)

            # TODO: Only display control messages at the end of a new line
            if msg.msg_type == MessageType.CONTROL:
                print(msg.message, flush=True, end="")
            elif msg.msg_type == MessageType.JOB_IO:
                sys.stdout.buffer.write(msg.buffer)
                sys.stdout.buffer.flush()
            elif msg.msg_type == MessageType.SESSION_END:
                self._handle_end_message(msg)
                return msg.status
        except Exception:
            traceback.print_exc()
            return JobStatus.INCOMPLETE

        return None

    def _forward_inputs_and_outputs(self, job_socket, job_response):
        # Set stdin to the raw input mode
        if sys.stdin.isatty():
            old_tty_attrs = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin)

        control_char = b'\x01'  # CTRL+A
        control_char_pressed = False

        try:
            while True:
                try:
                    readables = [job_socket]
                    if sys.stdin.isatty():
                        readables.append(sys.stdin)
                    r_fds, w_fds, x_fds = select.select(readables, [], [])

                    for fd in r_fds:
                        if fd is sys.stdin:
                            buf = os.read(sys.stdin.fileno(), 1)
                            msg = JobIOMessage.create(buf)
                            if buf == control_char:
                                if control_char_pressed:
                                    # Repeating the control char sends it through
                                    msg.send(job_socket)
                                else:
                                    control_char_pressed = True
                            else:
                                control_char_pressed = False
                                msg.send(job_socket)
                        elif fd is job_socket:
                            if job_response.version == 0:
                                ret = self._read_executor_message_v0(job_socket)
                            else:
                                ret = self._read_executor_message_v1(job_socket)

                            if ret:
                                return ret
                        else:
                            raise ValueError(f"Received an unexpected fd: {fd}")
                except KeyboardInterrupt:
                    if control_char_pressed:
                        logger.info("Exiting the client in response to CTRL+C...")
                        return JobStatus.INCOMPLETE

                    logger.info("forwarding CTRL+C to job, type CTRL+A followed by CTRL+C to quit the client")
                    msg = JobIOMessage.create(chr(3).encode())
                    msg.send(job_socket)
        finally:
            if sys.stdin.isatty():
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty_attrs)

    def close(self, sock):
        try:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
        except OSError:
            pass

    def run(self):
        sock = None

        try:
            sock, response = self._setup_connection()
            if sock is None:
                return JobStatus.SETUP_FAIL

            if response.version != 0 and shutil.which('mcli') is None:
                logger.error("The MinIO client is needed to run the job. "
                             "You may want to install it locally from "
                             "https://github.com/minio/mc")
                return JobStatus.SETUP_FAIL

            status = self._forward_inputs_and_outputs(sock, response)
        except json.decoder.JSONDecodeError:
            logger.error("Invalid response from executor server")
            status = JobStatus.SETUP_FAIL
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to the executor, is it running?")
            status = JobStatus.SETUP_FAIL
        except Exception:
            traceback.print_exc()
            status = JobStatus.UNKNOWN
        finally:
            if sock is not None:
                self.close(sock)

        return status

    @classmethod
    def from_file(cls, executor_url, path, wait_if_busy=False,
                  callback_host=None, machine_tags=None, machine_id=None,
                  share_directory=None, job_id=None,
                  minio_creds=None, minio_groups=None):
        with open(path) as f:
            job_desc = f.read()

        return cls(executor_url, job_desc, wait_if_busy=wait_if_busy,
                   callback_host=callback_host, machine_tags=machine_tags,
                   machine_id=machine_id, share_directory=share_directory,
                   job_id=job_id, minio_creds=minio_creds,
                   minio_groups=minio_groups)
