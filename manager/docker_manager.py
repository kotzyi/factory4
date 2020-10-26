import docker


class DockerManager:
    def __init__(self, conf):
        self.conf = conf
        self.client = docker.from_env()

    def run(self, envs):
        for key, value in envs.items():
            self.conf.environment.append(str(key) + "=" + str(value))
        self.client.containers.run(
            image=self.conf.image,
            command=self.conf.command,
            runtime=self.conf.runtime,
            environment=self.conf.environment,
            volumes=self.conf.volumes,
        )
