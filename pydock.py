import os
import tarfile
import docker

class DockerManager:

    def __init__(self):
        self.client = docker.from_env() 

    def execute(self):
        try:
            ls = self.client.containers.list(True)
            for c in ls:
                print("id:{}, name:{}".format(c.id, c.name))
        except:
            print("Docker execute error!")
    
    def run_node(self, id):
        pass

    def copy(self, src, dst):
        name, dst = dst.split(':')
        container = self.client.containers.get(name)
        os.chdir(os.path.dirname(src))
        srcname = os.path.basename(src)
        tar = tarfile.open(src + '.tar', mode='w')
        try:
            tar.add(srcname)
        finally:
            tar.close()
        data = open(src + '.tar', 'rb').read()
        container.put_archive(os.path.dirname(dst), data)


def main():
    docker = DockerManager()
    docker.execute()

if __name__ == "__main__":
    main()