import virtualenv
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Optional
import pkg_resources


class DependencyManager:
    def __init__(self, venv_path: Optional[Path] = None):
        """Initialize dependency manager with optional custom venv path"""
        self.venv_path = venv_path or Path(tempfile.mkdtemp()) / '.venv'
        # Added debug print
        print(f"Creating virtual environment at: {self.venv_path}")
        self._ensure_venv()

    def _ensure_venv(self):
        """Create virtual environment if it doesn't exist"""
        if not self.venv_path.exists():
            print(f"Creating new virtual environment...")  # Added debug print
            virtualenv.cli_run([str(self.venv_path)])
            # Added debug print
            print("Virtual environment created successfully")

    def _get_pip_path(self) -> Path:
        """Get path to pip executable in venv"""
        if os.name == 'nt':  # Windows
            return self.venv_path / 'Scripts' / 'pip.exe'
        return self.venv_path / 'bin' / 'pip'

    def _get_python_path(self) -> Path:
        """Get path to Python executable in venv"""
        if os.name == 'nt':  # Windows
            return self.venv_path / 'Scripts' / 'python.exe'
        return self.venv_path / 'bin' / 'python'

    def install_dependencies(self, dependencies: Optional[Dict]) -> None:
        """Install dependencies from Enact task definition"""
        print(f"Installing dependencies: {dependencies}")  # Added debug print

        if not dependencies or 'python' not in dependencies:
            print("No Python dependencies found")  # Added debug print
            return

        python_deps = dependencies.get('python')
        if not python_deps:
            print("Python dependencies section is empty")  # Added debug print
            return

        # Check Python version compatibility
        if python_deps.get('version'):
            # Added debug print
            print(
                f"Checking Python version compatibility: {python_deps['version']}")
            self._check_python_version(python_deps['version'])

        # Install required packages
        if python_deps.get('packages'):
            requirements = [
                f"{pkg['name']}{pkg['version']}"
                for pkg in python_deps['packages']
            ]
            print(f"Installing packages: {requirements}")  # Added debug print
            self._install_packages(requirements)

    def _check_python_version(self, version_spec: str) -> None:
        """Check if current Python version meets requirements"""
        import sys
        from packaging import version
        from packaging.specifiers import SpecifierSet

        current_version = version.parse(sys.version.split()[0])
        spec = SpecifierSet(version_spec)

        print(f"Current Python version: {current_version}")  # Debug print
        print(f"Required version spec: {version_spec}")  # Debug print

        if current_version not in spec:
            raise RuntimeError(
                f"Python version {current_version} does not meet requirement: {version_spec}")

    print("Python version check passed")  # Debug print

    def _install_packages(self, requirements: List[str]) -> None:
        """Install Python packages in the virtual environment"""
        pip_path = self._get_pip_path()
        print(f"Using pip at: {pip_path}")  # Added debug print
        print(f"Installing requirements: {requirements}")  # Added debug print

        process = subprocess.run(
            [str(pip_path), 'install'] + requirements,
            capture_output=True,
            text=True
        )
        if process.returncode != 0:
            # Added debug print
            print(f"Package installation failed: {process.stderr}")
            raise RuntimeError(
                f"Failed to install dependencies: {process.stderr}")
        print("Package installation successful")  # Added debug print

    def execute_in_venv(self, script: str) -> str:
        """Execute a script in the virtual environment"""
        python_path = self._get_python_path()
        # Added debug print
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
                    # Added debug print
                    print(f"Script execution failed: {process.stderr}")
                    raise RuntimeError(
                        f"Script execution failed: {process.stderr}")
                return process.stdout
            finally:
                os.unlink(tmp.name)
