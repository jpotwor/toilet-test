# toilet-test

A web application under development. The backend uses **Python 3.13** and **FastAPI**, running in Docker. A separate frontend container may be added later.

## Development prerequisites (Linux)

- Linux machine (developed on Ubuntu)
- [Git](https://git-scm.com/)
- [Docker Engine and Docker Compose plugin](https://docs.docker.com/engine/install/ubuntu/)
- [Visual Studio Code](https://code.visualstudio.com/)
- Recommended VS Code extensions: **Python**, **Pylance**, **Python Debugger**, **Dev Containers**, and **Docker**

Verify Docker is available to your user:

```bash
docker run --rm hello-world
docker compose version
```

> On Linux, access to the Docker daemon requires appropriate permissions. Adding a user to the `docker` group is convenient but effectively grants root-level access.

## Get started

1. Clone the repository (SSH URL shown; substitute your GitHub account):

   ```bash
   git clone git@github.com:YOUR_USERNAME/toilet-test.git
   cd toilet-test
   ```

2. Build and start the backend:

   ```bash
   docker compose up -d --build
   ```

3. Open the app:

   - API: http://localhost:8000/
   - Health check: http://localhost:8000/health
   - Interactive API docs: http://localhost:8000/docs

4. View logs or stop the backend:

   ```bash
   docker compose logs -f backend
   docker compose down
   ```

The repository is **bind-mounted** into the container at `/workspace`. Backend files are at `/workspace/backend`; changes to Python code are picked up by Uvicorn's development `--reload` mode.

## VS Code development workflow

Open the repository/workspace on your Linux host:

```bash
code toilet-test.code-workspace
```

The currently working workflow is to start the backend with Docker Compose and then use **Dev Containers: Attach to Running Container...** in VS Code. Select the `toilet-test` backend container and open `/workspace/toilet-test.code-workspace` (or the `/workspace` folder).

The regular **Reopen in Container** build flow previously failed with a Docker Buildx filesystem-permissions error; attaching to the already-running container is the known working workaround.

Inside the container, verify:

```bash
cd /workspace/backend
python --version
git --version
```

- `toilet-test.code-workspace`: VS Code workspace and recommended extensions
- `.vscode/launch.json`: Python debugging configurations
- `.devcontainer/devcontainer.json`: container development settings
- `compose.yaml`: services, bind mounts, ports and development command
- `backend/Dockerfile`: backend image definition (including Python and developer tools)
- `backend/requirements.txt`: backend Python dependencies

### Debugging

Docker Compose already starts Uvicorn on port **8000**. Starting a second Uvicorn debugger on the same port causes `Address already in use`.

To debug using a separate VS Code-launched server, configure `launch.json` to use another port (for example **8001**, without `--reload`) and publish that port in `compose.yaml`, then recreate the container. Open `http://localhost:8001/health` to hit a breakpoint in that process. **Port 8001 is not assumed to be enabled by default.**

## Git and GitHub authentication

Git commands can run on the Linux host, where your SSH key is already configured. The Git UI in a VS Code window attached to the container needs Git and working authentication **inside that container**.

Do **not** copy your private SSH key into the image, Git repository, or `.env` file. If container-side push/pull is needed, forward the Linux host's SSH agent socket into the container using Docker Compose. First check the agent on the host:

```bash
ssh-add -l
```

If you configure agent forwarding, remember that anyone with access to the forwarded socket can ask the agent to authenticate while it is available. You may need to recreate the container after logging out or restarting if the host socket path changes.

## Common commands

```bash
docker compose up -d --build   # Build and start
docker compose ps              # Container status
docker compose logs -f backend # Follow backend logs
docker compose down            # Stop and remove containers
```

Changes to the **Dockerfile** or installed Python packages require rebuilding the image. Changes to the Python application normally do not, thanks to the bind mount and auto-reload.

## License

[MIT License](LICENSE.md) — Copyright (c) 2026 Jan Potworowski.
