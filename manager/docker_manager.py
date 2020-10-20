import docker


class DockerManager:
    def __init__(self, conf):
        self.conf = conf
        self.client = docker.from_env()
        # if self.conf.image not in self.client.images.list():
        #     self.client.images.build(
        #         path=self.conf.build_context,
        #         tag=self.conf.image
        #     )

    def run(self, envs):
        for key, value in envs.items():
            self.conf.environment.append(key + "=" + value)
        self.client.containers.run(
            image=self.conf.image,
            command=self.conf.command,
            runtime=self.conf.runtime,
            environment=self.conf.environment,
            volumes=self.conf.volumes,
        )
