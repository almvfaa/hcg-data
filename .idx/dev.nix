{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-23.11"; # or "unstable"

  # The welcome message when you open the environment.
  welcomeMessage = ''
    This is the development environment for the inventory system.
    The following services will be started automatically:
    - Backend API on http://localhost:8000
    - Frontend Next.js app on http://localhost:3000
    - PostgreSQL database
  '';

  # Packages to make available in the environment.
  packages = [
    pkgs.python311
    pkgs.nodejs_20
    pkgs.nodePackages.npm
    pkgs.postgresql
  ];

  # Environment variables to set.
  env = {
    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/inventario_db";
  };

  # Scripts to run when the environment is created.
  pre-install = ''
    echo "Installing backend dependencies..."
    pip install -r backend/requirements.txt

    echo "Installing frontend dependencies..."
    npm install --prefix frontend
  '';

  # Scripts to run when you start a workspace.
  start-up = ''
    # Wait for PostgreSQL to be ready
    while ! pg_isready -q -h localhost -p 5432 -U postgres; do
      echo "Waiting for database to start..."
      sleep 1
    done

    echo "Database started. Applying schema..."
    psql $DATABASE_URL -f schema.sql
  '';

  # Services to run.
  services.postgres = {
    enable = true;
    package = pkgs.postgresql;
    initialDatabases = [{
      name = "inventario_db";
      owner = "postgres";
    }];
    initialUser = "postgres";
  };

  # Ports to expose from the environment.
  ports = [3000 8000];

  # Previews for your apps.
  idx.previews = {
    enable = true;
    previews = [
      {
        id = "frontend";
        port = 3000;
        label = "Frontend";
        command = "npm run dev --prefix frontend";
      }
      {
        id = "backend";
        port = 8000;
        label = "Backend API";
        command = "uvicorn backend.main:app --host 0.0.0.0 --port 8000";
      }
    ];
  };

  # VSCode extensions to install.
  extensions = [
    "ms-python.python"
    "esbenp.prettier-vscode"
    "dbaeumer.vscode-eslint"
    "bradlc.vscode-tailwindcss"
    "mtxr.sqltools"
    "mtxr.sqltools-driver-pg"
    "dsznajder.es7-react-js-snippets"
    "ms-python.debugpy"
    "Codeium.windsurfPyright"
    "ecmel.vscode-html-css"
    "GitHub.vscode-pull-request-github"
    "google.geminicodeassist"
    "ms-toolsai.jupyter"
    "ms-toolsai.jupyter-keymap"
    "ms-toolsai.jupyter-renderers"
    "ms-toolsai.vscode-jupyter-cell-tags"
    "ms-toolsai.vscode-jupyter-slideshow"
    "ms-vscode.js-debug"
    "ms-vscode.node-debug2"
    "msjsdiag.vscode-react-native"
    "Prisma.prisma-insider"
    "react-native-directory.vscode-react-native-directory"
    "redhat.java"
    "Tomi.xajssnippets"
    "vscjava.vscode-gradle"
    "vscjava.vscode-java-debug"
    "vscjava.vscode-java-dependency"
    "vscjava.vscode-java-pack"
    "vscjava.vscode-java-test"
    "vscjava.vscode-maven"
    "Vue.volar"
  ];
}
