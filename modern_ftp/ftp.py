from pyftpdlib.servers import FTPServer as pyftpdlibFTPServer
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.filesystems import AbstractedFS

from pathlib import Path
import s3fs

class S3FileSystem(AbstractedFS):
    def __init__(self, root: str, handler: FTPHandler):
        super().__init__(root, handler)
        self._cwd = '/'
        self._root = root
        self.cmd_channel = handler
        # this module use aiobotocore (with asyncio) which fail everything.
        self.s3 = s3fs.S3FileSystem(anon=False)
        self.bucket_name = handler.username

    def open(self, filename, mode):
        return self.s3.open(f"{self.bucket_name}/{filename}", mode)

    def chdir(self, path):
        self.cwd = self.fs2ftp(path)

    def mkdir(self, path):
        self.s3.mkdir(f"{self.bucket_name}/{path}")

    def listdir(self, path):
        return self.s3.ls(f"{self.bucket_name}/{path}")

    def listdirinfo(self, path):
        return self.s3.ls(f"{self.bucket_name}/{path}")

    def rmdir(self, path):
        self.s3.rm(f"{self.bucket_name}/{path}")

    def remove(self, path):
        self.s3.rm(f"{self.bucket_name}/{path}")

    def rename(self, src, dst):
        self.s3.mv(f"{self.bucket_name}/{src}", f"{self.bucket_name}/{dst}")


class S3BackedFTPHandler(FTPHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.banner = "S3 backed FTP, because fuck yeah"
        self.abstracted_fs = S3FileSystem
        #TODO
        #self.authorizer = DbAuthorizer()

    def on_connect(self):
        print(f"ip {self.remote_ip}:{self.remote_port} connected")

    def on_disconnect(self):
        print(f"ip {self.remote_ip}:{self.remote_port} disconnected")

    def on_login(self, username):
        print(f"User: {username} from ip {self.remote_ip}:{self.remote_port} logged")

    def on_logout(self, username):
        print(f"User: {username} from ip {self.remote_ip}:{self.remote_port} unlogged")

    def on_file_sent(self, file):
        # do something when a file has been sent
        pass

    def on_file_received(self, file):
        # do something when a file has been received
        pass

    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        pass

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        Path.unlink(file)


class FTPServer:
    def __init__(self, address: str= "0.0.0.0", port: int = 23) -> None:
        self.port = port
        self.handler = S3BackedFTPHandler
        authorizer = DummyAuthorizer()
        authorizer.add_anonymous("/tmp/test")
        self.handler.authorizer = authorizer
        self.server = pyftpdlibFTPServer((address, port), self.handler)

    def serve(self) -> None:
        self.server.serve_forever()


