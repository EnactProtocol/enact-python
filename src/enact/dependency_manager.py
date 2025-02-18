import virtualenv
import subprocess
import tempfile
import os
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional


class DependencyManager:
    def __init__(self, cache_dir: Optional[Path] = None):
        """Initialize dependency manager with optional cache directory"""
        self.cache_dir = cache_dir or Path.home() / '.enact' / 'venvs'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        print(f"Using cache directory: {self.cache_dir}")

    def _get_env_hash(self, dependencies: Dict) -> str:
        """Create a unique hash for the dependencies configuration"""
        # Sort dependencies to ensure consistent hashing
        dep_str = json.dumps(dependencies, sort_keys=True)
        return hashlib.sha256(dep_str.encode()).hexdigest()[:12]

    def _get_cached_venv(self, dependencies: Dict) -> Path:
        """Get or create a cached virtual environment for given dependencies"""
        env_hash = self._get_env_hash(dependencies)
        venv_path = self.cache_dir / env_hash

        if not venv_path.exists():
            print(f"Creating new virtual environment for hash {env_hash}")
            virtualenv.cli_run([str(venv_path)])

            # Install dependencies in the new environment
            if dependencies.get('python'):
                python_deps = dependencies['python']

                # Check Python version compatibility
                if python_deps.get('version'):
                    self._check_python_version(python_deps['version'])

                # Install required packages
                if python_deps.get('packages'):
                    requirements = [
                        f"{pkg['name']}{pkg['version']}"
                        for pkg in python_deps['packages']
                    ]
                    self._install_packages(venv_path, requirements)

            # Create a marker file with dependency info
            with open(venv_path / 'dependencies.json', 'w') as f:
                json.dump(dependencies, f)
        else:
            print(f"Using cached virtual environment: {env_hash}")

        return venv_path

    def _install_packages(self, venv_path: Path, requirements: List[str]) -> None:
        """Install Python packages in the specified virtual environment"""
        pip_path = self._get_pip_path(venv_path)
        print(f"Installing packages: {requirements}")

        try:
            process = subprocess.run(
                [str(pip_path), 'install'] + requirements,
                capture_output=True,
                text=True,
                check=True
            )
            print("Package installation successful")
        except subprocess.CalledProcessError as e:
            print(f"Package installation failed: {e.stderr}")
            raise RuntimeError(f"Failed to install dependencies: {e.stderr}")

    def _get_pip_path(self, venv_path: Path) -> Path:
        """Get path to pip executable in venv"""
        if os.name == 'nt':  # Windows
            return venv_path / 'Scripts' / 'pip.exe'
        return venv_path / 'bin' / 'pip'

    def _get_python_path(self, venv_path: Path) -> Path:
        """Get path to Python executable in venv"""
        if os.name == 'nt':  # Windows
            return venv_path / 'Scripts' / 'python.exe'
        return venv_path / 'bin' / 'python'

    def _check_python_version(self, version_spec: str) -> None:
        """Check if current Python version meets requirements"""
        import sys
        from packaging import version
        from packaging.specifiers import SpecifierSet

        current_version = version.parse(sys.version.split()[0])
        spec = SpecifierSet(version_spec)

        print(
            f"Checking Python version: {current_version} against {version_spec}")

        if current_version not in spec:
            raise RuntimeError(
                f"Python version {current_version} does not meet requirement: {version_spec}")

        print("Python version check passed")

    def execute_in_venv(self, script: str, dependencies: Dict) -> str:
        """Execute a script in a cached virtual environment"""
        venv_path = self._get_cached_venv(dependencies)
        python_path = self._get_python_path(venv_path)

        print(f"Executing script with Python at: {python_path}")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write(script)
            tmp.flush()

            try:
                process = subprocess.run(
                    [str(python_path), tmp.name],
                    capture_output=True,
                    text=True
                )
                if process.returncode != 0:
                    raise RuntimeError(
                        f"Script execution failed: {process.stderr}")
                return process.stdout
            finally:
                os.unlink(tmp.name)
